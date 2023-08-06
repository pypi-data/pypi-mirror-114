# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lowdash']

package_data = \
{'': ['*']}

install_requires = \
['sphinx-rtd-theme>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'lowdash',
    'version': '1.4.0',
    'description': 'A python implementation of lodash in javascript',
    'long_description': "# Lowdash\n\nLowdash is a simple implementation of lodash in python.\n\nLowdash will provide you with a set of functions that will help to work with arrays, objects and other data structures.\n\n# Installing\n\n```bash\npip install lowdash\n```\n\n# Getting Started\n\nTo get started you can use the following code:\n\n```python\nfrom lowdash.arrays import *\ncompact(['a', '', 'b', None, 'c'])\n# Output : ['a', 'b', 'c']\n```\n\n## Documentation Comming Soon!\n",
    'author': 'abh80',
    'author_email': 'boatgithub27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abh80/lowdash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
