# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyasync_orm', 'pyasync_orm.clients']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0']

extras_require = \
{'asyncpg': ['asyncpg>=0.23.0,<0.24.0']}

setup_kwargs = {
    'name': 'pyasync-orm',
    'version': '0.1.2',
    'description': 'An async ORM.',
    'long_description': '# pyasync orm\n\n[![pypi](https://img.shields.io/pypi/v/pyasync-orm?color=blue&style=plastic)](https://pypi.python.org/pypi/pyasync-orm)\n[![versions](https://img.shields.io/pypi/pyversions/pyasync-orm)](https://pypi.org/pypi/pyversions/pyasync-orm)\n\nAn asynchronous database ORM for Python.\n\n## Installation\n\nInstall using `pip install pyasync-orm` or `poetry add pyasync-orm`\n',
    'author': 'Ron Williams',
    'author_email': 'rnwprogramming@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ronaldnwilliams/pyasync-orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
