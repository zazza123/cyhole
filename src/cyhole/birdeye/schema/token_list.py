from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from ..param import BirdeyeOrder, BirdeyeV3TokenListSortBy

# classes used on GET "Token List" endpoint
class GetTokenListInfo(BaseModel):
    name: str | None                = None
    symbol: str | None              = None
    price: float
    address: str
    decimals: int
    liquidity: float
    volume_24h_usd: float           = Field(alias = "v24hUSD")
    market_cap: float               = Field(alias = "mc")
    volume_24h_change: float | None = Field(alias = "v24hChangePercent", default = None)
    last_trade_unix_time: float     = Field(alias = "lastTradeUnixTime")
    logo_uri: str  | None           = Field(alias = "logoURI", default = None)

class GetTokenListData(BaseModel):
    total: int | None = None
    update_time: datetime = Field(alias = "updateTime")
    update_unix_time: int = Field(alias = "updateUnixTime")
    tokens: list[GetTokenListInfo]

    @field_validator("update_time")
    def parse_update_time(cls, update_time_raw: str | datetime) -> datetime:
        if isinstance(update_time_raw, str):
            return datetime.strptime(update_time_raw, "%Y-%m-%dT%H:%M:%S")
        return update_time_raw

class GetTokenListResponse(BaseModel):
    """
        Model used to represent the **Token - List** endpoint from birdeye API.
    """
    data: GetTokenListData
    success: bool



# classes used on GET "Token - List (V3)" and GET "Token - List (V3) Scroll" endpoints
class V3TokenListExtensions(BaseModel):
    """
        Optional free-form metadata bag returned alongside each v3 token list item.

        Every key is optional and may be missing or `None`. Most tokens carry only a
        subset of these links.

        Attributes:
            coingecko_id: CoinGecko identifier for the token; `None` if untracked there.
            serum_v3_usdc: Serum V3 market address vs USDC (Solana specific); `None` if unavailable.
            serum_v3_usdt: Serum V3 market address vs USDT (Solana specific); `None` if unavailable.
            website: official website URL of the token project; `None` if unknown.
            telegram: official Telegram URL; `None` if unknown.
            twitter: official Twitter/X URL; `None` if unknown.
            description: textual description of the token; `None` if unknown.
            discord: official Discord URL; `None` if unknown.
            medium: official Medium URL; `None` if unknown.
            github: official GitHub URL; `None` if unknown.
    """
    coingecko_id: str | None = None
    serum_v3_usdc: str | None = None
    serum_v3_usdt: str | None = None
    website: str | None = None
    telegram: str | None = None
    twitter: str | None = None
    description: str | None = None
    discord: str | None = None
    medium: str | None = None
    github: str | None = None

    model_config = {"extra": "allow"}

