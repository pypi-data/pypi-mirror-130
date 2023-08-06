# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bpsci']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bpsci',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jerryvarghese1',
    'author_email': '63359305+jerryvarghese1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
