# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['em', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.7.4,<4.0.0',
 'arrow>=1.1.1,<2.0.0',
 'fire==0.4.0',
 'hacktcha==0.2.2',
 'pillow>=8.2,<9.0',
 'pyee>=7.0.4,<8.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'sanic>=21.3.4,<22.0.0',
 'websockets>=8.1.0,<9.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.2.4',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['em = em.cli:main']}

setup_kwargs = {
    'name': 'zillionare-em',
    'version': '0.1.0',
    'description': 'earn money.',
    'long_description': '# em\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/em">\n    <img src="https://img.shields.io/pypi/v/em.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/zillionare/em/actions">\n    <img src="https://github.com/zillionare/em/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://em.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/em/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\n\n\n\n* Free software: MIT\n* Documentation: <https://em.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Aaron Yang',
    'author_email': 'code@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zillionare/em',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '==3.7.9',
}


setup(**setup_kwargs)
