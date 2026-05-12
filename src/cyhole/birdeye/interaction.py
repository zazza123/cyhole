import os
from typing import Any, Coroutine, Literal, overload
from datetime import datetime

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..core.exception import MissingAPIKeyError
from ..birdeye.client import BirdeyeClient, BirdeyeAsyncClient
from ..birdeye.exception import BirdeyeTimeRangeError
from ..birdeye.param import (
    BirdeyeChain,
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTimeFrame,
    BirdeyeHourTimeFrame,
    BirdeyeTradeType,
    BirdeyeAddressType,
    BirdeyeUIAmountMode,
    BirdeyeV3TokenListSortBy,
    BirdeyeV2MarketsSortBy,
    BirdeyeMintBurnType,
    BirdeyeV2TopTradersSortBy,
    BirdeyeV2TopTradersTimeFrame
)
from ..birdeye.schema import (
    GetTokenListResponse,
    GetV3TokenListQuery,
    GetV3TokenListResponse,
    GetV3TokenListScrollQuery,
    GetV3TokenListScrollResponse,
    GetV2TokensNewListingResponse,
    GetV2MarketsResponse,
    GetV3TokenMetaDataResponse,
    GetV3TokenMetaDataMultipleResponse,
    GetV3TokenMarketDataResponse,
    GetV3TokenMarketDataMultipleResponse,
    GetV3TokenTradeDataResponse,
    GetV3TokenTradeDataMultipleResponse,
    GetV3TokenExitLiquidityResponse,
    GetV3TokenExitLiquidityMultipleResponse,
    GetV3TokenMintBurnTxsResponse,
    GetV2TopTradersResponse,
    GetTokenSecurityResponse,
    GetTokenCreationInfoResponse,
    GetTokenOverviewResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetPriceVolumeSingleResponse,
    PostPriceVolumeMultiResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse
)

