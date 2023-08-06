# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appletrun']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['appletrun = appletrun.__main__:main']}

setup_kwargs = {
    'name': 'appletrun',
    'version': '1.5.5',
    'description': '',
    'long_description': None,
    'author': 'Royal-lobster',
    'author_email': 'srujangs8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
