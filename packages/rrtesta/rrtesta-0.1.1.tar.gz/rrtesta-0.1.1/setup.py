# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrtesta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rrtesta',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'RJ Rybarczyk',
    'author_email': 'rj@rybar.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.5,<4.0.0',
}


setup(**setup_kwargs)
