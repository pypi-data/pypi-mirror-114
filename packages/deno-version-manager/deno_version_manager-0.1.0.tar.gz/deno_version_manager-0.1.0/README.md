# Deno Version Manager

Simple CLI to manage [Deno](https://deno.land/) versions


Created with [typer](typer.tiangolo.com) and [poetry](https://python-poetry.org)


# Usage

| Command               | Description                                             |
| --------------------- | ------------------------------------------------------- |
| dvm use               | look for a .dvm file and use the specified deno version |
| dvm install [version] | install a specific deno version or auto-install latest  |
| dvm upgrade [version] | upgrade to a specific version or auto-install latest    |
| dvm uninstall         | remove deno                                             |


# Development
In VSCode
  ```
    $ cd dvm && poetry shell && code .
    $ poetry install
    $ poetry run python main.py [ARGS]
  ```


## Linting & Formatting
[VSCode Guide](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-2/)

## Packaging
[Python packaging Guide](https://typer.tiangolo.com/tutorial/package/)

