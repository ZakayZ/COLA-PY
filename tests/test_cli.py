import os
from pathlib import Path
import subprocess
import sys


def test_cli_runs_python_module(tmp_path):
    """Run the CLI in a fresh process and verify the writer receives three events."""
    config = tmp_path / "pipeline.xml"
    config.write_text('''<program>
      <generator name="PythonGenerator" class="filters.Generator" momentum_e="10"/>
      <converter name="PythonConverter" class="filters.Converter" delta_e="5"/>
      <writer name="PythonWriter" class="cli_writer.Writer"/>
    </program>''')
    (tmp_path / "cli_writer.py").write_text('''import colapy
class Writer(colapy.WriterBase):
    def __init__(self, **kwargs):
        pass
    def __call__(self, event):
        assert len(event.particles) == 1
        assert event.particles[0].momentum.e == 15.0
        print("CLI_EVENT_OK", flush=True)
''')
    env = os.environ.copy()
    paths = [str(tmp_path), str(Path(__file__).resolve().parent)]
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(paths)
    result = subprocess.run(
        [sys.executable, "-m", "colapy", "run", "--config", str(config),
         "--library", "COLA-Py", "--steps", "3"],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.count("CLI_EVENT_OK") == 3
