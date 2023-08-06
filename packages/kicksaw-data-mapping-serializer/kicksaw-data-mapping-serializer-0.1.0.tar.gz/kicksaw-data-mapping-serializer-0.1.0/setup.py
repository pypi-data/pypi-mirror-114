# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kicksaw_data_mapping_serializer']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath-ng>=1.5.3,<2.0.0', 'kicksaw-data-mapping-base>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'kicksaw-data-mapping-serializer',
    'version': '0.1.0',
    'description': 'Reads a csv/gdoc from kicksaw-data-mapping-serializer and automatically performs serialization',
    'long_description': '# Setup\n\nFollow the steps from https://github.com/Kicksaw-Consulting/kicksaw-data-mapping-base to get connected to gdrive\n\nAfterwards, you should be good-to-go. See the `tests` folder for examples on how to use this libary\n',
    'author': 'Alex Drozd',
    'author_email': 'alex@kicksaw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kicksaw-Consulting/kicksaw-data-mapping-serializer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
