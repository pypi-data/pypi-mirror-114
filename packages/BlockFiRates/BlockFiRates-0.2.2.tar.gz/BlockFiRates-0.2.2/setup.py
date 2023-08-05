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
    'version': '0.2.2',
    'description': 'Scrape the latest APY rates for BlockFi Interest Accounts',
    'long_description': '![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blockfirates)\n\n# DISCLAIMER\n\nThis package is in no way affiliated in any way, shape or form with BlockFi and as such its use is entirely at the user\'s own risk.\n\n# BlockFiRates\n\nAn unofficial API to easily obtain the interest rates of [BlockFi Interest Accounts (BIA)](https://blockfi.com/rates/).\n\n# Getting Started\n\n### Installing\n```\npip install blockfirates\n```\n### Imports\n```\nfrom blockfirates import client\nClient=client.BlockFiRates()\n```\n\n## Available Functions\n* get_all_rates\n* get_amount\n* get_apy\n\n## get_all_rates\nPrinting info for all currencies:\n```\nrates = Client.get_all_rates()\nfor i in rates:\n    print(i)\n```\n\n## get_amount\nPrinting amount criteria for a specific currency:\n```\nClient.get_amount("BTC (Tier 1)")\n```\n\n## get_apy\nPrinting APY rate for a specific currency:\n```\nClient.get_apy("BTC (Tier 1)")\n```\n\n### Development\nUse [Poetry](https://python-poetry.org/) to create a virtual environment based on the `pyproject.toml` file:\n```\npoetry init\n```\nOnce changes have been committed the package can be updated on both Github and PyPi:\n```\ngit push -u origin master\n\npoetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD\n```\n',
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
