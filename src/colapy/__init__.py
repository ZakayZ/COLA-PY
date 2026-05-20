import abc
import typing as tp
from pathlib import Path

from ._cola_impl import (
    __doc__,
    __version__,
    LorentzVector,
    Particle,
    ParticleClass,
    EventInitialState,
    EventData,
    RunManager as _RunManager,
)


class RunManager(_RunManager):
    def load_config(self, *, file: str | Path = None, config: str = None) -> 'RunManager':
        """Load pipeline config from an XML file path or an inline XML string."""
        assert file is not None or config is not None, 'Either file or config must be provided'

        if config is not None:
            return self.load_config_xml(config)

        if isinstance(file, str):
            file = Path(file)

        return self.load_config_file(str(Path(file).expanduser()))


class AZ(tp.NamedTuple):
    A: int
    Z: int


class GeneratorBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self) -> EventData:
        raise NotImplementedError


class ConverterBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self, event_data: EventData) -> EventData:
        raise NotImplementedError


class WriterBase(abc.ABC):
    @abc.abstractmethod
    def __call__(self, event_data: EventData) -> None:
        raise NotImplementedError


__all__ = [
    '__doc__',
    '__version__',
    'AZ',
    'LorentzVector',
    'Particle',
    'ParticleClass',
    'EventInitialState',
    'EventData',
    'RunManager',
    'GeneratorBase',
    'ConverterBase',
    'WriterBase',
]
