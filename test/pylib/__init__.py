from colapy import WriterBase, EventData


class TestWriter(WriterBase):
    def __init__(self, **kwargs: dict[str, str]) -> None:
        print('init:', kwargs)

    def __call__(self, event_data: EventData) -> None:
        print('call:', event_data)