class V3TokenListItem(BaseModel):
    """
        Single token entry returned by the v3 Token - List and Token - List Scroll endpoints.

        Bundles token identity (address, symbol, name, social links), supply, liquidity,
        price, holder count, and per-window trade/volume aggregates for the trailing
        1m, 5m, 30m, 1h, 2h, 4h, 8h, 24h, 7d and 30d windows together with the equivalent
        percent change vs the previous window. The 24h, 7d and 30d windows additionally
        expose buy- and sell-side breakdowns.

        Attributes:
            address: contract address of the token on the selected chain.
            logo_uri: URL of the token logo; `None` if Birdeye does not have a logo for the token.
            name: human-readable name of the token; `None` if unknown.
            symbol: ticker symbol of the token; `None` if unknown.
            decimals: number of decimal places used by the token.
            extensions: free-form metadata bag (CoinGecko id, website, socials, ...); `None` when Birdeye has no extra metadata.
            market_cap: current market capitalisation of the token in USD; `None` when Birdeye cannot compute it.
            fdv: fully-diluted valuation in USD; `None` when Birdeye cannot compute it.
            total_supply: total on-chain supply of the token in UI units; `None` if undetermined.
            circulating_supply: currently circulating supply of the token in UI units; `None` if undetermined.
            liquidity: total on-chain liquidity of the token in USD; `None` if undetermined.
            last_trade_unix_time: unix-second timestamp of the last observed trade; `None` if no trades have been recorded.
            volume_1m_usd: traded volume during the trailing 1m window expressed in USD; `None` when no activity in that window.
            volume_1m_change_percent: percent change of traded USD volume between the current and previous 1m windows; `None` if change cannot be computed.
            volume_5m_usd: traded volume during the trailing 5m window expressed in USD; `None` when no activity in that window.
            volume_5m_change_percent: percent change of traded USD volume between the current and previous 5m windows; `None` if change cannot be computed.
            volume_30m_usd: traded volume during the trailing 30m window expressed in USD; `None` when no activity in that window.
            volume_30m_change_percent: percent change of traded USD volume between the current and previous 30m windows; `None` if change cannot be computed.
            volume_1h_usd: traded volume during the trailing 1h window expressed in USD; `None` when no activity in that window.
            volume_1h_change_percent: percent change of traded USD volume between the current and previous 1h windows; `None` if change cannot be computed.
            volume_2h_usd: traded volume during the trailing 2h window expressed in USD; `None` when no activity in that window.
            volume_2h_change_percent: percent change of traded USD volume between the current and previous 2h windows; `None` if change cannot be computed.
            volume_4h_usd: traded volume during the trailing 4h window expressed in USD; `None` when no activity in that window.
            volume_4h_change_percent: percent change of traded USD volume between the current and previous 4h windows; `None` if change cannot be computed.
            volume_8h_usd: traded volume during the trailing 8h window expressed in USD; `None` when no activity in that window.
            volume_8h_change_percent: percent change of traded USD volume between the current and previous 8h windows; `None` if change cannot be computed.
            volume_24h_usd: traded volume during the trailing 24h window expressed in USD; `None` when no activity in that window.
            volume_24h_change_percent: percent change of traded USD volume between the current and previous 24h windows; `None` if change cannot be computed.
            volume_7d_usd: traded volume during the trailing 7d window expressed in USD; `None` when no activity in that window.
            volume_7d_change_percent: percent change of traded USD volume between the current and previous 7d windows; `None` if change cannot be computed.
            volume_30d_usd: traded volume during the trailing 30d window expressed in USD; `None` when no activity in that window.
            volume_30d_change_percent: percent change of traded USD volume between the current and previous 30d windows; `None` if change cannot be computed.
            trade_1m_count: total number of trades during the trailing 1m window; `None` when no activity in that window.
            trade_5m_count: total number of trades during the trailing 5m window; `None` when no activity in that window.
            trade_30m_count: total number of trades during the trailing 30m window; `None` when no activity in that window.
            trade_1h_count: total number of trades during the trailing 1h window; `None` when no activity in that window.
            trade_2h_count: total number of trades during the trailing 2h window; `None` when no activity in that window.
            trade_4h_count: total number of trades during the trailing 4h window; `None` when no activity in that window.
            trade_8h_count: total number of trades during the trailing 8h window; `None` when no activity in that window.
            trade_24h_count: total number of trades during the trailing 24h window; `None` when no activity in that window.
            trade_7d_count: total number of trades during the trailing 7d window; `None` when no activity in that window.
            trade_30d_count: total number of trades during the trailing 30d window; `None` when no activity in that window.
            buy_24h: number of buy trades during the trailing 24h window; `None` when no activity in that window.
            buy_24h_change_percent: percent change of buy trade count between the current and previous 24h windows; `None` if change cannot be computed.
            volume_buy_24h_usd: buy-side traded volume during the trailing 24h window in USD; `None` when no activity in that window.
            volume_buy_24h_change_percent: percent change of buy-side traded USD volume between the current and previous 24h windows; `None` if change cannot be computed.
            buy_7d: number of buy trades during the trailing 7d window; `None` when no activity in that window.
            buy_7d_change_percent: percent change of buy trade count between the current and previous 7d windows; `None` if change cannot be computed.
            volume_buy_7d_usd: buy-side traded volume during the trailing 7d window in USD; `None` when no activity in that window.
            volume_buy_7d_change_percent: percent change of buy-side traded USD volume between the current and previous 7d windows; `None` if change cannot be computed.
            buy_30d: number of buy trades during the trailing 30d window; `None` when no activity in that window.
            buy_30d_change_percent: percent change of buy trade count between the current and previous 30d windows; `None` if change cannot be computed.
            volume_buy_30d_usd: buy-side traded volume during the trailing 30d window in USD; `None` when no activity in that window.
            volume_buy_30d_change_percent: percent change of buy-side traded USD volume between the current and previous 30d windows; `None` if change cannot be computed.
            sell_24h: number of sell trades during the trailing 24h window; `None` when no activity in that window.
            sell_24h_change_percent: percent change of sell trade count between the current and previous 24h windows; `None` if change cannot be computed.
            volume_sell_24h_usd: sell-side traded volume during the trailing 24h window in USD; `None` when no activity in that window.
            volume_sell_24h_change_percent: percent change of sell-side traded USD volume between the current and previous 24h windows; `None` if change cannot be computed.
            sell_7d: number of sell trades during the trailing 7d window; `None` when no activity in that window.
            sell_7d_change_percent: percent change of sell trade count between the current and previous 7d windows; `None` if change cannot be computed.
            volume_sell_7d_usd: sell-side traded volume during the trailing 7d window in USD; `None` when no activity in that window.
            volume_sell_7d_change_percent: percent change of sell-side traded USD volume between the current and previous 7d windows; `None` if change cannot be computed.
            sell_30d: number of sell trades during the trailing 30d window; `None` when no activity in that window.
            sell_30d_change_percent: percent change of sell trade count between the current and previous 30d windows; `None` if change cannot be computed.
            volume_sell_30d_usd: sell-side traded volume during the trailing 30d window in USD; `None` when no activity in that window.
            volume_sell_30d_change_percent: percent change of sell-side traded USD volume between the current and previous 30d windows; `None` if change cannot be computed.
            unique_wallet_24h: count of unique wallets that traded the token during the trailing 24h window; `None` if undetermined.
            unique_wallet_24h_change_percent: percent change of unique wallets between the current and previous 24h windows; `None` if change cannot be computed.
            price: latest known price of the token in USD; `None` if no price datapoint is available.
            price_change_1m_percent: price change versus the start of the trailing 1m window expressed in percent; `None` if change cannot be computed.
            price_change_5m_percent: price change versus the start of the trailing 5m window expressed in percent; `None` if change cannot be computed.
            price_change_30m_percent: price change versus the start of the trailing 30m window expressed in percent; `None` if change cannot be computed.
            price_change_1h_percent: price change versus the start of the trailing 1h window expressed in percent; `None` if change cannot be computed.
            price_change_2h_percent: price change versus the start of the trailing 2h window expressed in percent; `None` if change cannot be computed.
            price_change_4h_percent: price change versus the start of the trailing 4h window expressed in percent; `None` if change cannot be computed.
            price_change_8h_percent: price change versus the start of the trailing 8h window expressed in percent; `None` if change cannot be computed.
            price_change_24h_percent: price change versus the start of the trailing 24h window expressed in percent; `None` if change cannot be computed.
            price_change_7d_percent: price change versus the start of the trailing 7d window expressed in percent; `None` if change cannot be computed.
            price_change_30d_percent: price change versus the start of the trailing 30d window expressed in percent; `None` if change cannot be computed.
            holder: number of distinct holders of the token on the chain; `None` if undetermined.
            recent_listing_time: unix-second timestamp at which Birdeye first detected listings for the token; `None` if not tracked.
            is_scaled_ui_token: `True` when the token is a scaled-UI-amount SPL token (Solana only); `None` outside Solana or undetermined.
            multiplier: scaling multiplier applied by the API to UI amounts of scaled-UI-amount tokens; `None` when not applicable.
            creation_time: unix-second timestamp at which the token was first created on the chain; only populated by the scroll endpoint, `None` otherwise.
    """
    address: str = None
    logo_uri: str | None = None
    name: str | None = None
    symbol: str | None = None
    decimals: int = None
    extensions: V3TokenListExtensions | None = None
    market_cap: float | None = None
    fdv: float | None = None
    total_supply: float | None = None
    circulating_supply: float | None = None
    liquidity: float | None = None
    last_trade_unix_time: int | None = None
    volume_1m_usd: float | None = None
    volume_1m_change_percent: float | None = None
    volume_5m_usd: float | None = None
    volume_5m_change_percent: float | None = None
    volume_30m_usd: float | None = None
    volume_30m_change_percent: float | None = None
    volume_1h_usd: float | None = None
    volume_1h_change_percent: float | None = None
    volume_2h_usd: float | None = None
    volume_2h_change_percent: float | None = None
    volume_4h_usd: float | None = None
    volume_4h_change_percent: float | None = None
    volume_8h_usd: float | None = None
    volume_8h_change_percent: float | None = None
    volume_24h_usd: float | None = None
    volume_24h_change_percent: float | None = None
    volume_7d_usd: float | None = None
    volume_7d_change_percent: float | None = None
    volume_30d_usd: float | None = None
    volume_30d_change_percent: float | None = None
    trade_1m_count: int | None = None
    trade_5m_count: int | None = None
    trade_30m_count: int | None = None
    trade_1h_count: int | None = None
    trade_2h_count: int | None = None
    trade_4h_count: int | None = None
    trade_8h_count: int | None = None
    trade_24h_count: int | None = None
    trade_7d_count: int | None = None
    trade_30d_count: int | None = None
    buy_24h: int | None = None
    buy_24h_change_percent: float | None = None
    volume_buy_24h_usd: float | None = None
    volume_buy_24h_change_percent: float | None = None
    buy_7d: int | None = None
    buy_7d_change_percent: float | None = None
    volume_buy_7d_usd: float | None = None
    volume_buy_7d_change_percent: float | None = None
    buy_30d: int | None = None
    buy_30d_change_percent: float | None = None
    volume_buy_30d_usd: float | None = None
    volume_buy_30d_change_percent: float | None = None
    sell_24h: int | None = None
    sell_24h_change_percent: float | None = None
    volume_sell_24h_usd: float | None = None
    volume_sell_24h_change_percent: float | None = None
    sell_7d: int | None = None
    sell_7d_change_percent: float | None = None
    volume_sell_7d_usd: float | None = None
    volume_sell_7d_change_percent: float | None = None
    sell_30d: int | None = None
    sell_30d_change_percent: float | None = None
    volume_sell_30d_usd: float | None = None
    volume_sell_30d_change_percent: float | None = None
    unique_wallet_24h: int | None = None
    unique_wallet_24h_change_percent: float | None = None
    price: float | None = None
    price_change_1m_percent: float | None = None
    price_change_5m_percent: float | None = None
    price_change_30m_percent: float | None = None
    price_change_1h_percent: float | None = None
    price_change_2h_percent: float | None = None
    price_change_4h_percent: float | None = None
    price_change_8h_percent: float | None = None
    price_change_24h_percent: float | None = None
    price_change_7d_percent: float | None = None
    price_change_30d_percent: float | None = None
    holder: int | None = None
    recent_listing_time: int | None = None
    is_scaled_ui_token: bool | None = None
    multiplier: float | None = None
    creation_time: int | None = None

