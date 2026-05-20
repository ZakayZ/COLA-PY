# COLA-PY

[![CI](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml/badge.svg)](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml)

Python обертка над фреймворком COLA.

## Installation

If you don't have [COLA library](https://github.com/Spectator-matter-group-INR-RAS/COLA) already present on your system, set environment variable before installing to specify where to install COLA.

```shell
export COLA_INSTALL_PREFIX="~/.local" # or your path to COLA plugins dir
```

Then install as usual python package

```shell
pip install colapy
```

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
