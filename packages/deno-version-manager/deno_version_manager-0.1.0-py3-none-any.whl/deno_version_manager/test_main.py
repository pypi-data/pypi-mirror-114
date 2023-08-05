from typer.testing import CliRunner
from .main import app
import os

runner = CliRunner()

deno_version = "v1.11.0"
deno_version_upgraded = "v1.12.0"


def test_install_version():
    runner.invoke(app, ["remove"])
    result = runner.invoke(app, ["install", deno_version])
    assert result.exit_code == 0
    assert f"Deno {deno_version} installed" in result.stdout


def test_upgrade_to_version():
    result = runner.invoke(app, ["upgrade", deno_version_upgraded])
    assert result.exit_code == 0
    assert f"Deno {deno_version_upgraded} installed" in result.stdout


def test_remove_deno():
    result = runner.invoke(app, ["remove"])
    assert result.exit_code == 0
    assert "Deno removed" in result.stdout


def test_install_latest():
    result = runner.invoke(app, ["install"])
    assert result.exit_code == 0
    assert "latest Deno installed" in result.stdout


def test_use_without_dvm():
    result = runner.invoke(app, ["use"])
    assert result.exit_code == 0
    assert ".dvm not found" in result.stdout


def test_use_with_dvm():
    file_path = ".dvm"
    with open(file_path, "w") as fp:
        fp.write("v1.12.0")
    result = runner.invoke(app, ["use"])
    assert result.exit_code == 0
    assert f"Deno {deno_version_upgraded} installed" in result.stdout
    os.remove(file_path)


def test_recognize_same_version():
    runner.invoke(app, ["install", deno_version])
    result = runner.invoke(app, ["install", deno_version])
    assert result.exit_code == 0
    assert f"Deno {deno_version} already installed" in result.stdout
