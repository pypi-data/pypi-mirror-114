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
    'version': '2.2',
    'description': 'SnowFlake API Wrapper for Python',
    'long_description': '# Snowflake API\n\n## About\n\nThis is a asynchronous python  API wrapper for [SnowFlakeAPI](https://api.snowflakedev.org/). \n\n## How to Use\n\n```shell\npip install snowflakeapi\n```\n\n## Example Usage\n```python\n    import asyncio\n    from snowflakeapi import SnowClient\n\n    client = SnowClient("YOUR_API_KEY") # Your API Key can be found at https://api.snowflakedev.org/dashboard (sign in w/ discord)\n\n    async def main():\n        print(await client.chat_bot("hello!"))\n    \n    asyncio.run(main())\n\n ```\n\n## API Documentation\n\n[API Documentation](https://snowflakeapi.readthedocs.io/en/latest/)\n\n\n## Want To Contribute?\n\nYou can send a pull request or open an issue to contribute.\nCheck out [Code Of Conduct](CODE_OF_CONDUCT.md) before contributing.\n',
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
