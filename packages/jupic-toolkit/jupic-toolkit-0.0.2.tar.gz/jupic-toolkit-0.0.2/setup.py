# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupic_toolkit',
 'jupic_toolkit.grader',
 'jupic_toolkit.json',
 'jupic_toolkit.ninja_robot']

package_data = \
{'': ['*'], 'jupic_toolkit.ninja_robot': ['assets/*']}

setup_kwargs = {
    'name': 'jupic-toolkit',
    'version': '0.0.2',
    'description': 'JupIC toolkit',
    'long_description': '# jupic-toolkit\nJupIC toolkit\n\n## Run \n```shell\n$ make run\n```\n\n## Install\n```shell\n$ poetry install\n```\n\n## Package\nBump version with Poetry (or manually in `pyproject.toml`), \n```shell\n$ poetry version (patch|minor|major)\n```\n\nThen:\n```shell\n$ make package\n```',
    'author': 'g1stavo',
    'author_email': 'gustavocsalvador@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/g1stavo/jupic-toolkit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*',
}


setup(**setup_kwargs)
