"""Configure-only checks: never download or install dependencies."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest


MODULE = Path(__file__).resolve().parents[1] / "cmake" / "FindOrInstallCOLA.cmake"
pytestmark = pytest.mark.skipif(shutil.which("cmake") is None, reason="CMake is required")


def fake_cola(prefix):
    config = prefix / "lib" / "cmake" / "COLA" / "COLAConfig.cmake"
    config.parent.mkdir(parents=True)
    config.write_text('set(COLA_FOUND TRUE)\nset(PROBE_FOUND "yes")\n')


def configure(tmp_path, *, env_prefix=None, define_prefix=None, extra="", destdir=None):
    script = tmp_path / "probe.cmake"
    script.write_text(
        "set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH FALSE)\n"
        "set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH FALSE)\n"
        "set(CMAKE_FIND_USE_PACKAGE_REGISTRY FALSE)\n"
        "set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY FALSE)\n"
        + extra
        + f'\ninclude("{MODULE.as_posix()}")\n'
        + 'message(STATUS "PROBE_FOUND=${PROBE_FOUND}")\n'
    )
    env = os.environ.copy()
    for name in ("COLA_INSTALL_PREFIX", "COLA_DIR", "COLA_ROOT", "CMAKE_PREFIX_PATH", "DESTDIR"):
        env.pop(name, None)
    if env_prefix is not None:
        env["COLA_INSTALL_PREFIX"] = str(env_prefix)
    if destdir is not None:
        env["DESTDIR"] = str(destdir)
    command = ["cmake"]
    if define_prefix is not None:
        command.append(f"-DCOLA_INSTALL_PREFIX={define_prefix}")
    return subprocess.run(command + ["-P", str(script)], env=env, cwd=tmp_path,
                          capture_output=True, text=True)


@pytest.mark.parametrize("prefix", [None, ""])
def test_missing_prefix_does_not_download(tmp_path, prefix):
    result = configure(tmp_path, env_prefix=prefix)
    assert result.returncode != 0
    assert "without an explicit path" in result.stderr
    assert not (tmp_path / "_deps").exists()


def test_relative_prefix_rejected(tmp_path):
    result = configure(tmp_path, env_prefix="relative/cola")
    assert result.returncode != 0
    assert "single absolute path" in result.stderr


def test_environment_prefix_with_spaces(tmp_path):
    prefix = tmp_path / "custom COLA" / "install"
    fake_cola(prefix)
    result = configure(tmp_path, env_prefix=prefix)
    assert result.returncode == 0, result.stderr
    assert "PROBE_FOUND=yes" in result.stdout


def test_existing_cola_without_auto_install_prefix(tmp_path):
    prefix = tmp_path / "existing"
    fake_cola(prefix)
    result = configure(tmp_path, extra=f'set(CMAKE_PREFIX_PATH "{prefix.as_posix()}")\n')
    assert result.returncode == 0, result.stderr
    assert "PROBE_FOUND=yes" in result.stdout


def test_explicit_setting_overrides_environment_and_cached_dir(tmp_path):
    prefix = tmp_path / "selected"
    fake_cola(prefix)
    result = configure(tmp_path, env_prefix=tmp_path / "wrong", define_prefix=prefix,
                       extra='set(COLA_DIR "/nonexistent" CACHE PATH "")\n')
    assert result.returncode == 0, result.stderr
    assert "PROBE_FOUND=yes" in result.stdout


def test_explicit_prefix_does_not_fall_back_to_other_installation(tmp_path):
    other = tmp_path / "other"
    fake_cola(other)
    # DESTDIR forces an early error before download if the requested prefix is
    # empty. Finding the unrelated installation would incorrectly succeed.
    result = configure(tmp_path, env_prefix=tmp_path / "requested", destdir=tmp_path / "stage",
                       extra=f'set(CMAKE_PREFIX_PATH "{other.as_posix()}")\n'
                             f'set(COLA_DIR "{(other / "lib/cmake/COLA").as_posix()}" CACHE PATH "")\n')
    assert result.returncode != 0
    assert "Unset DESTDIR" in result.stderr
    assert not (tmp_path / "_deps").exists()
