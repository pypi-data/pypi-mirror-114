# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repltable']

package_data = \
{'': ['*']}

install_requires = \
['replit>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'repltable',
    'version': '0.1.2',
    'description': 'Table support for the replit database',
    'long_description': None,
    'author': 'terabyte.',
    'author_email': 'mikey@mikeyo.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
