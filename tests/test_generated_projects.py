"""Scaffold import/build tests; native builds opt in with COLA_GENERATOR_TEST_PREFIX."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from colapy.cli import cli


def generate(tmp_path, language):
    name = "Smoke" + language
    result = CliRunner().invoke(
        cli, ["setup", "project", "--name", name, "--language", language, "--prefix", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    return tmp_path / name, name


def run(command, root, env):
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=300)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def implement_fortran_test_filters(source):
    """Supply test-only bodies so the registration helper can instantiate the filters."""
    lines = []
    for line in source.read_text().splitlines():
        if "! TODO:" in line:
            continue
        if line.strip().startswith(("end subroutine", "end function")):
            lines.append("        err = ''")
            if "end function generator_run" in line:
                lines.append("        ed = EventData()")
        lines.append(line)
    source.write_text("\n".join(lines) + "\n")


def implement_java_test_filters(root, name):
    """Supply test-only bodies to exercise all three registered JVM factories."""
    implementations = {
        "Generator": ("EventData generate();", "EventData generate() { return new EventData(); }"),
        "Converter": ("EventData convert(EventData event);", "EventData convert(EventData event) { return event; }"),
        "Writer": (
            "void write(EventData event);",
            'void write(EventData event) { System.out.println("JAVA_WRITER_OK"); }',
        ),
    }
    for role, (signature, body) in implementations.items():
        source = root / f"src/main/java/org/cola/generated/{name.lower()}_filters/{name}{role}.java"
        source.write_text(source.read_text().replace("abstract ", "").replace(signature, body))


@pytest.mark.parametrize("role", ["Generator", "Converter", "Writer"])
def test_generated_python_declarations(tmp_path, role):
    root, _ = generate(tmp_path, "python")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + env.get("PYTHONPATH", "")
    run(
        [
            sys.executable,
            "-c",
            "from inspect import isabstract\n"
            f"from smokepython_filters.filters import {role} as Filter\n"
            f"from colapy import {role}Base\n"
            f"assert issubclass(Filter, {role}Base)\n"
            "assert isabstract(Filter)\n"
            "assert '__call__' in Filter.__abstractmethods__\n"
            "try:\n"
            "    Filter()\n"
            "except TypeError:\n"
            "    pass\n"
            "else:\n"
            "    raise AssertionError('An unimplemented filter must not be instantiated')\n",
        ],
        root,
        env,
    )


@pytest.mark.skipif(
    not os.environ.get("COLA_GENERATOR_TEST_PREFIX"),
    reason="Set COLA_GENERATOR_TEST_PREFIX to an installation with all native bridges",
)
@pytest.mark.parametrize("language", ["cpp", "fortran", "java"])
def test_generated_native_declarations(tmp_path, language):
    root, name = generate(tmp_path, language)
    prefix = Path(os.environ["COLA_GENERATOR_TEST_PREFIX"]).resolve()
    env = os.environ.copy()
    env["CMAKE_PREFIX_PATH"] = str(prefix)
    run(["cmake", "--preset", "release"], root, env)
    if language == "fortran":
        # Configuration must generate registration for every declared filter.
        for role in ("Generator", "Converter", "Writer"):
            assert (root / f"build/release/generated/{role}_wrapper.f90").is_file()
            assert (root / f"build/release/generated/{name}/{role}.hh").is_file()
        implement_fortran_test_filters(root / f"src/{name}.f90")
        run(["cmake", "--preset", "release"], root, env)
    elif language == "java":
        registration = (root / f"build/release/generated/{name}/{name}Module.cc").read_text()
        for role in ("Generator", "Converter", "Writer"):
            assert f"{name}{role}" in registration
        implement_java_test_filters(root, name)
    run(["cmake", "--build", "--preset", "release", "--parallel", "2"], root, env)
    if language in ("fortran", "java"):
        install = tmp_path / "installed module"
        run(["cmake", "--install", "build/release", "--prefix", str(install)], root, env)
        assert any(path.is_file() and name in path.name for path in install.rglob("*"))
        filter_prefix = name if language == "java" else ""
        (root / "pipeline.xml").write_text(
            f'<program><generator name="{filter_prefix}Generator"/>'
            f'<converter name="{filter_prefix}Converter"/><writer name="{filter_prefix}Writer"/></program>'
        )
        env["COLA_DIR"] = str(install)
        output = run(
            [sys.executable, "-m", "colapy", "run", "--config", "pipeline.xml", "--library", name, "--steps", "1"],
            root,
            env,
        )
        if language == "java":
            assert list(install.rglob(f"{name}-all.jar"))
            assert output.count("JAVA_WRITER_OK") == 1
