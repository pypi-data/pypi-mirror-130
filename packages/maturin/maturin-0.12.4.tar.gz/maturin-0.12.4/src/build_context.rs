use crate::auditwheel::auditwheel_rs;
use crate::auditwheel::PlatformTag;
use crate::auditwheel::Policy;
use crate::compile;
use crate::compile::warn_missing_py_init;
use crate::module_writer::write_python_part;
use crate::module_writer::WheelWriter;
use crate::module_writer::{write_bin, write_bindings_module, write_cffi_module};
use crate::python_interpreter::InterpreterKind;
use crate::source_distribution::source_distribution;
use crate::Metadata21;
use crate::PyProjectToml;
use crate::PythonInterpreter;
use crate::Target;
use anyhow::{anyhow, bail, Context, Result};
use cargo_metadata::Metadata;
use fs_err as fs;
use std::borrow::Cow;
use std::path::{Path, PathBuf};

/// The way the rust code is used in the wheel
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum BridgeModel {
    /// A native module with c bindings, i.e. `#[no_mangle] extern "C" <some item>`
    Cffi,
    /// A rust binary to be shipped a python package
    Bin,
    /// A native module with pyo3 or rust-cpython bindings. The String is the name of the bindings
    /// providing crate, e.g. pyo3.
    Bindings(String),
    /// `Bindings`, but specifically for pyo3 with feature flags that allow building a single wheel
    /// for all cpython versions (pypy still needs multiple versions).
    /// The numbers are the minimum major and minor version
    BindingsAbi3(u8, u8),
}

impl BridgeModel {
    /// Returns the name of the bindings crate
    pub fn unwrap_bindings(&self) -> &str {
        match self {
            BridgeModel::Bindings(value) => value,
            _ => panic!("Expected Bindings"),
        }
    }

    /// Test whether this is using a specific bindings crate
    pub fn is_bindings(&self, name: &str) -> bool {
        match self {
            BridgeModel::Bindings(value) => value == name,
            _ => false,
        }
    }
}

/// Whether this project is pure rust or rust mixed with python
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ProjectLayout {
    /// A rust crate compiled into a shared library with only some glue python for cffi
    PureRust {
        /// Contains the canonicialized (i.e. absolute) path to the rust part of the project
        rust_module: PathBuf,
        /// rust extension name
        extension_name: String,
    },
    /// A python package that is extended by a native rust module.
    Mixed {
        /// Contains the canonicialized (i.e. absolute) path to the python part of the project
        python_module: PathBuf,
        /// Contains the canonicialized (i.e. absolute) path to the rust part of the project
        rust_module: PathBuf,
        /// rust extension name
        extension_name: String,
    },
}

impl ProjectLayout {
    /// Checks whether a python module exists besides Cargo.toml with the right name
    pub fn determine(
        project_root: impl AsRef<Path>,
        module_name: &str,
        py_src: Option<impl AsRef<Path>>,
    ) -> Result<ProjectLayout> {
        // A dot in the module name means the extension module goes into the module folder specified by the path
        let parts: Vec<&str> = module_name.split('.').collect();
        let project_root = project_root.as_ref();
        let python_root = py_src.map_or(Cow::Borrowed(project_root), |py_src| {
            Cow::Owned(project_root.join(py_src))
        });
        let (python_module, rust_module, extension_name) = if parts.len() > 1 {
            let mut rust_module = project_root.to_path_buf();
            rust_module.extend(&parts[0..parts.len() - 1]);
            (
                python_root.join(parts[0]),
                rust_module,
                parts[parts.len() - 1].to_string(),
            )
        } else {
            (
                python_root.join(module_name),
                python_root.join(module_name),
                module_name.to_string(),
            )
        };
        if python_module.is_dir() {
            if !python_module.join("__init__.py").is_file() {
                bail!("Found a directory with the module name ({}) next to Cargo.toml, which indicates a mixed python/rust project, but the directory didn't contain an __init__.py file.", module_name)
            }

            println!("🍹 Building a mixed python/rust project");

            Ok(ProjectLayout::Mixed {
                python_module,
                rust_module,
                extension_name,
            })
        } else {
            Ok(ProjectLayout::PureRust {
                rust_module: project_root.to_path_buf(),
                extension_name,
            })
        }
    }

    pub fn extension_name(&self) -> &str {
        match *self {
            ProjectLayout::PureRust {
                ref extension_name, ..
            } => extension_name,
            ProjectLayout::Mixed {
                ref extension_name, ..
            } => extension_name,
        }
    }
}

