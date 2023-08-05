import typer
import subprocess
from typing import Optional
import pathlib

app = typer.Typer()


def is_installed():
    sp = subprocess.run((["bash", "-c", "deno --version"]), capture_output=True)
    return sp.stdout != b""


def read_dotdvm():
    path = ".dvm"
    file = pathlib.Path(path)
    if file.is_file():
        f = open(path, "r")
        return f.read()
    else:
        return False


def is_matching_version(version: str):
    sp = subprocess.run((["bash", "-c", "deno --version"]), capture_output=True)
    version_number = version.replace("v", "")
    if sp.stdout != b"":
        description = f"deno {version_number}".encode()
        return description in sp.stdout
    else:
        return False


@app.command()
def use():
    cfg = read_dotdvm()
    if cfg:
        install(cfg)
    else:
        typer.secho(".dvm not found", fg=typer.colors.YELLOW)
        return


@app.command()
def install(version: Optional[str] = typer.Argument(None)):
    if not version:
        typer.secho("version is not specified, installing latest", fg=typer.colors.CYAN)
        install("latest")
    if version == "latest":
        subprocess.run(
            ["bash", "-c", "curl -fsSL https://deno.land/x/install/install.sh | sh"]
        )
        typer.secho("latest Deno installed", fg=typer.colors.GREEN)
    else:
        if version and is_matching_version(version):
            typer.secho(f"Deno {version} already installed", fg=typer.colors.GREEN)
            return
        try:
            subprocess.check_output(
                [
                    "bash",
                    "-c",
                    "curl -fsSL https://deno.land/x/install/install.sh"
                    f" | sh -s {version}",
                ]
            )
            typer.secho(f"Deno {version} installed", fg=typer.colors.GREEN)
        except subprocess.CalledProcessError:
            typer.secho(
                "invalid request, check the specified Deno version",
                fg=typer.colors.YELLOW,
            )


@app.command()
def remove():
    subprocess.run(["bash", "-c", "rm -f $(which deno)"])
    typer.secho("Deno removed", fg=typer.colors.YELLOW)


@app.command()
def upgrade(version: Optional[str] = typer.Argument(None)):
    if not is_installed():
        typer.secho("Deno is not yet installed", fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)
    if not version:
        install()
    install(version)


if __name__ == "__main__":
    app()
