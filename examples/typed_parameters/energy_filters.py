"""User-side parameter conversion; no changes to the COLA Python bridge needed."""

import typing

import pydantic

import colapy


def parse_energy_gev(value: object) -> float:
    """Parse an explicit energy unit and return GeV (the convention in this example)."""
    if not isinstance(value, str):
        raise ValueError("Expected an energy string with a unit, e.g. '10ev' or '2.5GeV'")
    value = value.strip()
    # Check longer suffixes first: keV, MeV and GeV also end in eV.
    factors = {"GeV": 1.0, "MeV": 1e-3, "keV": 1e-6, "eV": 1e-9, "ev": 1e-9}
    for unit, factor in factors.items():
        if value.endswith(unit):
            return float(value[: -len(unit)]) * factor
    raise ValueError("Expected a number followed by eV (or ev), keV, MeV or GeV")


EnergyGeV = typing.Annotated[
    float,
    pydantic.BeforeValidator(parse_energy_gev),
    pydantic.Field(ge=0, allow_inf_nan=False),
]


class GeneratorParameters(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid", validate_default=True)

    energy: EnergyGeV
    pdg_code: int = 22


class Generator(colapy.GeneratorBase):
    def __init__(self, **kwargs: str) -> None:
        # The existing bridge passes these service attributes alongside user parameters.
        parameters = {key: value for key, value in kwargs.items() if key not in {"name", "class"}}
        self.params = GeneratorParameters.model_validate(parameters)

    def __call__(self) -> colapy.EventData:
        # A photon moving along z; all momentum components use GeV in this example.
        particle = colapy.Particle(
            position=colapy.LorentzVector(),
            momentum=colapy.LorentzVector(e=self.params.energy, x=0.0, y=0.0, z=self.params.energy),
            pdg_code=self.params.pdg_code,
            p_class=colapy.ParticleClass.PRODUCED,
        )
        return colapy.EventData(colapy.EventInitialState(pdg_code_a=11, pdg_code_b=-11), [particle])


class Writer(colapy.WriterBase):
    def __init__(self, **kwargs: str) -> None:
        parameters = {key: value for key, value in kwargs.items() if key not in {"name", "class"}}
        if parameters:
            raise ValueError(f"Unknown writer parameters: {', '.join(sorted(parameters))}")

    def __call__(self, event: colapy.EventData) -> None:
        for particle in event.particles:
            print(f"energy={particle.momentum.e:.12g} GeV, pdg_code={particle.pdg_code}", flush=True)
