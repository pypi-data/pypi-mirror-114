import copy
import datetime as dt
import time
from typing import Callable, Dict, List, Optional, Type, Union

import httpx

DATE_FORMAT = "%d-%m-%Y"
EVENTS_DATE_FORMAT = "%Y-%m-%d"


def _fix_params(params: Dict) -> Dict:
    params_ = copy.deepcopy(params)
    for k in params_:
        if isinstance(params_[k], list):
            params_[k] = ",".join(params_[k])
    return params_


class _BaseCoinGeckoAPIClient:
    _client: Union[httpx.Client, httpx.AsyncClient]

    def __init__(
        self,
        client_type: Type[Union[httpx.Client, httpx.AsyncClient]],
        base_url: str = "https://api.coingecko.com/api/v3",
        proxies: Optional[List[str]] = None,
    ) -> None:
        self._client = client_type(
            timeout=30,
            base_url=base_url,
            headers={"Connection": "keep-alive"},
            proxies=proxies,
        )


class CoinGeckoAPIClient(_BaseCoinGeckoAPIClient):
    def __init__(
        self,
        base_url: str = "https://api.coingecko.com/api/v3",
        proxies: Optional[List[str]] = None,
    ) -> None:
        super(CoinGeckoAPIClient, self).__init__(
            client_type=httpx.Client, base_url=base_url, proxies=proxies
        )

    def make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> httpx.Response:
        actual_method: Callable = getattr(self._client, method)
        response: httpx.Response = actual_method(
            url=url, params=_fix_params(params), headers=headers
        )
        response.raise_for_status()
        return response

    def ping(self) -> Dict:
        response = self.make_request("get", "/ping")
        return response.json()

    def simple_price(
        self,
        ids: List[str],
        vs_currencies: List[str],
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict:
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": include_market_cap,
            "include_24hr_vol": include_24hr_vol,
            "include_24hr_change": include_24hr_change,
            "include_last_updated_at": include_last_updated_at,
        }
        response = self.make_request("get", "/simple/price", params)
        return response.json()

    def simple_token_price(
        self,
        asset_platform_id: str,
        contract_addresses: List[str],
        vs_currencies: List[str],
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict:
        params = {
            "contract_addresses": contract_addresses,
            "vs_currencies": vs_currencies,
            "include_market_cap": include_market_cap,
            "include_24hr_vol": include_24hr_vol,
            "include_24hr_change": include_24hr_change,
            "include_last_updated_at": include_last_updated_at,
        }
        response = self.make_request(
            "get", f"/simple/token_price/{asset_platform_id}", params
        )
        return response.json()

    def simple_supported_vs_currencies(self) -> List[str]:
        response = self.make_request("get", "/simple/supported_vs_currencies")
        return response.json()

    def coins_list(
        self, include_platform: bool = False
    ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        response = self.make_request(
            "get", "/coins/list", params={"include_platform": include_platform}
        )
        return response.json()

    def coins_markets(
        self,
        vs_currency: str,
        ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: Optional[List[str]] = None,
    ) -> List:
        params = {
            "vs_currency": vs_currency,
            "ids": ids,
            "category": category,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": sparkline,
            "price_change_percentage": price_change_percentage,
        }
        response = self.make_request("get", "/coins/markets", params)
        return response.json()

    def coin(
        self,
        coin_id: str,
        localization: bool = True,
        tickers: bool = True,
        market_data: bool = True,
        community_data: bool = True,
        developer_data: bool = True,
        sparkline: bool = False,
    ) -> Dict:
        params = {
            "localization": localization,
            "tickers": tickers,
            "market_data": market_data,
            "community_data": community_data,
            "developer_data": developer_data,
            "sparkline": sparkline,
        }
        response = self.make_request("get", f"/coins/{coin_id}", params)
        return response.json()

    def coin_tickers(
        self,
        coin_id: str,
        exchange_ids: Optional[List[str]],
        include_exchange_logo: bool = False,
        page: int = 1,
        order: str = "trust_score_desc",
        depth: bool = False,
    ) -> Dict:
        params = {
            "exchange_ids": exchange_ids,
            "include_exchange_logo": include_exchange_logo,
            "page": page,
            "order": order,
            "depth": depth,
        }
        response = self.make_request("get", f"/coins/{coin_id}/tickers", params)
        return response.json()

    def coin_history(
        self, coin_id: str, date: dt.date, localization: bool = True
    ) -> Dict:
        params = {"date": date.strftime(DATE_FORMAT), "localization": localization}
        response = self.make_request("get", f"/coins/{coin_id}/history", params)
        return response.json()

    def coin_market_chart(
        self,
        coin_id: str,
        vs_currency: str,
        days: Union[int, str] = "max",
        interval: str = "daily",
    ) -> Dict:
        params = {"vs_currency": vs_currency, "days": days, "interval": interval}
        response = self.make_request("get", f"/coins/{coin_id}/market_chart", params)
        return response.json()

    def coin_market_chart_for_range(
        self, coin_id: str, vs_currency: str, date_from: dt.date, date_to: dt.date
    ) -> Dict:
        params = {
            "vs_currency": vs_currency,
            "from": int(time.mktime(date_from.timetuple())),
            "to": int(time.mktime(date_to.timetuple())),
        }
        response = self.make_request(
            "get", f"/coins/{coin_id}/market_chart/range", params
        )
        return response.json()

    def coin_status_updates(
        self, coin_id: str, per_page: int = 100, page: int = 1
    ) -> Dict:
        params = {"per_page": per_page, "page": page}
        response = self.make_request("get", f"/coins/{coin_id}/status_updates", params)
        return response.json()

    def coin_ohlc(
        self, coin_id: str, vs_currency: str, days: Union[int, str] = "max"
    ) -> List:
        params = {"vs_currency": vs_currency, "days": days}
        response = self.make_request("get", f"/coins/{coin_id}/ohlc", params)
        return response.json()

    def contract(self, asset_platform_id: str, contract_address: str) -> Dict:
        response = self.make_request(
            "get", f"/coins/{asset_platform_id}/contract/{contract_address}"
        )
        return response.json()

    def contract_market_chart(
        self,
        asset_platform_id: str,
        contract_address: str,
        vs_currency: str,
        days: Union[int, str] = "max",
    ) -> Dict:
        params = {"vs_currency": vs_currency, "days": days}
        response = self.make_request(
            "get",
            f"/coins/{asset_platform_id}/contract/{contract_address}/market_chart",
            params,
        )
        return response.json()

    def contract_market_chart_for_range(
        self,
        asset_platform_id: str,
        contract_address: str,
        vs_currency: str,
        date_from: dt.date,
        date_to: dt.date,
    ) -> Dict:
        params = {
            "vs_currency": vs_currency,
            "from": int(time.mktime(date_from.timetuple())),
            "to": int(time.mktime(date_to.timetuple())),
        }
        response = self.make_request(
            "get",
            f"/coins/{asset_platform_id}/contract/{contract_address}/market_chart/range",
            params,
        )
        return response.json()

    def asset_platforms(self) -> List:
        response = self.make_request("get", "/asset_platforms")
        return response.json()

    def categories_list(self) -> List:
        response = self.make_request("get", "/coins/categories/list")
        return response.json()

    def categories(self, order: str = "market_cap_desc") -> List:
        params = {"order": order}
        response = self.make_request("get", "/coins/categories/list", params)
        return response.json()

    def exchanges(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = self.make_request("get", "/exchanges", params)
        return response.json()

    def exchanges_list(self) -> List:
        response = self.make_request("get", "/exchanges/list")
        return response.json()

    def exchange(self, exchange_id: str) -> Dict:
        response = self.make_request("get", f"/exchanges/{exchange_id}")
        return response.json()

    def exchange_tickers(
        self,
        exchange_id: str,
        coin_ids: Optional[List[str]] = None,
        include_exchange_logo: bool = False,
        page: int = 1,
        depth: bool = False,
        order: str = "trust_score_desc",
    ) -> Dict:
        params = {
            "coin_ids": coin_ids,
            "include_exchange_logo": include_exchange_logo,
            "page": page,
            "depth": depth,
            "order": order,
        }
        response = self.make_request("get", f"/exchanges/{exchange_id}/tickers", params)
        return response.json()

    def exchange_status_updates(
        self, exchange_id: str, per_page: int = 100, page: int = 1
    ) -> Dict:
        params = {"per_page": per_page, "page": page}
        response = self.make_request(
            "get", f"/exchanges/{exchange_id}/status_updates", params
        )
        return response.json()

    def exchange_volume_chart(self, exchange_id: str, days: int) -> List:
        params = {"days": days}
        response = self.make_request(
            "get", f"/exchanges/{exchange_id}/volume_chart", params
        )
        return response.json()

    def finance_platforms(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = self.make_request("get", "/finance_platforms", params)
        return response.json()

    def finance_products(
        self,
        per_page: int = 100,
        page: int = 1,
        start_at: Optional[dt.date] = None,
        end_at: Optional[dt.date] = None,
    ) -> List:
        params = {
            "per_page": per_page,
            "page": page,
            "start_at": start_at.strftime(DATE_FORMAT),
            "end_at": end_at.strftime(DATE_FORMAT),
        }
        response = self.make_request("get", "/finance_products", params)
        return response.json()

    def indexes(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = self.make_request("get", "/indexes", params)
        return response.json()

    def index_by_market_id_and_index_id(self, market_id: str, index_id: str) -> Dict:
        response = self.make_request("get", f"/indexes/{market_id}/{index_id}")
        return response.json()

    def indexes_list(self) -> List:
        response = self.make_request("get", "/indexes/list")
        return response.json()

    def derivatives(self, include_tickers: str = "unexpired") -> List:
        params = {"include_tickers": include_tickers}
        response = self.make_request("get", "/derivatives", params)
        return response.json()

    def derivative_exchanges(
        self, order: Optional[str] = None, per_page: int = 100, page: int = 1
    ) -> List:
        params = {"order": order, "per_page": per_page, "page": page}
        response = self.make_request("get", "/derivatives/exchanges", params)
        return response.json()

    def derivative_exchange(
        self, exchange_id: str, include_tickers: str = "unexpired"
    ) -> Dict:
        params = {"include_tickers": include_tickers}
        response = self.make_request(
            "get", f"/derivatives/exchanges/{exchange_id}", params
        )
        return response.json()

    def derivative_exchanges_list(self) -> List:
        response = self.make_request("get", "/derivatives/exchanges/list")
        return response.json()

    def status_updates(
        self,
        category: Optional[str] = None,
        project_type: Optional[str] = None,
        per_page: int = 100,
        page: int = 1,
    ) -> Dict:
        params = {
            "category": category,
            "project_type": project_type,
            "per_page": per_page,
            "page": page,
        }
        response = self.make_request("get", "/status_updates", params)
        return response.json()

    def events(
        self,
        country_code: Optional[str] = None,
        event_type: Optional[str] = None,
        page: int = 1,
        upcoming_events_only: bool = True,
        from_date: Optional[dt.date] = None,
        to_date: Optional[dt.date] = None,
    ) -> Dict:
        params = {
            "country_code": country_code,
            "type": event_type,
            "page": page,
            "upcoming_events_only": upcoming_events_only,
            "from_date": from_date.strftime(EVENTS_DATE_FORMAT) if from_date else None,
            "to_date": to_date.strftime(EVENTS_DATE_FORMAT) if to_date else None,
        }
        response = self.make_request("get", "/events", params)
        return response.json()

    def events_countries(self) -> Dict:
        response = self.make_request("get", "/events/countries")
        return response.json()

    def events_types(self) -> Dict:
        response = self.make_request("get", "/events/types")
        return response.json()

    def exchange_rates(self) -> Dict:
        response = self.make_request("get", "/exchange_rates")
        return response.json()

    def trending_search_coins(self) -> Dict:
        response = self.make_request("get", "/search/trending")
        return response.json()

    def global_data(self) -> Dict:
        response = self.make_request("get", "/global")
        return response.json()

    def global_defi_data(self) -> Dict:
        response = self.make_request("get", "/global/decentralized_finance_defi")
        return response.json()

    def companies_data(self, coin_id: str) -> Dict:
        response = self.make_request("get", f"/companies/public_treasury/{coin_id}")
        return response.json()


class CoinGeckoAPIAsyncClient(_BaseCoinGeckoAPIClient):
    def __init__(
        self,
        base_url: str = "https://api.coingecko.com/api/v3",
        proxies: Optional[List[str]] = None,
    ) -> None:
        super(CoinGeckoAPIAsyncClient, self).__init__(
            client_type=httpx.AsyncClient, base_url=base_url, proxies=proxies
        )

    async def close(self):
        await self._client.aclose()

    async def make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> httpx.Response:
        actual_method: Callable = getattr(self._client, method)
        response: httpx.Response = await actual_method(
            url=url, params=_fix_params(params), headers=headers
        )
        response.raise_for_status()
        return response

    async def ping(self) -> Dict:
        response = await self.make_request("get", "/ping")
        return await response.json()

    async def simple_price(
        self,
        ids: List[str],
        vs_currencies: List[str],
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict:
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": include_market_cap,
            "include_24hr_vol": include_24hr_vol,
            "include_24hr_change": include_24hr_change,
            "include_last_updated_at": include_last_updated_at,
        }
        response = await self.make_request("get", "/simple/price", params)
        return await response.json()

    async def simple_token_price(
        self,
        asset_platform_id: str,
        contract_addresses: List[str],
        vs_currencies: List[str],
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict:
        params = {
            "contract_addresses": contract_addresses,
            "vs_currencies": vs_currencies,
            "include_market_cap": include_market_cap,
            "include_24hr_vol": include_24hr_vol,
            "include_24hr_change": include_24hr_change,
            "include_last_updated_at": include_last_updated_at,
        }
        response = await self.make_request(
            "get", f"/simple/token_price/{asset_platform_id}", params
        )
        return await response.json()

    async def simple_supported_vs_currencies(self) -> List[str]:
        response = await self.make_request("get", "/simple/supported_vs_currencies")
        return await response.json()

    async def coins_list(
        self, include_platform: bool = False
    ) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        response = await self.make_request(
            "get", "/coins/list", params={"include_platform": include_platform}
        )
        return await response.json()

    async def coins_markets(
        self,
        vs_currency: str,
        ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: Optional[List[str]] = None,
    ) -> List:
        params = {
            "vs_currency": vs_currency,
            "ids": ids,
            "category": category,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": sparkline,
            "price_change_percentage": price_change_percentage,
        }
        response = await self.make_request("get", "/coins/markets", params)
        return await response.json()

    async def coin(
        self,
        coin_id: str,
        localization: bool = True,
        tickers: bool = True,
        market_data: bool = True,
        community_data: bool = True,
        developer_data: bool = True,
        sparkline: bool = False,
    ) -> Dict:
        params = {
            "localization": localization,
            "tickers": tickers,
            "market_data": market_data,
            "community_data": community_data,
            "developer_data": developer_data,
            "sparkline": sparkline,
        }
        response = await self.make_request("get", f"/coins/{coin_id}", params)
        return await response.json()

    async def coin_tickers(
        self,
        coin_id: str,
        exchange_ids: Optional[List[str]],
        include_exchange_logo: bool = False,
        page: int = 1,
        order: str = "trust_score_desc",
        depth: bool = False,
    ) -> Dict:
        params = {
            "exchange_ids": exchange_ids,
            "include_exchange_logo": include_exchange_logo,
            "page": page,
            "order": order,
            "depth": depth,
        }
        response = await self.make_request("get", f"/coins/{coin_id}/tickers", params)
        return await response.json()

    async def coin_history(
        self, coin_id: str, date: dt.date, localization: bool = True
    ) -> Dict:
        params = {"date": date.strftime(DATE_FORMAT), "localization": localization}
        response = await self.make_request("get", f"/coins/{coin_id}/history", params)
        return await response.json()

    async def coin_market_chart(
        self,
        coin_id: str,
        vs_currency: str,
        days: Union[int, str] = "max",
        interval: str = "daily",
    ) -> Dict:
        params = {"vs_currency": vs_currency, "days": days, "interval": interval}
        response = await self.make_request(
            "get", f"/coins/{coin_id}/market_chart", params
        )
        return await response.json()

    async def coin_market_chart_for_range(
        self, coin_id: str, vs_currency: str, date_from: dt.date, date_to: dt.date
    ) -> Dict:
        params = {
            "vs_currency": vs_currency,
            "from": int(time.mktime(date_from.timetuple())),
            "to": int(time.mktime(date_to.timetuple())),
        }
        response = await self.make_request(
            "get", f"/coins/{coin_id}/market_chart/range", params
        )
        return await response.json()

    async def coin_status_updates(
        self, coin_id: str, per_page: int = 100, page: int = 1
    ) -> Dict:
        params = {"per_page": per_page, "page": page}
        response = await self.make_request(
            "get", f"/coins/{coin_id}/status_updates", params
        )
        return await response.json()

    async def coin_ohlc(
        self, coin_id: str, vs_currency: str, days: Union[int, str] = "max"
    ) -> List:
        params = {"vs_currency": vs_currency, "days": days}
        response = await self.make_request("get", f"/coins/{coin_id}/ohlc", params)
        return await response.json()

    async def contract(self, asset_platform_id: str, contract_address: str) -> Dict:
        response = await self.make_request(
            "get", f"/coins/{asset_platform_id}/contract/{contract_address}"
        )
        return await response.json()

    async def contract_market_chart(
        self,
        asset_platform_id: str,
        contract_address: str,
        vs_currency: str,
        days: Union[int, str] = "max",
    ) -> Dict:
        params = {"vs_currency": vs_currency, "days": days}
        response = await self.make_request(
            "get",
            f"/coins/{asset_platform_id}/contract/{contract_address}/market_chart",
            params,
        )
        return await response.json()

    async def contract_market_chart_for_range(
        self,
        asset_platform_id: str,
        contract_address: str,
        vs_currency: str,
        date_from: dt.date,
        date_to: dt.date,
    ) -> Dict:
        params = {
            "vs_currency": vs_currency,
            "from": int(time.mktime(date_from.timetuple())),
            "to": int(time.mktime(date_to.timetuple())),
        }
        response = await self.make_request(
            "get",
            f"/coins/{asset_platform_id}/contract/{contract_address}/market_chart/range",
            params,
        )
        return await response.json()

    async def asset_platforms(self) -> List:
        response = await self.make_request("get", "/asset_platforms")
        return await response.json()

    async def categories_list(self) -> List:
        response = await self.make_request("get", "/coins/categories/list")
        return await response.json()

    async def categories(self, order: str = "market_cap_desc") -> List:
        params = {"order": order}
        response = await self.make_request("get", "/coins/categories/list", params)
        return await response.json()

    async def exchanges(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = await self.make_request("get", "/exchanges", params)
        return await response.json()

    async def exchanges_list(self) -> List:
        response = await self.make_request("get", "/exchanges/list")
        return await response.json()

    async def exchange(self, exchange_id: str) -> Dict:
        response = await self.make_request("get", f"/exchanges/{exchange_id}")
        return await response.json()

    async def exchange_tickers(
        self,
        exchange_id: str,
        coin_ids: Optional[List[str]] = None,
        include_exchange_logo: bool = False,
        page: int = 1,
        depth: bool = False,
        order: str = "trust_score_desc",
    ) -> Dict:
        params = {
            "coin_ids": coin_ids,
            "include_exchange_logo": include_exchange_logo,
            "page": page,
            "depth": depth,
            "order": order,
        }
        response = await self.make_request(
            "get", f"/exchanges/{exchange_id}/tickers", params
        )
        return await response.json()

    async def exchange_status_updates(
        self, exchange_id: str, per_page: int = 100, page: int = 1
    ) -> Dict:
        params = {"per_page": per_page, "page": page}
        response = await self.make_request(
            "get", f"/exchanges/{exchange_id}/status_updates", params
        )
        return await response.json()

    async def exchange_volume_chart(self, exchange_id: str, days: int) -> List:
        params = {"days": days}
        response = await self.make_request(
            "get", f"/exchanges/{exchange_id}/volume_chart", params
        )
        return await response.json()

    async def finance_platforms(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = await self.make_request("get", "/finance_platforms", params)
        return await response.json()

    async def finance_products(
        self,
        per_page: int = 100,
        page: int = 1,
        start_at: Optional[dt.date] = None,
        end_at: Optional[dt.date] = None,
    ) -> List:
        params = {
            "per_page": per_page,
            "page": page,
            "start_at": start_at.strftime(DATE_FORMAT),
            "end_at": end_at.strftime(DATE_FORMAT),
        }
        response = await self.make_request("get", "/finance_products", params)
        return await response.json()

    async def indexes(self, per_page: int = 100, page: int = 1) -> List:
        params = {"per_page": per_page, "page": page}
        response = await self.make_request("get", "/indexes", params)
        return await response.json()

    async def index_by_market_id_and_index_id(
        self, market_id: str, index_id: str
    ) -> Dict:
        response = await self.make_request("get", f"/indexes/{market_id}/{index_id}")
        return await response.json()

    async def indexes_list(self) -> List:
        response = await self.make_request("get", "/indexes/list")
        return await response.json()

    async def derivatives(self, include_tickers: str = "unexpired") -> List:
        params = {"include_tickers": include_tickers}
        response = await self.make_request("get", "/derivatives", params)
        return await response.json()

    async def derivative_exchanges(
        self, order: Optional[str] = None, per_page: int = 100, page: int = 1
    ) -> List:
        params = {"order": order, "per_page": per_page, "page": page}
        response = await self.make_request("get", "/derivatives/exchanges", params)
        return await response.json()

    async def derivative_exchange(
        self, exchange_id: str, include_tickers: str = "unexpired"
    ) -> Dict:
        params = {"include_tickers": include_tickers}
        response = await self.make_request(
            "get", f"/derivatives/exchanges/{exchange_id}", params
        )
        return await response.json()

    async def derivative_exchanges_list(self) -> List:
        response = await self.make_request("get", "/derivatives/exchanges/list")
        return await response.json()

    async def status_updates(
        self,
        category: Optional[str] = None,
        project_type: Optional[str] = None,
        per_page: int = 100,
        page: int = 1,
    ) -> Dict:
        params = {
            "category": category,
            "project_type": project_type,
            "per_page": per_page,
            "page": page,
        }
        response = await self.make_request("get", "/status_updates", params)
        return await response.json()

    async def events(
        self,
        country_code: Optional[str] = None,
        event_type: Optional[str] = None,
        page: int = 1,
        upcoming_events_only: bool = True,
        from_date: Optional[dt.date] = None,
        to_date: Optional[dt.date] = None,
    ) -> Dict:
        params = {
            "country_code": country_code,
            "type": event_type,
            "page": page,
            "upcoming_events_only": upcoming_events_only,
            "from_date": from_date.strftime(EVENTS_DATE_FORMAT) if from_date else None,
            "to_date": to_date.strftime(EVENTS_DATE_FORMAT) if to_date else None,
        }
        response = await self.make_request("get", "/events", params)
        return await response.json()

    async def events_countries(self) -> Dict:
        response = await self.make_request("get", "/events/countries")
        return await response.json()

    async def events_types(self) -> Dict:
        response = await self.make_request("get", "/events/types")
        return await response.json()

    async def exchange_rates(self) -> Dict:
        response = await self.make_request("get", "/exchange_rates")
        return await response.json()

    async def trending_search_coins(self) -> Dict:
        response = await self.make_request("get", "/search/trending")
        return await response.json()

    async def global_data(self) -> Dict:
        response = await self.make_request("get", "/global")
        return await response.json()

    async def global_defi_data(self) -> Dict:
        response = await self.make_request("get", "/global/decentralized_finance_defi")
        return await response.json()

    async def companies_data(self, coin_id: str) -> Dict:
        response = await self.make_request(
            "get", f"/companies/public_treasury/{coin_id}"
        )
        return await response.json()
