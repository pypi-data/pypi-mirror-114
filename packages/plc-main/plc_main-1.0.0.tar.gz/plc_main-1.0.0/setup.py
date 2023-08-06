# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['plc_main']
setup_kwargs = {
    'name': 'plc-main',
    'version': '1.0.0',
    'description': 'Logical components in python.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
