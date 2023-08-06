# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brant_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = brant_csv_converter.converter:converter',
                     'json_converter = '
                     'brant_csv_converter.converter:converter2']}

setup_kwargs = {
    'name': 'brant-csv-converter',
    'version': '0.1.0',
    'description': 'Program that convert a archive csv to json and json to csv',
    'long_description': None,
    'author': 'Bruno Brant',
    'author_email': 'bruno.tombrant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
