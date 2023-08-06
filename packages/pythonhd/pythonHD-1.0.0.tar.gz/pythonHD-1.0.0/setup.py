# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pythonhd']
setup_kwargs = {
    'name': 'pythonhd',
    'version': '1.0.0',
    'description': 'Make a best music player in your project now! // write only "import pyHD"',
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
