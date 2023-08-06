# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptovwap', 'cryptovwap.back', 'cryptovwap.front']

package_data = \
{'': ['*'], 'cryptovwap': ['assets/*']}

install_requires = \
['dash>=2.0.0,<3.0.0',
 'krakenex>=2.1.0,<3.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pykrakenapi>=0.2.3,<0.3.0',
 'python-bitvavo-api>=1.2.2,<2.0.0',
 'twine>=3.7.1,<4.0.0']

entry_points = \
{'console_scripts': ['cryptovwap = cryptovwap.app']}

setup_kwargs = {
    'name': 'cryptovwap',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Pablo Manso',
    'author_email': '92manso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
