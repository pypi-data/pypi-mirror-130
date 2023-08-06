# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['posit_playground']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0', 'pytest>=6.2.5,<7.0.0', 'softposit>=0.3.4.4,<0.4.0.0']

setup_kwargs = {
    'name': 'posit-playground',
    'version': '0.1.0',
    'description': 'Posit arithmetic library with no frills',
    'long_description': None,
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
