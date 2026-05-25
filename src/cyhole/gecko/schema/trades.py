"""Schemas for the Pool Trades and Token Trades endpoints."""

from pydantic import BaseModel


class TradeAttributes(BaseModel):
    """
    Attributes block of a single trade resource as returned by the Pool Trades endpoint.

    Attributes:
        block_number: on-chain block number containing the trade.
        tx_hash: transaction hash on the underlying network.
        tx_from_address: signer/sender address of the transaction.
        from_token_amount: input-token amount of the trade (decimal string).
        to_token_amount: output-token amount of the trade (decimal string).
        price_from_in_currency_token: price of `from_token` quoted in the chosen `currency` token.
        price_to_in_currency_token: price of `to_token` quoted in the chosen `currency` token.
        price_from_in_usd: price of `from_token` in USD at the time of the trade.
        price_to_in_usd: price of `to_token` in USD at the time of the trade.
        block_timestamp: ISO-8601 timestamp of the block.
        kind: trade direction relative to the pool's base token (`"buy"` or `"sell"`).
        volume_in_usd: USD value of the trade.
        from_token_address: contract address of `from_token`.
        to_token_address: contract address of `to_token`.
    """
    block_number: int
    tx_hash: str
    tx_from_address: str
    from_token_amount: str
    to_token_amount: str
    price_from_in_currency_token: str
    price_to_in_currency_token: str
    price_from_in_usd: str
    price_to_in_usd: str
    block_timestamp: str
    kind: str
    volume_in_usd: str
    from_token_address: str
    to_token_address: str


class TokenTradeAttributes(TradeAttributes):
    """
    Attributes block of a single trade resource as returned by the Token Trades endpoint.

    Extends [`TradeAttributes`][cyhole.gecko.schema.TradeAttributes] with the pool the trade was
    routed through.

    Attributes:
        pool_address: contract address of the pool that executed the trade.
        pool_dex: identifier of the DEX the pool belongs to.
    """
    pool_address: str | None = None
    pool_dex: str | None = None


class TradeData(BaseModel):
    """
    Single trade resource from the Pool Trades endpoint.

    Attributes:
        id: identifier of the trade.
        type: JSON:API resource type.
        attributes: trade payload.
    """
    id: str
    type: str
    attributes: TradeAttributes


class TokenTradeData(BaseModel):
    """
    Single trade resource from the Token Trades endpoint.

    Attributes:
        id: identifier of the trade.
        type: JSON:API resource type.
        attributes: trade payload extended with `pool_address` and `pool_dex`.
    """
    id: str
    type: str
    attributes: TokenTradeAttributes


class GetPoolTradesResponse(BaseModel):
    """
    Response payload from the **Pool Trades** endpoint, returning the trade history of the requested
    pool over the trailing 24 hours, optionally filtered by minimum USD volume.

    Attributes:
        data: list of trades, ordered newest-first.
    """
    data: list[TradeData]


class GetTokenTradesResponse(BaseModel):
    """
    Response payload from the **Token Trades** endpoint, returning the trade history involving the
    requested token across every indexed pool over the trailing 24 hours.

    Attributes:
        data: list of trades, ordered newest-first; each entry also reports the pool that executed it.
    """
    data: list[TokenTradeData]
