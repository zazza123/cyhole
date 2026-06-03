from pydantic import BaseModel

from ...birdeye.param import BirdeyeOrder, BirdeyeV3MemeListSortBy, BirdeyeV3MemeSource

# classes used on GET "Meme Token Detail - Single" endpoint
class GetV3TokenMemeDetailSingleTxRef(BaseModel):
    """
        Reference to a blockchain transaction associated with a meme token lifecycle event
        (creation, last update, or graduation). All fields are `None` when the event has
        not yet occurred.

        Attributes:
            tx_hash: base-58 transaction signature; `None` when the event has not occurred.
            slot: Solana slot number in which the transaction was confirmed; `None` when not
                yet confirmed or not applicable.
            block_time: unix timestamp (seconds) of the block that included the transaction;
                `None` when not available.
    """
    tx_hash: str | None = None
    slot: int | None = None
    block_time: int | None = None

class GetV3TokenMemeDetailSinglePool(BaseModel):
    """
        On-chain pool (bonding curve) state for a meme token at the time of the API call.
        Reserve values are returned as decimal strings because they are large integers that
        cannot be represented exactly as JSON numbers.

        Attributes:
            address: contract address of the bonding-curve pool.
            real_sol_reserves: actual SOL reserves held in the pool, in lamports (as string).
            real_token_reserves: actual token reserves held in the pool, in the token's
                raw (non-UI) units (as string).
            token_total_supply: total token supply tracked by the pool, in raw units (as string).
            virtual_token_reserves: virtual token reserves used by the bonding-curve pricing
                formula, in raw units (as string).
    """
    address: str
    real_sol_reserves: str
    real_token_reserves: str
    token_total_supply: str
    virtual_token_reserves: str

class GetV3TokenMemeDetailSingleMemeInfo(BaseModel):
    """
        Meme-platform-specific metadata for a token, covering its origin, lifecycle events,
        current bonding-curve state, and graduation status.

        Attributes:
            source: meme launchpad that originated the token (e.g. ``"pump_dot_fun"``);
                `None` if not determined.
            platform_id: contract address of the launchpad program on the chain; `None` if
                not available.
            created_at: transaction reference for the token creation event; `None` if not
                available.
            creation_time: unix timestamp (seconds) of the token creation; `None` if not
                available.
            creator: wallet address that deployed the token; `None` if not available.
            updated_at: transaction reference for the most recent on-chain update; `None` if
                not available.
            graduated_at: transaction reference for the graduation event (migration from the
                bonding curve to a DEX pool); all fields are `None` while the token has not
                yet graduated.
            graduated: `True` once the token has graduated to a DEX pool.
            graduated_time: unix timestamp (seconds) of the graduation event; `None` before
                graduation.
            pool: current bonding-curve pool state; `None` if pool data is unavailable.
            progress_percent: percentage of the bonding-curve funding target that has been
                reached (0–100); `None` if not available.
            address: contract address of the meme token (mirrors the top-level
                ``data.address`` field); `None` if not available.
    """
    source: str | None = None
    platform_id: str | None = None
    created_at: GetV3TokenMemeDetailSingleTxRef | None = None
    creation_time: int | None = None
    creator: str | None = None
    updated_at: GetV3TokenMemeDetailSingleTxRef | None = None
    graduated_at: GetV3TokenMemeDetailSingleTxRef | None = None
    graduated: bool | None = None
    graduated_time: int | None = None
    pool: GetV3TokenMemeDetailSinglePool | None = None
    progress_percent: float | None = None
    address: str | None = None

