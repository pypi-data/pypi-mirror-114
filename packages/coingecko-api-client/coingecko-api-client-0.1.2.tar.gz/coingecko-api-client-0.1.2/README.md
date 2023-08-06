# CoinGecko API Client

Unofficial [CoinGecko API](https://www.coingecko.com/en/api) client based on HTTPX.

## Badges

[![codecov](https://codecov.io/gh/eserdk/coingecko-api-client/branch/main/graph/badge.svg?token=7NQRF7FPKU)](https://codecov.io/gh/eserdk/coingecko-api-client)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install coingecko-api-client
```  

Or [poetry](https://python-poetry.org).

```bash
poetry add coingecko-api-client
```  

## Usage

```python
# imports sync client
from coingecko_api_client.client import CoinGeckoAPIClient

# imports async client
from coingecko_api_client.client import CoinGeckoAPIAsyncClient

# instantiates sync client
sync_client = CoinGeckoAPIClient()

# instantiates async client
async_client = CoinGeckoAPIAsyncClient()

# pings CoinGecko API with sync client
sync_ping_data = sync_client.ping()

# pings CoinGecko API with async client
async_ping_data = await async_client.ping()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Thanks
This readme file was constructed using [this template](https://www.makeareadme.com).
