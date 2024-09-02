from datetime import datetime
from pydantic import BaseModel, Field, field_validator

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

# GET - Account ExportRewards
class GetAccountExportRewardsResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account ExportRewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** of **V1** API endpoint.
    """
    csv: str

# GET - Account Detail
class GetAccountDetailResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** of **V1** API endpoint.
    """
    lamports: int
    owner_program: str = Field(alias = "ownerProgram")
    type: str
    rent_epoch: int = Field(alias = "rentEpoch")
    executable: bool
    account: str

# GET - Token Holders
class GetTokenHoldersHolder(BaseModel):
    """
        This class refers to the model of a holder inside the response of GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-holders)** of **V1** API endpoint.
    """
    address: str
    amount: int
    decimals: int
    owner: str
    rank: int

class GetTokenHoldersResponse(BaseModel):
    """
        This class refers to the response model of GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-holders)** of **V1** API endpoint.
    """
    total: int
    data: list[GetTokenHoldersHolder]

# GET - Token Meta
class GetTokenMetaResponse(BaseModel):
    """
        This class refers to the response model of GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-meta)** of **V1** API endpoint.
    """
    name: str | None = None
    symbol: str | None = None
    icon: str | None = None
    price: float
    volume: int
    decimals: int
    token_authority: str | None = Field(default = None, alias = "tokenAuthority")
    supply: str
    type: str
    address: str

# GET - Token Transfer
class GetTokenTransferTransferTokenInfo(BaseModel):
    """
        This class refers to the model of a token info inside the response of GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** of **V1** API endpoint.
    """
    symbol: str | None = None
    address: str
    name: str | None = None
    icon: str | None = None
    decimals: int

class GetTokenTransferTransfer(BaseModel):
    """
        This class refers to the model of a transfer inside the response of GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** of **V1** API endpoint.
    """
    slot: int
    block_time_unix_utc: int = Field(alias = "blockTime")
    transaction_id: str = Field(alias = "txHash")
    common_type: str = Field(alias = "commonType")
    source_owner_account: str = Field(alias = "sourceOwnerAccount")
    source_token_account: str = Field(alias = "sourceTokenAccount")
    destination_owner_account: str = Field(alias = "destOwnerAccount")
    destination_token_account: str = Field(alias = "destTokenAccount")
    token_address: str = Field(alias = "tokenAddress")
    amount: int
    token_info: GetTokenTransferTransferTokenInfo = Field(alias = "tokenInfo")

class GetTokenTransferResponse(BaseModel):
    """
        This class refers to the response model of GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** of **V1** API endpoint.
    """
    total: int
    items: list[GetTokenTransferTransfer]

# GET - Token List
class GetTokenListTokenSupply(BaseModel):
    """
        This class refers to the model of a token supply inside the response of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    amount: int
    ui_amount: float = Field(alias = "uiAmount")
    ui_amount_string: str = Field(alias = "uiAmountString")

class GetTokenListTokenExtensions(BaseModel):
    """
        This class refers to the model of token extensions inside the response of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    coingecko_id: str | None = Field(default = None, alias = "coingeckoId")
    discord: str | None = None
    medium: str | None = None
    telegram: str | None = None
    twitter: str | None = None
    website: str | None = None
    description: str | None = None
    coin_marketcap_id: str | None = Field(default = None, alias = "coinMarketCapId")
    serum_v3_usdc: str | None = Field(default = None, alias = "serumV3Usdc")
    serum_v3_usdt: str | None = Field(default = None, alias = "serumV3Usdt")

