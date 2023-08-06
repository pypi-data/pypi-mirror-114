# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sindri', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0', 'livereload[doc]>=2.6.3,<3.0.0']

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
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['sindri = sindri.cli:main']}

setup_kwargs = {
    'name': 'sindri',
    'version': '0.1.4',
    'description': 'Set of python functions.',
    'long_description': '# Sindri library\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/sindri">\n    <img src="https://img.shields.io/pypi/v/sindri.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/DarkDemiurg/sindri/actions">\n    <img src="https://github.com/DarkDemiurg/sindri/actions/workflows/dev.yml/badge.svg?branch=master" alt="CI Status">\n</a>\n\n<a href="https://sindri.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/sindri/badge/?version=latest" alt="Documentation Status">\n</a>\n\n<img src="https://img.shields.io/pypi/pyversions/sindri" alt="Python versions">\n<img src="https://img.shields.io/pypi/l/sindri" alt="License">\n</p>\n\n\nSet of python functions\n\n\n* Free software: MIT\n* Documentation: <https://sindri.readthedocs.io>\n\n\n## Features\n\n* TODO\n\n## Credits\n',
    'author': 'Dmitriy Efimov',
    'author_email': 'daefimov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DarkDemiurg/sindri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
