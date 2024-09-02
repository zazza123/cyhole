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
    block_time_unix_utc: int = Field(alias = "blockTime")
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

# GET - Account StakeAccounts
class GetAccountStakeAccountsStakeAccount(BaseModel):
    """
        This class refers to the model of a stake account inside the response of GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** of **V1** API endpoint.
    """
    active_stake_amount: int = Field(alias = "activeStakeAmount")
    amount: int
    delegated_stake_amount: int = Field(alias = "delegatedStakeAmount")
    role: list[str]
    sol_balance: int = Field(alias = "solBalance")
    total_reward: str = Field(alias = "totalReward")
    status: str
    stake_account: str = Field(alias = "stakeAccount")
    type: str
    voter: str
    activation_epoch: int = Field(alias = "activationEpoch")
    stake_type: str = Field(alias = "stakeType")

class GetAccountStakeAccountsResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** of **V1** API endpoint.
    """
    stake_accounts: dict[str, GetAccountStakeAccountsStakeAccount]

# GET - Account SplTransfers
class GetAccountSplTransfersTransfer(BaseModel):
    """
        This class refers to the model of a transfer inside the response of GET **[Account SplTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-splTransfers)** of **V1** API endpoint.
    """
    slot: int
    block_time_unix_utc: int = Field(alias = "blockTime")
    signature: list[str]
    change_type: str = Field(alias = "changeType")
    change_amount: str = Field(alias = "changeAmount")
    decimals: int
    post_balance: str = Field(alias = "postBalance")
    pre_balance: str = Field(alias = "preBalance")
    token_address: str = Field(alias = "tokenAddress")
    owner: str
    fee: int
    address: str
    symbol: str
    token_name: str = Field(alias = "tokenName")

class GetAccountSplTransfersResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account SplTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-splTransfers)** of **V1** API endpoint.
    """
    total: int
    data: list[GetAccountSplTransfersTransfer]

# GET - Account SolTransfers
class GetAccountSolTransfersTransfer(BaseModel):
    """
        This class refers to the model of a transfer inside the response of GET **[Account SolTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-solTransfers)** of **V1** API endpoint.
    """
    slot: int
    block_time_unix_utc: int = Field(alias = "blockTime")
    transaction_id: str = Field(alias = "txHash")
    source_account : str = Field(alias = "src")
    decimals: int
    destination_account: str = Field(alias = "dst")
    lamport: int
    status: str
    fee: int

class GetAccountSolTransfersResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account SolTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-solTransfers)** of **V1** API endpoint.
    """
    data: list[GetAccountSolTransfersTransfer]

# GET - Account ExportTransactions
class GetAccountExportTransactionsResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account ExportTransactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** of **V1** API endpoint.
    """
    csv: str