/// Contains all the metadata required to build the crate
#[derive(Clone)]
pub struct BuildContext {
    /// The platform, i.e. os and pointer width
    pub target: Target,
    /// Whether to use cffi or pyo3/rust-cpython
    pub bridge: BridgeModel,
    /// Whether this project is pure rust or rust mixed with python
    pub project_layout: ProjectLayout,
    /// Python Package Metadata 2.1
    pub metadata21: Metadata21,
    /// The name of the crate
    pub crate_name: String,
    /// The name of the module can be distinct from the package name, mostly
    /// because package names normally contain minuses while module names
    /// have underscores. The package name is part of metadata21
    pub module_name: String,
    /// The path to the Cargo.toml. Required for the cargo invocations
    pub manifest_path: PathBuf,
    /// The directory to store the built wheels in. Defaults to a new "wheels"
    /// directory in the project's target directory
    pub out: PathBuf,
    /// Pass --release to cargo
    pub release: bool,
    /// Strip the library for minimum file size
    pub strip: bool,
    /// Whether to skip checking the linked libraries for manylinux/musllinux compliance
    pub skip_auditwheel: bool,
    /// Whether to use the the manylinux/musllinux or use the native linux tag (off)
    pub platform_tag: Option<PlatformTag>,
    /// Extra arguments that will be passed to cargo as `cargo rustc [...] [arg1] [arg2] --`
    pub cargo_extra_args: Vec<String>,
    /// Extra arguments that will be passed to rustc as `cargo rustc [...] -- [arg1] [arg2]`
    pub rustc_extra_args: Vec<String>,
    /// The available python interpreter
    pub interpreter: Vec<PythonInterpreter>,
    /// Cargo.toml as resolved by [cargo_metadata]
    pub cargo_metadata: Metadata,
    /// Whether to use universal2 or use the native macOS tag (off)
    pub universal2: bool,
    /// Build editable wheels
    pub editable: bool,
}

/// The wheel file location and its Python version tag (e.g. `py3`).
///
/// For bindings the version tag contains the Python interpreter version
/// they bind against (e.g. `cp37`).
pub type BuiltWheelMetadata = (PathBuf, String);

impl BuildContext {
    /// Checks which kind of bindings we have (pyo3/rust-cypthon or cffi or bin) and calls the
    /// correct builder.
    pub fn build_wheels(&self) -> Result<Vec<BuiltWheelMetadata>> {
        fs::create_dir_all(&self.out)
            .context("Failed to create the target directory for the wheels")?;

        let wheels = match &self.bridge {
            BridgeModel::Cffi => self.build_cffi_wheel()?,
            BridgeModel::Bin => self.build_bin_wheel()?,
            BridgeModel::Bindings(_) => self.build_binding_wheels(&self.interpreter)?,
            BridgeModel::BindingsAbi3(major, minor) => {
                let cpythons: Vec<_> = self
                    .interpreter
                    .iter()
                    .filter(|interp| interp.interpreter_kind == InterpreterKind::CPython)
                    .cloned()
                    .collect();
                let pypys: Vec<_> = self
                    .interpreter
                    .iter()
                    .filter(|interp| interp.interpreter_kind == InterpreterKind::PyPy)
                    .cloned()
                    .collect();
                let mut built_wheels = Vec::new();
                if !cpythons.is_empty() {
                    built_wheels.extend(self.build_binding_wheel_abi3(&cpythons, *major, *minor)?);
                }
                if !pypys.is_empty() {
                    println!(
                        "⚠️ Warning: PyPy does not yet support abi3 so the build artifacts will be version-specific. \
                        See https://foss.heptapod.net/pypy/pypy/-/issues/3397 for more information."
                    );
                    built_wheels.extend(self.build_binding_wheels(&pypys)?);
                }
                built_wheels
            }
        };

        Ok(wheels)
    }

    /// Builds a source distribution and returns the same metadata as [BuildContext::build_wheels]
    pub fn build_source_distribution(&self) -> Result<Option<BuiltWheelMetadata>> {
        fs::create_dir_all(&self.out)
            .context("Failed to create the target directory for the source distribution")?;

        match PyProjectToml::new(self.manifest_path.parent().unwrap()) {
            Ok(pyproject) => {
                let sdist_path = source_distribution(
                    &self.out,
                    &self.metadata21,
                    &self.manifest_path,
                    &self.cargo_metadata,
                    pyproject.sdist_include(),
                )
                .context("Failed to build source distribution")?;
                Ok(Some((sdist_path, "source".to_string())))
            }
            Err(_) => Ok(None),
        }
    }

