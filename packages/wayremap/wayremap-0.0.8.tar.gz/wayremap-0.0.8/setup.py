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
    'version': '0.0.8',
    'description': 'A dynamic keyboard remapper for Wayland.',
    'long_description': "[![test](https://github.com/acro5piano/wayremap/actions/workflows/test.yml/badge.svg)](https://github.com/acro5piano/wayremap/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/wayremap.svg)](https://badge.fury.io/py/wayremap)\n\n# wayremap\n\nDynamic keyboard remapper for Wayland.\n\nIt works on both X Window Manager and Wayland, but focused on Wayland as it intercepts evdev input and require root permission.\n\n# Motivation\n\nWayland and Sway is awesome. It brings lots of benefit to Linux desktop environment.\n\nWhen I was using X desktop envionment, there is an awesome tool called `xremap` which remap keys **based on current focused application**.\n\nhttps://github.com/k0kubun/xremap\n\nI was looking for something similar to `xremap` for Wayland, but not found, so I decided to create on my own.\n\n# Install\n\n```bash\nsudo pip install wayremap\n\n# For beta version\nsudo pip3 install git+https://github.com/acro5piano/wayremap\n\n```\n\n# Run\n\nFor Wayland security model, we have to do execute key remapping as root.\n\nSimply write your own service and run it as python script:\n\n```python\n # /etc/wayremap.config.py\n\nfrom wayremap.config import WayremapConfig, Binding\nfrom wayremap.main import run\nfrom wayremap import ecodes as e\nimport uinput as k\n\nwayremap_config = WayremapConfig(\n    # Filter applications which remap will be applied\n    applications=[\n        'Chromium',\n        'Brave-browser',\n        'Leafpad',\n        'firefoxdeveloperedition',\n    ],\n    bindings=[\n        # To see all available binding keys, please see\n        # https://github.com/acro5piano/wayremap/blob/06d27c9bb86b766d7fd1e4230f3a16827785519e/wayremap/ecodes.py\n        # modifier keys are `KEY_LEFTCTRL` or `KEY_LEFTALT`, or both. Neither `shift` nor `super` is not implemented yet.\n\n        # Emacs-like key binding\n        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_A],\n                [[k.KEY_LEFTCTRL, k.KEY_HOME]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_E],\n                [[k.KEY_LEFTCTRL, k.KEY_END]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_H],\n                [[k.KEY_LEFTCTRL, k.KEY_BACKSPACE]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_F], [[k.KEY_RIGHT]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_B], [[k.KEY_LEFT]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_P], [[k.KEY_UP]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_N], [[k.KEY_DOWN]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_K],\n                [[k.KEY_LEFTSHIFT, k.KEY_END], [k.KEY_LEFTCTRL, k.KEY_X]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_A], [[k.KEY_HOME]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_E], [[k.KEY_END]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_Y], [[k.KEY_LEFTCTRL, k.KEY_V]]),\n        Binding([e.KEY_LEFTALT, e.KEY_F], [[k.KEY_LEFTCTRL, k.KEY_RIGHT]]),\n        Binding([e.KEY_LEFTALT, e.KEY_B], [[k.KEY_LEFTCTRL, k.KEY_LEFT]]),\n        Binding([e.KEY_LEFTALT, e.KEY_D], [[k.KEY_LEFTCTRL, k.KEY_DELETE]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_H], [[k.KEY_BACKSPACE]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_D], [[k.KEY_DELETE]]),\n        Binding([e.KEY_LEFTCTRL, e.KEY_S], [[k.KEY_LEFTCTRL, k.KEY_F]]),\n\n\n        # OSX-like key binding\n        Binding([e.KEY_LEFTALT, e.KEY_A], [[k.KEY_LEFTCTRL, k.KEY_A]]),\n        Binding([e.KEY_LEFTALT, e.KEY_C], [[k.KEY_LEFTCTRL, k.KEY_C]]),\n        Binding([e.KEY_LEFTALT, e.KEY_V], [[k.KEY_LEFTCTRL, k.KEY_V]]),\n\n        # Slack helm!\n        Binding([e.KEY_LEFTALT, e.KEY_X], [[k.KEY_LEFTCTRL, k.KEY_K]]),\n    ])\n\n# Finally, run wayremap.\n# Note that `'/dev/input/event4'` varies among system.\nrun(wayremap_config, '/dev/input/event4')\n\n```\n\nAnd then\n\n```\nsudo modprobe uinput\nsudo python /opt/wayremap.py\n```\n\n# Enable wayremap as a systemd service\n\n```bash\necho uinput | sudo tee /etc/modules-load.d/wayremap.conf # Add uinput to auto-loaded linux modules\nsudo vim /etc/wayremap.config.py # Edit your config\nsudo cp ./systemd/wayremap.service /etc/systemd/system/wayremap.service\nsudo systemctl enable wayremap\nsudo reboot\n```\n\n# Known bugs\n\n- ~~`3` is pressed when changing focused window~~ → Fixed now\n- Key repeating become slow while switching focused windowd\n\n# Roadmap\n\n- [x] Enable to run wihtout Sway.\n- [ ] Support `shift` and `super` keys too.\n- [ ] Packaging for Arch Linux, Debian, Fedora, etc.\n- [ ] Enable to load per-application config.\n- [ ] Re-write in Rust for better performance.\n",
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
