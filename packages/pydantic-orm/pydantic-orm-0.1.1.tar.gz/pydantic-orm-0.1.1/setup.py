# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_orm']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-orm',
    'version': '0.1.1',
    'description': 'An asynchronous ORM that uses pydantic.',
    'long_description': '# pydantic orm\n\n[![pypi](https://img.shields.io/pypi/v/pydantic-orm?color=blue&style=plastic)](https://pypi.python.org/pypi/pydantic-orm)\n[![versions](https://img.shields.io/pypi/pyversions/pydantic-orm)](https://pypi.org/pypi/pyversions/pydantic-orm)\n\nAsynchronous database ORM using Pydantic.\n\n## Installation\n\nInstall using `pip install -U pydantic-orm` or `poetry add pydantic-orm`\n',
    'author': 'Ronald Williams',
    'author_email': 'rnwprogramming@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
