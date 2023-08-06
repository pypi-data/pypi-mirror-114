# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libp',
    'version': '1.0.0',
    'description': 'libp',
    'long_description': None,
    'author': 'Ardustri',
    'author_email': 'contact@ardustri.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