class GetV3TokenListData(BaseModel):
    """
        Payload of the v3 Token - List response.

        Attributes:
            items: list of token entries matching the request filters.
            has_next: `True` when more pages are available; advance with the next offset
                (aliased to `hasNext`).
    """
    items: list[V3TokenListItem]
    has_next: bool = Field(alias = "hasNext")

class GetV3TokenListResponse(BaseModel):
    """
        Model used to represent the **Token - List (V3)** endpoint from birdeye API.

        Attributes:
            data: paginated list of token entries.
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenListData
    success: bool

class GetV3TokenListQuery(BaseModel):
    """
        Query-parameter bag for the v3 Token - List endpoint.

        Every filter is optional and only sent when set. The base call returns the top
        100 tokens sorted by liquidity descending.

        Attributes:
            sort_by: metric used to rank the returned tokens. Pick one of the constants on [`BirdeyeV3TokenListSortBy`][cyhole.birdeye.param.BirdeyeV3TokenListSortBy].
            sort_type: ascending or descending order. Pick one of the constants on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
            offset: zero-based pagination offset. Birdeye requires `offset + limit <= 10000`.
            limit: number of records to return (1..100).
            min_liquidity: inclusive lower bound on token liquidity in USD; `None` to disable the filter.
            max_liquidity: inclusive upper bound on token liquidity in USD; `None` to disable the filter.
            min_market_cap: inclusive lower bound on market cap in USD; `None` to disable the filter.
            max_market_cap: inclusive upper bound on market cap in USD; `None` to disable the filter.
            min_fdv: inclusive lower bound on FDV in USD; `None` to disable the filter.
            max_fdv: inclusive upper bound on FDV in USD; `None` to disable the filter.
            min_recent_listing_time: inclusive lower bound (unix seconds) on the token recent-listing timestamp; `None` to disable the filter.
            max_recent_listing_time: inclusive upper bound (unix seconds) on the token recent-listing timestamp; `None` to disable the filter.
            min_last_trade_unix_time: inclusive lower bound (unix seconds) on the last-trade timestamp; `None` to disable the filter.
            max_last_trade_unix_time: inclusive upper bound (unix seconds) on the last-trade timestamp; `None` to disable the filter.
            min_holder: inclusive minimum number of distinct token holders; `None` to disable the filter.
            ui_amount_mode: how to format scaled-UI-amount token figures on Solana; pick a [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode] member or leave `None` for the server default (`scaled`).
            min_volume_1m_usd: inclusive minimum USD volume in the trailing 1m window; `None` to disable the filter.
            min_volume_5m_usd: inclusive minimum USD volume in the trailing 5m window; `None` to disable the filter.
            min_volume_30m_usd: inclusive minimum USD volume in the trailing 30m window; `None` to disable the filter.
            min_volume_1h_usd: inclusive minimum USD volume in the trailing 1h window; `None` to disable the filter.
            min_volume_2h_usd: inclusive minimum USD volume in the trailing 2h window; `None` to disable the filter.
            min_volume_4h_usd: inclusive minimum USD volume in the trailing 4h window; `None` to disable the filter.
            min_volume_8h_usd: inclusive minimum USD volume in the trailing 8h window; `None` to disable the filter.
            min_volume_24h_usd: inclusive minimum USD volume in the trailing 24h window; `None` to disable the filter.
            min_volume_7d_usd: inclusive minimum USD volume in the trailing 7d window; `None` to disable the filter.
            min_volume_30d_usd: inclusive minimum USD volume in the trailing 30d window; `None` to disable the filter.
            min_volume_1m_change_percent: inclusive minimum percent change of USD volume between the current and previous 1m windows; `None` to disable the filter.
            min_volume_5m_change_percent: inclusive minimum percent change of USD volume between the current and previous 5m windows; `None` to disable the filter.
            min_volume_30m_change_percent: inclusive minimum percent change of USD volume between the current and previous 30m windows; `None` to disable the filter.
            min_volume_1h_change_percent: inclusive minimum percent change of USD volume between the current and previous 1h windows; `None` to disable the filter.
            min_volume_2h_change_percent: inclusive minimum percent change of USD volume between the current and previous 2h windows; `None` to disable the filter.
            min_volume_4h_change_percent: inclusive minimum percent change of USD volume between the current and previous 4h windows; `None` to disable the filter.
            min_volume_8h_change_percent: inclusive minimum percent change of USD volume between the current and previous 8h windows; `None` to disable the filter.
            min_volume_24h_change_percent: inclusive minimum percent change of USD volume between the current and previous 24h windows; `None` to disable the filter.
            min_volume_7d_change_percent: inclusive minimum percent change of USD volume between the current and previous 7d windows; `None` to disable the filter.
            min_volume_30d_change_percent: inclusive minimum percent change of USD volume between the current and previous 30d windows; `None` to disable the filter.
            min_price_change_1m_percent: inclusive minimum percent price change vs the start of the trailing 1m window; `None` to disable the filter.
            min_price_change_5m_percent: inclusive minimum percent price change vs the start of the trailing 5m window; `None` to disable the filter.
            min_price_change_30m_percent: inclusive minimum percent price change vs the start of the trailing 30m window; `None` to disable the filter.
            min_price_change_1h_percent: inclusive minimum percent price change vs the start of the trailing 1h window; `None` to disable the filter.
            min_price_change_2h_percent: inclusive minimum percent price change vs the start of the trailing 2h window; `None` to disable the filter.
            min_price_change_4h_percent: inclusive minimum percent price change vs the start of the trailing 4h window; `None` to disable the filter.
            min_price_change_8h_percent: inclusive minimum percent price change vs the start of the trailing 8h window; `None` to disable the filter.
            min_price_change_24h_percent: inclusive minimum percent price change vs the start of the trailing 24h window; `None` to disable the filter.
            min_price_change_7d_percent: inclusive minimum percent price change vs the start of the trailing 7d window; `None` to disable the filter.
            min_price_change_30d_percent: inclusive minimum percent price change vs the start of the trailing 30d window; `None` to disable the filter.
            min_trade_1m_count: inclusive minimum number of trades during the trailing 1m window; `None` to disable the filter.
            min_trade_5m_count: inclusive minimum number of trades during the trailing 5m window; `None` to disable the filter.
            min_trade_30m_count: inclusive minimum number of trades during the trailing 30m window; `None` to disable the filter.
            min_trade_1h_count: inclusive minimum number of trades during the trailing 1h window; `None` to disable the filter.
            min_trade_2h_count: inclusive minimum number of trades during the trailing 2h window; `None` to disable the filter.
            min_trade_4h_count: inclusive minimum number of trades during the trailing 4h window; `None` to disable the filter.
            min_trade_8h_count: inclusive minimum number of trades during the trailing 8h window; `None` to disable the filter.
            min_trade_24h_count: inclusive minimum number of trades during the trailing 24h window; `None` to disable the filter.
            min_trade_7d_count: inclusive minimum number of trades during the trailing 7d window; `None` to disable the filter.
            min_trade_30d_count: inclusive minimum number of trades during the trailing 30d window; `None` to disable the filter.
    """
    sort_by: str = BirdeyeV3TokenListSortBy.LIQUIDITY.value
    sort_type: str = BirdeyeOrder.DESCENDING.value
    offset: int = 0
    limit: int = 100
    min_liquidity: float | None = None
    max_liquidity: float | None = None
    min_market_cap: float | None = None
    max_market_cap: float | None = None
    min_fdv: float | None = None
    max_fdv: float | None = None
    min_recent_listing_time: int | None = None
    max_recent_listing_time: int | None = None
    min_last_trade_unix_time: int | None = None
    max_last_trade_unix_time: int | None = None
    min_holder: int | None = None
    ui_amount_mode: str | None = None
    min_volume_1m_usd: float | None = None
    min_volume_5m_usd: float | None = None
    min_volume_30m_usd: float | None = None
    min_volume_1h_usd: float | None = None
    min_volume_2h_usd: float | None = None
    min_volume_4h_usd: float | None = None
    min_volume_8h_usd: float | None = None
    min_volume_24h_usd: float | None = None
    min_volume_7d_usd: float | None = None
    min_volume_30d_usd: float | None = None
    min_volume_1m_change_percent: float | None = None
    min_volume_5m_change_percent: float | None = None
    min_volume_30m_change_percent: float | None = None
    min_volume_1h_change_percent: float | None = None
    min_volume_2h_change_percent: float | None = None
    min_volume_4h_change_percent: float | None = None
    min_volume_8h_change_percent: float | None = None
    min_volume_24h_change_percent: float | None = None
    min_volume_7d_change_percent: float | None = None
    min_volume_30d_change_percent: float | None = None
    min_price_change_1m_percent: float | None = None
    min_price_change_5m_percent: float | None = None
    min_price_change_30m_percent: float | None = None
    min_price_change_1h_percent: float | None = None
    min_price_change_2h_percent: float | None = None
    min_price_change_4h_percent: float | None = None
    min_price_change_8h_percent: float | None = None
    min_price_change_24h_percent: float | None = None
    min_price_change_7d_percent: float | None = None
    min_price_change_30d_percent: float | None = None
    min_trade_1m_count: int | None = None
    min_trade_5m_count: int | None = None
    min_trade_30m_count: int | None = None
    min_trade_1h_count: int | None = None
    min_trade_2h_count: int | None = None
    min_trade_4h_count: int | None = None
    min_trade_8h_count: int | None = None
    min_trade_24h_count: int | None = None
    min_trade_7d_count: int | None = None
    min_trade_30d_count: int | None = None

# classes used on GET "Token - List (V3) Scroll" endpoint
class GetV3TokenListScrollData(BaseModel):
    """
        Payload of the v3 Token - List Scroll response.

        The scroll endpoint pages results via a server-issued opaque cursor instead of an
        offset. Pass the returned `next_scroll_id` back as the `scroll_id` query parameter
        on the next call to continue the same scroll session.

        Attributes:
            items: list of token entries returned in this batch.
            next_scroll_id: opaque cursor to fetch the next batch; `None` (or missing) when no
                additional batches are available.
            scroll_time: server-side scroll session expiration timestamp; `None` (or missing) when
                not provided by the API.
            has_next: convenience flag indicating whether at least one more batch is available
                (aliased to `hasNext`); `None` when the API does not include the flag.
    """
    items: list[V3TokenListItem]
    next_scroll_id: str | None = None
    scroll_time: str | None = None
    has_next: bool | None = Field(alias = "hasNext", default = None)

class GetV3TokenListScrollResponse(BaseModel):
    """
        Model used to represent the **Token - List (V3) Scroll** endpoint from birdeye API.

        Attributes:
            data: scroll payload (current batch + cursor metadata).
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenListScrollData
    success: bool

