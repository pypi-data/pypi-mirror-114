# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flon',
    'version': '0.1.0',
    'description': 'FLON parser for Python',
    'long_description': None,
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
