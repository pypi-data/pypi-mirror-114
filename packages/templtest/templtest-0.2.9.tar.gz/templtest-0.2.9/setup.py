# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['templtest']

package_data = \
{'': ['*']}

install_requires = \
['ansible>=2.9,<3.0', 'packaging>=20.9,<21.0']

entry_points = \
{'console_scripts': ['templtest = templtest.cli:main']}

setup_kwargs = {
    'name': 'templtest',
    'version': '0.2.9',
    'description': 'A tool for testing Ansible role templates.',
    'long_description': None,
    'author': 'Alexey Busygin',
    'author_email': 'yaabusygin@gmail.com',
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
