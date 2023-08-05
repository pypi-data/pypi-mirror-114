# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lowdash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lowdash',
    'version': '0.1.0',
    'description': 'A python implementation of lodash in javascript',
    'long_description': None,
    'author': 'abh80',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
