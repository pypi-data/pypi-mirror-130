# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quacks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quacks',
    'version': '0.0.1',
    'description': 'Improved, mypy-compatible duck typing with Protocol',
    'long_description': "# 🦆 Quacks\n\n> If it walks like a duck and it quacks like a duck, then it must be a duck\n\nImproved, mypy-compatible duck typing with `Protocol`.\n\n(🚧 work in progress 🚧)\n\n## Why?\n\nPEP544 gave us `Protocol`, a way to define duck typing statically.\nIn some cases, it's still a bit cumbersome to work with.\nThis library gives you some much needed niceties.\n\n## Features\n\n### Easy read-only protocols\n\nDefining read-only protocols is great for encouraging immutability and\nworking with frozen dataclasses. Use the `readonly` decorator:\n\n```python\nfrom quacks import readonly\n\n@readonly\nclass User(Protocol):\n    id: int\n    name: str\n    is_premium: bool\n```\n\nWithout this decorator, we'd have to write quite a lot of cruft,\nreducing readability:\n\n```python\nclass User(Protocol):\n    @property\n    def id(self) -> int: ...\n    @property\n    def name(self) -> str: ...\n    @property\n    def is_premium(self) -> bool: ...\n```\n\n### Partial protocols\n\nWhat if you only need part of a protocol?\nImagine we have several functions who use various properties of `User`.\nWith partial protocols you can reuse a data 'shape' without requiring\nall attributes.\n\n(exact syntax TBD)\n\n```python\nfrom quacks import q\n\ndef determine_discount(u: User[q.id.is_premium]) -> int:\n    ...  # access `id` and `is_premium` attributes\n\ndef greet(u: User[q.id.name]) -> None:\n    ...  # access `id` and `name` attributes\n\nu: User = ...\n\ndetermine_discount(u)\ngreet(u)\n```\n",
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ariebovenberg/quacks',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
