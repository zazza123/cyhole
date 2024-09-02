from pydantic import BaseModel, Field

# GET - Account Tokens
class GetAccountTokensTokenAmount(BaseModel):
    """
        This class refers to the model of a token amount inside the response of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    amount: str
    decimals: int
    ui_amount: float = Field(alias = "uiAmount")
    ui_amount_string: str = Field(alias = "uiAmountString")

class GetAccountTokensToken(BaseModel):
    """
        This class refers to the model of a token inside the response of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    token_account: str = Field(alias = "tokenAccount")
    token_address: str = Field(alias = "tokenAddress")
    token_symbol: str | None = Field(default = None, alias = "tokenSymbol")
    token_name: str | None = Field(default = None, alias = "tokenName")
    token_icon: str | None = Field(default = None, alias = "tokenIcon")
    token_amount: GetAccountTokensTokenAmount = Field(alias = "tokenAmount")
    decimals: int
    rent_epoch: int = Field(alias = "rentEpoch")
    lamports: int

class GetAccountTokensResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint.
    """
    tokens: list[GetAccountTokensToken]

# GET - Account Transactions
class GetAccountTransactionsTransactionInstruction(BaseModel):
    """
        This class refers to the model of an instruction inside the response of GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** of **V1** API endpoint.
    """
    program_id: str = Field(alias = "programId")
    program: str | None = None
    type: str 

class GetAccountTransactionsTransaction(BaseModel):
    """
        This class refers to the model of a transaction inside the response of GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** of **V1** API endpoint.
    """
    block_time: int = Field(alias = "blockTime")
    slot: int
    transaction_id: str = Field(alias = "txHash")
    fee: int
    status: str
    lamport: int
    signer: list[str]
    include_spl_transfer: bool | None = Field(default = None, alias = "includeSPLTransfer")
    parsed_instruction: list[GetAccountTransactionsTransactionInstruction] = Field(alias = "parsedInstruction")

class GetAccountTransactionsResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** of **V1** API endpoint.
    """
    transactions: list[GetAccountTransactionsTransaction]