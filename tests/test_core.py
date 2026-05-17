import pytest
import colapy
import filters


def pipeline_config_xml(
    *,
    pdg_a: str = '1000073',
    pdg_b: str = '2212',
    momentum_e: str = '10.0',
    delta_e: str = '5.0',
) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<program>
    <generator name="PythonGenerator"
               class="filters.Generator"
               pdg_a="{pdg_a}"
               pdg_b="{pdg_b}"
               momentum_e="{momentum_e}"/>
    <converter name="PythonConverter"
               class="filters.Converter"
               delta_e="{delta_e}"/>
    <writer name="PythonWriter" class="filters.Writer"/>
</program>
"""


def run_pipeline(config_xml: str, steps: int = 1):
    filters.RECORDS.clear()
    manager = colapy.RunManager()
    manager.load_module('COLA-Py')
    manager.load_config(config=config_xml)
    manager.run(steps)


def test_python_pipeline():
    run_pipeline(pipeline_config_xml())

    assert len(filters.RECORDS) == 1
    event = filters.RECORDS[0]
    assert event.initial_state.pdg_code_a == 1000073
    assert event.initial_state.pdg_code_b == 2212
    assert len(event.particles) == 1
    assert event.particles[0].momentum.e == pytest.approx(15.0)


def test_python_pipeline_multiple_steps():
    config_xml = pipeline_config_xml(momentum_e='1.0', delta_e='2.0')

    run_pipeline(config_xml, steps=3)

    assert len(filters.RECORDS) == 3
    assert all(event.particles[0].momentum.e == pytest.approx(3.0) for event in filters.RECORDS)
