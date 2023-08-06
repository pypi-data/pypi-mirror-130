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
    'version': '0.0.7',
    'description': 'A dynamic keyboard remapper for Wayland.',
    'long_description': "[![test](https://github.com/acro5piano/wayremap/actions/workflows/test.yml/badge.svg)](https://github.com/acro5piano/wayremap/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/wayremap.svg)](https://badge.fury.io/py/wayremap)\n\n# wayremap\n\nDynamic keyboard remapper for Wayland.\n\nIt works on both X Window Manager and Wayland, but focused on Wayland as it intercepts evdev input and require root permission.\n\n# Motivation\n\nWayland and Sway is awesome. It brings lots of benefit to Linux desktop environment.\n\nWhen I was using X desktop envionment, there is an awesome tool called `xremap` which remap keys **based on current focused application**.\n\nhttps://github.com/k0kubun/xremap\n\nI was looking for something similar to `xremap` for Wayland, but not found, so I decided to create on my own.\n\n# Install\n\n```bash\nsudo pip install wayremap\n```\n\n# Run\n\nFor Wayland security model, we have to do execute key remapping as root.\n\nSimply write your own service and run it as python script:\n\n```python\n # /opt/wayremap.py\n\nfrom wayremap.config import WayremapConfig, Binding\nfrom wayremap.main import run\nimport uinput as k\n\nwayremap_config = WayremapConfig(\n    # Filter applications which remap will be applied\n    applications=[\n        'Chromium',\n        'Brave-browser',\n        'Leafpad',\n        'firefoxdeveloperedition',\n    ],\n    bindings=[\n        # Emacs-like key binding\n        Binding('ctrl.alt.a', [[k.KEY_LEFTCTRL, k.KEY_HOME]]),\n        Binding('ctrl.alt.e', [[k.KEY_LEFTCTRL, k.KEY_END]]),\n        Binding('ctrl.alt.h', [[k.KEY_LEFTCTRL, k.KEY_BACKSPACE]]),\n        Binding('ctrl.f', [[k.KEY_RIGHT]]),\n        Binding('ctrl.b', [[k.KEY_LEFT]]),\n        Binding('ctrl.p', [[k.KEY_UP]]),\n        Binding('ctrl.n', [[k.KEY_DOWN]]),\n        Binding('ctrl.k',\n                [[k.KEY_LEFTSHIFT, k.KEY_END], [k.KEY_LEFTCTRL, k.KEY_X]]),\n        Binding('ctrl.a', [[k.KEY_HOME]]),\n        Binding('ctrl.e', [[k.KEY_END]]),\n        Binding('ctrl.y', [[k.KEY_LEFTCTRL, k.KEY_V]]),\n        Binding('alt.f', [[k.KEY_LEFTCTRL, k.KEY_RIGHT]]),\n        Binding('alt.b', [[k.KEY_LEFTCTRL, k.KEY_LEFT]]),\n        Binding('alt.d', [[k.KEY_LEFTCTRL, k.KEY_DELETE]]),\n        Binding('ctrl.h', [[k.KEY_BACKSPACE]]),\n        Binding('ctrl.s', [[k.KEY_LEFTCTRL, k.KEY_F]]),\n\n        # OSX-like key binding\n        Binding('alt.a', [[k.KEY_LEFTCTRL, k.KEY_A]]),\n        Binding('alt.c', [[k.KEY_LEFTCTRL, k.KEY_C]]),\n        Binding('alt.v', [[k.KEY_LEFTCTRL, k.KEY_V]]),\n        Binding('alt.x', [[k.KEY_LEFTCTRL, k.KEY_X]]),\n\n        # Slack helm!\n        Binding('alt.x', [[k.KEY_LEFTCTRL, k.KEY_K]]),\n    ])\n\nrun(wayremap_config, '/dev/input/event4')\n\n```\n\nAnd then\n\n```\nsudo modprobe uinput\nsudo python /opt/wayremap.py\n```\n\nPlease note that\n\n- modifier keys are `ctrl` or `alt` or both\n- `'/dev/input/event4'` varies among system.\n\n# Known bugs\n\n- `3` is pressed when changing focused window\n- Key repeating become slow while switching focused windowd\n\n# Roadmap\n\n- Support `shift` key too.\n- Enable to run wihtout Sway.\n- Packaging for Arch Linux, Debian, Fedora, etc.\n- Enable to load per-application config.\n- Re-write in Rust for better performance.\n",
    'author': 'Kay Gosho',
    'author_email': 'ketsume0211@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acro5piano/wayremap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