class GetTokenListTokenCoingeckoInfoMarketData(BaseModel):
    """
        This class refers to the model of token coingecko info market data inside the response of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    current_price: float = Field(alias = "currentPrice")
    all_time_high: float = Field(alias = "ath")
    all_time_high_change_percentage: float = Field(alias = "athChangePercentage")
    all_time_high_date: datetime = Field(alias = "athDate")
    all_time_low: float = Field(alias = "atl")
    all_time_low_change_percentage: float = Field(alias = "atlChangePercentage")
    all_time_low_date: datetime = Field(alias = "atlDate")
    market_cap: int = Field(alias = "marketCap")
    market_cap_rank: int = Field(alias = "marketCapRank")
    fully_diluted_valuation: int = Field(alias = "fullyDilutedValuation")
    total_volume: float = Field(alias = "totalVolume")
    price_high_24h: float = Field(alias = "priceHigh24h")
    price_low_24h: float = Field(alias = "priceLow24h")
    price_change_24h: float = Field(alias = "priceChange24h")
    price_change_percentage_24h: float = Field(alias = "priceChangePercentage24h")
    price_change_percentage_7d: float | None = Field(default = None, alias = "priceChangePercentage7d")
    price_change_percentage_14d: float | None = Field(default = None, alias = "priceChangePercentage14d")
    price_change_percentage_30d: float | None = Field(default = None, alias = "priceChangePercentage30d")
    price_change_percentage_60d: float | None = Field(default = None, alias = "priceChangePercentage60d")
    price_change_percentage_200d: float | None = Field(default = None, alias = "priceChangePercentage200d")
    price_change_percentage_1y: float | None = Field(default = None, alias = "priceChangePercentage1y")
    market_cap_change_24h: float = Field(alias = "marketCapChange24h")
    market_cap_change_percentage_24h: float = Field( alias = "marketCapChangePercentage24h")
    total_supply: float = Field(alias = "totalSupply")
    max_supply: float | None = Field(default = None, alias = "maxSupply")
    circulating_supply: float = Field(alias = "circulatingSupply")
    last_updated: datetime = Field(alias = "lastUpdated")

    @field_validator("all_time_high_date", "all_time_low_date", "last_updated")
    def parse_datetime(cls, datetime_raw: str | datetime) -> datetime:
        if isinstance(datetime_raw, str):
            return datetime.strptime(datetime_raw, "%Y-%m-%dT%H:%M:%S")
        return datetime_raw

class GetTokenListTokenCoingeckoInfo(BaseModel):
    """
        This class refers to the model of token coingecko info inside the response of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    coingecko_rank: int = Field(alias = "coingeckoRank")
    market_cap_rank: int = Field(alias = "marketCapRank")
    market_data: GetTokenListTokenCoingeckoInfoMarketData = Field(alias = "marketData")

class GetTokenListToken(BaseModel):
    """
        This class refers to the model of a token inside the response of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    address: str
    coingecko_info: GetTokenListTokenCoingeckoInfo | None = Field(default = None, alias = "coingeckoInfo")
    decimals: int
    extensions: GetTokenListTokenExtensions
    holder: int
    icon: str | None = None
    is_violate: bool | None = Field(default = None, alias = "isViolate")
    market_cap_fd: float | None = Field(default = None, alias = "marketCapFD")
    market_cap_rank: int | None = Field(default = None, alias = "marketCapRank")
    mint_address: str = Field(alias = "mintAddress")
    price_ust: float | None = Field(default = None, alias = "priceUst")
    sol_alpha_volume: float | None = Field(default = None, alias = "solAlphaVolume")
    tags: list[str] | None = None
    name: str | None = Field(default = None, alias = "tokenName")
    symbol: str | None = Field(default = None, alias = "tokenSymbol")
    reputation: str | None = None
    twitter: str | None = None
    website: str | None = None
    on_chain_extensions: str | None = None
    supply: GetTokenListTokenSupply | None = None
    chain_id: int | None = Field(default = None, alias = "chainId")

class GetTokenListResponse(BaseModel):
    """
        This class refers to the response model of GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint.
    """
    total: int
    data: list[GetTokenListToken]

# GET - Market Token Detail
class GetMarketTokenDetailMarketBaseQuote(BaseModel):
    """
        This class refers to the model of a base or quote inside the response of GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** of **V1** API endpoint.
    """
    symbol: str | None = None
    decimals: int
    address: str

class GetMarketTokenDetailMarket(BaseModel):
    """
        This class refers to the model of a market inside the response of GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** of **V1** API endpoint.
    """
    address: str
    amm_id: str = Field(alias = "ammId")
    base: GetMarketTokenDetailMarketBaseQuote
    base_token_account: str = Field(alias = "baseTokenAccount")
    name: str
    quote: GetMarketTokenDetailMarketBaseQuote
    source: str
    quote_token_account: str = Field(alias = "quoteTokenAccount")
    volume_24h: int = Field(alias = "volume24h")

class GetMarketTokenDetailResponse(BaseModel):
    """
        This class refers to the response model of GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** of **V1** API endpoint.
    """
    price_usdt: float = Field(alias = "priceUsdt")
    volume_usdt: int = Field(alias = "volumeUsdt")
    market_cap_fd: int = Field(alias = "marketCapFD")
    market_cap_rank: int = Field(alias = "marketCapRank")
    price_change_24h: float = Field(alias = "priceChange24h")
    markets: list[GetMarketTokenDetailMarket]