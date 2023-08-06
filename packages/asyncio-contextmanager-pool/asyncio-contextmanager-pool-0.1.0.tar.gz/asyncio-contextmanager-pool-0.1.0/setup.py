# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_contextmanager_pool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncio-contextmanager-pool',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'André Carvalho',
    'author_email': 'afecarvalho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