class GetV3TokenListScrollQuery(BaseModel):
    """
        Query-parameter bag for the v3 Token - List Scroll endpoint.

        Pagination is cursor-based: leave `scroll_id` `None` for the first call (then any
        other filter is honoured), and pass back the `next_scroll_id` value from the previous
        response on subsequent calls (filters are ignored once `scroll_id` is set).

        Attributes:
            scroll_id: cursor returned by a previous scroll response (`next_scroll_id`). When set, all other filters are ignored and Birdeye returns the next page of the original scroll session; `None` to start a fresh scroll. Birdeye limits a given API key to one active scroll per 30 seconds.
            sort_by: metric used to rank the returned tokens. Pick one of the constants on [`BirdeyeV3TokenListSortBy`][cyhole.birdeye.param.BirdeyeV3TokenListSortBy].
            sort_type: ascending or descending order. Pick one of the constants on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
            limit: number of records to return per batch (1..5000).
            min_liquidity: inclusive lower bound on token liquidity in USD; `None` to disable the filter.
            max_liquidity: inclusive upper bound on token liquidity in USD; `None` to disable the filter.
            min_market_cap: inclusive lower bound on market cap in USD; `None` to disable the filter.
            max_market_cap: inclusive upper bound on market cap in USD; `None` to disable the filter.
            min_fdv: inclusive lower bound on FDV in USD; `None` to disable the filter.
            max_fdv: inclusive upper bound on FDV in USD; `None` to disable the filter.
            min_recent_listing_time: inclusive lower bound (unix seconds) on the token recent-listing timestamp; `None` to disable the filter.
            max_recent_listing_time: inclusive upper bound (unix seconds) on the token recent-listing timestamp; `None` to disable the filter.
            min_last_trade_unix_time: inclusive lower bound (unix seconds) on the last-trade timestamp; `None` to disable the filter.
            max_last_trade_unix_time: inclusive upper bound (unix seconds) on the last-trade timestamp; `None` to disable the filter.
            min_holder: inclusive minimum number of distinct token holders; `None` to disable the filter.
            ui_amount_mode: how to format scaled-UI-amount token figures on Solana; pick a [`BirdeyeUIAmountMode`][cyhole.birdeye.param.BirdeyeUIAmountMode] member or leave `None` for the server default (`scaled`).
            min_volume_1m_usd: inclusive minimum USD volume in the trailing 1m window; `None` to disable the filter.
            min_volume_5m_usd: inclusive minimum USD volume in the trailing 5m window; `None` to disable the filter.
            min_volume_30m_usd: inclusive minimum USD volume in the trailing 30m window; `None` to disable the filter.
            min_volume_1h_usd: inclusive minimum USD volume in the trailing 1h window; `None` to disable the filter.
            min_volume_2h_usd: inclusive minimum USD volume in the trailing 2h window; `None` to disable the filter.
            min_volume_4h_usd: inclusive minimum USD volume in the trailing 4h window; `None` to disable the filter.
            min_volume_8h_usd: inclusive minimum USD volume in the trailing 8h window; `None` to disable the filter.
            min_volume_24h_usd: inclusive minimum USD volume in the trailing 24h window; `None` to disable the filter.
            min_volume_7d_usd: inclusive minimum USD volume in the trailing 7d window; `None` to disable the filter.
            min_volume_30d_usd: inclusive minimum USD volume in the trailing 30d window; `None` to disable the filter.
            min_volume_1m_change_percent: inclusive minimum percent change of USD volume between the current and previous 1m windows; `None` to disable the filter.
            min_volume_5m_change_percent: inclusive minimum percent change of USD volume between the current and previous 5m windows; `None` to disable the filter.
            min_volume_30m_change_percent: inclusive minimum percent change of USD volume between the current and previous 30m windows; `None` to disable the filter.
            min_volume_1h_change_percent: inclusive minimum percent change of USD volume between the current and previous 1h windows; `None` to disable the filter.
            min_volume_2h_change_percent: inclusive minimum percent change of USD volume between the current and previous 2h windows; `None` to disable the filter.
            min_volume_4h_change_percent: inclusive minimum percent change of USD volume between the current and previous 4h windows; `None` to disable the filter.
            min_volume_8h_change_percent: inclusive minimum percent change of USD volume between the current and previous 8h windows; `None` to disable the filter.
            min_volume_24h_change_percent: inclusive minimum percent change of USD volume between the current and previous 24h windows; `None` to disable the filter.
            min_volume_7d_change_percent: inclusive minimum percent change of USD volume between the current and previous 7d windows; `None` to disable the filter.
            min_volume_30d_change_percent: inclusive minimum percent change of USD volume between the current and previous 30d windows; `None` to disable the filter.
            min_price_change_1m_percent: inclusive minimum percent price change vs the start of the trailing 1m window; `None` to disable the filter.
            min_price_change_5m_percent: inclusive minimum percent price change vs the start of the trailing 5m window; `None` to disable the filter.
            min_price_change_30m_percent: inclusive minimum percent price change vs the start of the trailing 30m window; `None` to disable the filter.
            min_price_change_1h_percent: inclusive minimum percent price change vs the start of the trailing 1h window; `None` to disable the filter.
            min_price_change_2h_percent: inclusive minimum percent price change vs the start of the trailing 2h window; `None` to disable the filter.
            min_price_change_4h_percent: inclusive minimum percent price change vs the start of the trailing 4h window; `None` to disable the filter.
            min_price_change_8h_percent: inclusive minimum percent price change vs the start of the trailing 8h window; `None` to disable the filter.
            min_price_change_24h_percent: inclusive minimum percent price change vs the start of the trailing 24h window; `None` to disable the filter.
            min_price_change_7d_percent: inclusive minimum percent price change vs the start of the trailing 7d window; `None` to disable the filter.
            min_price_change_30d_percent: inclusive minimum percent price change vs the start of the trailing 30d window; `None` to disable the filter.
            min_trade_1m_count: inclusive minimum number of trades during the trailing 1m window; `None` to disable the filter.
            min_trade_5m_count: inclusive minimum number of trades during the trailing 5m window; `None` to disable the filter.
            min_trade_30m_count: inclusive minimum number of trades during the trailing 30m window; `None` to disable the filter.
            min_trade_1h_count: inclusive minimum number of trades during the trailing 1h window; `None` to disable the filter.
            min_trade_2h_count: inclusive minimum number of trades during the trailing 2h window; `None` to disable the filter.
            min_trade_4h_count: inclusive minimum number of trades during the trailing 4h window; `None` to disable the filter.
            min_trade_8h_count: inclusive minimum number of trades during the trailing 8h window; `None` to disable the filter.
            min_trade_24h_count: inclusive minimum number of trades during the trailing 24h window; `None` to disable the filter.
            min_trade_7d_count: inclusive minimum number of trades during the trailing 7d window; `None` to disable the filter.
            min_trade_30d_count: inclusive minimum number of trades during the trailing 30d window; `None` to disable the filter.
    """
    scroll_id: str | None = None
    sort_by: str = BirdeyeV3TokenListSortBy.LIQUIDITY.value
    sort_type: str = BirdeyeOrder.DESCENDING.value
    limit: int = 5000
    min_liquidity: float | None = None
    max_liquidity: float | None = None
    min_market_cap: float | None = None
    max_market_cap: float | None = None
    min_fdv: float | None = None
    max_fdv: float | None = None
    min_recent_listing_time: int | None = None
    max_recent_listing_time: int | None = None
    min_last_trade_unix_time: int | None = None
    max_last_trade_unix_time: int | None = None
    min_holder: int | None = None
    ui_amount_mode: str | None = None
    min_volume_1m_usd: float | None = None
    min_volume_5m_usd: float | None = None
    min_volume_30m_usd: float | None = None
    min_volume_1h_usd: float | None = None
    min_volume_2h_usd: float | None = None
    min_volume_4h_usd: float | None = None
    min_volume_8h_usd: float | None = None
    min_volume_24h_usd: float | None = None
    min_volume_7d_usd: float | None = None
    min_volume_30d_usd: float | None = None
    min_volume_1m_change_percent: float | None = None
    min_volume_5m_change_percent: float | None = None
    min_volume_30m_change_percent: float | None = None
    min_volume_1h_change_percent: float | None = None
    min_volume_2h_change_percent: float | None = None
    min_volume_4h_change_percent: float | None = None
    min_volume_8h_change_percent: float | None = None
    min_volume_24h_change_percent: float | None = None
    min_volume_7d_change_percent: float | None = None
    min_volume_30d_change_percent: float | None = None
    min_price_change_1m_percent: float | None = None
    min_price_change_5m_percent: float | None = None
    min_price_change_30m_percent: float | None = None
    min_price_change_1h_percent: float | None = None
    min_price_change_2h_percent: float | None = None
    min_price_change_4h_percent: float | None = None
    min_price_change_8h_percent: float | None = None
    min_price_change_24h_percent: float | None = None
    min_price_change_7d_percent: float | None = None
    min_price_change_30d_percent: float | None = None
    min_trade_1m_count: int | None = None
    min_trade_5m_count: int | None = None
    min_trade_30m_count: int | None = None
    min_trade_1h_count: int | None = None
    min_trade_2h_count: int | None = None
    min_trade_4h_count: int | None = None
    min_trade_8h_count: int | None = None
    min_trade_24h_count: int | None = None
    min_trade_7d_count: int | None = None
    min_trade_30d_count: int | None = None

