# COLA-PY

Python обертка над фреймворком COLA.

## Description
This library is a COLA plugin that adds support for pure Python modules as stages in your model.
Moreover it shipped with the utility to simplify working with COLA:
- script to setup new COLA modules.
- script to run COLA calculation without the need to write and build C++ code.
This script is available from python, so you can orchestrate execution in any python environment including IPython.

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
### Python binding
All objects from COLA C++ library is available with native types in Python. More details [here](src/colapy/__init__.pyi).

#### Python Filters
To create a custom filter one need to create a class derived from one of these:
- derive from `GeneratorBase` and override `def __call__(self) -> EventData`
- derive from `ConverterBase` and override `def __call__(self, event_data: EventData) -> EventData`
- derive from `WriterBase` and override `def __call__(self, event_data: EventData) -> None`

For example, lets create a writer that stores results in a json lines format:
```python
class JSONWriter(colapy.WriterBase):
    file: str

    def __init__(self, **kwargs: dict[str, str]) -> None:
        self.file = kwargs.get('file', 'out.jsonl')
        with open(self.file, 'w') as f:
            pass

    def __call__(self, event_data: colapy.EventData) -> None:
        with open(self.file, 'a') as f:
            json.dump(self.to_dict(event_data), f)

    @classmethod
    def to_dict(cls, obj: object) -> object:
        if isinstance(obj, (int, str, float)):
            return obj

        if isinstance(obj, list):
            return [to_dict(el) for el in obj]

        if isinstance(obj, dict):
            return {
                to_dict(k): to_dict(v) for k, v in obj.items()
            }

        return {
            el: to_dict(getattr(obj, el))
            for el in dir(obj)
            if not el.startswith('_')
        }
```

These filters are constructed from the parameters described in the config:
```xml
...
    <writer name="PythonWriter" class="JSONWriter" file="config_out.jsonl"/>
...
```
All the attributes will be forwarded as kwargs to the constructor.

#### Config
All python filters must have a `class` attribute, that stores whole path to the python class including module.
- Class defined in `__main__.py` file should be described as one of: `__main__.FilterName` or just `FilterName`.
- Class from a library should be described as: `library_name.your_submodule.FilterName`.

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
