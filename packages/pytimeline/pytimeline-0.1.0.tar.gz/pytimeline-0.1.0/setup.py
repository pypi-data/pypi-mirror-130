# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimeline']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'svgwrite>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pytimeline',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