class GetV3TokenMemeDetailSingleData(BaseModel):
    """
        Full detail payload for a single meme token as returned by the Birdeye v3
        Meme Token Detail endpoint.

        Attributes:
            address: contract address of the meme token on the selected chain.
            name: human-readable name of the token; `None` if not available.
            symbol: ticker symbol of the token; `None` if not available.
            decimals: number of decimal places used by the token; `None` if not available.
            extensions: free-form metadata bag containing optional social and descriptive
                fields (e.g. ``twitter``, ``website``, ``description``); individual values
                may be `None`, and the whole dict is `None` when Birdeye has no metadata.
            logo_uri: URL of the token logo image; `None` if not available.
            price: latest known price of the token in USD; `None` if not available.
            liquidity: current on-chain liquidity of the token in USD; `None` if not
                available.
            circulating_supply: circulating token supply in UI units; `None` if not
                available.
            market_cap: market capitalisation in USD; `None` if not available.
            total_supply: total token supply in UI units; `None` if not available.
            fdv: fully-diluted valuation in USD; `None` if not available.
            meme_info: meme-platform-specific metadata including launchpad origin,
                bonding-curve pool state, and graduation status; `None` if not available.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    extensions: dict[str, str | None] | None = None
    logo_uri: str | None = None
    price: float | None = None
    liquidity: float | None = None
    circulating_supply: float | None = None
    market_cap: float | None = None
    total_supply: float | None = None
    fdv: float | None = None
    meme_info: GetV3TokenMemeDetailSingleMemeInfo | None = None

class GetV3TokenMemeDetailSingleResponse(BaseModel):
    """
        Model used to represent the **Meme Token Detail - Single** endpoint from the
        Birdeye v3 API.

        Attributes:
            data: full detail payload for the requested meme token.
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenMemeDetailSingleData
    success: bool

# classes used on GET "Meme Token - List" endpoint

class GetV3TokenMemeListQuery(BaseModel):
    """
        Query parameters for the Birdeye v3 **Meme Token - List** endpoint.

        All filter fields are optional; unset fields are excluded from the request.
        `sort_by` and `sort_type` default to ``progress_percent`` descending.

        Attributes:
            sort_by: metric to sort the result set by; defaults to
                ``BirdeyeV3MemeListSortBy.PROGRESS_PERCENT``.
            sort_type: sort direction; defaults to ``BirdeyeOrder.DESCENDING``.
            source: restrict results to a specific launchpad; defaults to
                ``BirdeyeV3MemeSource.ALL`` (all platforms).
            creator: filter by token creator wallet address.
            platform_id: filter by launchpad program address on the chain.
            graduated: when `True` return only graduated tokens; when `False`
                return only non-graduated tokens; `None` returns all.
            min_progress_percent: lower bound on bonding-curve progress (0–100).
            max_progress_percent: upper bound on bonding-curve progress (0–100).
            min_graduated_time: lower bound on graduation unix timestamp.
            max_graduated_time: upper bound on graduation unix timestamp.
            min_creation_time: lower bound on token creation unix timestamp.
            max_creation_time: upper bound on token creation unix timestamp.
            min_liquidity: lower bound on current liquidity (USD).
            max_liquidity: upper bound on current liquidity (USD).
            min_market_cap: lower bound on market cap (USD).
            max_market_cap: upper bound on market cap (USD).
            min_fdv: lower bound on fully-diluted valuation (USD).
            max_fdv: upper bound on fully-diluted valuation (USD).
            min_recent_listing_time: lower bound on the Birdeye listing unix timestamp.
            max_recent_listing_time: upper bound on the Birdeye listing unix timestamp.
            min_last_trade_unix_time: lower bound on the last trade unix timestamp.
            max_last_trade_unix_time: upper bound on the last trade unix timestamp.
            min_holder: minimum number of distinct token holders.
            min_volume_1m_usd: minimum USD volume over the trailing 1 minute window.
            min_volume_5m_usd: minimum USD volume over the trailing 5 minute window.
            min_volume_30m_usd: minimum USD volume over the trailing 30 minute window.
            min_volume_1h_usd: minimum USD volume over the trailing 1 hour window.
            min_volume_2h_usd: minimum USD volume over the trailing 2 hour window.
            min_volume_4h_usd: minimum USD volume over the trailing 4 hour window.
            min_volume_8h_usd: minimum USD volume over the trailing 8 hour window.
            min_volume_24h_usd: minimum USD volume over the trailing 24 hour window.
            min_volume_7d_usd: minimum USD volume over the trailing 7 day window.
            min_volume_30d_usd: minimum USD volume over the trailing 30 day window.
            min_volume_1m_change_percent: minimum 1 minute volume change percentage.
            min_volume_5m_change_percent: minimum 5 minute volume change percentage.
            min_volume_30m_change_percent: minimum 30 minute volume change percentage.
            min_volume_1h_change_percent: minimum 1 hour volume change percentage.
            min_volume_2h_change_percent: minimum 2 hour volume change percentage.
            min_volume_4h_change_percent: minimum 4 hour volume change percentage.
            min_volume_8h_change_percent: minimum 8 hour volume change percentage.
            min_volume_24h_change_percent: minimum 24 hour volume change percentage.
            min_volume_7d_change_percent: minimum 7 day volume change percentage.
            min_volume_30d_change_percent: minimum 30 day volume change percentage.
            min_price_change_1m_percent: minimum 1 minute price change percentage.
            min_price_change_5m_percent: minimum 5 minute price change percentage.
            min_price_change_30m_percent: minimum 30 minute price change percentage.
            min_price_change_1h_percent: minimum 1 hour price change percentage.
            min_price_change_2h_percent: minimum 2 hour price change percentage.
            min_price_change_4h_percent: minimum 4 hour price change percentage.
            min_price_change_8h_percent: minimum 8 hour price change percentage.
            min_price_change_24h_percent: minimum 24 hour price change percentage.
            min_price_change_7d_percent: minimum 7 day price change percentage.
            min_price_change_30d_percent: minimum 30 day price change percentage.
            min_trade_1m_count: minimum number of trades in the trailing 1 minute window.
            min_trade_5m_count: minimum number of trades in the trailing 5 minute window.
            min_trade_30m_count: minimum number of trades in the trailing 30 minute window.
            min_trade_1h_count: minimum number of trades in the trailing 1 hour window.
            min_trade_2h_count: minimum number of trades in the trailing 2 hour window.
            min_trade_4h_count: minimum number of trades in the trailing 4 hour window.
            min_trade_8h_count: minimum number of trades in the trailing 8 hour window.
            min_trade_24h_count: minimum number of trades in the trailing 24 hour window.
            min_trade_7d_count: minimum number of trades in the trailing 7 day window.
            min_trade_30d_count: minimum number of trades in the trailing 30 day window.
            offset: number of items to skip for pagination; defaults to 0 (max 10000).
            limit: maximum number of items to return; defaults to 100 (max 100).
    """
    sort_by: str = BirdeyeV3MemeListSortBy.PROGRESS_PERCENT.value
    sort_type: str = BirdeyeOrder.DESCENDING.value
    source: str | None = BirdeyeV3MemeSource.ALL.value
    creator: str | None = None
    platform_id: str | None = None
    graduated: bool | None = None
    min_progress_percent: float | None = None
    max_progress_percent: float | None = None
    min_graduated_time: int | None = None
    max_graduated_time: int | None = None
    min_creation_time: int | None = None
    max_creation_time: int | None = None
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
    offset: int | None = None
    limit: int | None = None

