from pydantic import BaseModel


# classes used on POST "Token - Transfer List" endpoint
class PostTokenTransferBody(BaseModel):
    """
        Request body for the POST Token - Transfer List endpoint.

        Every field except `token_address` is optional and acts as a filter on the returned list.

        Attributes:
            token_address: contract address of the SPL token whose transfers must be listed.
            time_from: optional inclusive lower bound on the transfer time, in unix seconds; `None`
                to disable the filter.
            time_to: optional inclusive upper bound on the transfer time, in unix seconds; `None`
                to disable the filter.
            from_amount: optional inclusive lower bound on the transfer amount in UI units; `None`
                to disable.
            to_amount: optional inclusive upper bound on the transfer amount in UI units; `None`
                to disable.
            from_value: optional inclusive lower bound on the transfer USD value; `None` to disable.
            to_value: optional inclusive upper bound on the transfer USD value; `None` to disable.
            from_wallet: optional sender wallet address to filter by; `None` to disable the filter.
            to_wallet: optional receiver wallet address to filter by; `None` to disable the filter.
            cursor: opaque pagination cursor returned by a previous call; leave `None` for the
                first page.
            limit: maximum number of transfers to return per call; `None` defers to Birdeye's
                server-side default.
    """
    token_address: str
    time_from: int | None = None
    time_to: int | None = None
    from_amount: float | None = None
    to_amount: float | None = None
    from_value: float | None = None
    to_value: float | None = None
    from_wallet: str | None = None
    to_wallet: str | None = None
    cursor: str | None = None
    limit: int | None = None

class PostTokenTransferItemTokenInfo(BaseModel):
    """
        Compact identity payload Birdeye attaches to every transfer entry.

        Attributes:
            address: contract address of the SPL token transferred.
            decimals: number of decimal places used by the token.
            symbol: ticker symbol of the token; `None` if unknown.
            name: human-readable name of the token; `None` if unknown.
            logo_uri: URL of the token logo; `None` if Birdeye does not have a logo for the token.
    """
    address: str
    decimals: int
    symbol: str | None = None
    name: str | None = None
    logo_uri: str | None = None

class PostTokenTransferItem(BaseModel):
    """
        Single SPL token transfer transaction returned by the POST Token - Transfer List endpoint.

        Attributes:
            tx_hash: signature of the on-chain transaction that produced the transfer.
            block_number: slot/block number in which the transaction was processed.
            time: ISO-8601 timestamp of the transfer.
            unix_time: unix-second timestamp matching `time`.
            action: high-level classification of the on-chain action (e.g. `transfer`).
            flow: direction of the transfer relative to the queried token (`in` / `out`).
            token_address: contract address of the SPL token transferred.
            token_info: compact identity payload (`address`, `decimals`, `symbol`, ...) of the token.
            from_address: wallet address that sent the tokens.
            from_token_account: SPL token account on the sender side.
            to_address: wallet address that received the tokens.
            to_token_account: SPL token account on the receiver side.
            amount: raw amount transferred, in the token's smallest units (string).
            ui_amount: UI-formatted amount (i.e. `amount / 10**decimals`).
            price: per-token price in USD at the time of the transfer.
            value: total USD value of the transfer (`ui_amount * price`).
    """
    tx_hash: str
    block_number: int
    time: str
    unix_time: int
    action: str
    flow: str
    token_address: str
    token_info: PostTokenTransferItemTokenInfo
    from_address: str
    from_token_account: str
    to_address: str
    to_token_account: str
    amount: str
    ui_amount: float
    price: float
    value: float

class PostTokenTransferResponse(BaseModel):
    """
        Model used to represent the **Token - Transfer List** endpoint from birdeye API.

        Attributes:
            data: paginated list of transfer entries; the API returns the list directly under
                `data` (no wrapping `items` key). To fetch the next page, reissue the call with
                the appropriate `cursor` value.
            success: `True` when the API call completed without errors.
    """
    data: list[PostTokenTransferItem]
    success: bool


# classes used on POST "Token - Transfer Total" endpoint
class PostTokenTransferTotalBody(BaseModel):
    """
        Request body for the POST Token - Transfer Total endpoint.

        Mirrors [`PostTokenTransferBody`][cyhole.birdeye.schema.PostTokenTransferBody] minus the
        pagination fields (`cursor`, `limit`), since the endpoint returns only an aggregate count.

        Attributes:
            token_address: contract address of the SPL token whose transfer count must be returned.
            time_from: optional inclusive lower bound on the transfer time, in unix seconds; `None`
                to disable the filter.
            time_to: optional inclusive upper bound on the transfer time, in unix seconds; `None`
                to disable the filter.
            from_amount: optional inclusive lower bound on the transfer amount in UI units; `None`
                to disable.
            to_amount: optional inclusive upper bound on the transfer amount in UI units; `None`
                to disable.
            from_value: optional inclusive lower bound on the transfer USD value; `None` to disable.
            to_value: optional inclusive upper bound on the transfer USD value; `None` to disable.
            from_wallet: optional sender wallet address to filter by; `None` to disable the filter.
            to_wallet: optional receiver wallet address to filter by; `None` to disable the filter.
    """
    token_address: str
    time_from: int | None = None
    time_to: int | None = None
    from_amount: float | None = None
    to_amount: float | None = None
    from_value: float | None = None
    to_value: float | None = None
    from_wallet: str | None = None
    to_wallet: str | None = None

class PostTokenTransferTotalData(BaseModel):
    """
        Payload of the POST Token - Transfer Total response.

        Attributes:
            total: total number of transfers matching the request filters.
    """
    total: int

class PostTokenTransferTotalResponse(BaseModel):
    """
        Model used to represent the **Token - Transfer Total** endpoint from birdeye API.

        Attributes:
            data: aggregate-count payload.
            success: `True` when the API call completed without errors.
    """
    data: PostTokenTransferTotalData
    success: bool
