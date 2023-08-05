# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deft_hep']

package_data = \
{'': ['*']}

install_requires = \
['corner>=2.2.1,<3.0.0',
 'emcee>=3.0.2,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'deft-hep',
    'version': '0.5.6',
    'description': 'dEFT is a tool for performing fits of EFT coefficients to HEP data in seconds',
    'long_description': None,
    'author': 'Alexander Veltman',
    'author_email': 'alexveltman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codecalec/dEFT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
