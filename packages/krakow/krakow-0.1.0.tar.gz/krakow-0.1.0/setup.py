# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['krakow']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0', 'networkx>=2.6.1,<3.0.0', 'numpy>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'krakow',
    'version': '0.1.0',
    'description': 'Well balanced hierarchical graph clustering',
    'long_description': None,
    'author': 'Filip Sondej',
    'author_email': 'filipsondej@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
