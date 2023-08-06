# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databasedrivers',
 'databasedrivers.Configs',
 'databasedrivers.Configs.Classes',
 'databasedrivers.Configs.Dictonaries',
 'databasedrivers.Connectors',
 'databasedrivers.Interfaces']

package_data = \
{'': ['*']}

install_requires = \
['mysql-connector-python>=8.0.26,<9.0.0']

setup_kwargs = {
    'name': 'databasedrivers',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ptabis',
    'author_email': 'p.tabis@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
