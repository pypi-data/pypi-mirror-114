# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shioajicaller', 'shioajicaller.cli', 'shioajicaller.codes']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.18.0,<0.19.0',
 'redis>=3.5.3,<4.0.0',
 'shioaji>=0.3.2.dev4,<0.4.0']

entry_points = \
{'console_scripts': ['shioajicaller = shioajicaller.cli:run']}

setup_kwargs = {
    'name': 'shioajicaller',
    'version': '0.1.3.2',
    'description': 'shioaj warp caller',
    'long_description': None,
    'author': 'Steve Lo',
    'author_email': 'info@sd.idv.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
