from pydantic import BaseModel, Field

# classes used on GET "Search" endpoint
class GetV3SearchQuery(BaseModel):
    """
        Query-parameter bag for the Birdeye v3 Search endpoint.

        Every field is optional and only sent when set. The default call returns all
        matching tokens and markets sorted by 24h USD volume descending, using exact
        symbol matching across all supported chains.

        Attributes:
            chain: chain to restrict the search to; pass a
                [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain] value, or `"all"` to
                search every supported chain (server default when `None`).
            keyword: search term — token name, symbol, or contract address.
            target: result type to return. Use
                [`BirdeyeSearchTarget`][cyhole.birdeye.param.BirdeyeSearchTarget] constants.
                `None` → server defaults to `"all"` (tokens and markets).
            search_mode: matching behaviour — `"exact"` or `"fuzzy"`. Use
                [`BirdeyeSearchMode`][cyhole.birdeye.param.BirdeyeSearchMode] constants.
                `None` → server defaults to `"exact"`.
            search_by: field to match the keyword against — `"combination"`, `"address"`,
                `"name"`, or `"symbol"`. Use
                [`BirdeyeSearchBy`][cyhole.birdeye.param.BirdeyeSearchBy] constants.
                `None` → server defaults to `"symbol"`.
            sort_by: metric used to rank results. Use
                [`BirdeyeSearchSortBy`][cyhole.birdeye.param.BirdeyeSearchSortBy] constants.
                `None` → server defaults to `"volume_24h_usd"`.
            sort_type: ascending or descending direction. Use
                [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder] constants.
                `None` → server defaults to `"desc"`.
            verify_token: when `True`, restrict results to Birdeye-verified tokens
                (Solana only). `None` → no verification filter applied.
            markets: comma-separated list of DEX/market sources to restrict results to
                (e.g. `"Raydium,Orca"`). `None` → no market-source filter.
            offset: zero-based pagination offset. `None` → server defaults to `0`.
            limit: number of results per page (1–20). `None` → server defaults to `20`.
            ui_amount_mode: how to format scaled-UI-amount token figures on Solana. Use
                [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode] constants.
                `None` → server defaults to `"scaled"`.
    """
    chain: str | None = None
    keyword: str | None = None
    target: str | None = None
    search_mode: str | None = None
    search_by: str | None = None
    sort_by: str | None = None
    sort_type: str | None = None
    verify_token: bool | None = None
    markets: str | None = None
    offset: int | None = None
    limit: int | None = None
    ui_amount_mode: str | None = None


class GetV3SearchResultItem(BaseModel):
    """
        Single result item inside a v3 Search response bucket.

        This model covers both token and market result types. Fields that belong to
        only one type are `None` when the other type is returned. Inspect the parent
        [`GetV3SearchItem.type`][cyhole.birdeye.schema.GetV3SearchItem] field (either
        `"token"` or `"market"`) to determine which subset of fields is populated.

        Attributes:
            name: human-readable name of the token or market pair.
            symbol: ticker symbol; present for token results, `None` for market results.
            address: contract address of the token, or market (pair) address.
            decimals: on-chain decimal places of the token; `None` for market results.
            fdv: fully-diluted valuation in USD; present for token results, `None` otherwise.
            market_cap: market capitalisation in USD; present for token results, `None` otherwise.
            liquidity: current on-chain liquidity in USD; `None` when not available.
            price: latest price in USD; `None` when not available.
            price_change_24h_percent: percent price change over the trailing 24h window;
                `None` when not available.
            volume_24h_usd: USD traded volume during the trailing 24h window; `None` when
                not available.
            volume_24h_change_percent: percent change of USD volume vs the previous 24h
                window; `None` when not available.
            trade_24h: total number of trades during the trailing 24h window; `None` when
                not available.
            trade_24h_change_percent: percent change of trade count vs the previous 24h
                window; `None` when not available.
            buy_24h: number of buy-side trades during the trailing 24h window; `None` when
                not available.
            buy_24h_change_percent: percent change of buy trades vs the previous 24h window;
                `None` when not available.
            sell_24h: number of sell-side trades during the trailing 24h window; `None` when
                not available.
            sell_24h_change_percent: percent change of sell trades vs the previous 24h
                window; `None` when not available.
            unique_wallet_24h: unique wallets that traded during the trailing 24h window;
                `None` when not available.
            unique_view_24h_change_percent: percent change of unique wallet count vs the
                previous 24h window; `None` when not available.
            last_trade_unix_time: unix-second timestamp of the most recent trade; `None` when
                not available.
            logo_uri: URL of the token or market logo; `None` when Birdeye has no image.
                (alias `logoURI`)
            network: chain identifier the result belongs to (e.g. `"solana"`, `"ethereum"`);
                `None` when not provided by the API.
            verify_status: Birdeye verification status (e.g. `"verified"`); `None` for
                market results or unverified tokens.
            created_at: ISO-8601 creation timestamp of the token or market; `None` when
                unknown.
            num_markets: number of DEX markets that list this token; present for token
                results, `None` otherwise.
            source: DEX or AMM name the market belongs to; present for market results,
                `None` for token results.
            base_address: base token address of the market pair; present for market results,
                `None` for token results.
            quote_address: quote token address of the market pair; present for market
                results, `None` for token results.
    """
    model_config = {"extra": "allow", "populate_by_name": True}

    name: str | None = None
    symbol: str | None = None
    address: str | None = None
    decimals: int | None = None
    fdv: float | None = None
    market_cap: float | None = None
    liquidity: float | None = None
    price: float | None = None
    price_change_24h_percent: float | None = None
    volume_24h_usd: float | None = None
    volume_24h_change_percent: float | None = None
    trade_24h: int | None = None
    trade_24h_change_percent: float | None = None
    buy_24h: int | None = None
    buy_24h_change_percent: float | None = None
    sell_24h: int | None = None
    sell_24h_change_percent: float | None = None
    unique_wallet_24h: int | None = None
    unique_view_24h_change_percent: float | None = None
    last_trade_unix_time: int | None = None
    logo_uri: str | None = Field(default = None, alias = "logoURI")
    network: str | None = None
    verify_status: str | None = None
    created_at: str | None = None
    num_markets: int | None = None
    source: str | None = None
    base_address: str | None = None
    quote_address: str | None = None


class GetV3SearchItem(BaseModel):
    """
        One entity-type bucket in the v3 Search response data payload.

        The search endpoint groups results by type — tokens and markets are returned
        in separate buckets. Each bucket holds all matching items of its type.

        Attributes:
            type: entity type for the results in this bucket; either `"token"` or `"market"`.
            result: list of matching items for this bucket type.
    """
    type: str
    result: list[GetV3SearchResultItem]


class GetV3SearchData(BaseModel):
    """
        Data wrapper for the Birdeye v3 Search response.

        Attributes:
            items: list of result buckets, one per entity type returned by the query.
                Depending on the `target` filter, this typically contains a `"token"` bucket,
                a `"market"` bucket, or both.
    """
    items: list[GetV3SearchItem]


class GetV3SearchResponse(BaseModel):
    """
        Model used to represent the **Search** endpoint from the Birdeye API.

        Attributes:
            data: search result buckets grouped by entity type.
            success: `True` when the API processed the request successfully.
    """
    data: GetV3SearchData
    success: bool