class GetV3TokenMemeListMemeInfo(BaseModel):
    """
        Meme-platform-specific metadata embedded in each item of the Meme Token - List response.
        Covers the token's origin platform, creator, bonding-curve state, and graduation status.

        Attributes:
            created_at: transaction reference for the token creation event; `None` if not
                available.
            creator: wallet address that deployed the token; `None` if not available.
            address: contract address of the meme token; `None` if not available.
            creation_time: unix timestamp (seconds) of the token creation; `None` if not
                available.
            graduated: `True` once the token has graduated to a DEX pool; `None` if not
                available.
            pool: current bonding-curve pool state; `None` if pool data is unavailable.
            progress_percent: percentage of the bonding-curve funding target that has been
                reached (0–100); `None` if not available.
            source: meme launchpad that originated the token (e.g. ``"pump_dot_fun"``);
                `None` if not determined.
            platform_id: contract address of the launchpad program on the chain; `None` if
                not available.
            graduated_time: unix timestamp (seconds) of the graduation event; `None` before
                graduation.
    """
    created_at: GetV3TokenMemeDetailSingleTxRef | None = None
    creator: str | None = None
    address: str | None = None
    creation_time: int | None = None
    graduated: bool | None = None
    pool: GetV3TokenMemeDetailSinglePool | None = None
    progress_percent: float | None = None
    source: str | None = None
    platform_id: str | None = None
    graduated_time: int | None = None

