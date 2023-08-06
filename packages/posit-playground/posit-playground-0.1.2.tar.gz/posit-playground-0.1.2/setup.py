# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['posit_playground']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.0.0,<2.0.0', 'pytest>=6.2.5,<7.0.0', 'softposit>=0.3.4.4,<0.4.0.0']

setup_kwargs = {
    'name': 'posit-playground',
    'version': '0.1.2',
    'description': 'Posit arithmetic library with no frills',
    'long_description': '<a href="https://github.com/urbanij/posit-playground/actions"><img src="https://github.com/urbanij/posit-playground/actions/workflows/main.yml/badge.svg"></a>\n[![codecov](https://codecov.io/gh/urbanij/posit-playground/branch/main/graph/badge.svg?token=U37RUDDRN1)](https://codecov.io/gh/urbanij/posit-playground)\n\n# posit-playground\n\nPosit library with no frills\n\n## Install\n\n- stable\n\n```sh\npip install posit-playground\n```\n\n<!-- - main\n\n```sh\npip install git+https://github.com/urbanij/posit-playground.git\n``` -->\n\n## Usage\n\n```python\nfrom posit_playground import posit\n\np1 = posit.from_bits(\n    bits = 0b000110111011101, \n    size = 16, \n    es = 3,\n)\n\np1 * p1 # implements posit multiplication\n```\n\nor better yet, launch a notebook on binder \n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/urbanij/posit-playground/HEAD?labpath=notebooks%2F1_posit_decode.ipynb)\n\nor visit [notebooks/1_posit_decode.ipynb](https://github.com/urbanij/posit-playground/blob/main/notebooks/1_posit_decode.ipynb)\n\n\n## Demo\n\n[![asciicast](https://asciinema.org/a/455652.svg)](https://asciinema.org/a/455652)\n\n\nScreenshot of posit-playground in action, with a corner case example in which the exponent is chopped off the bit fields\n\n![Imgur](https://imgur.com/0M8USPC.jpg)\n',
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbanij/posit-playground',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
