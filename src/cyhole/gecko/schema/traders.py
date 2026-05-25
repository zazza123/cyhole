"""Schema for the Top Token Traders endpoint."""

from pydantic import BaseModel


class TopTokenTrader(BaseModel):
    """
    Single entry in the Top Token Traders list.

    Attributes:
        address: trader wallet address.
        name: human-readable wallet name; `None` when unknown.
        label: descriptive label (e.g. exchange / smart-money tag); `None` when unlabelled.
        type: classification tag assigned by GeckoTerminal (e.g. `"wallet"`, `"contract"`).
        realized_pnl_usd: realized PnL in USD across closed trades on the token.
        unrealized_pnl_usd: unrealized PnL in USD for the open position; `None` when no position remains.
        token_balance: current token balance held; `None` when the position is closed.
        average_buy_price_usd: average USD buy price across all buy fills.
        average_sell_price_usd: average USD sell price across all sell fills.
        total_buy_count: number of buy trades.
        total_sell_count: number of sell trades.
        total_buy_token_amount: aggregate token amount bought (decimal string).
        total_sell_token_amount: aggregate token amount sold (decimal string).
        total_buy_usd: aggregate USD value bought.
        total_sell_usd: aggregate USD value sold.
        explorer_url: blockchain explorer URL for the wallet.
    """
    address: str
    name: str | None = None
    label: str | None = None
    type: str | None = None
    realized_pnl_usd: str | None = None
    unrealized_pnl_usd: str | None = None
    token_balance: str | None = None
    average_buy_price_usd: str | None = None
    average_sell_price_usd: str | None = None
    total_buy_count: int | None = None
    total_sell_count: int | None = None
    total_buy_token_amount: str | None = None
    total_sell_token_amount: str | None = None
    total_buy_usd: str | None = None
    total_sell_usd: str | None = None
    explorer_url: str | None = None


class TopTokenTradersAttributes(BaseModel):
    """
    Attributes block of the Top Token Traders resource.

    Attributes:
        traders: ordered list of top traders, sorted by the requested `sort` criterion.
    """
    traders: list[TopTokenTrader]


class TopTokenTradersData(BaseModel):
    """
    Top-level `data` block of the Top Token Traders response.

    Attributes:
        id: identifier of the traders snapshot.
        type: JSON:API resource type.
        attributes: top-traders payload.
    """
    id: str
    type: str
    attributes: TopTokenTradersAttributes


class GetTopTokenTradersResponse(BaseModel):
    """
    Response payload from the **Top Token Traders** endpoint, returning the highest-performing
    wallets on the requested token by realised PnL, unrealised PnL, total buy or total sell USD.
    Useful for smart-money / whale-watching strategies.

    Attributes:
        data: top traders payload.
    """
    data: TopTokenTradersData
