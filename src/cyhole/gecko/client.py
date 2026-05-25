from __future__ import annotations
from typing import TYPE_CHECKING, Any, overload

from ..core.client import APIClient, AsyncAPIClient
from ..gecko.schema import (
    GetNetworksResponse,
    GetDexesResponse,
    GetPoolOhlcvQuery,
    GetPoolOHLCVResponse,
    GetTokenOhlcvQuery,
    GetTokenOHLCVResponse,
    GetPoolTokenInfoResponse,
    GetPoolTradesResponse,
    GetTokenTradesResponse,
    GetTokenDataResponse,
    GetTokenDataMultipleResponse,
    GetTokenInfoResponse,
    GetRecentlyUpdatedTokensResponse,
    GetTokenHoldersChartResponse,
    GetTopTokenHoldersResponse,
    GetTopTokenTradersResponse,
    GetSimpleTokenPriceQuery,
    GetSimpleTokenPriceResponse,
    GetSearchPoolsResponse,
)

if TYPE_CHECKING:
    from ..gecko.interaction import Gecko


class GeckoClient(APIClient):
    """Client for synchronous API calls for `Gecko` interaction."""

    def __init__(self, interaction: Gecko, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Gecko = self._interaction

    def get_networks(self, page: int | None = None) -> GetNetworksResponse:
        """
        Call the Gecko's GET **[Networks](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_networks`][cyhole.gecko.interaction.Gecko._get_networks].
        """
        return self._interaction._get_networks(True, page)

    def get_dexes(self, network: str, page: int | None = None) -> GetDexesResponse:
        """
        Call the Gecko's GET **[Dexes by Network](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_dexes`][cyhole.gecko.interaction.Gecko._get_dexes].
        """
        return self._interaction._get_dexes(True, network, page)

    def get_pool_ohlcv(self, network: str, pool_address: str, timeframe: str, query: GetPoolOhlcvQuery | None = None) -> GetPoolOHLCVResponse:
        """
        Call the Gecko's GET **[Pool OHLCV](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_ohlcv`][cyhole.gecko.interaction.Gecko._get_pool_ohlcv].
        """
        return self._interaction._get_pool_ohlcv(True, network, pool_address, timeframe, query)

    def get_pool_token_info(self, network: str, pool_address: str) -> GetPoolTokenInfoResponse:
        """
        Call the Gecko's GET **[Pool Tokens Info](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_token_info`][cyhole.gecko.interaction.Gecko._get_pool_token_info].
        """
        return self._interaction._get_pool_token_info(True, network, pool_address)

    def get_pool_trades(self, network: str, pool_address: str, trade_volume_in_usd_greater_than: float | None = None, token: str | None = None) -> GetPoolTradesResponse:
        """
        Call the Gecko's GET **[Pool Trades](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_trades`][cyhole.gecko.interaction.Gecko._get_pool_trades].
        """
        return self._interaction._get_pool_trades(True, network, pool_address, trade_volume_in_usd_greater_than, token)

    @overload
    def get_token_data(self, network: str, address: str, include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataResponse: ...
    @overload
    def get_token_data(self, network: str, address: list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataMultipleResponse: ...

    def get_token_data(self, network: str, address: str | list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataResponse | GetTokenDataMultipleResponse:
        """
        Call the Gecko's GET **[Token Data](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_data`][cyhole.gecko.interaction.Gecko._get_token_data].
        """
        return self._interaction._get_token_data(True, network, address, include, include_composition, include_inactive_source)  # type: ignore[call-overload]

    def get_token_info(self, network: str, address: str) -> GetTokenInfoResponse:
        """
        Call the Gecko's GET **[Token Info](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_info`][cyhole.gecko.interaction.Gecko._get_token_info].
        """
        return self._interaction._get_token_info(True, network, address)

    def get_recently_updated_tokens(self, network: str | None = None, include: str | None = None) -> GetRecentlyUpdatedTokensResponse:
        """
        Call the Gecko's GET **[Recently Updated Tokens](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_recently_updated_tokens`][cyhole.gecko.interaction.Gecko._get_recently_updated_tokens].
        """
        return self._interaction._get_recently_updated_tokens(True, network, include)

    def get_token_ohlcv(self, network: str, token_address: str, timeframe: str, query: GetTokenOhlcvQuery | None = None) -> GetTokenOHLCVResponse:
        """
        Call the Gecko's GET **[Token OHLCV](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_ohlcv`][cyhole.gecko.interaction.Gecko._get_token_ohlcv].
        """
        return self._interaction._get_token_ohlcv(True, network, token_address, timeframe, query)

    def get_token_trades(self, network: str, token_address: str, trade_volume_in_usd_greater_than: float | None = None) -> GetTokenTradesResponse:
        """
        Call the Gecko's GET **[Token Trades](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_trades`][cyhole.gecko.interaction.Gecko._get_token_trades].
        """
        return self._interaction._get_token_trades(True, network, token_address, trade_volume_in_usd_greater_than)

    def get_token_holders_chart(self, network: str, token_address: str, days: str | None = None) -> GetTokenHoldersChartResponse:
        """
        Call the Gecko's GET **[Token Holders Chart](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_holders_chart`][cyhole.gecko.interaction.Gecko._get_token_holders_chart].
        """
        return self._interaction._get_token_holders_chart(True, network, token_address, days)

    def get_top_token_holders(self, network: str, address: str, holders: str | None = None, include_pnl_details: bool | None = None) -> GetTopTokenHoldersResponse:
        """
        Call the Gecko's GET **[Top Token Holders](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_top_token_holders`][cyhole.gecko.interaction.Gecko._get_top_token_holders].
        """
        return self._interaction._get_top_token_holders(True, network, address, holders, include_pnl_details)

    def get_top_token_traders(self, network: str, token_address: str, traders: str | None = None, sort: str | None = None, include_address_label: bool | None = None) -> GetTopTokenTradersResponse:
        """
        Call the Gecko's GET **[Top Token Traders](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_top_token_traders`][cyhole.gecko.interaction.Gecko._get_top_token_traders].
        """
        return self._interaction._get_top_token_traders(True, network, token_address, traders, sort, include_address_label)

    def get_simple_token_price(self, network: str, address: str | list[str], query: GetSimpleTokenPriceQuery | None = None) -> GetSimpleTokenPriceResponse:
        """
        Call the Gecko's GET **[Simple Token Price](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_simple_token_price`][cyhole.gecko.interaction.Gecko._get_simple_token_price].
        """
        return self._interaction._get_simple_token_price(True, network, address, query)

    def get_search_pools(self, query: str, network: str | None = None, include: str | None = None, page: int | None = None) -> GetSearchPoolsResponse:
        """
        Call the Gecko's GET **[Search Pools](https://www.geckoterminal.com/dex-api)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Gecko._get_search_pools`][cyhole.gecko.interaction.Gecko._get_search_pools].
        """
        return self._interaction._get_search_pools(True, query, network, include, page)


class GeckoAsyncClient(AsyncAPIClient):
    """Client for asynchronous API calls for `Gecko` interaction."""

    def __init__(self, interaction: Gecko, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Gecko = self._interaction

    async def get_networks(self, page: int | None = None) -> GetNetworksResponse:
        """
        Call the Gecko's GET **[Networks](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_networks`][cyhole.gecko.interaction.Gecko._get_networks].
        """
        return await self._interaction._get_networks(False, page)

    async def get_dexes(self, network: str, page: int | None = None) -> GetDexesResponse:
        """
        Call the Gecko's GET **[Dexes by Network](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_dexes`][cyhole.gecko.interaction.Gecko._get_dexes].
        """
        return await self._interaction._get_dexes(False, network, page)

    async def get_pool_ohlcv(self, network: str, pool_address: str, timeframe: str, query: GetPoolOhlcvQuery | None = None) -> GetPoolOHLCVResponse:
        """
        Call the Gecko's GET **[Pool OHLCV](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_ohlcv`][cyhole.gecko.interaction.Gecko._get_pool_ohlcv].
        """
        return await self._interaction._get_pool_ohlcv(False, network, pool_address, timeframe, query)

    async def get_pool_token_info(self, network: str, pool_address: str) -> GetPoolTokenInfoResponse:
        """
        Call the Gecko's GET **[Pool Tokens Info](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_token_info`][cyhole.gecko.interaction.Gecko._get_pool_token_info].
        """
        return await self._interaction._get_pool_token_info(False, network, pool_address)

    async def get_pool_trades(self, network: str, pool_address: str, trade_volume_in_usd_greater_than: float | None = None, token: str | None = None) -> GetPoolTradesResponse:
        """
        Call the Gecko's GET **[Pool Trades](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_pool_trades`][cyhole.gecko.interaction.Gecko._get_pool_trades].
        """
        return await self._interaction._get_pool_trades(False, network, pool_address, trade_volume_in_usd_greater_than, token)

    @overload
    async def get_token_data(self, network: str, address: str, include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataResponse: ...
    @overload
    async def get_token_data(self, network: str, address: list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataMultipleResponse: ...

    async def get_token_data(self, network: str, address: str | list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataResponse | GetTokenDataMultipleResponse:
        """
        Call the Gecko's GET **[Token Data](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_data`][cyhole.gecko.interaction.Gecko._get_token_data].
        """
        return await self._interaction._get_token_data(False, network, address, include, include_composition, include_inactive_source)  # type: ignore[call-overload]

    async def get_token_info(self, network: str, address: str) -> GetTokenInfoResponse:
        """
        Call the Gecko's GET **[Token Info](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_info`][cyhole.gecko.interaction.Gecko._get_token_info].
        """
        return await self._interaction._get_token_info(False, network, address)

    async def get_recently_updated_tokens(self, network: str | None = None, include: str | None = None) -> GetRecentlyUpdatedTokensResponse:
        """
        Call the Gecko's GET **[Recently Updated Tokens](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_recently_updated_tokens`][cyhole.gecko.interaction.Gecko._get_recently_updated_tokens].
        """
        return await self._interaction._get_recently_updated_tokens(False, network, include)

    async def get_token_ohlcv(self, network: str, token_address: str, timeframe: str, query: GetTokenOhlcvQuery | None = None) -> GetTokenOHLCVResponse:
        """
        Call the Gecko's GET **[Token OHLCV](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_ohlcv`][cyhole.gecko.interaction.Gecko._get_token_ohlcv].
        """
        return await self._interaction._get_token_ohlcv(False, network, token_address, timeframe, query)

    async def get_token_trades(self, network: str, token_address: str, trade_volume_in_usd_greater_than: float | None = None) -> GetTokenTradesResponse:
        """
        Call the Gecko's GET **[Token Trades](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_trades`][cyhole.gecko.interaction.Gecko._get_token_trades].
        """
        return await self._interaction._get_token_trades(False, network, token_address, trade_volume_in_usd_greater_than)

    async def get_token_holders_chart(self, network: str, token_address: str, days: str | None = None) -> GetTokenHoldersChartResponse:
        """
        Call the Gecko's GET **[Token Holders Chart](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_token_holders_chart`][cyhole.gecko.interaction.Gecko._get_token_holders_chart].
        """
        return await self._interaction._get_token_holders_chart(False, network, token_address, days)

    async def get_top_token_holders(self, network: str, address: str, holders: str | None = None, include_pnl_details: bool | None = None) -> GetTopTokenHoldersResponse:
        """
        Call the Gecko's GET **[Top Token Holders](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_top_token_holders`][cyhole.gecko.interaction.Gecko._get_top_token_holders].
        """
        return await self._interaction._get_top_token_holders(False, network, address, holders, include_pnl_details)

    async def get_top_token_traders(self, network: str, token_address: str, traders: str | None = None, sort: str | None = None, include_address_label: bool | None = None) -> GetTopTokenTradersResponse:
        """
        Call the Gecko's GET **[Top Token Traders](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_top_token_traders`][cyhole.gecko.interaction.Gecko._get_top_token_traders].
        """
        return await self._interaction._get_top_token_traders(False, network, token_address, traders, sort, include_address_label)

    async def get_simple_token_price(self, network: str, address: str | list[str], query: GetSimpleTokenPriceQuery | None = None) -> GetSimpleTokenPriceResponse:
        """
        Call the Gecko's GET **[Simple Token Price](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_simple_token_price`][cyhole.gecko.interaction.Gecko._get_simple_token_price].
        """
        return await self._interaction._get_simple_token_price(False, network, address, query)

    async def get_search_pools(self, query: str, network: str | None = None, include: str | None = None, page: int | None = None) -> GetSearchPoolsResponse:
        """
        Call the Gecko's GET **[Search Pools](https://www.geckoterminal.com/dex-api)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Gecko._get_search_pools`][cyhole.gecko.interaction.Gecko._get_search_pools].
        """
        return await self._interaction._get_search_pools(False, query, network, include, page)
