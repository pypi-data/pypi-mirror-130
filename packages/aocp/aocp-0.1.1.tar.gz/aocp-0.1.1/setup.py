# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aocp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aocp',
    'version': '0.1.1',
    'description': 'A collection of convenient parsers for Advent of Code problems.',
    'long_description': '# Advent of Code parsers\nA collection of convenient parsers for Advent of Code problems.\n',
    'author': 'Miguel Blanco Marcos',
    'author_email': 'miguel.blanco.marcos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miguel-bm/advent-of-code-parsers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
