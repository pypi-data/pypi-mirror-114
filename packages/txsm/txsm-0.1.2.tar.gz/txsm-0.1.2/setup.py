# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['txsm']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'clipboard>=0.0.4,<0.0.5']

entry_points = \
{'console_scripts': ['tuxsm = txsm.main:say', 'txsm = txsm.main:main']}

setup_kwargs = {
    'name': 'txsm',
    'version': '0.1.2',
    'description': 'A combination of tuxsay and mockman',
    'long_description': None,
    'author': 'Arghya Sarkar',
    'author_email': 'arghyasarkar.nolan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
