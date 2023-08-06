# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csaad_crypto2']

package_data = \
{'': ['*'], 'csaad_crypto2': ['assets/*']}

install_requires = \
['dash>=2.0.0,<3.0.0',
 'krakenex>=2.1.0,<3.0.0',
 'pandas>=1.3.4,<2.0.0',
 'plotly>=5.4.0,<6.0.0',
 'pykrakenapi>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'csaad-crypto2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Carlos Saad',
    'author_email': 'csaad@alumni.unav.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
