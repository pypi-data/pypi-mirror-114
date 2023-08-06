# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cdh_main']
setup_kwargs = {
    'name': 'cdh-main',
    'version': '2.0.5',
    'description': 'Three folded data structure {(ID) key : value} with ID as int, key as str and value as variable type',
    'long_description': None,
    'author': 'Roberto Amadori',
    'author_email': 'robiamado@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
}


setup(**setup_kwargs)
