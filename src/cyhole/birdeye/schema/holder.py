from pydantic import BaseModel


# classes used on GET "Token - Holder" endpoint
class GetTokenHolderItem(BaseModel):
    """
        Single top-holder entry returned by the v3 Token - Holder endpoint.

        Attributes:
            mint: contract address of the SPL token being held.
            owner: wallet address that owns the token balance.
            token_account: SPL token account address holding the balance for `owner`.
            amount: raw amount held, expressed in the token's smallest units (string).
            decimals: number of decimal places used by the token.
            ui_amount: UI-formatted amount (i.e. `amount` divided by `10 ** decimals`) as a number.
            is_scaled_ui_token: `True` when the token is a scaled-UI-amount SPL token; `None` if
                undetermined.
            multiplier: scaling multiplier applied to UI amounts of scaled-UI-amount tokens; `None`
                when not applicable.
    """
    mint: str
    owner: str
    token_account: str
    amount: str
    decimals: int
    ui_amount: float
    is_scaled_ui_token: bool | None = None
    multiplier: float | None = None

class GetTokenHolderData(BaseModel):
    """
        Payload of the v3 Token - Holder response.

        Attributes:
            items: ranked list of top holder entries (largest balance first by default).
    """
    items: list[GetTokenHolderItem]

class GetTokenHolderResponse(BaseModel):
    """
        Model used to represent the **Token - Holder** endpoint from birdeye API.

        Attributes:
            data: payload containing the ranked top-holder list.
            success: `True` when the API call completed without errors.
    """
    data: GetTokenHolderData
    success: bool


# classes used on POST "Token - Holder (Batch)" endpoint
class PostTokenHolderBatchItem(BaseModel):
    """
        Single wallet/token balance entry returned by the POST Token - Holder (Batch) endpoint.

        Attributes:
            mint: contract address of the SPL token being held.
            owner: wallet address whose balance is being reported.
            amount: UI-formatted balance (numeric).
            balance: raw balance expressed in the token's smallest units (string).
            decimals: number of decimal places used by the token.
    """
    mint: str
    owner: str
    amount: float
    balance: str
    decimals: int

class PostTokenHolderBatchData(BaseModel):
    """
        Payload of the POST Token - Holder (Batch) response.

        Attributes:
            items: list of balance entries, one per `(owner, mint)` combination requested. Owners
                that have never held the token are omitted from the list.
    """
    items: list[PostTokenHolderBatchItem]

class PostTokenHolderBatchBody(BaseModel):
    """
        Request body for the POST Token - Holder (Batch) endpoint.

        Attributes:
            token_address: contract address of the SPL token whose balances must be looked up.
            wallets: list of wallet addresses whose balance in `token_address` should be returned.
    """
    token_address: str
    wallets: list[str]

class PostTokenHolderBatchResponse(BaseModel):
    """
        Model used to represent the **Token - Holder (Batch)** endpoint from birdeye API.

        Attributes:
            data: payload containing the balance entries.
            success: `True` when the API call completed without errors.
    """
    data: PostTokenHolderBatchData
    success: bool