# classes used on GET "Token - New Listing" endpoint
class GetV2TokensNewListingItem(BaseModel):
    """
        Single newly-listed token entry returned by the v2 Token - New Listing endpoint.

        Attributes:
            address: contract address of the freshly listed token on the selected chain.
            symbol: ticker symbol of the token.
            name: human-readable name of the token.
            decimals: number of decimal places used by the token.
            source: name of the venue (DEX/aggregator) Birdeye picked up the listing from.
            liquidity_added_at: ISO-8601 timestamp of the listing event (alias `liquidityAddedAt`).
            logo_uri: URL of the token logo (alias `logoURI`); `None` if Birdeye has no logo for the token.
            liquidity: total liquidity of the token at listing time, expressed in USD.
    """
    address: str
    symbol: str
    name: str
    decimals: int
    source: str
    liquidity_added_at: str = Field(alias = "liquidityAddedAt")
    logo_uri: str | None = Field(alias = "logoURI", default = None)
    liquidity: float

class GetV2TokensNewListingData(BaseModel):
    """
        Payload of the v2 Token - New Listing response.

        Attributes:
            items: list of newly-listed tokens, ordered most-recent-first.
    """
    items: list[GetV2TokensNewListingItem]

class GetV2TokensNewListingResponse(BaseModel):
    """
        Model used to represent the **Token - New Listing** endpoint from birdeye API.

        Attributes:
            data: payload containing the list of newly-listed tokens.
            success: `True` when the API call completed without errors.
    """
    data: GetV2TokensNewListingData
    success: bool


