# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jm_crypto_ciphers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jm-crypto-ciphers',
    'version': '1.0.3',
    'description': 'Implements various ciphers from the pycryptodome package and some custom ones.',
    'long_description': None,
    'author': 'Jonathan Mahaffey',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
