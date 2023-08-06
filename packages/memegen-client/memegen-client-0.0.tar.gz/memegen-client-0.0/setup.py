# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memegen', 'memegen.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'minilog>=2.0,<3.0']

entry_points = \
{'console_scripts': ['memegen = memegen.cli:main']}

setup_kwargs = {
    'name': 'memegen-client',
    'version': '0.0',
    'description': 'The official Python client for Memegen.link',
    'long_description': None,
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/memegen-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
