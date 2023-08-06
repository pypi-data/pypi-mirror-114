# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kicksaw_data_mapping_base', 'kicksaw_data_mapping_base.constants']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.15.0,<3.0.0',
 'gspread>=3.7.0,<4.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'python-configuration-management>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'kicksaw-data-mapping-base',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Timothy Sabat',
    'author_email': 'tim@kicksaw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
