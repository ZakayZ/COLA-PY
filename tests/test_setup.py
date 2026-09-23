import pytest
from click.testing import CliRunner

from colapy.cli import cli


@pytest.mark.parametrize(
    "language,expected_files",
    [
        (
            "cpp",
            {
                ".clang-format",
                ".clang-tidy",
                ".cmake-format.yaml",
                "CMakeLists.txt",
                "CMakePresets.json",
                "include/My_Project42.hh",
                "src/My_Project42.cc",
            },
        ),
        (
            "python",
            {
                "pyproject.toml",
                "src/my_project42_filters/__init__.py",
                "src/my_project42_filters/filters.py",
            },
        ),
        (
            "fortran",
            {
                ".cmake-format.yaml",
                ".fprettify.rc",
                "CMakeLists.txt",
                "CMakePresets.json",
                "src/My_Project42.f90",
            },
        ),
        (
            "java",
            {
                ".cmake-format.yaml",
                "CMakeLists.txt",
                "CMakePresets.json",
                "build.gradle.kts",
                "settings.gradle.kts",
                "config/checkstyle/checkstyle.xml",
                "src/main/java/org/cola/generated/my_project42_filters/My_Project42Generator.java",
                "src/main/java/org/cola/generated/my_project42_filters/My_Project42Converter.java",
                "src/main/java/org/cola/generated/my_project42_filters/My_Project42Writer.java",
            },
        ),
    ],
)
def test_generate_complete_file_manifest(tmp_path, language, expected_files):
    # Keep the manifest independent of the templates so a missing template fails the test.
    result = CliRunner().invoke(
        cli,
        ["setup", "project", "--language", language, "--name", "My_Project42", "--prefix", str(tmp_path)],
    )
    assert result.exit_code == 0, result.output
    root = tmp_path / "My_Project42"
    actual_files = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    assert actual_files == expected_files | {".editorconfig", ".gitignore", "README.md"}
    for relative in sorted(actual_files):
        content = (root / relative).read_text(encoding="utf-8")
        assert content.strip(), f"Empty generated file: {relative}"
        assert "{{" not in content and "{%" not in content, f"Unrendered template: {relative}"


@pytest.mark.parametrize(
    "language,source,quality",
    [
        ("cpp", "src/Demo.cc", ".clang-tidy"),
        ("python", "src/demo_filters/filters.py", "pyproject.toml"),
        ("fortran", "src/Demo.f90", ".fprettify.rc"),
        (
            "java",
            "src/main/java/org/cola/generated/demo_filters/DemoConverter.java",
            "config/checkstyle/checkstyle.xml",
        ),
    ],
)
def test_generate_project(tmp_path, language, source, quality):
    result = CliRunner().invoke(
        cli,
        ["setup", "project", "--language", language, "--name", "Demo", "--prefix", str(tmp_path), "--version", "2.3.4"],
    )
    assert result.exit_code == 0, result.output
    root = tmp_path / "Demo"
    assert (root / source).is_file()
    assert (root / quality).is_file()
    assert (root / ".editorconfig").is_file()
    assert (root / ".gitignore").is_file()
    assert "2.3.4" in (root / "README.md").read_text()
    assert not (root / "config.xml").exists()
    assert not (root / "tests").exists()
    assert ".ruff_cache" not in (root / ".gitignore").read_text()
    build_file = root / ("pyproject.toml" if language == "python" else "CMakeLists.txt")
    assert "2.3.4" in build_file.read_text()
    assert (root / "CMakeLists.txt").exists() == (language != "python")
    if language == "cpp":
        header = (root / "include/Demo.hh").read_text()
        assert 'extern "C" cola::VModule* LoadCOLAModule();' in header
        for role in ("Generator", "Converter", "Writer"):
            assert f"class {role} : public cola::V{role}" in header
        assert '#include "Demo.hh"' in (root / source).read_text()
    elif language == "python":
        for role in ("Generator", "Converter", "Writer"):
            assert f"class {role}(colapy.{role}Base):" in (root / source).read_text()
    elif language == "fortran":
        cmake = build_file.read_text()
        assert "add_cola_fortran_library(" in cmake
        assert "OBJECT" not in cmake
        assert "install(" in cmake
        declarations = (root / source).read_text()
        assert ", abstract," not in declarations
        assert "abstract interface" not in declarations
        assert "deferred" not in declarations
        assert "\ncontains\n" in declarations
        for role in ("Generator", "Converter", "Writer"):
            assert f"extends(AbstractFortran{role}) :: {role}" in declarations
            assert f"procedure :: init => {role.lower()}_init" in declarations
            assert f"procedure :: run => {role.lower()}_run" in declarations
    elif language == "java":
        cmake = build_file.read_text()
        assert "add_cola_gradle_library(" in cmake
        assert "add_custom_target(" not in cmake
        for role, signature in (
            ("Generator", "EventData generate()"),
            ("Converter", "EventData convert(EventData event)"),
            ("Writer", "void write(EventData event)"),
        ):
            declarations = (root / source).with_name(f"Demo{role}.java").read_text()
            assert f"public abstract class Demo{role} implements {role}" in declarations
            assert f"public abstract {signature};" in declarations
            assert f"Demo{role}=org.cola.generated.demo_filters.Demo{role}" in cmake
    for file in root.rglob("*"):
        if file.is_file():
            assert "{{" not in file.read_text(), file


@pytest.mark.parametrize("name", ["../escape", "/tmp/escape", "bad-name", "1demo", 'bad"name', "a" * 33])
def test_reject_invalid_names(tmp_path, name):
    result = CliRunner().invoke(cli, ["setup", "project", "--name", name, "--prefix", str(tmp_path)])
    assert result.exit_code != 0
    assert not list(tmp_path.iterdir())


def test_reject_invalid_version(tmp_path):
    result = CliRunner().invoke(
        cli, ["setup", "project", "--name", "Demo", "--prefix", str(tmp_path), "--version", "1.0;bad"]
    )
    assert result.exit_code != 0
    assert not list(tmp_path.iterdir())


def test_default_cpp_and_force_preserves_unrelated_files(tmp_path):
    runner = CliRunner()
    args = ["setup", "project", "--name", "Demo", "--prefix", str(tmp_path)]
    assert runner.invoke(cli, args).exit_code == 0
    root = tmp_path / "Demo"
    (root / "notes.txt").write_text("keep")
    (root / "src/Demo.cc").write_text("custom")
    assert runner.invoke(cli, args).exit_code != 0
    assert (root / "src/Demo.cc").read_text() == "custom"
    assert runner.invoke(cli, args + ["--force"]).exit_code == 0
    assert (root / "notes.txt").read_text() == "keep"
    assert '#include "Demo.hh"' in (root / "src/Demo.cc").read_text()


def test_force_rejects_symlinks_before_writing(tmp_path):
    root = tmp_path / "Demo"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "src").symlink_to(outside, target_is_directory=True)
    result = CliRunner().invoke(cli, ["setup", "project", "--name", "Demo", "--prefix", str(tmp_path), "--force"])
    assert result.exit_code != 0
    assert "symlink" in result.output
    assert not list(outside.iterdir())
    assert not (root / "CMakeLists.txt").exists()


def test_legacy_component_commands(tmp_path):
    for command in ("cmake", "sources", "git"):
        result = CliRunner().invoke(cli, ["setup", command, "--name", "Demo", "--prefix", str(tmp_path)])
        assert result.exit_code == 0, result.output
    assert (tmp_path / "Demo/CMakeLists.txt").exists()
    assert (tmp_path / "Demo/src/Demo.cc").exists()
    assert (tmp_path / "Demo/.gitignore").exists()
