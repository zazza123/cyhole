"""Schemas for the Token Holders Chart and Top Token Holders endpoints."""

from pydantic import BaseModel


class TokenHoldersChartAttributes(BaseModel):
    """
    Attributes block of the Token Holders Chart resource.

    Attributes:
        token_holders_list: ordered list of `[timestamp_iso8601, holders_count_string]` pairs.
            Both values are strings as returned by the API.
    """
    token_holders_list: list[list[str]]


class TokenHoldersChartData(BaseModel):
    """
    Top-level `data` block of the Token Holders Chart response.

    Attributes:
        id: identifier of the holders-chart series.
        type: JSON:API resource type.
        attributes: time-series payload.
    """
    id: str
    type: str
    attributes: TokenHoldersChartAttributes


class TokenHoldersChartMetaToken(BaseModel):
    """
    Reference info for the token whose holders chart is returned.

    Attributes:
        name: human-readable token name.
        symbol: token ticker symbol.
        coingecko_coin_id: CoinGecko coin id; `None` when not mapped.
        address: token contract address.
    """
    name: str
    symbol: str
    coingecko_coin_id: str | None = None
    address: str


class TokenHoldersChartMeta(BaseModel):
    """
    `meta` block of the Token Holders Chart response.

    Attributes:
        token: identification of the token whose holders chart is returned.
    """
    token: TokenHoldersChartMetaToken


class GetTokenHoldersChartResponse(BaseModel):
    """
    Response payload from the **Token Holders Chart** endpoint, returning the historical holders
    count for the requested token across the chosen window (`7`, `30` or `max` days). Useful to
    track adoption or sell-off pressure over time.

    Attributes:
        data: time-series payload of holder counts.
        meta: token identification block.
    """
    data: TokenHoldersChartData
    meta: TokenHoldersChartMeta


class TopTokenHolder(BaseModel):
    """
    Single entry in the Top Token Holders list.

    Attributes:
        rank: 1-based rank of the holder by token balance.
        address: holder wallet address.
        label: descriptive label assigned by GeckoTerminal (e.g. exchange wallet); `None` when unlabelled.
        amount: token amount held (decimal string, decimals applied).
        percentage: holder share of total supply, as a percentage string.
        value: USD value of the holding (decimal string).
        average_buy_price_usd: estimated average USD buy price of the position.
        total_buy_count: number of buy trades observed for this address.
        total_sell_count: number of sell trades observed for this address.
        unrealized_pnl_usd: unrealized PnL in USD for the current position.
        unrealized_pnl_percentage: unrealized PnL as a percentage string.
        realized_pnl_usd: realized PnL in USD across closed positions.
        realized_pnl_percentage: realized PnL as a percentage string.
        explorer_url: blockchain explorer URL for the wallet on its network.
    """
    rank: int
    address: str
    label: str | None = None
    amount: str | None = None
    percentage: str | None = None
    value: str | None = None
    average_buy_price_usd: str | None = None
    total_buy_count: int | None = None
    total_sell_count: int | None = None
    unrealized_pnl_usd: str | None = None
    unrealized_pnl_percentage: str | None = None
    realized_pnl_usd: str | None = None
    realized_pnl_percentage: str | None = None
    explorer_url: str | None = None


class TopTokenHoldersAttributes(BaseModel):
    """
    Attributes block of the Top Token Holders resource.

    Attributes:
        last_updated_at: ISO-8601 timestamp of the snapshot.
        holders: ordered list of top holders.
    """
    last_updated_at: str | None = None
    holders: list[TopTokenHolder]


class TopTokenHoldersData(BaseModel):
    """
    Top-level `data` block of the Top Token Holders response.

    Attributes:
        id: identifier of the holders snapshot.
        type: JSON:API resource type.
        attributes: list of top holders + snapshot timestamp.
    """
    id: str
    type: str
    attributes: TopTokenHoldersAttributes


class GetTopTokenHoldersResponse(BaseModel):
    """
    Response payload from the **Top Token Holders** endpoint, returning the top wallets holding the
    requested token along with realised/unrealised PnL details when `include_pnl_details=true`.

    Attributes:
        data: top holders payload.
    """
    data: TopTokenHoldersData
