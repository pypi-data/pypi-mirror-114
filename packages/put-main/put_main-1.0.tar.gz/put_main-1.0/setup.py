# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['put_main']
setup_kwargs = {
    'name': 'put-main',
    'version': '1.0',
    'description': 'A set of utility classes and functions',
    'long_description': None,
    'author': 'Roberto Amadori',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
