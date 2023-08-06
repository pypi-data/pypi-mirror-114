# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsserpent', 'rsserpent.model']

package_data = \
{'': ['*'], 'rsserpent': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'arrow>=1.1.1,<2.0.0',
 'fastapi>=0.65.2,<0.66.0',
 'importlib-metadata>=4.5.0,<5.0.0',
 'pydantic[email]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'rsserpent',
    'version': '0.1.2',
    'description': '🐍 This snake helps you reconnect the Web, with RSS feeds!',
    'long_description': None,
    'author': 'Queensferry',
    'author_email': 'queensferry.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
