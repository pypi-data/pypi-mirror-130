# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_clash_configer', 'py_clash_configer.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.16.0,<11.0.0']

entry_points = \
{'console_scripts': ['py-clash-configer = py_clash_configer.cli.root:root']}

setup_kwargs = {
    'name': 'py-clash-configer',
    'version': '0.1.0',
    'description': 'Merge Clash configuration subscription and local overrides.',
    'long_description': None,
    'author': 'genzj',
    'author_email': 'zj0512@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
