# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['late_bound_arguments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'late-bound-arguments',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Shakya Majumdar',
    'author_email': 'shakyamajumdar1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
