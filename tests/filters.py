import colapy


RECORDS: list[colapy.EventData] = []


class Generator(colapy.GeneratorBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        self._pdg_a = int(kwargs.get('pdg_a', '11'))
        self._pdg_b = int(kwargs.get('pdg_b', '13'))
        self._momentum_e = float(kwargs.get('momentum_e', '10.0'))

    def __call__(self) -> colapy.EventData:
        state = colapy.EventInitialState(pdg_code_a=self._pdg_a, pdg_code_b=self._pdg_b)
        particle = colapy.Particle(
            position=colapy.LorentzVector(),
            momentum=colapy.LorentzVector(e=self._momentum_e, x=1.0, y=0.0, z=0.0),
            pdg_code=211,
            p_class=colapy.ParticleClass.PRODUCED,
        )
        return colapy.EventData(state, [particle])


class Converter(colapy.ConverterBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        self._delta_e = float(kwargs.get('delta_e', '5.0'))

    def __call__(self, event_data: colapy.EventData) -> colapy.EventData:
        for particle in event_data.particles:
            particle.momentum.e += self._delta_e
        return event_data


class Writer(colapy.WriterBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        pass

    def __call__(self, event_data: colapy.EventData) -> None:
        RECORDS.append(event_data)
