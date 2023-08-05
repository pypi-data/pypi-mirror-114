# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tox_demo']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=57.1.0,<58.0.0', 'tox>=3.23.1,<4.0.0', 'wheel>=0.36.2,<0.37.0']

setup_kwargs = {
    'name': 'tox-demo',
    'version': '0.1.0',
    'description': 'A demo for tox, pyproject, wheel, setuptools',
    'long_description': None,
    'author': 'mog',
    'author_email': 'mo.gao@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
