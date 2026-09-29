# COLA-PY

[![CI](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml/badge.svg)](https://github.com/ZakayZ/COLA-PY/actions/workflows/ci.yml)

Python bindings and CLI for [COLA](https://github.com/Spectator-matter-group-INR-RAS/COLA).

## Quick start

Install from source into an explicit native COLA prefix (requires Git, CMake and a C++ compiler):

```shell
COLA_INSTALL_PREFIX="$HOME/physics/cola" python -m pip install --no-binary=colapy colapy
export COLA_DIR="$HOME/physics/cola"
cola run --config config.xml --library COLA-Py
```

Use an XML configuration referring to your installed filters.

## Project setup

Create a project with Generator, Converter and Writer stubs:

```shell
cola setup project --name MyProject --language python --prefix ./projects
```

Supported languages: `cpp`, `python`, `fortran`, `java`, `julia`. Add your filter implementations
to the generated project.

## Examples

See the examples to learn how to write a [simple filter library](examples/pylib/) and work with [typed parameters](examples/typed_parameters/).
