# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydra_slayer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0']

setup_kwargs = {
    'name': 'hydra-slayer',
    'version': '0.1.0rc0',
    'description': 'A framework for elegantly configuring complex applications',
    'long_description': '# Hydra Slayer\n\nHydra Slayer is a 4th level spell in the School of Fire Magic.\nDepending of the level of expertise in fire magic,\nslayer spell increases attack of target troop by 8 against\nhydras, snakes (especially pythons), and other creatures.\n',
    'author': 'Sergey Kolesnikov',
    'author_email': 'scitator@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://catalyst-team.github.io/hydra-slayer/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
