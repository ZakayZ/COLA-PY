# COLA-PY

[![CI](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml/badge.svg)](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml)

Python обертка над фреймворком COLA.

## Installation

COLA-PY can use an existing [COLA](https://github.com/Spectator-matter-group-INR-RAS/COLA)
installation or build and install COLA into an explicitly requested prefix:

```shell
COLA_INSTALL_PREFIX="$HOME/physics/cola" python -m pip install --no-binary=colapy colapy
# From a local checkout:
COLA_INSTALL_PREFIX="$HOME/physics/cola" python -m pip install .
# Equivalent explicit CMake setting (takes precedence over the environment):
python -m pip install . -Ccmake.define.COLA_INSTALL_PREFIX="/absolute/path/to/COLA"
```

The prefix must be an absolute path to the installation root, not a source directory.
With an explicit prefix, only that prefix is searched; if COLA is missing there,
a pinned revision is downloaded, built with the selected C++ toolchain, and installed
there. Git, network access, a working compiler and write access to the prefix are
required for auto-installation. No system package manager or sudo is invoked.

Without a prefix, an existing COLA can be found through standard CMake search paths
(e.g. `CMAKE_PREFIX_PATH`). If it is not found, configuration fails without downloading
or installing COLA. There is no default auto-installation destination.

These settings apply to source builds; installing an existing wheel does not run CMake.
COLA and its global COLA-Py module are installed outside pip's wheel ownership and are
not removed by `pip uninstall colapy`. Even `pip wheel` performs this external installation.
Do not set `DESTDIR` during auto-installation: the explicit prefix is the final destination.

At runtime, point the module loader to the same installation:

```shell
export COLA_DIR="$HOME/physics/cola"
```

### Conda environments

Activate the environment and use its Python and a compatible C++ toolchain. For example,
after installing Python, pip, CMake, Ninja, Git and a C++ compiler in the environment:

```shell
conda activate myenv
COLA_INSTALL_PREFIX="$CONDA_PREFIX" python -m pip install .
export COLA_DIR="$CONDA_PREFIX"
```

The prefix is still explicit: COLA-PY does not choose `CONDA_PREFIX` automatically.
The nested COLA build reuses the parent compiler/toolchain settings. Native files installed
this way are not conda-managed packages; avoid overwriting a separately conda-managed COLA.
Build COLA and its plugins with compatible C++ runtimes. Moving/cloning the environment or
shipping a standalone conda package requires separate packaging and relocation validation.

## Usage

### cola script

`colapy` package installs `cola` utility to your system.

#### Setup

Generate a project scaffold with imports, Generator/Converter/Writer declarations, build files
and language-specific code-quality configuration. Add your own implementations
and pipeline configuration:

```shell
cola setup project --name=MyCpp --language=cpp --prefix=./projects
cola setup project --name=MyPython --language=python --prefix=./projects
cola setup project --name=MyFortran --language=fortran --prefix=./projects
cola setup project --name=MyJava --language=java --prefix=./projects
```

`--language` defaults to `cpp`; `--version` defaults to `1.0.0`. Project names must
start with an ASCII letter and contain up to 32 letters, digits or underscores.
The destination is `<prefix>/<name>`. Existing projects are not overwritten unless
`--force` is supplied; unrelated files are preserved, and symlinks are never overwritten.

| Language | Based on | Build and quality tooling |
| --- | --- | --- |
| C++ | COLA-min-example | CMake presets, ClangFormat, Clang-Tidy |
| Python | COLA-PY/example and tests | `pyproject.toml`, src layout, Ruff |
| Fortran | COLA_Fortran/example and COLA_UrQMD | `add_cola_fortran_library`, CMake presets, fprettify |
| Java | COLA_JVM/examples/java-scaler | CMake presets, Gradle, Checkstyle, javac lint |

Each language has separate `.j2` files in `src/colapy/_cli_lib/templates/`.
The CLI renders file paths and contents using the project name, package name and version.
All projects include `.editorconfig`, `.gitignore`, and a README with build and
quality-check commands. Native projects have their own `CMakeLists.txt` and CMake
formatting configuration. C++ compiles declarations into an object target.
Fortran uses `add_cola_fortran_library`, following COLA_UrQMD, to generate wrappers
and build an installable shared module. Its concrete types bind to procedure stubs
in `contains`, as in UrQMD; fill in the bodies before running a pipeline.
Java uses `add_cola_gradle_library` to build and install the native module and JAR
with all three classes registered; implement them before running a pipeline.
The Python classes are also abstract,
with ellipsis stubs. No sample implementations or pipeline XML are generated.
The READMEs explain implementation and module registration for each language.
Fortran and Java need the corresponding installed COLA_Fortran/COLA_JVM bridge;
the generator does not install them. Python uses the installed COLA-Py module.

The existing `cola setup cmake`, `cola setup sources`, and `cola setup git` commands
remain available for generating individual parts of a project. `setup cmake` is
for native languages; Python uses `pyproject.toml`.

#### Run

It is possible to run COLA calculation without the need to write and compile driver C++ code.
If you have COLA modules installed on your system you can run the calculation using filters exposed by them with the following command:

```shell
cola run \
    --config="<path_to_config>/config.xml" \ # config that can use all the filters from the included libraries
    --library="COLA-Py" # includes filters from COLA-Py module
    --library="Deexcitation" # includes filters from Deexcitation module
```

## Develop

To install locally from source run from the repo root

```shell
pip install -e .
```

The generator tests run with `python -m pytest tests`. To also compile the
generated C++, Fortran and Java projects, install both language bridges into a test
prefix and enable the native integration tests:

```shell
COLA_DIR="/path/to/test/cola" \
COLA_GENERATOR_TEST_PREFIX="/path/to/test/cola" \
  python -m pytest tests
```

These tests require Ninja, Gradle, a JDK and compatible C++/Fortran compilers on PATH.
Set `CC`, `CXX` and `FC` explicitly if multiple toolchains are installed.
The Fortran and Java integration tests supply minimal implementations in temporary
projects to verify registration, shared-library build, installation and CLI execution.

### Publish

To publish your changes to the [pypi](https://pypi.org) run from the repo root

```shell
python -m build --sdist
python -m twine upload dist/*
```
