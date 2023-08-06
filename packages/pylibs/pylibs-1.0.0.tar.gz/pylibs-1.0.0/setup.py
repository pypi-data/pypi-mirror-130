# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pylibs']
setup_kwargs = {
    'name': 'pylibs',
    'version': '1.0.0',
    'description': 'Install all main modules in one click! :)',
    'long_description': None,
    'author': 'OwoNicoo',
    'author_email': '86409467+DiscordBotML@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
