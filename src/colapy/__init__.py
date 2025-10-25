import typing as tp


from ._cola_impl import (
    __doc__,
    __version__,
    LorentzVector,
    Particle,
    ParticleClass,
    EventInitialState,
    EventData,
)


class AZ(tp.NamedTuple):
    A: int
    Z: int


__all__ = [
    '__doc__',
    '__version__',
    'AZ',
    'LorentzVector',
    'Particle',
    'ParticleClass',
    'EventInitialState',
    'EventData',
]