class Birdeye(Interaction):
    """
        Class used to connect [https://birdeye.so](https://birdeye.so) API.
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check [https://docs.birdeye.so](https://docs.birdeye.so) for all the details on the available endpoints.

        !!! info
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from ENV variable **BIRDEYE_API_KEY**.

        Parameters:
            api_key: specify the API key to use for the connection.
            chain: identifier of the chain to use in all the requests.
                The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                Import them from the library to use the correct identifier.

        **Example**
        ```python
        import asyncio
        from cyhole.birdeye import Birdeye

        birdeye = Birdeye()

        # Get current token list on Solana
        # synchronous
        response = birdeye.client.get_token_list()
        print(f"Currently listed {len(response.data.tokens)} tokens on Solana")

        # asynchronous
        async def main() -> None:
            async with birdeye.async_client as client:
                response = await client.get_token_list()
                print(f"Currently listed {len(response.data.tokens)} tokens on Solana")

        asyncio.run(main())
        ```

        Raises:
            MissingAPIKeyError: if no API Key was available during the object creation.
    """
    def __init__(self, api_key: str | None = None, chain: str = BirdeyeChain.SOLANA.value) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("BIRDEYE_API_KEY")
        if self.api_key is None:
            raise MissingAPIKeyError("no API key is provided during object's creation.")

        # headers setup
        headers = {
            "X-API-KEY": self.api_key,
            "x-chain": chain
        }
        super().__init__(headers)
        self.headers: dict[str, str]

        # clients
        self.client = BirdeyeClient(self, headers = headers)
        self.async_client = BirdeyeAsyncClient(self, headers = headers)

        # API urls
        self.url_api_public = "https://public-api.birdeye.so/defi/"
        self.url_api_private = "https://public-api.birdeye.so/defi/"
        self.url_api_private_wallet = "https://public-api.birdeye.so/v1/wallet"
        return

    @overload
    def _get_token_list(
        self,
        sync: Literal[True],
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        min_liquidity: float | None = None,
        max_liquidity: float | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenListResponse: ...

    @overload
    def _get_token_list(
        self,
        sync: Literal[False],
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        min_liquidity: float | None = None,
        max_liquidity: float | None = None,
        ui_amount_mode: str | None = None
    ) -> Coroutine[None, None, GetTokenListResponse]: ...

    def _get_token_list(
        self,
        sync: bool,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        min_liquidity: float | None = None,
        max_liquidity: float | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenListResponse | Coroutine[None, None, GetTokenListResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Token - List (V1)](https://docs.birdeye.so/reference/get-defi-tokenlist)** and is used
            to retrieve a ranked list of tokens on the selected chain, scored by the chosen metric
            (USD volume, market cap, 24h change, or liquidity). It is the legacy V1 listing endpoint:
            results are returned in a flat page of at most 50 entries and each row carries the core
            identity, price/liquidity, market cap and 24h volume fields that power Birdeye's public
            token discovery views.

            Parameters:
                sort_by: define the metric used to rank the returned tokens (e.g. USD volume in the
                    last 24h, market cap, 24h change, or liquidity).
                    The supported values are available on [`BirdeyeSort`][cyhole.birdeye.param.BirdeyeSort].
                    Import them from the library to use the correct identifier.
                order_by: define the order of the ranking (ascending or descending).
                    The supported values are available on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
                    Import them from the library to use the correct identifier.
                offset: zero-based offset to use for pagination. Combined with `limit` it returns the
                    `[offset, offset + limit)` slice of the ranking. Default behaviour: `0`.
                limit: number of records to return per page. The API caps this at `50`; values above
                    `50` are rejected by Birdeye. Default behaviour: `50`.
                min_liquidity: exclusive lower bound on the on-chain liquidity (USD) of returned tokens.
                    Birdeye applies a default of `100` server-side when not provided.
                max_liquidity: exclusive upper bound on the on-chain liquidity (USD) of returned tokens.
                    If not provided, the API does not apply any upper bound.
                ui_amount_mode: how to format scaled-UI-amount token figures on Solana.
                    The supported values are available on [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode].
                    Only applies on Solana; ignored on other chains. Default behaviour: `scaled`.

            Returns:
                ranked list of tokens for the selected chain along with the snapshot timestamp.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeSort.check(sort_by)
        BirdeyeOrder.check(order_by)
        if ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(ui_amount_mode)

        # set params
        url = self.url_api_public + "tokenlist"
        params = {
            "sort_by" : sort_by,
            "sort_type" : order_by,
            "offset" : offset,
            "limit": limit,
            "min_liquidity": min_liquidity,
            "max_liquidity": max_liquidity,
            "ui_amount_mode": ui_amount_mode
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenListResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenListResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_list(self, sync: Literal[True], query: GetV3TokenListQuery | None = None) -> GetV3TokenListResponse: ...

    @overload
    def _get_v3_token_list(self, sync: Literal[False], query: GetV3TokenListQuery | None = None) -> Coroutine[None, None, GetV3TokenListResponse]: ...

    def _get_v3_token_list(
        self,
        sync: bool,
        query: GetV3TokenListQuery | None = None
    ) -> GetV3TokenListResponse | Coroutine[None, None, GetV3TokenListResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - List (V3)](https://docs.birdeye.so/reference/get-defi-v3-token-list)** and is used
            to retrieve a paginated ranked list of tokens on the selected chain, with a much richer filter
            surface than the legacy V1 listing endpoint: callers can rank by any of the 46 metrics exposed
            on [`BirdeyeV3TokenListSortBy`][cyhole.birdeye.param.BirdeyeV3TokenListSortBy] and restrict
            results by liquidity, market cap, FDV, holder count, recent-listing time, last-trade time
            and a wide range of per-window (1m..30d) volume, price-change and trade-count thresholds.
            Each entry returned by the endpoint mirrors the cyhole [`V3TokenListItem`][cyhole.birdeye.schema.V3TokenListItem]
            shape (identity, supply, liquidity, price, per-window aggregates).

            !!! info
                The endpoint is restricted by Birdeye to Solana, Base, BSC, Ethereum and Monad. Pagination
                must satisfy `offset + limit <= 10000`; each page is capped at 100 entries.

            Parameters:
                query: optional [`GetV3TokenListQuery`][cyhole.birdeye.schema.GetV3TokenListQuery] instance
                    holding the desired sort metric, sort direction, pagination cursor and filters. When
                    `None` (or omitted) the call uses Birdeye's defaults — top 100 tokens sorted by liquidity
                    descending.

            Returns:
                paginated list of tokens decoded as [`GetV3TokenListResponse`][cyhole.birdeye.schema.GetV3TokenListResponse].

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        if query is None:
            query = GetV3TokenListQuery()

        # check param consistency
        BirdeyeV3TokenListSortBy.check(query.sort_by)
        BirdeyeOrder.check(query.sort_type)
        if query.ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(query.ui_amount_mode)

        # set params - drop None values so we only send what was set
        url = self.url_api_public + "v3/token/list"
        params = {k: v for k, v in query.model_dump().items() if v is not None}

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV3TokenListResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV3TokenListResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_list_scroll(self, sync: Literal[True], query: GetV3TokenListScrollQuery | None = None) -> GetV3TokenListScrollResponse: ...

    @overload
    def _get_v3_token_list_scroll(self, sync: Literal[False], query: GetV3TokenListScrollQuery | None = None) -> Coroutine[None, None, GetV3TokenListScrollResponse]: ...

    def _get_v3_token_list_scroll(
        self,
        sync: bool,
        query: GetV3TokenListScrollQuery | None = None
    ) -> GetV3TokenListScrollResponse | Coroutine[None, None, GetV3TokenListScrollResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - List (V3) Scroll](https://docs.birdeye.so/reference/get-defi-v3-token-list-scroll)** and is used
            to iterate through the full v3 token list using a server-issued opaque cursor instead of
            offset/limit pagination. Each call returns up to 5 000 token entries (vs the 100/page cap
            of the offset-based v3 list) and an `next_scroll_id` cursor; pass that cursor back as
            `scroll_id` on the next call to fetch the next batch of the same scroll session. Filters
            (liquidity, market cap, FDV, holder, recent listing time, per-window thresholds, ...) are
            honoured only on the first call (with `scroll_id` left to `None`) and ignored on
            continuation calls. Items share the [`V3TokenListItem`][cyhole.birdeye.schema.V3TokenListItem]
            shape used by the regular v3 list, with the additional `creation_time` field populated
            on scroll results.

            !!! info
                Birdeye enforces a hard cap of one active `scroll_id` per account per 30 seconds.

            Parameters:
                query: optional [`GetV3TokenListScrollQuery`][cyhole.birdeye.schema.GetV3TokenListScrollQuery]
                    instance. Leave `None` to start a fresh scroll with Birdeye's defaults (top 5 000
                    tokens by liquidity descending). To continue a previous scroll set
                    `query = GetV3TokenListScrollQuery(scroll_id = <previous next_scroll_id>)`.

            Returns:
                scroll batch decoded as [`GetV3TokenListScrollResponse`][cyhole.birdeye.schema.GetV3TokenListScrollResponse].
                Inspect `data.next_scroll_id` / `data.has_next` to decide whether to keep iterating.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        if query is None:
            query = GetV3TokenListScrollQuery()

        # check param consistency
        BirdeyeV3TokenListSortBy.check(query.sort_by)
        BirdeyeOrder.check(query.sort_type)
        if query.ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(query.ui_amount_mode)

        # set params - drop None values so we only send what was set
        url = self.url_api_public + "v3/token/list/scroll"
        params = {k: v for k, v in query.model_dump().items() if v is not None}

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV3TokenListScrollResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV3TokenListScrollResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v2_tokens_new_listing(
        self,
        sync: Literal[True],
        time_to: int | None = None,
        limit: int | None = None,
        meme_platform_enabled: bool | None = None
    ) -> GetV2TokensNewListingResponse: ...

    @overload
    def _get_v2_tokens_new_listing(
        self,
        sync: Literal[False],
        time_to: int | None = None,
        limit: int | None = None,
        meme_platform_enabled: bool | None = None
    ) -> Coroutine[None, None, GetV2TokensNewListingResponse]: ...

    def _get_v2_tokens_new_listing(
        self,
        sync: bool,
        time_to: int | None = None,
        limit: int | None = None,
        meme_platform_enabled: bool | None = None
    ) -> GetV2TokensNewListingResponse | Coroutine[None, None, GetV2TokensNewListingResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - New Listing](https://docs.birdeye.so/reference/get-defi-v2-tokens-new_listing)** and is used
            to retrieve a feed of tokens that Birdeye has just detected listings for on the selected
            chain, ordered most-recent first. It is the canonical way to discover freshly-launched
            tokens before they show up in the ranked token list, and powers Birdeye's "new pairs"
            UIs. The endpoint returns a single batch (no offset pagination); call it repeatedly with
            an updated `time_to` to walk further back in time.

            !!! info
                Available on every Birdeye chain except Sui. The `meme_platform_enabled` toggle is
                Solana-only.

            Parameters:
                time_to: optional unix-second cursor; when set Birdeye returns only listings observed at
                    or before this timestamp. Default behaviour: most recent listings.
                limit: number of records to return (1..20). Default behaviour: `10`.
                meme_platform_enabled: when `True` includes listings detected on meme-coin launchpads
                    such as pump.fun (Solana only). Default behaviour: `False`.

            Returns:
                feed of newly-listed tokens decoded as [`GetV2TokensNewListingResponse`][cyhole.birdeye.schema.GetV2TokensNewListingResponse].

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        url = self.url_api_public + "v2/tokens/new_listing"
        params = {
            "time_to": time_to,
            "limit": limit,
            "meme_platform_enabled": str(meme_platform_enabled).lower() if meme_platform_enabled is not None else None,
        }

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV2TokensNewListingResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV2TokensNewListingResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v2_markets(
        self,
        sync: Literal[True],
        address: str,
        sort_by: str = BirdeyeV2MarketsSortBy.LIQUIDITY.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV2MarketsResponse: ...

    @overload
    def _get_v2_markets(
        self,
        sync: Literal[False],
        address: str,
        sort_by: str = BirdeyeV2MarketsSortBy.LIQUIDITY.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> Coroutine[None, None, GetV2MarketsResponse]: ...

    def _get_v2_markets(
        self,
        sync: bool,
        address: str,
        sort_by: str = BirdeyeV2MarketsSortBy.LIQUIDITY.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV2MarketsResponse | Coroutine[None, None, GetV2MarketsResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - All Market List](https://docs.birdeye.so/reference/get-defi-v2-markets)** and is used
            to retrieve the list of markets (trading pairs) Birdeye knows for a given token, ranked
            by liquidity or 24h USD volume. Each entry describes the market address, its source
            (DEX/aggregator), the base/quote token identities, current liquidity, price, and 24h
            trade/volume/unique-wallet aggregates plus the percent change vs the previous 24h window.
            Useful when a caller wants to drill down from a token to where it actually trades.

            Parameters:
                address: contract address of the token whose markets must be listed.
                sort_by: ranking metric. Pick one of the constants on
                    [`BirdeyeV2MarketsSortBy`][cyhole.birdeye.param.BirdeyeV2MarketsSortBy].
                sort_type: ascending or descending order. Pick one of the constants on
                    [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
                offset: zero-based pagination offset. Default behaviour: `0`.
                limit: number of records to return (1..20). Default behaviour: `10`.

            Returns:
                paginated list of markets decoded as [`GetV2MarketsResponse`][cyhole.birdeye.schema.GetV2MarketsResponse],
                plus the total number of markets Birdeye tracks for the token in `data.total`.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        BirdeyeV2MarketsSortBy.check(sort_by)
        BirdeyeOrder.check(sort_type)

        url = self.url_api_public + "v2/markets"
        params = {
            "address": address,
            "sort_by": sort_by,
            "sort_type": sort_type,
            "offset": offset,
            "limit": limit,
        }

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV2MarketsResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV2MarketsResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_meta_data(self, sync: Literal[True], address: str) -> GetV3TokenMetaDataResponse: ...

    @overload
    def _get_v3_token_meta_data(self, sync: Literal[True], address: list[str]) -> GetV3TokenMetaDataMultipleResponse: ...

    @overload
    def _get_v3_token_meta_data(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetV3TokenMetaDataResponse]: ...

    @overload
    def _get_v3_token_meta_data(self, sync: Literal[False], address: list[str]) -> Coroutine[None, None, GetV3TokenMetaDataMultipleResponse]: ...

    def _get_v3_token_meta_data(
        self,
        sync: bool,
        address: str | list[str]
    ) -> (
        GetV3TokenMetaDataResponse
        | GetV3TokenMetaDataMultipleResponse
        | Coroutine[None, None, GetV3TokenMetaDataResponse]
        | Coroutine[None, None, GetV3TokenMetaDataMultipleResponse]
    ):
        """
            This function refers to the v3 Birdeye token-metadata endpoints **[Token - Metadata (Single)](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-single)**
            and **[Token - Metadata (Multiple)](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-multiple)**.
            They return the lightweight identity payload for one or more tokens on the selected chain
            (address, symbol, name, decimals, logo URL and the free-form `extensions` bag of social
            links / CoinGecko id). This is the right call when a caller just needs to resolve a token
            address to a display name and icon without paying for the full Token - Overview payload.

            The method is polymorphic: pass a single `str` address and the function routes to
            `/defi/v3/token/meta-data/single`, returning a [`GetV3TokenMetaDataResponse`][cyhole.birdeye.schema.GetV3TokenMetaDataResponse];
            pass a `list[str]` of addresses and it routes to `/defi/v3/token/meta-data/multiple`,
            returning a [`GetV3TokenMetaDataMultipleResponse`][cyhole.birdeye.schema.GetV3TokenMetaDataMultipleResponse]
            whose `data` is a dict keyed by token address.

            Parameters:
                address: a single token contract address (string) or a list of token contract addresses.
                    The list flavour issues one HTTP call instead of N.

            Returns:
                metadata payload for the requested token(s); the concrete type depends on the input
                cardinality (see above).

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        if isinstance(address, str):
            url = self.url_api_public + "v3/token/meta-data/single"
            params = {"address": address}
            response_model: type = GetV3TokenMetaDataResponse
        else:
            url = self.url_api_public + "v3/token/meta-data/multiple"
            params = {"list_address": ",".join(address)}
            response_model = GetV3TokenMetaDataMultipleResponse

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return response_model(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_market_data(self, sync: Literal[True], address: str, ui_amount_mode: str | None = None) -> GetV3TokenMarketDataResponse: ...

    @overload
    def _get_v3_token_market_data(self, sync: Literal[True], address: list[str], ui_amount_mode: str | None = None) -> GetV3TokenMarketDataMultipleResponse: ...

    @overload
    def _get_v3_token_market_data(self, sync: Literal[False], address: str, ui_amount_mode: str | None = None) -> Coroutine[None, None, GetV3TokenMarketDataResponse]: ...

    @overload
    def _get_v3_token_market_data(self, sync: Literal[False], address: list[str], ui_amount_mode: str | None = None) -> Coroutine[None, None, GetV3TokenMarketDataMultipleResponse]: ...

    def _get_v3_token_market_data(
        self,
        sync: bool,
        address: str | list[str],
        ui_amount_mode: str | None = None
    ) -> (
        GetV3TokenMarketDataResponse
        | GetV3TokenMarketDataMultipleResponse
        | Coroutine[None, None, GetV3TokenMarketDataResponse]
        | Coroutine[None, None, GetV3TokenMarketDataMultipleResponse]
    ):
        """
            This function refers to the v3 Birdeye token market-data endpoints **[Token - Market Data (Single)](https://docs.birdeye.so/reference/get-defi-v3-token-market-data)**
            and **[Token - Market Data (Multiple)](https://docs.birdeye.so/reference/get-defi-v3-token-market-data-multiple)**.
            They return a compact market snapshot per token: price, liquidity, total/circulating supply,
            FDV, market cap and holder count. It is a cheaper alternative to Token - Overview when a
            caller only needs the headline numbers without the per-window trade/volume breakdown.

            The method is polymorphic: pass a single `str` address and the function routes to
            `/defi/v3/token/market-data`, returning a [`GetV3TokenMarketDataResponse`][cyhole.birdeye.schema.GetV3TokenMarketDataResponse];
            pass a `list[str]` of addresses and it routes to `/defi/v3/token/market-data/multiple`,
            returning a [`GetV3TokenMarketDataMultipleResponse`][cyhole.birdeye.schema.GetV3TokenMarketDataMultipleResponse]
            whose `data` is a dict keyed by token address.

            Parameters:
                address: a single token contract address (string) or a list of token contract addresses.
                ui_amount_mode: how to format scaled-UI-amount token figures on Solana.
                    The supported values are available on [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode].
                    Only applies on Solana; ignored on other chains. Default behaviour: `scaled`.

            Returns:
                market snapshot payload for the requested token(s); the concrete type depends on the
                input cardinality (see above).

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        if ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(ui_amount_mode)

        if isinstance(address, str):
            url = self.url_api_public + "v3/token/market-data"
            params: dict[str, Any] = {"address": address}
            response_model: type = GetV3TokenMarketDataResponse
        else:
            url = self.url_api_public + "v3/token/market-data/multiple"
            params = {"list_address": ",".join(address)}
            response_model = GetV3TokenMarketDataMultipleResponse
        if ui_amount_mode is not None:
            params["ui_amount_mode"] = ui_amount_mode

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return response_model(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_trade_data(self, sync: Literal[True], address: str, frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataResponse: ...

    @overload
    def _get_v3_token_trade_data(self, sync: Literal[True], address: list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataMultipleResponse: ...

    @overload
    def _get_v3_token_trade_data(self, sync: Literal[False], address: str, frames: str | None = None, ui_amount_mode: str | None = None) -> Coroutine[None, None, GetV3TokenTradeDataResponse]: ...

    @overload
    def _get_v3_token_trade_data(self, sync: Literal[False], address: list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> Coroutine[None, None, GetV3TokenTradeDataMultipleResponse]: ...

    def _get_v3_token_trade_data(
        self,
        sync: bool,
        address: str | list[str],
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> (
        GetV3TokenTradeDataResponse
        | GetV3TokenTradeDataMultipleResponse
        | Coroutine[None, None, GetV3TokenTradeDataResponse]
        | Coroutine[None, None, GetV3TokenTradeDataMultipleResponse]
    ):
        """
            This function refers to the v3 Birdeye token trade-data endpoints **[Token - Trade Data (Single)](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-single)**
            and **[Token - Trade Data (Multiple)](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-multiple)**.
            They return the full trading-activity snapshot of a token: latest price, price history at the
            1m/5m/30m/1h/2h/4h/6h/8h/12h/24h windows, per-window (1m..24h) unique-wallet counts and full
            sell/buy/volume breakdowns, all aligned with the equivalent metric over the previous window.
            This is the "give me everything about how this token is trading" call — heavier than
            Token - Market Data but lighter than Token - Overview as it skips the identity and supply
            sections.

            The method is polymorphic: pass a single `str` address and the function routes to
            `/defi/v3/token/trade-data/single`, returning a [`GetV3TokenTradeDataResponse`][cyhole.birdeye.schema.GetV3TokenTradeDataResponse];
            pass a `list[str]` of addresses and it routes to `/defi/v3/token/trade-data/multiple`,
            returning a [`GetV3TokenTradeDataMultipleResponse`][cyhole.birdeye.schema.GetV3TokenTradeDataMultipleResponse]
            whose `data` is a dict keyed by token address.

            Parameters:
                address: a single token contract address (string) or a list of token contract addresses.
                frames: optional comma-separated list of additional custom time intervals to include in
                    the response (up to 8 entries). Same grammar as on Token - Overview: minute intervals
                    `1m..1440m`, multiples-of-5 second intervals `5s..3600s`, and `1h/2h/4h/8h/24h`.
                    Default behaviour: only the standard windows listed above are returned.
                ui_amount_mode: how to format scaled-UI-amount token figures on Solana.
                    The supported values are available on [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode].
                    Only applies on Solana; ignored on other chains. Default behaviour: `scaled`.

            Returns:
                trading-activity snapshot for the requested token(s); the concrete type depends on the
                input cardinality (see above).

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        if ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(ui_amount_mode)

        if isinstance(address, str):
            url = self.url_api_public + "v3/token/trade-data/single"
            params: dict[str, Any] = {"address": address}
            response_model: type = GetV3TokenTradeDataResponse
        else:
            url = self.url_api_public + "v3/token/trade-data/multiple"
            params = {"list_address": ",".join(address)}
            response_model = GetV3TokenTradeDataMultipleResponse
        if frames is not None:
            params["frames"] = frames
        if ui_amount_mode is not None:
            params["ui_amount_mode"] = ui_amount_mode

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return response_model(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_exit_liquidity(self, sync: Literal[True], address: str) -> GetV3TokenExitLiquidityResponse: ...

    @overload
    def _get_v3_token_exit_liquidity(self, sync: Literal[True], address: list[str]) -> GetV3TokenExitLiquidityMultipleResponse: ...

    @overload
    def _get_v3_token_exit_liquidity(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetV3TokenExitLiquidityResponse]: ...

    @overload
    def _get_v3_token_exit_liquidity(self, sync: Literal[False], address: list[str]) -> Coroutine[None, None, GetV3TokenExitLiquidityMultipleResponse]: ...

    def _get_v3_token_exit_liquidity(
        self,
        sync: bool,
        address: str | list[str]
    ) -> (
        GetV3TokenExitLiquidityResponse
        | GetV3TokenExitLiquidityMultipleResponse
        | Coroutine[None, None, GetV3TokenExitLiquidityResponse]
        | Coroutine[None, None, GetV3TokenExitLiquidityMultipleResponse]
    ):
        """
            This function refers to the v3 Birdeye token exit-liquidity endpoints **[Token - Liquidity (Single)](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity)**
            and **[Token - Liquidity (Multiple)](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity-multiple)**.
            They return Birdeye's estimate of how much value the largest holders of a token could
            realistically extract by selling without crashing the price, computed from the on-chain
            liquidity profile of the token's biggest markets. The single variant returns the payload
            directly under `data`; the multiple variant returns `data.items` as a list (one entry per
            requested address).

            !!! info
                Birdeye restricts both endpoints to the **Base** chain at the time of writing.

            The method is polymorphic: pass a single `str` address and the function routes to
            `/defi/v3/token/exit-liquidity`, returning a [`GetV3TokenExitLiquidityResponse`][cyhole.birdeye.schema.GetV3TokenExitLiquidityResponse];
            pass a `list[str]` of addresses and it routes to `/defi/v3/token/exit-liquidity/multiple`,
            returning a [`GetV3TokenExitLiquidityMultipleResponse`][cyhole.birdeye.schema.GetV3TokenExitLiquidityMultipleResponse]
            whose `data.items` is a list of entries.

            Parameters:
                address: a single token contract address (string) or a list of token contract addresses.

            Returns:
                exit-liquidity payload for the requested token(s); the concrete type depends on the
                input cardinality (see above).

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        if isinstance(address, str):
            url = self.url_api_public + "v3/token/exit-liquidity"
            params: dict[str, Any] = {"address": address}
            response_model: type = GetV3TokenExitLiquidityResponse
        else:
            url = self.url_api_public + "v3/token/exit-liquidity/multiple"
            params = {"list_address": ",".join(address)}
            response_model = GetV3TokenExitLiquidityMultipleResponse

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return response_model(**content_raw.json())
            return async_request()

    @overload
    def _get_v3_token_mint_burn_txs(
        self,
        sync: Literal[True],
        address: str,
        type: str = BirdeyeMintBurnType.ALL.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        after_time: int | None = None,
        before_time: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV3TokenMintBurnTxsResponse: ...

    @overload
    def _get_v3_token_mint_burn_txs(
        self,
        sync: Literal[False],
        address: str,
        type: str = BirdeyeMintBurnType.ALL.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        after_time: int | None = None,
        before_time: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> Coroutine[None, None, GetV3TokenMintBurnTxsResponse]: ...

    def _get_v3_token_mint_burn_txs(
        self,
        sync: bool,
        address: str,
        type: str = BirdeyeMintBurnType.ALL.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        after_time: int | None = None,
        before_time: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV3TokenMintBurnTxsResponse | Coroutine[None, None, GetV3TokenMintBurnTxsResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Mint/Burn](https://docs.birdeye.so/reference/get-defi-v3-token-mint-burn-txs)** and is used
            to retrieve the on-chain mint and burn transactions of an SPL token: every transaction that
            either increases or decreases the token's total supply. Each entry exposes the on-chain
            signature, the affected mint, the program that emitted the instruction, raw and UI-formatted
            amounts, slot, and the block timestamp. Useful for auditing supply changes (rewards,
            redemptions, buybacks) outside of normal trades.

            !!! info
                Birdeye restricts this endpoint to the **Solana** chain at the time of writing.

            Parameters:
                address: contract address of the SPL token whose mint/burn history must be retrieved.
                type: kind of supply change to return. Pick one of the constants on
                    [`BirdeyeMintBurnType`][cyhole.birdeye.param.BirdeyeMintBurnType].
                    Default behaviour: `all`.
                sort_type: ascending or descending order on `block_time`. Pick one of the constants on
                    [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder]. Default behaviour: `desc`
                    (most recent first).
                after_time: optional inclusive lower bound on the transaction block time, in unix
                    seconds; `None` to disable.
                before_time: optional inclusive upper bound on the transaction block time, in unix
                    seconds; `None` to disable.
                offset: zero-based pagination offset. Default behaviour: `0`.
                    Birdeye requires `offset + limit <= 10000`.
                limit: number of records to return (1..100). Default behaviour: `100`.

            Returns:
                ranked list of mint/burn transactions decoded as
                [`GetV3TokenMintBurnTxsResponse`][cyhole.birdeye.schema.GetV3TokenMintBurnTxsResponse].

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        BirdeyeMintBurnType.check(type)
        BirdeyeOrder.check(sort_type)

        url = self.url_api_public + "v3/token/mint-burn-txs"
        params = {
            "address": address,
            "sort_by": "block_time",
            "sort_type": sort_type,
            "type": type,
            "after_time": after_time,
            "before_time": before_time,
            "offset": offset,
            "limit": limit,
        }

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV3TokenMintBurnTxsResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV3TokenMintBurnTxsResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_v2_tokens_top_traders(
        self,
        sync: Literal[True],
        address: str,
        time_frame: str = BirdeyeV2TopTradersTimeFrame.H24.value,
        sort_by: str = BirdeyeV2TopTradersSortBy.VOLUME.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetV2TopTradersResponse: ...

    @overload
    def _get_v2_tokens_top_traders(
        self,
        sync: Literal[False],
        address: str,
        time_frame: str = BirdeyeV2TopTradersTimeFrame.H24.value,
        sort_by: str = BirdeyeV2TopTradersSortBy.VOLUME.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> Coroutine[None, None, GetV2TopTradersResponse]: ...

    def _get_v2_tokens_top_traders(
        self,
        sync: bool,
        address: str,
        time_frame: str = BirdeyeV2TopTradersTimeFrame.H24.value,
        sort_by: str = BirdeyeV2TopTradersSortBy.VOLUME.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetV2TopTradersResponse | Coroutine[None, None, GetV2TopTradersResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Top Traders](https://docs.birdeye.so/reference/get-defi-v2-tokens-top_traders)** and is used
            to retrieve the wallets that traded the most of a given token over a configurable time
            frame, ranked by raw volume, USD volume, trade count, or realised/unrealised PnL. Each
            entry exposes the wallet address, optional Birdeye tags (`whale`, `bot`, ...), trade and
            volume splits between buy and sell sides, and Solana-only profit-and-loss figures.
            Useful when surfacing the dominant participants behind a token's recent activity.

            !!! info
                The PnL-based sort metrics (`total_pnl`, `unrealized_pnl`, `realized_pnl`,
                `volume_usd`) and the longer time frames (2d..90d) are restricted by Birdeye to
                Solana. On every other chain only `volume` / `trade` sort and time frames up to 24h
                are honoured.

            Parameters:
                address: contract address of the token whose top traders must be listed.
                time_frame: trailing window for the metrics. Pick one of the constants on
                    [`BirdeyeV2TopTradersTimeFrame`][cyhole.birdeye.param.BirdeyeV2TopTradersTimeFrame].
                    Default behaviour: `24h`.
                sort_by: ranking metric. Pick one of the constants on
                    [`BirdeyeV2TopTradersSortBy`][cyhole.birdeye.param.BirdeyeV2TopTradersSortBy].
                    Default behaviour: `volume`.
                sort_type: ascending or descending order. Pick one of the constants on
                    [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder]. Default behaviour: `desc`.
                offset: zero-based pagination offset. Default behaviour: `0`. Birdeye requires
                    `offset + limit <= 10000`.
                limit: number of records to return. Default behaviour: `10`.
                ui_amount_mode: how to format scaled-UI-amount token figures on Solana. Pick a
                    [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode] member or leave
                    `None` for the server default (`scaled`).

            Returns:
                ranked list of top trader entries decoded as
                [`GetV2TopTradersResponse`][cyhole.birdeye.schema.GetV2TopTradersResponse].

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        BirdeyeV2TopTradersTimeFrame.check(time_frame)
        BirdeyeV2TopTradersSortBy.check(sort_by)
        BirdeyeOrder.check(sort_type)
        if ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(ui_amount_mode)

        url = self.url_api_public + "v2/tokens/top_traders"
        params = {
            "address": address,
            "time_frame": time_frame,
            "sort_type": sort_type,
            "sort_by": sort_by,
            "offset": offset,
            "limit": limit,
            "ui_amount_mode": ui_amount_mode,
        }

        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetV2TopTradersResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetV2TopTradersResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_creation_info(
        self,
        sync: Literal[True],
        address: str
    ) -> GetTokenCreationInfoResponse: ...

    @overload
    def _get_token_creation_info(
        self,
        sync: Literal[False],
        address: str
    ) -> Coroutine[None, None, GetTokenCreationInfoResponse]: ...

    def _get_token_creation_info(
        self,
        sync: bool,
        address: str
    ) -> GetTokenCreationInfoResponse | Coroutine[None, None, GetTokenCreationInfoResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get-defi-token_creation_info)** and is used
            to retrieve the on-chain transaction that originally minted a given token together with its
            slot, block timestamp (both unix and human-readable), creator/owner address and decimals.
            It is the canonical way to answer "when and by whom was this token created?" on Birdeye-supported
            chains and is typically used as part of a token vetting flow (age check, deployer profiling).

            !!! info
                Currently the endpoint is restricted by Birdeye to the Solana, BSC, Base, Ethereum and Monad chains.

            Parameters:
                address: contract address of the token whose creation information must be retrieved.

            Returns:
                creation transaction hash, slot, block timestamps, creator/owner address and decimals.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "token_creation_info"
        params = {
            "address" : address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenCreationInfoResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenCreationInfoResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_security(
        self,
        sync: Literal[True],
        address: str
    ) -> GetTokenSecurityResponse: ...

    @overload
    def _get_token_security(
        self,
        sync: Literal[False],
        address: str
    ) -> Coroutine[None, None, GetTokenSecurityResponse]: ...

    def _get_token_security(
        self,
        sync: bool,
        address: str
    ) -> GetTokenSecurityResponse | Coroutine[None, None, GetTokenSecurityResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get-defi-token_security)** and is used
            to retrieve Birdeye's risk profile of a token: ownership and authority addresses, creator/owner
            balances, top-holder concentration, freeze/mint/Token-2022 flags, lock information and
            metadata mutability. It is the canonical endpoint behind Birdeye's "is this token safe?"
            checks and is typically consumed when surfacing scam/rug warnings before showing a swap UI.

            !!! info
                The endpoint is available on every Birdeye chain except Sui. The response payload
                differs between Solana (typed schema below) and EVM chains (free-form dictionary).

            Parameters:
                address: contract address of the token to analyse on the currently selected chain.

            Returns:
                security profile of the token.
                    Observe that the content of `data` depends on the selected chain: on Solana the
                    payload is decoded as
                    [`GetTokenSecurityDataSolana`][cyhole.birdeye.schema.GetTokenSecurityDataSolana];
                    on other chains it is exposed as a raw dictionary.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "token_security"
        params = {
            "address" : address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenSecurityResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenSecurityResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_overview(
        self,
        sync: Literal[True],
        address: str,
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenOverviewResponse: ...

    @overload
    def _get_token_overview(
        self,
        sync: Literal[False],
        address: str,
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> Coroutine[None, None, GetTokenOverviewResponse]: ...

    def _get_token_overview(
        self,
        sync: bool,
        address: str,
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenOverviewResponse | Coroutine[None, None, GetTokenOverviewResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get-defi-token_overview)** and is used
            to retrieve Birdeye's full analytics snapshot of a single token: identity (address, symbol,
            name, social links), pricing (current price and per-window history at 1m/5m/30m/1h/2h/4h/6h/8h/12h/24h),
            liquidity, supply (total, circulating, holders count), unique-wallet counts and
            per-side trade activity (sell, buy, volume in both token-UI units and USD) for the trailing
            1m/5m/30m/1h/2h/4h/8h/24h windows together with the equivalent metric over the previous window
            and a precomputed percent change. It is the canonical endpoint behind Birdeye's token detail
            page and is normally used as the "give me everything you know about this token" call.

            Parameters:
                address: contract address of the token whose analytics snapshot must be retrieved.
                frames: comma-separated list of additional custom time intervals to include in the
                    response (up to 8 entries). Birdeye accepts minute intervals from `1m` to `1440m`,
                    second intervals in multiples of 5 from `5s` to `3600s`, and hour intervals among
                    `1h`, `2h`, `4h`, `8h` and `24h`. Default behaviour: only the standard windows
                    listed above are returned.
                ui_amount_mode: how to format scaled-UI-amount token figures on Solana.
                    The supported values are available on [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode].
                    Only applies on Solana; ignored on other chains. Default behaviour: `scaled`.

            Returns:
                token analytics snapshot decoded as [`GetTokenOverviewData`][cyhole.birdeye.schema.GetTokenOverviewData].

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        if ui_amount_mode is not None:
            BirdeyeUIAmountMode.check(ui_amount_mode)

        # set params
        url = self.url_api_public + "token_overview"
        params = {
            "address" : address,
            "frames" : frames,
            "ui_amount_mode" : ui_amount_mode
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenOverviewResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenOverviewResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price(
        self,
        sync: Literal[True],
        address: str,
        include_liquidity: bool | None = None
    ) -> GetPriceResponse: ...

    @overload
    def _get_price(
        self,
        sync: Literal[False],
        address: str,
        include_liquidity: bool | None = None
    ) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(
        self,
        sync: bool,
        address: str,
        include_liquidity: bool | None = None
    ) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Price](https://docs.birdeye.so/reference/get_defi-price)** and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)

            Returns:
                token's price returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """        # set params
        url = self.url_api_public + "price"
        params = {
            "address" : address,
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price_multiple(
        self,
        sync: Literal[True],
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> GetPriceMultipleResponse: ...

    @overload
    def _get_price_multiple(
        self,
        sync: Literal[False],
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> Coroutine[None, None, GetPriceMultipleResponse]: ...

    def _get_price_multiple(
        self,
        sync: bool,
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> GetPriceMultipleResponse | Coroutine[None, None, GetPriceMultipleResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Price - Multiple](https://docs.birdeye.so/reference/get_defi-multi-price)** and is used 
            to get the current price of multeple tokens on a specific chain on Birdeye.

            Parameters:
                list_address: CA of the tokens to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)

            Returns:
                list of tokens returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "multi_price"
        params = {
            "list_address" : ",".join(list_address),
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceMultipleResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceMultipleResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price_historical(
        self,
        sync: Literal[True],
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> GetPriceHistoricalResponse: ...

    @overload
    def _get_price_historical(
        self,
        sync: Literal[False],
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> Coroutine[None, None, GetPriceHistoricalResponse]: ...

    def _get_price_historical(
        self,
        sync: bool,
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> GetPriceHistoricalResponse | Coroutine[None, None, GetPriceHistoricalResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Price - Historical](https://docs.birdeye.so/reference/get_defi-history-price)** and is used 
            to get the history of prices of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                address_type: the type of address involved in the extraction.
                    The supported chains are available on [`BirdeyeAddressType`][cyhole.birdeye.param.BirdeyeAddressType].
                    Import them from the library to use the correct identifier.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeAddressType.check(address_type)
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "history_price"
        params = {
            "address" : address,
            "address_type" : address_type,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceHistoricalResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceHistoricalResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price_volume_single(
        self,
        sync: Literal[True],
        address: str,
        timeframe: str = BirdeyeHourTimeFrame.H24.value
    ) -> GetPriceVolumeSingleResponse: ...

    @overload
    def _get_price_volume_single(
        self,
        sync: Literal[False],
        address: str,
        timeframe: str = BirdeyeHourTimeFrame.H24.value
    ) -> Coroutine[None, None, GetPriceVolumeSingleResponse]: ...

    def _get_price_volume_single(self, sync: bool, address: str, timeframe: str = BirdeyeHourTimeFrame.H24.value) -> GetPriceVolumeSingleResponse | Coroutine[None, None, GetPriceVolumeSingleResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Price Volume - Single Token](https://docs.birdeye.so/reference/get_defi-price-volume-single)** and is used 
            to get the current price and volume data for a specified token over a given time period on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported timeframes are available on [`BirdeyeHourTimeFrame`][cyhole.birdeye.param.BirdeyeHourTimeFrame].
                    Import them from the library to use the correct identifier.

            Returns:
                current price and volume data for a specified token over a given time period.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is not aligned to it.
        """
        # check param consistency
        BirdeyeHourTimeFrame.check(timeframe)

        # set params
        url = self.url_api_private + "price_volume/single"
        params = {
            "address" : address,
            "type" : timeframe
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceVolumeSingleResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceVolumeSingleResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_price_volume_multi(
        self,
        sync: Literal[True],
        list_address: list[str],
        timeframe: str = BirdeyeHourTimeFrame.H24.value
    ) -> PostPriceVolumeMultiResponse: ...

    @overload
    def _post_price_volume_multi(
        self,
        sync: Literal[False],
        list_address: list[str],
        timeframe: str = BirdeyeHourTimeFrame.H24.value
    ) -> Coroutine[None, None, PostPriceVolumeMultiResponse]: ...

    def _post_price_volume_multi(self, sync: bool, list_address: list[str], timeframe: str = BirdeyeHourTimeFrame.H24.value) -> PostPriceVolumeMultiResponse | Coroutine[None, None, PostPriceVolumeMultiResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Price Volume - Multiple Token](https://docs.birdeye.so/reference/post_defi-price-volume-multi)** and is used 
            to get the current price and volume data for multiple tokens over a given time period on Birdeye.

            Parameters:
                list_address: list of CA of the tokens to search on the chain.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported timeframes are available on [`BirdeyeHourTimeFrame`][cyhole.birdeye.param.BirdeyeHourTimeFrame].
                    Import them from the library to use the correct identifier.

            Returns:
                current price and volume data for multiple tokens over a given time period.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is not aligned to it.
        """
        # check param consistency
        BirdeyeHourTimeFrame.check(timeframe)

        # set params
        url = self.url_api_private + "price_volume/multi"

        # set headers
        headers = self.headers.copy()
        headers["content-type"] = "application/json"

        # set body
        body = {
            "list_address" : ",".join(list_address),
            "type" : timeframe
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.POST.value, url, json = body, headers = headers)
            return PostPriceVolumeMultiResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.POST.value, url, json = body, headers = headers)
                return PostPriceVolumeMultiResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_trades_token(
            self,
            sync: Literal[True],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse: ...

    @overload
    def _get_trades_token(
            self,
            sync: Literal[False],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> Coroutine[None, None, GetTradesTokenResponse]: ...

    def _get_trades_token(
            self,
            sync: bool,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse | Coroutine[None, None, GetTradesTokenResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Trades - Token](https://docs.birdeye.so/reference/get_defi-txs-token)** and is used 
            to get the associated trades of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                offset: offset to apply in the extraction.
                limit: limit the number of returned records in the extraction.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/token"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTradesTokenResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTradesTokenResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_trades_pair(
            self,
            sync: Literal[True],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesPairResponse: ...

    @overload
    def _get_trades_pair(
            self,
            sync: Literal[False],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> Coroutine[None, None, GetTradesPairResponse]: ...

    def _get_trades_pair(
            self,
            sync: bool,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesPairResponse | Coroutine[None, None, GetTradesPairResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Trades - Pair](https://docs.birdeye.so/reference/get_defi-txs-pair)** and is used 
            to get the associated trades of a tokens pair according on a specific chain on Birdeye. 
            Use the 'Trades - Token' endpoint to retrieve the trades associated to a specific token.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                order_by: define the type of ordering to apply in the 
                    extraction; e.g. ascending or descending.
                    The sorting types are available on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
                    Import them from the library to use the correct identifier.
                offset: offset to apply in the extraction.
                limit: limit the number of returned records in the extraction.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeOrder.check(order_by)
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/pair"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "sort_type": order_by,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTradesPairResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTradesPairResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ohlcv(
            self,
            sync: Literal[True],
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVTokenPairResponse: ...

    @overload
    def _get_ohlcv(
            self,
            sync: Literal[False],
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> Coroutine[None, None, GetOHLCVTokenPairResponse]: ...

    def _get_ohlcv(
            self,
            sync: bool,
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVTokenPairResponse | Coroutine[None, None, GetOHLCVTokenPairResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[OHLCV - Token/Pair](https://docs.birdeye.so/reference/get_defi-ohlcv)** and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific token/pair on a chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                address_type: the type of address involved in the extraction (token/pair).
                    The supported chains are available on [`BirdeyeAddressType`][cyhole.birdeye.param.BirdeyeAddressType].
                    Import them from the library to use the correct identifier.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeAddressType.check(address_type)
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "ohlcv"
        if address_type == BirdeyeAddressType.PAIR.value:
            url = url + "/" + BirdeyeAddressType.PAIR.value
        params = {
            "address" : address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetOHLCVTokenPairResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetOHLCVTokenPairResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ohlcv_base_quote(
            self,
            sync: Literal[True],
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVBaseQuoteResponse: ...

    @overload
    def _get_ohlcv_base_quote(
            self,
            sync: Literal[False],
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> Coroutine[None, None, GetOHLCVBaseQuoteResponse]: ...

    def _get_ohlcv_base_quote(
            self,
            sync: bool,
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVBaseQuoteResponse | Coroutine[None, None, GetOHLCVBaseQuoteResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[OHLCV - Base/Quote](https://docs.birdeye.so/reference/get_defi-ohlcv-base-quote)** and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific base/quote combination 
            on a chain on Birdeye.

            Parameters:
                base_address: CA of the token to search on the chain.
                quote_address: CA of the token to search on the chain.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.
            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "ohlcv/base_quote"
        params = {
            "base_address" : base_address,
            "quote_address" : quote_address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetOHLCVBaseQuoteResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetOHLCVBaseQuoteResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_wallet_supported_networks(self, sync: Literal[True]) -> GetWalletSupportedNetworksResponse: ...

    @overload
    def _get_wallet_supported_networks(self, sync: Literal[False]) -> Coroutine[None, None, GetWalletSupportedNetworksResponse]: ...

    def _get_wallet_supported_networks(self, sync: bool) -> GetWalletSupportedNetworksResponse | Coroutine[None, None, GetWalletSupportedNetworksResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Wallet - Supported Networks](https://docs.birdeye.so/reference/get_v1-wallet-list-supported-chain)** and 
            it is used to get the list of supported chains on Birdeye.

            Returns:
                list of chains returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        url = self.url_api_private_wallet + "/list_supported_chain"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetWalletSupportedNetworksResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetWalletSupportedNetworksResponse(**content_raw.json())
            return async_request()