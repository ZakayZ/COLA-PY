import abc
import typing as tp


from ._cola_impl import (
    __doc__,
    __version__,
    LorentzVector,
    Particle,
    ParticleClass,
    EventInitialState,
    EventData,
    RunManager,
)


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