class GetV3TokenMemeListItem(BaseModel):
    """
        A single meme token record returned in the Birdeye v3 Meme Token - List response.

        Each item combines standard token identity and market metrics with meme-platform-
        specific data (bonding-curve progress, graduation status, creator) nested under
        ``meme_info``.

        Attributes:
            address: on-chain contract address of the meme token.
            logo_uri: URL of the token logo image; `None` if not available.
            name: human-readable name of the token; `None` if not available.
            symbol: ticker symbol; `None` if not available.
            decimals: number of decimal places; `None` if not available.
            extensions: free-form metadata bag (social links, description); individual values
                may be `None`, and the whole dict is `None` when Birdeye has no metadata.
            market_cap: market capitalisation in USD; `None` if not available.
            fdv: fully-diluted valuation in USD; `None` if not available.
            total_supply: total token supply in UI units; `None` if not available.
            circulating_supply: circulating supply in UI units; `None` if not available.
            liquidity: current on-chain liquidity in USD; `None` if not available.
            last_trade_unix_time: unix timestamp (seconds) of the most recent trade;
                `None` if not available.
            volume_1m_usd: USD traded volume over the trailing 1 minute; `None` if not available.
            volume_5m_usd: USD traded volume over the trailing 5 minutes; `None` if not available.
            volume_30m_usd: USD traded volume over the trailing 30 minutes; `None` if not available.
            volume_1m_change_percent: volume percent change vs previous 1 minute window;
                `None` if not available.
            volume_5m_change_percent: volume percent change vs previous 5 minute window;
                `None` if not available.
            volume_30m_change_percent: volume percent change vs previous 30 minute window;
                `None` if not available.
            volume_1h_usd: USD traded volume over the trailing 1 hour; `None` if not available.
            volume_1h_change_percent: volume percent change vs previous 1 hour window;
                `None` if not available.
            volume_2h_usd: USD traded volume over the trailing 2 hours; `None` if not available.
            volume_2h_change_percent: volume percent change vs previous 2 hour window;
                `None` if not available.
            volume_4h_usd: USD traded volume over the trailing 4 hours; `None` if not available.
            volume_4h_change_percent: volume percent change vs previous 4 hour window;
                `None` if not available.
            volume_8h_usd: USD traded volume over the trailing 8 hours; `None` if not available.
            volume_8h_change_percent: volume percent change vs previous 8 hour window;
                `None` if not available.
            volume_24h_usd: USD traded volume over the trailing 24 hours; `None` if not available.
            volume_24h_change_percent: volume percent change vs previous 24 hour window;
                `None` if not available.
            volume_7d_usd: USD traded volume over the trailing 7 days; `None` if not available.
            volume_7d_change_percent: volume percent change vs previous 7 day window;
                `None` if not available.
            volume_30d_usd: USD traded volume over the trailing 30 days; `None` if not available.
            volume_30d_change_percent: volume percent change vs previous 30 day window;
                `None` if not available.
            trade_1m_count: number of trades in the trailing 1 minute window; `None` if not available.
            trade_5m_count: number of trades in the trailing 5 minute window; `None` if not available.
            trade_30m_count: number of trades in the trailing 30 minute window; `None` if not available.
            trade_1h_count: number of trades in the trailing 1 hour window; `None` if not available.
            trade_2h_count: number of trades in the trailing 2 hour window; `None` if not available.
            trade_4h_count: number of trades in the trailing 4 hour window; `None` if not available.
            trade_8h_count: number of trades in the trailing 8 hour window; `None` if not available.
            trade_24h_count: number of trades in the trailing 24 hour window; `None` if not available.
            trade_7d_count: number of trades in the trailing 7 day window; `None` if not available.
            trade_30d_count: number of trades in the trailing 30 day window; `None` if not available.
            buy_24h: number of buy transactions in the trailing 24 hours; `None` if not available.
            buy_24h_change_percent: buy count percent change vs previous 24h window;
                `None` if not available.
            volume_buy_24h_usd: USD volume of buy transactions in the trailing 24 hours;
                `None` if not available.
            volume_buy_24h_change_percent: buy volume percent change vs previous 24h window;
                `None` if not available.
            buy_7d: number of buy transactions in the trailing 7 days; `None` if not available.
            buy_7d_change_percent: buy count percent change vs previous 7d window;
                `None` if not available.
            volume_buy_7d_usd: USD volume of buy transactions in the trailing 7 days;
                `None` if not available.
            volume_buy_7d_change_percent: buy volume percent change vs previous 7d window;
                `None` if not available.
            buy_30d: number of buy transactions in the trailing 30 days; `None` if not available.
            buy_30d_change_percent: buy count percent change vs previous 30d window;
                `None` if not available.
            volume_buy_30d_usd: USD volume of buy transactions in the trailing 30 days;
                `None` if not available.
            volume_buy_30d_change_percent: buy volume percent change vs previous 30d window;
                `None` if not available.
            sell_24h: number of sell transactions in the trailing 24 hours; `None` if not available.
            sell_24h_change_percent: sell count percent change vs previous 24h window;
                `None` if not available.
            volume_sell_24h_usd: USD volume of sell transactions in the trailing 24 hours;
                `None` if not available.
            volume_sell_24h_change_percent: sell volume percent change vs previous 24h window;
                `None` if not available.
            sell_7d: number of sell transactions in the trailing 7 days; `None` if not available.
            sell_7d_change_percent: sell count percent change vs previous 7d window;
                `None` if not available.
            volume_sell_7d_usd: USD volume of sell transactions in the trailing 7 days;
                `None` if not available.
            volume_sell_7d_change_percent: sell volume percent change vs previous 7d window;
                `None` if not available.
            sell_30d: number of sell transactions in the trailing 30 days; `None` if not available.
            sell_30d_change_percent: sell count percent change vs previous 30d window;
                `None` if not available.
            volume_sell_30d_usd: USD volume of sell transactions in the trailing 30 days;
                `None` if not available.
            volume_sell_30d_change_percent: sell volume percent change vs previous 30d window;
                `None` if not available.
            unique_wallet_24h: number of unique wallets that traded in the trailing 24 hours;
                `None` if not available.
            unique_wallet_24h_change_percent: unique wallet count percent change vs previous
                24h window; `None` if not available.
            price: latest known price in USD; `None` if not available.
            price_change_1m_percent: price percent change over the trailing 1 minute;
                `None` if not available.
            price_change_5m_percent: price percent change over the trailing 5 minutes;
                `None` if not available.
            price_change_30m_percent: price percent change over the trailing 30 minutes;
                `None` if not available.
            price_change_1h_percent: price percent change over the trailing 1 hour;
                `None` if not available.
            price_change_2h_percent: price percent change over the trailing 2 hours;
                `None` if not available.
            price_change_4h_percent: price percent change over the trailing 4 hours;
                `None` if not available.
            price_change_8h_percent: price percent change over the trailing 8 hours;
                `None` if not available.
            price_change_24h_percent: price percent change over the trailing 24 hours;
                `None` if not available.
            price_change_7d_percent: price percent change over the trailing 7 days;
                `None` if not available.
            price_change_30d_percent: price percent change over the trailing 30 days;
                `None` if not available.
            holder: number of distinct token holders; `None` if not available.
            recent_listing_time: unix timestamp (seconds) when Birdeye first detected this
                token listing; `None` if not available.
            meme_info: meme-platform-specific metadata (origin, pool state, graduation status);
                `None` if not available.
    """
    address: str
    logo_uri: str | None = None
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    extensions: dict[str, str | None] | None = None
    market_cap: float | None = None
    fdv: float | None = None
    total_supply: float | None = None
    circulating_supply: float | None = None
    liquidity: float | None = None
    last_trade_unix_time: int | None = None
    volume_1m_usd: float | None = None
    volume_5m_usd: float | None = None
    volume_30m_usd: float | None = None
    volume_1m_change_percent: float | None = None
    volume_5m_change_percent: float | None = None
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
    meme_info: GetV3TokenMemeListMemeInfo | None = None

class GetV3TokenMemeListData(BaseModel):
    """
        Data wrapper for the Birdeye v3 Meme Token - List response.

        Attributes:
            items: list of meme token records matching the requested filters and sort order.
            has_next: `True` when additional pages are available beyond the current ``offset``.
    """
    items: list[GetV3TokenMemeListItem]
    has_next: bool

class GetV3TokenMemeListResponse(BaseModel):
    """
        Model used to represent the **Meme Token - List** endpoint from the Birdeye v3 API.

        Attributes:
            data: paginated list of meme tokens with market and launchpad metadata.
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenMemeListData
    success: bool