    fn auditwheel(
        &self,
        python_interpreter: Option<&PythonInterpreter>,
        artifact: &Path,
        platform_tag: Option<PlatformTag>,
    ) -> Result<Policy> {
        if self.skip_auditwheel {
            return Ok(Policy::default());
        }

        let target = python_interpreter
            .map(|x| &x.target)
            .unwrap_or(&self.target);

        let policy = auditwheel_rs(artifact, target, platform_tag).context(
            if let Some(platform_tag) = platform_tag {
                format!("Error ensuring {} compliance", platform_tag)
            } else {
                "Error checking for manylinux/musllinux compliance".to_string()
            },
        )?;
        Ok(policy)
    }

    fn add_pth(&self, writer: &mut WheelWriter) -> Result<()> {
        if self.editable {
            writer.add_pth(&self.project_layout, &self.metadata21)?;
        }
        Ok(())
    }

    fn write_binding_wheel_abi3(
        &self,
        artifact: &Path,
        platform_tag: PlatformTag,
        major: u8,
        min_minor: u8,
    ) -> Result<BuiltWheelMetadata> {
        let platform = self
            .target
            .get_platform_tag(platform_tag, self.universal2)?;
        let tag = format!("cp{}{}-abi3-{}", major, min_minor, platform);

        let mut writer = WheelWriter::new(&tag, &self.out, &self.metadata21, &[tag.clone()])?;

        write_bindings_module(
            &mut writer,
            &self.project_layout,
            &self.module_name,
            artifact,
            None,
            &self.target,
            self.editable,
        )
        .context("Failed to add the files to the wheel")?;

        self.add_pth(&mut writer)?;

        let wheel_path = writer.finish()?;
        Ok((wheel_path, format!("cp{}{}", major, min_minor)))
    }

    /// For abi3 we only need to build a single wheel and we don't even need a python interpreter
    /// for it
    pub fn build_binding_wheel_abi3(
        &self,
        interpreters: &[PythonInterpreter],
        major: u8,
        min_minor: u8,
    ) -> Result<Vec<BuiltWheelMetadata>> {
        let mut wheels = Vec::new();
        // On windows, we have picked an interpreter to set the location of python.lib,
        // otherwise it's none
        let python_interpreter = interpreters.get(0);
        let artifact = self.compile_cdylib(
            python_interpreter,
            Some(self.project_layout.extension_name()),
        )?;
        let policy = self.auditwheel(python_interpreter, &artifact, self.platform_tag)?;
        let (wheel_path, tag) =
            self.write_binding_wheel_abi3(&artifact, policy.platform_tag(), major, min_minor)?;

        println!(
            "📦 Built wheel for abi3 Python ≥ {}.{} to {}",
            major,
            min_minor,
            wheel_path.display()
        );
        wheels.push((wheel_path, tag));

        Ok(wheels)
    }

    fn write_binding_wheel(
        &self,
        python_interpreter: &PythonInterpreter,
        artifact: &Path,
        platform_tag: PlatformTag,
    ) -> Result<BuiltWheelMetadata> {
        let tag = python_interpreter.get_tag(platform_tag, self.universal2)?;

        let mut writer = WheelWriter::new(&tag, &self.out, &self.metadata21, &[tag.clone()])?;

        write_bindings_module(
            &mut writer,
            &self.project_layout,
            &self.module_name,
            artifact,
            Some(python_interpreter),
            &self.target,
            self.editable,
        )
        .context("Failed to add the files to the wheel")?;

        self.add_pth(&mut writer)?;

        let wheel_path = writer.finish()?;
        Ok((
            wheel_path,
            format!("cp{}{}", python_interpreter.major, python_interpreter.minor),
        ))
    }

    /// Builds wheels for a Cargo project for all given python versions.
    /// Return type is the same as [BuildContext::build_wheels()]
    ///
    /// Defaults to 3.{5, 6, 7, 8, 9} if no python versions are given
    /// and silently ignores all non-existent python versions.
    ///
    /// Runs [auditwheel_rs()] if not deactivated
    pub fn build_binding_wheels(
        &self,
        interpreters: &[PythonInterpreter],
    ) -> Result<Vec<BuiltWheelMetadata>> {
        let mut wheels = Vec::new();
        for python_interpreter in interpreters {
            let artifact = self.compile_cdylib(
                Some(python_interpreter),
                Some(self.project_layout.extension_name()),
            )?;
            let policy = self.auditwheel(Some(python_interpreter), &artifact, self.platform_tag)?;
            let (wheel_path, tag) =
                self.write_binding_wheel(python_interpreter, &artifact, policy.platform_tag())?;
            println!(
                "📦 Built wheel for {} {}.{}{} to {}",
                python_interpreter.interpreter_kind,
                python_interpreter.major,
                python_interpreter.minor,
                python_interpreter.abiflags,
                wheel_path.display()
            );

            wheels.push((wheel_path, tag));
        }

        Ok(wheels)
    }

