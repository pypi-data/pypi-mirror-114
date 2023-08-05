# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deno_version_manager']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.7b0,<22.0',
 'coverage>=5.5,<6.0',
 'mypy>=0.910,<0.911',
 'pytest-cov>=2.12.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dvm = deno_version_manager.main:app']}

setup_kwargs = {
    'name': 'deno-version-manager',
    'version': '0.1.0',
    'description': 'dvm - a cli to manage deno versions',
    'long_description': '# Deno Version Manager\n\nSimple CLI to manage [Deno](https://deno.land/) versions\n\n\nCreated with [typer](typer.tiangolo.com) and [poetry](https://python-poetry.org)\n\n\n# Usage\n\n| Command               | Description                                             |\n| --------------------- | ------------------------------------------------------- |\n| dvm use               | look for a .dvm file and use the specified deno version |\n| dvm install [version] | install a specific deno version or auto-install latest  |\n| dvm upgrade [version] | upgrade to a specific version or auto-install latest    |\n| dvm uninstall         | remove deno                                             |\n\n\n# Development\nIn VSCode\n  ```\n    $ cd dvm && poetry shell && code .\n    $ poetry install\n    $ poetry run python main.py [ARGS]\n  ```\n\n\n## Linting & Formatting\n[VSCode Guide](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-2/)\n\n## Packaging\n[Python packaging Guide](https://typer.tiangolo.com/tutorial/package/)\n\n',
    'author': 'dev-124',
    'author_email': '60511077+dev-124@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dev-124/dvm/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
