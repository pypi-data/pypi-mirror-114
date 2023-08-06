# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tym', 'tym.commands', 'tym.config_parser']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'aiohttp_cors>=0.7.0,<0.8.0',
 'cached-property>=1.5.2,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'pygit2>=1.6.1,<2.0.0',
 'simple-term-menu>=1.2.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'watchgod>=0.7,<0.8']

entry_points = \
{'console_scripts': ['tym = tym.main:app']}

setup_kwargs = {
    'name': 'tym',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Tym',
    'author_email': 'dev@tym.so',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