# classes used on GET "Token - All Market List" endpoint
class GetV2MarketsTokenSide(BaseModel):
    """
        Identity of one side (base or quote) of a market returned by the v2 Token - All Market List endpoint.

        Attributes:
            address: contract address of the token making up this side of the market.
            decimals: number of decimal places used by the token.
            symbol: ticker symbol of the token; `None` if Birdeye does not know it.
            icon: URL of the token logo; `None` if Birdeye does not have a logo for the token.
    """
    address: str
    decimals: int
    symbol: str | None = None
    icon: str | None = None

class GetV2MarketsItem(BaseModel):
    """
        Single market (trading pair) entry returned by the v2 Token - All Market List endpoint.

        Attributes:
            address: on-chain address of the market/pool.
            base: identity of the base side of the market.
            quote: identity of the quote side of the market.
            created_at: ISO-8601 timestamp at which Birdeye first observed the market (alias `createdAt`).
            liquidity: total liquidity of the market in USD.
            name: human-readable market name (e.g. `JitoSOL-SOL`).
            price: current price of the market quoted in USD; `None` when Birdeye cannot compute it.
            source: name of the venue (DEX/aggregator) that hosts the market.
            trade_24h: total number of trades on the market during the trailing 24h window (alias `trade24h`).
            trade_24h_change_percent: percent change of the 24h trade count vs the previous 24h window (alias `trade24hChangePercent`).
            unique_wallet_24h: number of unique wallets that traded the market in the trailing 24h window (alias `uniqueWallet24h`).
            unique_wallet_24h_change_percent: percent change of unique wallets vs the previous 24h window (alias `uniqueWallet24hChangePercent`).
            volume_24h: traded volume during the trailing 24h window expressed in USD (alias `volume24h`).
    """
    address: str
    base: GetV2MarketsTokenSide
    quote: GetV2MarketsTokenSide
    created_at: str = Field(alias = "createdAt")
    liquidity: float
    name: str
    price: float | None = None
    source: str
    trade_24h: int = Field(alias = "trade24h")
    trade_24h_change_percent: float = Field(alias = "trade24hChangePercent")
    unique_wallet_24h: int = Field(alias = "uniqueWallet24h")
    unique_wallet_24h_change_percent: float = Field(alias = "uniqueWallet24hChangePercent")
    volume_24h: float = Field(alias = "volume24h")

