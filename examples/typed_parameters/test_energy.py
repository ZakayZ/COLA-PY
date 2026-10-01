import os
import subprocess
import sys
from pathlib import Path

import energy_filters
import pydantic
import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10ev", 1e-8),
        ("10eV", 1e-8),
        ("2keV", 2e-6),
        ("250MeV", 0.25),
        ("2.5GeV", 2.5),
        ("  +.5 GeV  ", 0.5),
        ("1e3 MeV", 1.0),
        ("0eV", 0.0),
    ],
)
def test_energy_conversion(value, expected):
    params = energy_filters.GeneratorParameters.model_validate({"energy": value, "pdg_code": "22"})
    assert isinstance(params.energy, float)
    assert params.energy == pytest.approx(expected, rel=1e-12, abs=0)
    assert params.pdg_code == 22


@pytest.mark.parametrize("value", ["10", "10J", "10mev", "bad", "-1GeV", "nanGeV", "1e999GeV", 10, None])
def test_invalid_energy(value):
    with pytest.raises(pydantic.ValidationError) as caught:
        energy_filters.GeneratorParameters.model_validate({"energy": value})
    assert caught.value.errors()[0]["loc"] == ("energy",)


def test_required_energy_and_unknown_parameters():
    with pytest.raises(pydantic.ValidationError, match="Field required"):
        energy_filters.GeneratorParameters.model_validate({})
    with pytest.raises(pydantic.ValidationError, match="Extra inputs"):
        energy_filters.Generator(**{"energy": "1GeV", "enrgy": "2GeV"})


def test_bridge_metadata_and_default():
    generator = energy_filters.Generator(
        **{"name": "PythonGenerator", "class": "energy_filters.Generator", "energy": "250MeV"}
    )
    assert generator.params.pdg_code == 22
    event = generator()
    assert event.particles[0].momentum.e == pytest.approx(0.25)
    assert event.particles[0].momentum.z == pytest.approx(0.25)


def test_cli():
    root = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, "-m", "colapy", "run", "--config", "config.xml", "--library", "COLA-Py", "--steps", "1"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "energy=1e-08 GeV, pdg_code=22" in result.stdout
