# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['degiro_connector',
 'degiro_connector.migration',
 'degiro_connector.quotecast',
 'degiro_connector.quotecast.constants',
 'degiro_connector.quotecast.helpers',
 'degiro_connector.quotecast.models',
 'degiro_connector.quotecast.pb',
 'degiro_connector.trading',
 'degiro_connector.trading.constants',
 'degiro_connector.trading.helpers',
 'degiro_connector.trading.models',
 'degiro_connector.trading.pb']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.38.1,<2.0.0',
 'onetimepass>=1.0.1,<2.0.0',
 'orjson>=3.6.0,<4.0.0',
 'pandas<=1.1.5',
 'protobuf>=3.17.3,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'degiro-connector',
    'version': '1.0.6',
    'description': "This is yet another library to access Degiro's API.",
    'long_description': None,
    'author': 'Chavithra PARANA',
    'author_email': 'chavithra@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chavithra/degiro-connector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