class GetV2MarketsData(BaseModel):
    """
        Payload of the v2 Token - All Market List response.

        Attributes:
            total: total number of markets known to Birdeye for the requested token.
            items: paginated list of markets matching the request, ranked per `sort_by` / `sort_type`.
    """
    total: int
    items: list[GetV2MarketsItem]

class GetV2MarketsResponse(BaseModel):
    """
        Model used to represent the **Token - All Market List** endpoint from birdeye API.

        Attributes:
            data: paginated list of markets for the requested token.
            success: `True` when the API call completed without errors.
    """
    data: GetV2MarketsData
    success: bool


# classes used on GET "Token - Top Traders" endpoint
class GetV2TopTradersItem(BaseModel):
    """
        Single trader entry returned by the v2 Token - Top Traders endpoint.

        Numeric fields with `pnl` in their name and `volume_usd` are only meaningful on the Solana
        chain — on other chains Birdeye returns them but they may be `0` or unreliable.

        Attributes:
            token_address: contract address of the token the trader has been ranked for
                (alias `tokenAddress`).
            owner: on-chain wallet address of the trader.
            type: time frame the metrics in this entry refer to (mirrors the request `time_frame`).
            tags: list of optional Birdeye tags attached to the wallet (e.g. `whale`, `bot`); empty
                when no tags are assigned.
            trade: total number of trades the wallet executed on the token within the time frame.
            trade_buy: number of buy trades within the time frame (alias `tradeBuy`).
            trade_sell: number of sell trades within the time frame (alias `tradeSell`).
            volume: total traded volume in the token's UI units.
            volume_buy: buy-side traded volume in the token's UI units (alias `volumeBuy`).
            volume_sell: sell-side traded volume in the token's UI units (alias `volumeSell`).
            volume_usd: total traded volume expressed in USD (alias `volumeUsd`).
            volume_buy_usd: buy-side traded volume expressed in USD (alias `volumeBuyUSD`).
            volume_sell_usd: sell-side traded volume expressed in USD (alias `volumeSellUSD`).
            total_pnl: total profit-and-loss of the wallet on the token over the time frame, in USD
                (alias `totalPnl`); Solana-only, may be `0` on other chains.
            realized_pnl: realised profit-and-loss in USD (alias `realizedPnl`); Solana-only.
            unrealized_pnl: unrealised profit-and-loss in USD (alias `unrealizedPnl`); Solana-only.
            is_scaled_ui_token: `True` when the underlying token is a scaled-UI-amount SPL token
                (Solana only) (alias `isScaledUiToken`); `None` outside Solana or undetermined.
            multiplier: scaling multiplier applied to UI amounts for scaled-UI-amount tokens; `None`
                when not applicable.
    """
    token_address: str = Field(alias = "tokenAddress")
    owner: str
    type: str
    tags: list[str] = []
    trade: int
    trade_buy: int = Field(alias = "tradeBuy")
    trade_sell: int = Field(alias = "tradeSell")
    volume: float
    volume_buy: float = Field(alias = "volumeBuy")
    volume_sell: float = Field(alias = "volumeSell")
    volume_usd: float = Field(alias = "volumeUsd")
    volume_buy_usd: float = Field(alias = "volumeBuyUSD")
    volume_sell_usd: float = Field(alias = "volumeSellUSD")
    total_pnl: float = Field(alias = "totalPnl")
    realized_pnl: float = Field(alias = "realizedPnl")
    unrealized_pnl: float = Field(alias = "unrealizedPnl")
    is_scaled_ui_token: bool | None = Field(alias = "isScaledUiToken", default = None)
    multiplier: float | None = None

class GetV2TopTradersData(BaseModel):
    """
        Payload of the v2 Token - Top Traders response.

        Attributes:
            items: ranked list of trader entries matching the request.
    """
    items: list[GetV2TopTradersItem]

class GetV2TopTradersResponse(BaseModel):
    """
        Model used to represent the **Token - Top Traders** endpoint from birdeye API.

        Attributes:
            data: payload containing the ranked trader list.
            success: `True` when the API call completed without errors.
    """
    data: GetV2TopTradersData
    success: bool
