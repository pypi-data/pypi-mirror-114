# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scholarium']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scholarium',
    'version': '0.1.0',
    'description': 'Environment for scholarly computational books (compBook)',
    'long_description': '# Computational books for scholars\n',
    'author': 'Gerd Graßhoff',
    'author_email': 'gerd.grasshoff@opensciencetechnology.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
