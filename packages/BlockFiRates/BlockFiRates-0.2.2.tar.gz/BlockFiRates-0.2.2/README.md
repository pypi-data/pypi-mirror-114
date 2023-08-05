![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blockfirates)

# DISCLAIMER

This package is in no way affiliated in any way, shape or form with BlockFi and as such its use is entirely at the user's own risk.

# BlockFiRates

An unofficial API to easily obtain the interest rates of [BlockFi Interest Accounts (BIA)](https://blockfi.com/rates/).

# Getting Started

### Installing
```
pip install blockfirates
```
### Imports
```
from blockfirates import client
Client=client.BlockFiRates()
```

## Available Functions
* get_all_rates
* get_amount
* get_apy

## get_all_rates
Printing info for all currencies:
```
rates = Client.get_all_rates()
for i in rates:
    print(i)
```

## get_amount
Printing amount criteria for a specific currency:
```
Client.get_amount("BTC (Tier 1)")
```

## get_apy
Printing APY rate for a specific currency:
```
Client.get_apy("BTC (Tier 1)")
```

### Development
Use [Poetry](https://python-poetry.org/) to create a virtual environment based on the `pyproject.toml` file:
```
poetry init
```
Once changes have been committed the package can be updated on both Github and PyPi:
```
git push -u origin master

poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```