    /// Runs cargo build, extracts the cdylib from the output, runs auditwheel and returns the
    /// artifact
    ///
    /// The module name is used to warn about missing a `PyInit_<module name>` function for
    /// bindings modules.
    pub fn compile_cdylib(
        &self,
        python_interpreter: Option<&PythonInterpreter>,
        extension_name: Option<&str>,
    ) -> Result<PathBuf> {
        let artifacts = compile(self, python_interpreter, &self.bridge)
            .context("Failed to build a native library through cargo")?;

        let artifact = artifacts.get("cdylib").cloned().ok_or_else(|| {
            anyhow!(
                "Cargo didn't build a cdylib. Did you miss crate-type = [\"cdylib\"] \
                 in the lib section of your Cargo.toml?",
            )
        })?;

        if let Some(extension_name) = extension_name {
            warn_missing_py_init(&artifact, extension_name)
                .context("Failed to parse the native library")?;
        }

        Ok(artifact)
    }

    fn write_cffi_wheel(
        &self,
        artifact: &Path,
        platform_tag: PlatformTag,
    ) -> Result<BuiltWheelMetadata> {
        let (tag, tags) = self
            .target
            .get_universal_tags(platform_tag, self.universal2)?;

        let mut writer = WheelWriter::new(&tag, &self.out, &self.metadata21, &tags)?;

        write_cffi_module(
            &mut writer,
            &self.project_layout,
            self.manifest_path.parent().unwrap(),
            &self.module_name,
            artifact,
            &self.interpreter[0].executable,
            self.editable,
        )?;

        self.add_pth(&mut writer)?;

        let wheel_path = writer.finish()?;
        Ok((wheel_path, "py3".to_string()))
    }

    /// Builds a wheel with cffi bindings
    pub fn build_cffi_wheel(&self) -> Result<Vec<BuiltWheelMetadata>> {
        let mut wheels = Vec::new();
        let artifact = self.compile_cdylib(None, None)?;
        let policy = self.auditwheel(None, &artifact, self.platform_tag)?;
        let (wheel_path, tag) = self.write_cffi_wheel(&artifact, policy.platform_tag())?;

        // Warn if cffi isn't specified in the requirements
        if !self
            .metadata21
            .requires_dist
            .iter()
            .any(|dep| dep.to_ascii_lowercase().starts_with("cffi"))
        {
            eprintln!(
                "⚠️  Warning: missing cffi package dependency, please add it to pyproject.toml. \
                e.g: `dependencies = [\"cffi\"]`. This will become an error."
            );
        }

        println!("📦 Built wheel to {}", wheel_path.display());
        wheels.push((wheel_path, tag));

        Ok(wheels)
    }

    fn write_bin_wheel(
        &self,
        artifact: &Path,
        platform_tag: PlatformTag,
    ) -> Result<BuiltWheelMetadata> {
        let (tag, tags) = self
            .target
            .get_universal_tags(platform_tag, self.universal2)?;

        if !self.metadata21.scripts.is_empty() {
            bail!("Defining entrypoints and working with a binary doesn't mix well");
        }

        let mut writer = WheelWriter::new(&tag, &self.out, &self.metadata21, &tags)?;

        match self.project_layout {
            ProjectLayout::Mixed {
                ref python_module,
                ref extension_name,
                ..
            } => {
                if !self.editable {
                    write_python_part(&mut writer, python_module, extension_name)
                        .context("Failed to add the python module to the package")?;
                }
            }
            ProjectLayout::PureRust { .. } => {}
        }

        // I wouldn't know of any case where this would be the wrong (and neither do
        // I know a better alternative)
        let bin_name = artifact
            .file_name()
            .expect("Couldn't get the filename from the binary produced by cargo");
        write_bin(&mut writer, artifact, &self.metadata21, bin_name)?;

        self.add_pth(&mut writer)?;

        let wheel_path = writer.finish()?;
        Ok((wheel_path, "py3".to_string()))
    }

    /// Builds a wheel that contains a binary
    ///
    /// Runs [auditwheel_rs()] if not deactivated
    pub fn build_bin_wheel(&self) -> Result<Vec<BuiltWheelMetadata>> {
        let mut wheels = Vec::new();
        let artifacts = compile(self, None, &self.bridge)
            .context("Failed to build a native library through cargo")?;

        let artifact = artifacts
            .get("bin")
            .cloned()
            .ok_or_else(|| anyhow!("Cargo didn't build a binary"))?;

        let policy = self.auditwheel(None, &artifact, self.platform_tag)?;

        let (wheel_path, tag) = self.write_bin_wheel(&artifact, policy.platform_tag())?;
        println!("📦 Built wheel to {}", wheel_path.display());
        wheels.push((wheel_path, tag));

        Ok(wheels)
    }
}
