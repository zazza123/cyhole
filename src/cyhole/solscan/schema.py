from pydantic import BaseModel, Field

# **************************
# * V1 API                 *
# **************************
class GetV1AccountTokensTokenAmount(BaseModel):
    """
        This class refers to the model of a token amount inside the response of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    amount: str
    decimals: int
    ui_amount: float = Field(alias = "uiAmount")
    ui_amount_string: str = Field(alias = "uiAmountString")

class GetV1AccountTokensToken(BaseModel):
    """
        This class refers to the model of a token inside the response of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    token_account: str = Field(alias = "tokenAccount")
    token_address: str = Field(alias = "tokenAddress")
    token_symbol: str = Field(alias = "tokenSymbol")
    token_name: str = Field(alias = "tokenName")
    token_icon: str = Field(alias = "tokenIcon")
    token_amount: GetV1AccountTokensTokenAmount = Field(alias = "tokenAmount")
    decimals: int
    rent_epoch: int = Field(alias = "rentEpoch")
    lamports: int

class GetV1AccountTokensResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    tokens: list[GetV1AccountTokensToken]

# **************************
# * V2 API                 *
# **************************