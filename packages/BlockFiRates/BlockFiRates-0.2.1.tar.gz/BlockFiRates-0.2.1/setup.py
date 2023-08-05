# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blockfirates']

package_data = \
{'': ['*']}

install_requires = \
['cloudscraper>=1.2.58,<2.0.0', 'lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'blockfirates',
    'version': '0.2.1',
    'description': 'Scrape the latest APY rates for BlockFi Interest Accounts',
    'long_description': None,
    'author': 'P.G. Ó Slatara',
    'author_email': 'pgoslatara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pgoslatara/blockfirates',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
