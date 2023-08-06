# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coingecko_api_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'coingecko-api-client',
    'version': '0.1.1',
    'description': 'Unofficial CoinGecko API client based on HTTPX',
    'long_description': '# CoinGecko API Client\n\nUnofficial [CoinGecko API](https://www.coingecko.com/en/api) client based on HTTPX.\n\n## Badges\n\n[![codecov](https://codecov.io/gh/eserdk/coingecko-api-client/branch/main/graph/badge.svg?token=7NQRF7FPKU)](https://codecov.io/gh/eserdk/coingecko-api-client)\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.\n\n```bash\npip install coingecko-api-client\n```  \n\nOr [poetry](https://python-poetry.org).\n\n```bash\npoetry add coingecko-api-client\n```  \n\n## Usage\n\n```python\n# imports sync client\nfrom coingecko_api_client.client import CoinGeckoAPIClient\n\n# imports async client\nfrom coingecko_api_client.client import CoinGeckoAPIAsyncClient\n\n# instantiates sync client\nsync_client = CoinGeckoAPIClient()\n\n# instantiates async client\nasync_client = CoinGeckoAPIAsyncClient()\n\n# pings CoinGecko API with sync client\nsync_ping_data = sync_client.ping()\n\n# pings CoinGecko API with async client\nasync_ping_data = await async_client.ping()\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Thanks\nThis readme file was constructed using [this template](https://www.makeareadme.com).\n',
    'author': 'Eugene Serdyuk',
    'author_email': 'eugene.serdyuk@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eserdk/coingecko-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
