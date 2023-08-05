# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdmn', 'sdmn.elements']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'clint>=0.5.1,<0.6.0',
 'docker>=3.5.0,<4.0.0',
 'pastel>=0.1.0,<0.2.0',
 'python-slugify>=1.2,<2.0']

entry_points = \
{'console_scripts': ['sdmn = sdmn.sdmn:main']}

setup_kwargs = {
    'name': 'sdmn',
    'version': '0.1.2',
    'description': 'Quickstart your masternode',
    'long_description': "SmartDex MasterNode (sdmn) is a cli tool to help you run a SmartDex masternode\n\n## Running and applying a masternode\n\nIf you are consulting this repo, it's probably because you want to run a masternode.\nFor complete guidelines on running a masternode candidate, please refer to the [documentation](https://docs.swapdex.net/masternode/requirements/).\n",
    'author': 'Etienne Napoleone',
    'author_email': 'info@swapdex.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://swapdex.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
