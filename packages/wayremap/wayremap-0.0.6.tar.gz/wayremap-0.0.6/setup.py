# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wayremap']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.4.0,<2.0.0', 'i3ipc>=2.2.1,<3.0.0', 'python-uinput>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'wayremap',
    'version': '0.0.6',
    'description': 'A dynamic keyboard remapper for Wayland.',
    'long_description': None,
    'author': 'Kay Gosho',
    'author_email': 'ketsume0211@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
