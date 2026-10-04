import subprocess
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE = Path(__file__).parent.parent


def render(dest: Path, **answers: object) -> Path:
    data = {
        "project_name": "Demo Project",
        "author_name": "Demo",
        "author_email": "demo@example.com",
        **answers,
    }
    run_copy(
        str(TEMPLATE),
        dest,
        data=data,
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
        quiet=True,
    )
    return dest


def run(project: Path, *args: str) -> None:
    subprocess.run(["uv", *args], cwd=project, check=True)


@pytest.mark.parametrize("api", [False, True], ids=["cli", "api"])
def test_generated_project_passes_its_own_checks(tmp_path: Path, api: bool) -> None:
    project = render(tmp_path / "demo", api=api)

    run(project, "sync", "--locked")
    run(project, "run", "invoke", "lint")
    run(project, "run", "invoke", "test")


@pytest.mark.parametrize("api", [False, True], ids=["cli", "api"])
def test_api_files_only_when_requested(tmp_path: Path, api: bool) -> None:
    project = render(tmp_path / "demo", api=api)

    for path in ["bruno", "src/demo_project/api.py", "tests/fake_upstream.py"]:
        assert (project / path).exists() == api, path


def test_names_derive_from_project_name(tmp_path: Path) -> None:
    project = render(tmp_path / "demo", project_name="Acme Data.Tools")

    assert (project / "src/acme_data_tools").is_dir()
    assert 'name = "acme-data-tools"' in (project / "pyproject.toml").read_text()


def test_rejects_invalid_package_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="lowercase Python identifier"):
        render(tmp_path / "demo", package_name="Not-Valid")


def test_proprietary_licence_is_all_rights_reserved(tmp_path: Path) -> None:
    project = render(tmp_path / "demo", license="Proprietary")

    assert "All rights reserved" in (project / "LICENSE").read_text()
    assert "license =" not in (project / "pyproject.toml").read_text()
