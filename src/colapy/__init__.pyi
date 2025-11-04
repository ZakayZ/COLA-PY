import enum
import typing as tp


from . import AZ


EventParticles: tp.TypeAlias = tp.List[Particle]


class LorentzVector:
    x: float
    y: float
    z: float
    e: float
    t: float

    @tp.overload
    def __init__(self, other: 'LorentzVector') -> None: ...
    
    @tp.overload
    def __init__(
        self,
        e: float = ...,
        x: float = ...,
        y: float = ...,
        z: float = ...,
    ) -> None: ...

    def __add__(self, other: 'LorentzVector') -> 'LorentzVector': ...
    def __sub__(self, other: 'LorentzVector') -> 'LorentzVector': ...
    def __iadd__(self, other: 'LorentzVector') -> 'LorentzVector': ...
    def __isub__(self, other: 'LorentzVector') -> 'LorentzVector': ...

    def __mul__(self, scalar: float) -> 'LorentzVector': ...
    def __rmul__(self, scalar: float) -> 'LorentzVector': ...
    def __truediv__(self, scalar: float) -> 'LorentzVector': ...
    def __imul__(self, scalar: float) -> 'LorentzVector': ...
    def __itruediv__(self, scalar: float) -> 'LorentzVector': ...

    def __eq__(self, other: object) -> bool: ...

    def __copy__(self) -> 'LorentzVector': ...
    def __deepcopy__(self, memo: object) -> 'LorentzVector': ...

    def __repr__(self) -> str: ...


class ParticleClass(enum.Enum):
    PRODUCED: int
    ELASTIC_A: int
    ELASTIC_B: int
    NON_ELASTIC_A: int
    NON_ELASTIC_B: int
    SPECTATOR_A: int
    SPECTATOR_B: int


class Particle:
    position: LorentzVector
    momentum: LorentzVector
    pdg_code: int
    p_class: ParticleClass

    @tp.overload
    def __init__(self, other: 'Particle') -> None: ...

    @tp.overload
    def __init__(
        self,
        position: LorentzVector = ...,
        momentum: LorentzVector = ...,
        pdg_code: int = ...,
        p_class: ParticleClass = ..., 
    ) -> None: ...
    def get_az(self) -> AZ: ...


class EventInitialState:
    pdg_code_a: int
    pdg_code_b: int
    pz_a: float
    pz_b: float
    energy: float
    sect_nn: float
    b: float
    n_coll: int
    n_coll_pp: int
    n_coll_pn: int
    n_coll_nn: int
    n_part: int
    n_part_a: int
    n_part_b: int
    phi_rot_a: float
    theta_rot_a: float
    phi_rot_b: float
    theta_rot_b: float
    initial_particles: EventParticles

    def __init__(
        self,
        pdg_code_a: int= ...,
        pdg_code_b: int= ...,
        pz_a: float = ...,
        pz_b: float = ...,
        energy: float = ...,
        sect_nn: float = ...,
        b: float = ...,
        n_coll: int= ...,
        n_coll_pp: int= ...,
        n_coll_pn: int= ...,
        n_coll_nn: int= ...,
        n_part: int= ...,
        n_part_a: int= ...,
        n_part_b: int= ...,
        phi_rot_a: float = ...,
        theta_rot_a: float = ...,
        phi_rot_b: float = ...,
        theta_rot_b: float = ...,
        initial_particles: EventParticles = list(),
    ) -> None: ...


class EventData:
    initial_state: EventInitialState
    particles: EventParticles

    def __init__(
        self,
        initial_state: EventInitialState = ...,
        particles: EventParticles = ...,
    ) -> None: ...


class RunManager:
    def __init__(self) -> None: ...

    def run(self, n: int) -> None: ...

    def load_library(self, library_path: str, library_prefix: str = ...) -> None: ...

    def load_config(self, config_path: str) -> None: ...
