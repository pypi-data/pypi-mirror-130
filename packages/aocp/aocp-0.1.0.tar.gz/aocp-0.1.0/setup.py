# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aocp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aocp',
    'version': '0.1.0',
    'description': 'A collection of convenient parsers for Advent of Code problems.',
    'long_description': None,
    'author': 'Miguel Blanco Marcos',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
