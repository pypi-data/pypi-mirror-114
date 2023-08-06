# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowflakeapi']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.1.1,<5.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'pytest-asyncio>=0.15.1,<0.16.0',
 'pytest>=6.2.4,<7.0.0',
 'python-dotenv>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'snowflakeapi',
    'version': '2.1',
    'description': 'SnowFlake API Wrapper for Python',
    'long_description': None,
    'author': 'DevSynth',
    'author_email': 'synth@snowflakedev.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
