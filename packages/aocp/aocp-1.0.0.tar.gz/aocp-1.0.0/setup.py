# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aocp']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'aocp',
    'version': '1.0.0',
    'description': 'A collection of convenient parsers for Advent of Code problems.',
    'long_description': '# Advent of Code Parsers\n\n[![pyversions](https://img.shields.io/pypi/pyversions/aocp)](https://www.python.org/)\n\n\nA collection of convenient Python parsers for Advent of Code problems.\n\n\n## Installation\n\n```bash\npip install aocp\n```\n\n## Quickstart\n\nYou can import parsers from the base module. There are two main types of parsers:\n * Iterable parsers, which return a sequence of elements from parsing a `str`, such as `list`, `tuple` or `dict`\n * Transform parsers, which return a single object from parsing a `str`, such as an `int`, `bool` or another `str`\n\nIterable parsers can be composed with other parsers nested within, including Transform parsers and other Iterable parsers. They can also be nested with some base types such as `int`.\n\nTransform parsers cannot have nested parsers, but they can be composed with other parsers in a sequence using `ChainParser`.\n\nThis way, the structure of the output data mirrors that of the expression used to instantiate the parser transform.\n\nHere is a basic usage example:\n\n```python\nraw_data = "46,79,77,45,57,34,44,13,32,88,86,82,91,97"\nparser = ListParser(IntParser)\nparser.parse(raw_data)\n```\n\nWhich results in:\n```\n[46, 79, 77, 45, 57, 34, 44, 13, 32, 88, 86, 82, 91, 97]\n```\n\nAnd here is a more advanced example, from [AoC 2021 day 4](https://adventofcode.com/2021/day/4):\n```python\nraw_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n\n22 13 17 11  0\n 8  2 23  4 24\n21  9 14 16  7\n 6 10  3 18  5\n 1 12 20 15 19\n\n 3 15  0  2 22\n 9 18 13 17  5\n19  8  7 25 23\n20 11 10 24  4\n14 21 16 12  6\n\n14 21 17 24  4\n10 16 15  9 19\n18  8 23 26 20\n22 11 13  6  5\n 2  0 12  3  7"""\nparser = TupleParser(\n    (\n        IntListParser(),\n        ListParser(ListParser(IntListParser())),\n    )\n)\nparser.parse(raw_data)\n```\n\nWhich results in:\n```\n(\n    [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1], \n    [[[22, 13, 17, 11, 0],\n     [8, 2, 23, 4, 24],\n     [21, 9, 14, 16, 7],\n     [6, 10, 3, 18, 5],\n     [1, 12, 20, 15, 19]],\n    [[3, 15, 0, 2, 22],\n     [9, 18, 13, 17, 5],\n     [19, 8, 7, 25, 23],\n     [20, 11, 10, 24, 4],\n     [14, 21, 16, 12, 6]],\n    [[14, 21, 17, 24, 4],\n     [10, 16, 15, 9, 19],\n     [18, 8, 23, 26, 20],\n     [22, 11, 13, 6, 5],\n     [2, 0, 12, 3, 7]]]\n)\n```\n\nBy default, the splitting elements in an iterable are guessed from the string provided. However, you can provide them through the `splitter` argument. This can be a strings or a sequence of strings, which will all act as splitters.\n\nA notebook with more examples from Aoc 2021 is available [here](./examples/aoc-2021.ipynb).\n\n## To be done\n * Full testing coverage\n * Documentation page (full docstrings are available, though)\n * More examples from other previous years\n * Regex Parser\n * Defaults in tuple parser in case of missing components in origin string\n## Source code\n\n[https://github.com/miguel-bm/advent-of-code-parsers](https://github.com/miguel-bm/advent-of-code-parsers)',
    'author': 'Miguel Blanco Marcos',
    'author_email': 'miguel.blanco.marcos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miguel-bm/advent-of-code-parsers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
