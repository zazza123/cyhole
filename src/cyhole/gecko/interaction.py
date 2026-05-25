from typing import Any, Coroutine, Literal, overload

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..gecko.client import GeckoClient, GeckoAsyncClient
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


class Gecko(Interaction):
    """
    Class used to connect [GeckoTerminal](https://www.geckoterminal.com/dex-api) v2 API.

    GeckoTerminal exposes on-chain DEX market data across 250+ networks. The public base URL is
    [`https://api.geckoterminal.com/api/v2`](https://api.geckoterminal.com/api/v2) and works without
    an API key on a 10 calls/min free tier. Paying CoinGecko users can pass an `api_key` to route
    requests through the higher-rate `pro-api.coingecko.com/api/v3/onchain` mirror.

    Parameters:
        api_key: optional CoinGecko Pro API key. When provided, requests are sent to the
            `pro-api.coingecko.com` on-chain mirror with the `x-cg-pro-api-key` header set.
        headers: optional extra headers merged into every request.

    **Example**

    ```python
    import asyncio
    from cyhole.gecko import Gecko

    gecko = Gecko()

    # synchronous
    response = gecko.client.get_networks()
    print(f"Currently supported networks: {len(response.data)}")

    # asynchronous
    async def main() -> None:
        async with gecko.async_client as client:
            response = await client.get_search_pools("SOL/USDC")
            for pool in response.data:
                print(pool.attributes.address)

    asyncio.run(main())
    ```
    """

    def __init__(self, api_key: str | None = None, headers: Any | None = None) -> None:
        self.api_key = api_key

        # merge caller headers with auth + accept header
        request_headers: dict[str, str] = {"Accept": "application/json;version=20230302"}
        if isinstance(headers, dict):
            request_headers.update(headers)
        if self.api_key:
            request_headers["x-cg-pro-api-key"] = self.api_key

        super().__init__(request_headers)
        self.headers: dict[str, str]

        # API URL — pro mirror when an API key is supplied, public otherwise
        if self.api_key:
            self.url_api = "https://pro-api.coingecko.com/api/v3/onchain/"
        else:
            self.url_api = "https://api.geckoterminal.com/api/v2/"

        # clients
        self.client = GeckoClient(self, headers = request_headers)
        self.async_client = GeckoAsyncClient(self, headers = request_headers)

    # -----------------------------------------------------------------------
    # Networks
    # -----------------------------------------------------------------------

    @overload
    def _get_networks(self, sync: Literal[True], page: int | None = None) -> GetNetworksResponse: ...
    @overload
    def _get_networks(self, sync: Literal[False], page: int | None = None) -> Coroutine[None, None, GetNetworksResponse]: ...

    def _get_networks(self, sync: bool, page: int | None = None) -> GetNetworksResponse | Coroutine[None, None, GetNetworksResponse]:
        """
        This function refers to the **Networks** API endpoint.

        Returns the paginated list of every blockchain network supported by GeckoTerminal. Use it
        to discover the network identifier strings required by all other endpoints (e.g. `"eth"`,
        `"solana"`, `"bsc"`, `"polygon_pos"`).

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            page: 1-based page number; defaults to `1` server-side.

        Returns:
            GetNetworksResponse: paginated list of supported networks with their CoinGecko
                asset-platform mapping when available.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + "networks"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        return self.api_return_model(sync, RequestType.GET.value, url, GetNetworksResponse, params = params)

    # -----------------------------------------------------------------------
    # Dexes
    # -----------------------------------------------------------------------

    @overload
    def _get_dexes(self, sync: Literal[True], network: str, page: int | None = None) -> GetDexesResponse: ...
    @overload
    def _get_dexes(self, sync: Literal[False], network: str, page: int | None = None) -> Coroutine[None, None, GetDexesResponse]: ...

    def _get_dexes(self, sync: bool, network: str, page: int | None = None) -> GetDexesResponse | Coroutine[None, None, GetDexesResponse]:
        """
        This function refers to the **Dexes by Network** API endpoint.

        Returns the paginated list of every DEX indexed by GeckoTerminal on the requested network.
        Useful to scope pool / volume queries to a specific exchange or to surface the DEX universe
        of a given chain.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`); from [`get_networks`][cyhole.gecko.Gecko._get_networks].
            page: 1-based page number; defaults to `1` server-side.

        Returns:
            GetDexesResponse: paginated list of DEXes available on the network.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/dexes"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        return self.api_return_model(sync, RequestType.GET.value, url, GetDexesResponse, params = params)

    # -----------------------------------------------------------------------
    # Pool OHLCV
    # -----------------------------------------------------------------------

    @overload
    def _get_pool_ohlcv(self, sync: Literal[True], network: str, pool_address: str, timeframe: str, query: GetPoolOhlcvQuery | None = None) -> GetPoolOHLCVResponse: ...
    @overload
    def _get_pool_ohlcv(self, sync: Literal[False], network: str, pool_address: str, timeframe: str, query: GetPoolOhlcvQuery | None = None) -> Coroutine[None, None, GetPoolOHLCVResponse]: ...

    def _get_pool_ohlcv(self, sync: bool, network: str, pool_address: str, timeframe: str, query: GetPoolOhlcvQuery | None = None) -> GetPoolOHLCVResponse | Coroutine[None, None, GetPoolOHLCVResponse]:
        """
        This function refers to the **Pool OHLCV** API endpoint.

        Returns historical candlestick data for the requested pool at the chosen timeframe. The
        candles are returned newest-first up to the configured `limit` and can be denominated in
        USD or quoted in either side of the pool. Useful for charting and for backtesting price
        action against a specific DEX pair.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            pool_address: contract address of the pool.
            timeframe: candle granularity; one of the values declared by
                [`GeckoTimeframe`][cyhole.gecko.param.GeckoTimeframe] (`"day"`, `"hour"`, `"minute"`, `"second"`).
            query: optional [`GetPoolOhlcvQuery`][cyhole.gecko.schema.GetPoolOhlcvQuery] bundling
                the `aggregate`, `before_timestamp`, `limit`, `currency`, `token` and
                `include_empty_intervals` query parameters.

        Returns:
            GetPoolOHLCVResponse: OHLCV series plus a `meta` block identifying the pool's base and
                quote tokens.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/pools/{pool_address}/ohlcv/{timeframe}"
        params = query.model_dump(exclude_none = True) if query is not None else {}
        return self.api_return_model(sync, RequestType.GET.value, url, GetPoolOHLCVResponse, params = params)

    # -----------------------------------------------------------------------
    # Pool Tokens Info
    # -----------------------------------------------------------------------

    @overload
    def _get_pool_token_info(self, sync: Literal[True], network: str, pool_address: str) -> GetPoolTokenInfoResponse: ...
    @overload
    def _get_pool_token_info(self, sync: Literal[False], network: str, pool_address: str) -> Coroutine[None, None, GetPoolTokenInfoResponse]: ...

    def _get_pool_token_info(self, sync: bool, network: str, pool_address: str) -> GetPoolTokenInfoResponse | Coroutine[None, None, GetPoolTokenInfoResponse]:
        """
        This function refers to the **Pool Tokens Info** API endpoint.

        Returns the full metadata block of every token that participates in the requested pool
        (typically two entries — base and quote). The payload includes image set, GeckoTerminal
        trust score breakdown, holder distribution and social links, so callers can enrich a pool
        view without making a separate request per token.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            pool_address: contract address of the pool.

        Returns:
            GetPoolTokenInfoResponse: list of token-info entries, one per pool side.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/pools/{pool_address}/info"
        return self.api_return_model(sync, RequestType.GET.value, url, GetPoolTokenInfoResponse)

    # -----------------------------------------------------------------------
    # Pool Trades
    # -----------------------------------------------------------------------

    @overload
    def _get_pool_trades(self, sync: Literal[True], network: str, pool_address: str, trade_volume_in_usd_greater_than: float | None = None, token: str | None = None) -> GetPoolTradesResponse: ...
    @overload
    def _get_pool_trades(self, sync: Literal[False], network: str, pool_address: str, trade_volume_in_usd_greater_than: float | None = None, token: str | None = None) -> Coroutine[None, None, GetPoolTradesResponse]: ...

    def _get_pool_trades(self, sync: bool, network: str, pool_address: str, trade_volume_in_usd_greater_than: float | None = None, token: str | None = None) -> GetPoolTradesResponse | Coroutine[None, None, GetPoolTradesResponse]:
        """
        This function refers to the **Pool Trades** API endpoint.

        Returns the trade history of the requested pool over the trailing 24 hours, optionally
        filtered by a minimum USD volume threshold. Each trade reports block / transaction info,
        amounts on both sides, prices in the chosen currency token, and a `kind` flag distinguishing
        buys from sells.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            pool_address: contract address of the pool.
            trade_volume_in_usd_greater_than: minimum USD volume per trade; defaults to `0` server-side.
            token: which side of the pool to express prices on. `"base"`, `"quote"` (see
                [`GeckoTokenSide`][cyhole.gecko.param.GeckoTokenSide]) or a token contract address.
                Defaults to `"base"` server-side.

        Returns:
            GetPoolTradesResponse: list of trades, newest-first.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/pools/{pool_address}/trades"
        params: dict[str, Any] = {}
        if trade_volume_in_usd_greater_than is not None:
            params["trade_volume_in_usd_greater_than"] = trade_volume_in_usd_greater_than
        if token is not None:
            params["token"] = token
        return self.api_return_model(sync, RequestType.GET.value, url, GetPoolTradesResponse, params = params)

    # -----------------------------------------------------------------------
    # Token Data (single + multiple, consolidated)
    # -----------------------------------------------------------------------

    @overload
    def _get_token_data(self, sync: Literal[True], network: str, address: str, include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataResponse: ...
    @overload
    def _get_token_data(self, sync: Literal[True], network: str, address: list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> GetTokenDataMultipleResponse: ...
    @overload
    def _get_token_data(self, sync: Literal[False], network: str, address: str, include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> Coroutine[None, None, GetTokenDataResponse]: ...
    @overload
    def _get_token_data(self, sync: Literal[False], network: str, address: list[str], include: str | None = None, include_composition: bool | None = None, include_inactive_source: bool | None = None) -> Coroutine[None, None, GetTokenDataMultipleResponse]: ...

    def _get_token_data(
        self,
        sync: bool,
        network: str,
        address: str | list[str],
        include: str | None = None,
        include_composition: bool | None = None,
        include_inactive_source: bool | None = None,
    ) -> GetTokenDataResponse | GetTokenDataMultipleResponse | Coroutine[None, None, GetTokenDataResponse] | Coroutine[None, None, GetTokenDataMultipleResponse]:
        """
        This function refers to the **Token Data** API endpoint.

        Returns current price, supply, liquidity and volume metrics for one or more tokens on a
        given network. When a single `address` string is provided, the single-token endpoint is
        used and the response is a [`GetTokenDataResponse`][cyhole.gecko.schema.GetTokenDataResponse];
        when a `list[str]` of addresses is provided, the multi-token endpoint is used and the
        response is a [`GetTokenDataMultipleResponse`][cyhole.gecko.schema.GetTokenDataMultipleResponse]
        whose entries also carry a `launchpad_details` block. Pass `include="top_pools"` to embed
        each token's most relevant pools inside the `included` array.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            address: token contract address, or list of addresses (up to ~50 for the multi endpoint).
            include: when set to `"top_pools"` (see
                [`GeckoTokenDataInclude`][cyhole.gecko.param.GeckoTokenDataInclude]) the response
                expands each token's top pools in the JSON:API `included` array.
            include_composition: only effective with `include="top_pools"`; when `True`, asks the
                server to compute the per-pool composition fields.
            include_inactive_source: when `True`, include data from sources GeckoTerminal has
                flagged as inactive; defaults to `False`.

        Returns:
            GetTokenDataResponse: when `address` is a single string.
            GetTokenDataMultipleResponse: when `address` is a list of strings.

        Raises:
            GeckoException: if the API returns an error.
        """
        if isinstance(address, str):
            url = self.url_api + f"networks/{network}/tokens/{address}"
            response_model: Any = GetTokenDataResponse
        else:
            addresses = ",".join(address)
            url = self.url_api + f"networks/{network}/tokens/multi/{addresses}"
            response_model = GetTokenDataMultipleResponse

        params: dict[str, Any] = {}
        if include is not None:
            params["include"] = include
        if include_composition is not None:
            params["include_composition"] = include_composition
        if include_inactive_source is not None:
            params["include_inactive_source"] = include_inactive_source
        return self.api_return_model(sync, RequestType.GET.value, url, response_model, params = params)

    # -----------------------------------------------------------------------
    # Token Info
    # -----------------------------------------------------------------------

    @overload
    def _get_token_info(self, sync: Literal[True], network: str, address: str) -> GetTokenInfoResponse: ...
    @overload
    def _get_token_info(self, sync: Literal[False], network: str, address: str) -> Coroutine[None, None, GetTokenInfoResponse]: ...

    def _get_token_info(self, sync: bool, network: str, address: str) -> GetTokenInfoResponse | Coroutine[None, None, GetTokenInfoResponse]:
        """
        This function refers to the **Token Info** API endpoint.

        Returns the complete metadata block of a single token on a given network: image set,
        GeckoTerminal trust score (with per-dimension breakdown), holders distribution, social
        links, free-text description, mint/freeze authorities, and the honeypot flag.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            address: token contract address.

        Returns:
            GetTokenInfoResponse: token metadata block.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{address}/info"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenInfoResponse)

    # -----------------------------------------------------------------------
    # Recently Updated Tokens
    # -----------------------------------------------------------------------

    @overload
    def _get_recently_updated_tokens(self, sync: Literal[True], network: str | None = None, include: str | None = None) -> GetRecentlyUpdatedTokensResponse: ...
    @overload
    def _get_recently_updated_tokens(self, sync: Literal[False], network: str | None = None, include: str | None = None) -> Coroutine[None, None, GetRecentlyUpdatedTokensResponse]: ...

    def _get_recently_updated_tokens(self, sync: bool, network: str | None = None, include: str | None = None) -> GetRecentlyUpdatedTokensResponse | Coroutine[None, None, GetRecentlyUpdatedTokensResponse]:
        """
        This function refers to the **Recently Updated Tokens** API endpoint.

        Returns tokens whose metadata (description, social links, GeckoTerminal score, ...) was
        updated most recently. Useful to surface newly enriched projects across a network.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier; defaults to `"eth"` server-side. Pass any valid network id
                from [`get_networks`][cyhole.gecko.Gecko._get_networks].
            include: when set to `"network"` (see
                [`GeckoRecentlyUpdatedInclude`][cyhole.gecko.param.GeckoRecentlyUpdatedInclude])
                the response embeds the network resource for each entry.

        Returns:
            GetRecentlyUpdatedTokensResponse: list of recently updated tokens.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + "tokens/info_recently_updated"
        params: dict[str, Any] = {}
        if network is not None:
            params["network"] = network
        if include is not None:
            params["include"] = include
        return self.api_return_model(sync, RequestType.GET.value, url, GetRecentlyUpdatedTokensResponse, params = params)

    # -----------------------------------------------------------------------
    # Token OHLCV
    # -----------------------------------------------------------------------

    @overload
    def _get_token_ohlcv(self, sync: Literal[True], network: str, token_address: str, timeframe: str, query: GetTokenOhlcvQuery | None = None) -> GetTokenOHLCVResponse: ...
    @overload
    def _get_token_ohlcv(self, sync: Literal[False], network: str, token_address: str, timeframe: str, query: GetTokenOhlcvQuery | None = None) -> Coroutine[None, None, GetTokenOHLCVResponse]: ...

    def _get_token_ohlcv(self, sync: bool, network: str, token_address: str, timeframe: str, query: GetTokenOhlcvQuery | None = None) -> GetTokenOHLCVResponse | Coroutine[None, None, GetTokenOHLCVResponse]:
        """
        This function refers to the **Token OHLCV** API endpoint.

        Returns aggregated candlestick data for the requested token at the chosen timeframe. The
        server automatically selects the most relevant pool on the network and returns the same
        candle structure as [`get_pool_ohlcv`][cyhole.gecko.Gecko._get_pool_ohlcv]. Useful when the
        caller wants a per-token chart without first resolving the underlying pool.

        !!! warning "Pro plan required"
            This endpoint is **not** exposed on the public `api.geckoterminal.com` tier and returns
            `401 Unauthorized` without a CoinGecko Pro API key. Construct the `Gecko` interaction
            with `api_key = "..."` so requests are routed through the `pro-api.coingecko.com`
            on-chain mirror.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            token_address: token contract address.
            timeframe: candle granularity; one of the values declared by
                [`GeckoTimeframe`][cyhole.gecko.param.GeckoTimeframe].
            query: optional [`GetTokenOhlcvQuery`][cyhole.gecko.schema.GetTokenOhlcvQuery] bundling
                the `aggregate`, `before_timestamp`, `limit`, `currency`, `include_empty_intervals`
                and `include_inactive_source` query parameters.

        Returns:
            GetTokenOHLCVResponse: OHLCV series plus a `meta` block identifying base and quote tokens
                of the pool selected by GeckoTerminal.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{token_address}/ohlcv/{timeframe}"
        params = query.model_dump(exclude_none = True) if query is not None else {}
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenOHLCVResponse, params = params)

    # -----------------------------------------------------------------------
    # Token Trades
    # -----------------------------------------------------------------------

    @overload
    def _get_token_trades(self, sync: Literal[True], network: str, token_address: str, trade_volume_in_usd_greater_than: float | None = None) -> GetTokenTradesResponse: ...
    @overload
    def _get_token_trades(self, sync: Literal[False], network: str, token_address: str, trade_volume_in_usd_greater_than: float | None = None) -> Coroutine[None, None, GetTokenTradesResponse]: ...

    def _get_token_trades(self, sync: bool, network: str, token_address: str, trade_volume_in_usd_greater_than: float | None = None) -> GetTokenTradesResponse | Coroutine[None, None, GetTokenTradesResponse]:
        """
        This function refers to the **Token Trades** API endpoint.

        Returns the trade history involving the requested token across every indexed pool over the
        trailing 24 hours, optionally filtered by a minimum USD volume threshold. Each trade also
        reports the pool that executed it (`pool_address`, `pool_dex`).

        !!! warning "Pro plan required"
            This endpoint is **not** exposed on the public `api.geckoterminal.com` tier and returns
            `401 Unauthorized` without a CoinGecko Pro API key. Construct the `Gecko` interaction
            with `api_key = "..."` so requests are routed through the `pro-api.coingecko.com`
            on-chain mirror.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            token_address: token contract address.
            trade_volume_in_usd_greater_than: minimum USD volume per trade; defaults to `0` server-side.

        Returns:
            GetTokenTradesResponse: list of trades, newest-first.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{token_address}/trades"
        params: dict[str, Any] = {}
        if trade_volume_in_usd_greater_than is not None:
            params["trade_volume_in_usd_greater_than"] = trade_volume_in_usd_greater_than
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenTradesResponse, params = params)

    # -----------------------------------------------------------------------
    # Token Holders Chart
    # -----------------------------------------------------------------------

    @overload
    def _get_token_holders_chart(self, sync: Literal[True], network: str, token_address: str, days: str | None = None) -> GetTokenHoldersChartResponse: ...
    @overload
    def _get_token_holders_chart(self, sync: Literal[False], network: str, token_address: str, days: str | None = None) -> Coroutine[None, None, GetTokenHoldersChartResponse]: ...

    def _get_token_holders_chart(self, sync: bool, network: str, token_address: str, days: str | None = None) -> GetTokenHoldersChartResponse | Coroutine[None, None, GetTokenHoldersChartResponse]:
        """
        This function refers to the **Token Holders Chart** API endpoint.

        Returns the historical holders count for the requested token across the chosen window
        (`"7"`, `"30"`, or `"max"` days). Useful to track adoption or sell-off pressure over time.

        !!! warning "Pro plan required"
            This endpoint is **not** exposed on the public `api.geckoterminal.com` tier and returns
            `401 Unauthorized` without a CoinGecko Pro API key. Construct the `Gecko` interaction
            with `api_key = "..."` so requests are routed through the `pro-api.coingecko.com`
            on-chain mirror.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            token_address: token contract address.
            days: time window; one of the values declared by
                [`GeckoHoldersChartDays`][cyhole.gecko.param.GeckoHoldersChartDays]. Defaults to
                `"7"` server-side.

        Returns:
            GetTokenHoldersChartResponse: list of `[timestamp_iso, holders_count]` pairs plus a
                `meta` block identifying the token.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{token_address}/holders_chart"
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenHoldersChartResponse, params = params)

    # -----------------------------------------------------------------------
    # Top Token Holders
    # -----------------------------------------------------------------------

    @overload
    def _get_top_token_holders(self, sync: Literal[True], network: str, address: str, holders: str | None = None, include_pnl_details: bool | None = None) -> GetTopTokenHoldersResponse: ...
    @overload
    def _get_top_token_holders(self, sync: Literal[False], network: str, address: str, holders: str | None = None, include_pnl_details: bool | None = None) -> Coroutine[None, None, GetTopTokenHoldersResponse]: ...

    def _get_top_token_holders(self, sync: bool, network: str, address: str, holders: str | None = None, include_pnl_details: bool | None = None) -> GetTopTokenHoldersResponse | Coroutine[None, None, GetTopTokenHoldersResponse]:
        """
        This function refers to the **Top Token Holders** API endpoint.

        Returns the top wallets holding the requested token, ordered by balance. When
        `include_pnl_details=True` each entry also carries realised/unrealised PnL fields, average
        buy price, and the number of buy/sell trades. Useful for whale-tracking dashboards.

        !!! warning "Pro plan required"
            This endpoint is **not** exposed on the public `api.geckoterminal.com` tier and returns
            `401 Unauthorized` without a CoinGecko Pro API key. Construct the `Gecko` interaction
            with `api_key = "..."` so requests are routed through the `pro-api.coingecko.com`
            on-chain mirror.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            address: token contract address.
            holders: number of top holders to return as a decimal string, or `"max"` for the API
                cap. Defaults to `"10"` server-side.
            include_pnl_details: when `True`, every entry carries realised/unrealised PnL fields.
                Defaults to `False`.

        Returns:
            GetTopTokenHoldersResponse: ordered list of top holders with snapshot timestamp.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{address}/top_holders"
        params: dict[str, Any] = {}
        if holders is not None:
            params["holders"] = holders
        if include_pnl_details is not None:
            params["include_pnl_details"] = include_pnl_details
        return self.api_return_model(sync, RequestType.GET.value, url, GetTopTokenHoldersResponse, params = params)

    # -----------------------------------------------------------------------
    # Top Token Traders
    # -----------------------------------------------------------------------

    @overload
    def _get_top_token_traders(self, sync: Literal[True], network: str, token_address: str, traders: str | None = None, sort: str | None = None, include_address_label: bool | None = None) -> GetTopTokenTradersResponse: ...
    @overload
    def _get_top_token_traders(self, sync: Literal[False], network: str, token_address: str, traders: str | None = None, sort: str | None = None, include_address_label: bool | None = None) -> Coroutine[None, None, GetTopTokenTradersResponse]: ...

    def _get_top_token_traders(self, sync: bool, network: str, token_address: str, traders: str | None = None, sort: str | None = None, include_address_label: bool | None = None) -> GetTopTokenTradersResponse | Coroutine[None, None, GetTopTokenTradersResponse]:
        """
        This function refers to the **Top Token Traders** API endpoint.

        Returns the highest-performing wallets on the requested token, ranked by the chosen `sort`
        criterion (default: realised PnL in USD). Each entry includes buy/sell counts, amounts and
        USD totals — useful for smart-money / copy-trading strategies.

        !!! warning "Pro plan required"
            This endpoint is **not** exposed on the public `api.geckoterminal.com` tier and returns
            `401 Unauthorized` without a CoinGecko Pro API key. Construct the `Gecko` interaction
            with `api_key = "..."` so requests are routed through the `pro-api.coingecko.com`
            on-chain mirror.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            token_address: token contract address.
            traders: number of top traders to return as a decimal string, or `"max"`. Defaults to
                `"10"` server-side.
            sort: sorting criterion; one of the values declared by
                [`GeckoTopTradersSort`][cyhole.gecko.param.GeckoTopTradersSort]. Defaults to
                `"realized_pnl_usd_desc"` server-side.
            include_address_label: when `True`, populate the `label` field with descriptive tags
                where available. Defaults to `False`.

        Returns:
            GetTopTokenTradersResponse: ordered list of top traders.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + f"networks/{network}/tokens/{token_address}/top_traders"
        params: dict[str, Any] = {}
        if traders is not None:
            params["traders"] = traders
        if sort is not None:
            params["sort"] = sort
        if include_address_label is not None:
            params["include_address_label"] = include_address_label
        return self.api_return_model(sync, RequestType.GET.value, url, GetTopTokenTradersResponse, params = params)

    # -----------------------------------------------------------------------
    # Simple Token Price
    # -----------------------------------------------------------------------

    @overload
    def _get_simple_token_price(self, sync: Literal[True], network: str, address: str | list[str], query: GetSimpleTokenPriceQuery | None = None) -> GetSimpleTokenPriceResponse: ...
    @overload
    def _get_simple_token_price(self, sync: Literal[False], network: str, address: str | list[str], query: GetSimpleTokenPriceQuery | None = None) -> Coroutine[None, None, GetSimpleTokenPriceResponse]: ...

    def _get_simple_token_price(self, sync: bool, network: str, address: str | list[str], query: GetSimpleTokenPriceQuery | None = None) -> GetSimpleTokenPriceResponse | Coroutine[None, None, GetSimpleTokenPriceResponse]:
        """
        This function refers to the **Onchain Simple Token Price** API endpoint.

        Returns current USD prices for up to 100 tokens on a single network in one request, plus
        optional market-cap / 24h-volume / 24h-price-change / total-reserve metrics when the
        corresponding `include_*` flag is enabled in `query`. Designed for lightweight quote
        lookups when the full Token Data payload is not needed.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            network: network identifier (e.g. `"eth"`, `"solana"`).
            address: token contract address or list of addresses (up to 100). Lists are joined with
                commas before being sent.
            query: optional [`GetSimpleTokenPriceQuery`][cyhole.gecko.schema.GetSimpleTokenPriceQuery]
                bundling the six `include_*` flags.

        Returns:
            GetSimpleTokenPriceResponse: per-address maps of price plus any optional metrics.

        Raises:
            GeckoException: if the API returns an error.
        """
        addresses = address if isinstance(address, str) else ",".join(address)
        url = self.url_api + f"simple/networks/{network}/token_price/{addresses}"
        params = query.model_dump(exclude_none = True) if query is not None else {}
        return self.api_return_model(sync, RequestType.GET.value, url, GetSimpleTokenPriceResponse, params = params)

    # -----------------------------------------------------------------------
    # Search Pools
    # -----------------------------------------------------------------------

    @overload
    def _get_search_pools(self, sync: Literal[True], query: str, network: str | None = None, include: str | None = None, page: int | None = None) -> GetSearchPoolsResponse: ...
    @overload
    def _get_search_pools(self, sync: Literal[False], query: str, network: str | None = None, include: str | None = None, page: int | None = None) -> Coroutine[None, None, GetSearchPoolsResponse]: ...

    def _get_search_pools(self, sync: bool, query: str, network: str | None = None, include: str | None = None, page: int | None = None) -> GetSearchPoolsResponse | Coroutine[None, None, GetSearchPoolsResponse]:
        """
        This function refers to the **Search Pools** API endpoint.

        Returns the pools matching the requested query (pool address, token name, token symbol or
        token contract address), optionally restricted to one network. When `include` is provided,
        the linked `base_token`, `quote_token` and / or `dex` resources are expanded inline inside
        the JSON:API `included` array.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            query: free-text search query.
            network: optional network identifier to constrain the search.
            include: comma-separated list of relationships to expand; values from
                [`GeckoSearchInclude`][cyhole.gecko.param.GeckoSearchInclude] (`"base_token"`,
                `"quote_token"`, `"dex"`).
            page: 1-based page number; defaults to `1` server-side.

        Returns:
            GetSearchPoolsResponse: matching pools with optional embedded token / DEX resources.

        Raises:
            GeckoException: if the API returns an error.
        """
        url = self.url_api + "search/pools"
        params: dict[str, Any] = {"query": query}
        if network is not None:
            params["network"] = network
        if include is not None:
            params["include"] = include
        if page is not None:
            params["page"] = page
        return self.api_return_model(sync, RequestType.GET.value, url, GetSearchPoolsResponse, params = params)
