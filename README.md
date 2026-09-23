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

To setup a new COLA module you can run the following command:

```shell
cola setup project --name="ModuleName" --prefix="PathToProjectDir" --version="1.0.0"
```

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

### Publish

To publish your changes to the [pypi](https://pypi.org) run from the repo root

```shell
python -m build --sdist
python -m twine upload dist/*
```
