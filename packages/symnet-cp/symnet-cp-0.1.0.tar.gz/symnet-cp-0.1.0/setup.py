# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symnet_cp']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<21.3.0', 'prometheus-client>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'symnet-cp',
    'version': '0.1.0',
    'description': 'SymNet External Control Protocol implementation',
    'long_description': '# SymNet Control Protocol implementation\n\nThis is an asyncio implementation of the [SymNet Control Protocol](https://www.symetrix.co/repository/SymNet_cp.pdf).\nAt bermudafunk we use this to control a Solus 16x8.\n',
    'author': 'Christian Kohlstedde',
    'author_email': 'christian@kohlsted.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
