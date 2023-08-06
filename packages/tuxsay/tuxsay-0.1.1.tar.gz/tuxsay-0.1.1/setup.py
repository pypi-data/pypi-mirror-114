# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuxsay']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['txs = tuxsay.main:main']}

setup_kwargs = {
    'name': 'tuxsay',
    'version': '0.1.1',
    'description': 'A CLI like cowsay but its Tux as your host',
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
