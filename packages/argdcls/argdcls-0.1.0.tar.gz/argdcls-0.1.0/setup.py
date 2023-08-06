# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argdcls']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argdcls',
    'version': '0.1.0',
    'description': 'A simple tool to use dataclass as your config',
    'long_description': None,
    'author': 'Sotetsu KOYAMADA',
    'author_email': 'koyamada-s@sys.i.kyoto-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
