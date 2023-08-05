# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_websockets']

package_data = \
{'': ['*']}

install_requires = \
['pylint']

setup_kwargs = {
    'name': 'pylint-websockets',
    'version': '0.1.0',
    'description': 'A Pylint plugin for the Python websockets library',
    'long_description': None,
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
