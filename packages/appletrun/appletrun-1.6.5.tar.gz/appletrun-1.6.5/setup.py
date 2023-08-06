# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appletrun']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['appletrun = appletrun._main_:main']}

setup_kwargs = {
    'name': 'appletrun',
    'version': '1.6.5',
    'description': '✨ Appletrun takes java file as input and runs the applet instantly with out compilation and html files',
    'long_description': '# APPLETRUN\n![](https://img.shields.io/pypi/v/appletrun?style=for-the-badge)\n![](https://img.shields.io/apm/l/vim-mode?style=for-the-badge)\n![](https://img.shields.io/badge/requires-Java%20%3C%3D%208-red?style=for-the-badge)\n\nAppletRun runs applet code from given java file in a new window\n\n## 👉 Installation\n```\npip install appletrun\n```\n## 👉 Usage\n```\n appletrun nameOfFile.java\n```\n<p align="center">\n<img src="https://user-images.githubusercontent.com/52039218/127250568-51bfd770-49c3-4d32-9da3-18627d9abde3.gif"/>\n </p>\n',
    'author': 'Royal-lobster',
    'author_email': 'srujangs8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Royal-lobster/appletrun-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
