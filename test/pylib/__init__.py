import colapy
import pprint


def to_dict(obj: object) -> object:
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


class Generator(colapy.GeneratorBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        print(f'init: {self}, {kwargs}')

    def __call__(self) -> colapy.EventData:
        return colapy.EventData(colapy.EventInitialState(pdg_code_a=11, pdg_code_b=13), [])


class Converter(colapy.ConverterBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        print(f'init: {self}, {kwargs}')

    def __call__(self, event_data: colapy.EventData) -> colapy.EventData:
        return event_data


class Writer(colapy.WriterBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        print(f'init: {self}, {kwargs}')

    def __call__(self, event_data: colapy.EventData) -> None:
        pprint.pprint(to_dict(event_data))
