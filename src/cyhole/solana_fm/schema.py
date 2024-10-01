from datetime import datetime
from pydantic import BaseModel, Field, field_serializer, field_validator

class SolanaFMBaseResponse(BaseModel):
    """
        Model used to identify the base response of the SolanaFM API.
    """
    status: str
    message: str

class SolanaFMPagination(BaseModel):
    """
        Model used to identify the pagination of the SolanaFM API.
    """
    current_page: int = Field(alias = "currentPage")
    total_pages: int = Field(alias = "totalPages")

# classes used on GET "Account - Transactions" endpoint
# Param
class GetAccountTransactionsParam(BaseModel):
    """
        Model used to identify the parameters of the GET "Account - Transactions" endpoint.
    """

    actions: str | None = None
    """The action(s) to filter by."""

    utc_from_unix_time: int | None = Field(default = None, serialization_alias = "utcFrom")
    """The start date of the transactions to filter by in Unix time."""

    utc_to_unix_time: int | None = Field(default = None, serialization_alias = "utcTo")
    """The end date of the transactions to filter by in Unix time."""

    inflow: bool | None = None
    """Whether to include inflow transactions."""

    outflow: bool | None = None
    """Whether to include outflow transactions."""

    mints: str | list[str] | None = None
    """The mint ID(s) to filter by."""

    amount_from: int | None = Field(default = None, serialization_alias = "amountFrom", gt = 0)
    """The minimum amount of the transaction."""

    amount_to: int | None = Field(default = None, serialization_alias = "amountTo", gt = 0)
    """The maximum amount of the transaction."""

    programs: str | list[str] | None = None
    """The program ID(s) to filter by."""

    limit: int | None = Field(default = None, le = 1000, gt = 0)
    """The number of transactions to return."""

    page: int = Field(default = 1, gt = 0)
    """The page number to return."""

    @field_serializer("mints", "programs")
    @classmethod
    def serialize_str_list_input(cls, str_input: str | list[str] | None) -> str | None:
        return ",".join(str_input) if str_input else None

    @field_serializer("outflow", "inflow")
    @classmethod
    def serialize_flows(cls, value: bool | None) -> str | None:
        if value is not None:
            return "true" if value else "false"
        return

# Response
class GetAccountTransactionsData(BaseModel):
    """
        Model used to identify the data of the GET "Account - Transactions" endpoint.
    """
    block_time: int = Field(alias = "blockTime")
    confirmation_status: str = Field(alias = "confirmationStatus")
    error: str | None = Field(default = None, alias = "err")
    memo: str | None = None
    signature: str
    slot: int

class GetAccountTransactionsResult(BaseModel):
    """
        Model used to identify the result of the GET "Account - Transactions" endpoint.
    """
    data: list[GetAccountTransactionsData]
    pagination: SolanaFMPagination

class GetAccountTransactionsResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Account - Transactions" endpoint.
    """
    result: GetAccountTransactionsResult

# classes used on GET "Account - Transfers" endpoint
# Param
class GetAccountTransfersParam(BaseModel):
    """
        Model used to identify the parameters of the GET "Account - Transfers" endpoint.
    """
    utc_from_unix_time: int | None = Field(default = None, serialization_alias = "utcFrom")
    """The start date of the transactions to filter by in Unix time."""

    utc_to_unix_time: int | None = Field(default = None, serialization_alias = "utcTo")
    """The end date of the transactions to filter by in Unix time."""

    inflow: bool | None = None
    """Whether to include inflow transactions."""

    outflow: bool | None = None
    """Whether to include outflow transactions."""

    mint: str | list[str] | None = None
    """The mint ID(s) to filter by."""

    limit: int | None = Field(default = None, le = 100, gt = 0)
    """The number of transactions to return."""

    page: int = Field(default = 1, gt = 0)
    """The page number to return."""

    @field_serializer("mint")
    @classmethod
    def serialize_str_list_input(cls, str_input: str | list[str] | None) -> str | None:
        return ",".join(str_input) if str_input else None

    @field_serializer("outflow", "inflow")
    @classmethod
    def serialize_flows(cls, value: bool | None) -> str | None:
        if value is not None:
            return "true" if value else "false"
        return

# Response
class GetAccountTransfersData(BaseModel):
    """
        Model used to identify the data of the GET "Account - Transfers" endpoint.
    """
    instruction_index: int = Field(alias = "instructionIndex")
    inner_instruction_index: int = Field(alias = "innerInstructionIndex")
    action: str
    status: str
    source: str | None = None
    source_association: str | None = Field(default = None, alias = "sourceAssociation")
    destination: str | None = None
    destination_association: str | None = Field(default = None, alias = "destinationAssociation")
    token: str
    amount: int
    timestamp: int

class GetAccountTransfersResults(BaseModel):
    """
        Model used to identify the results of the GET "Account - Transfers" endpoint.
    """
    transaction_hash: str = Field(alias = "transactionHash")
    data: list[GetAccountTransfersData]

class GetAccountTransfersResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Account - Transfers" endpoint.
    """
    results: list[GetAccountTransfersResults]
    pagination: SolanaFMPagination

# classes used on GET "Account - Transfers CSV Export" endpoint
# Param
class GetAccountTransfersCsvExportParam(GetAccountTransactionsParam):
    """
        Model used to identify the parameters of the GET "Account - Transfers CSV Export" endpoint.
    """
    pass

# Response
class GetAccountTransfersCsvExportResponse(BaseModel):
    """
        Model used to identify the response of the GET "Account - Transfers CSV Export" endpoint.
    """
    csv: str

# classes used on GET "Account Transactions Fees" endpoint
# Response
class GetAccountTransactionsFeesData(BaseModel):
    """
        Model used to identify the data of the GET "Account Transactions Fees" endpoint.
    """
    tx_fees: int
    time: datetime

    @field_serializer("time")
    @classmethod
    def serialize_time(cls, time: datetime) -> str:
        return time.strftime("%Y-%m-%d")

class GetAccountTransactionsFeesResponse(BaseModel):
    """
        Model used to identify the response of the GET "Account Transactions Fees" endpoint.
    """
    data: list[GetAccountTransactionsFeesData]

# classes used on GET "Blocks" endpoint
class SolanaFMBlockData(BaseModel):
    """
        Model used to identify the data of the SolanaFM block.
    """
    epoch: int
    previous_hash: str = Field(alias = "previousHash")
    hash: str
    parent_number: int = Field(alias = "parentNumber")
    number: int
    data_size: int = Field(alias = "dataSize")
    number_of_transactions: int = Field(alias = "numberOfTransactions")
    successful_transactions: int = Field(alias = "successfulTransactions")
    vote_transactions: int = Field(alias = "voteTransactions")
    total_tx_fees: int = Field(alias = "totalTxFees")
    number_of_rewards: int = Field(alias = "numberOfRewards")
    total_reward_amount: int = Field(alias = "totalRewardAmount")
    total_compute_units_consumed: int = Field(alias = "totalComputeUnitsConsumed")
    total_compute_units_limit: int = Field(alias = "totalComputeUnitsLimit")
    block_time: int = Field(alias = "blockTime")

# Response
class GetBlocksDataData(SolanaFMBlockData):
    """
        Model used to identify the info of the GET "Blocks" endpoint.
    """
    producer: str

class GetBlocksData(BaseModel):
    """
        Model used to identify the data of the GET "Blocks" endpoint.
    """
    block_number: int = Field(alias = "blockNumber")
    data: GetBlocksDataData

class GetBlocksPagination(BaseModel):
    """
        Model used to identify the pagination of the GET "Blocks" endpoint.
    """
    next: int | None = None
    previous: int | None = None

class GetBlocksResult(BaseModel):
    """
        Model used to identify the result of the GET "Blocks" endpoint.
    """
    data: list[GetBlocksData]
    pagination: GetBlocksPagination

class GetBlocksResponse(SolanaFMBaseResponse):
    """
        Model used to identify the data of the GET "Blocks" endpoint.
    """
    result: GetBlocksResult

# classes used on GET "Block" endpoint
# Response
class GetBlockResult(GetBlocksData):
    """
        Model used to identify the result of the GET "Block" endpoint.
    """
    pass

class GetBlockResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Block" endpoint.
    """
    result: GetBlockResult

# classes used on POST "Multiple Blocks" endpoint
# Response
class PostMultipleBlocksProducerData(BaseModel):
    """
        Model used to identify the data of the producer from POST "Multiple Blocks" endpoint.
    """
    friendly_name: str = Field(alias = "friendlyName")
    abbreviation: str
    category: str
    vote_key: str = Field(alias = "voteKey")
    network: str
    tags: list[str]
    logo_uri: str | None = Field(default = None, alias = "logoURI")
    flag: str | None = None

class PostMultipleBlocksProducer(BaseModel):
    """
        Model used to identify the producer of the POST "Multiple Blocks" endpoint.
    """
    account_hash: str = Field(alias = "accountHash")
    data: PostMultipleBlocksProducerData

class PostMultipleBlocksData(SolanaFMBlockData):
    """
        Model used to identify the data of the POST "Multiple Blocks" endpoint.
    """
    producer: str | PostMultipleBlocksProducer

class PostMultipleBlocksResult(BaseModel):
    """
        Model used to identify the result of the POST "Multiple Blocks" endpoint.
    """
    block_number: int = Field(alias = "blockNumber")
    data: PostMultipleBlocksData

class PostMultipleBlocksResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the POST "Multiple Blocks" endpoint.
    """
    result: list[PostMultipleBlocksResult]

# classes used on GET "Solana Daily Transaction Fees" endpoint
# Response
class GetSolanaDailyTransactionFeesResult(BaseModel):
    """
        Model used to identify the result of the GET "Solana Daily Transaction Fees" endpoint.
    """
    total_tx_fees: int = Field(alias = "totalTxFees")
    date: str

    @field_validator("date")
    @classmethod
    def parse_date(cls, dt: str) -> datetime:
        return datetime.strptime(dt, "%d-%m-%Y")

    @field_serializer("date")
    @classmethod
    def serialize_date(cls, dt: datetime) -> str:
        return dt.strftime("%d-%m-%Y")

class GetSolanaDailyTransactionFeesResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Solana Daily Transaction Fees" endpoint.
    """
    result: GetSolanaDailyTransactionFeesResult

# classes used on GET "Tagged Tokens List" endpoint
# Response
class GetTaggedTokensListPagination(BaseModel):
    """
        Model used to identify the pagination of the GET "Blocks" endpoint.
    """
    next: str | None = None
    previous: str | None = None

class GetTaggedTokensListDataData(BaseModel):
    """
        Model used to identify the data of a token inside the GET "Tagged Tokens List" endpoint.
    """
    mint: str
    token_name: str = Field(alias = "tokenName")
    symbol: str
    decimals: int
    description: str
    logo: str
    tags: list[str]
    verified: str
    network: list[str]
    metadata_token: str = Field(alias = "metadataToken")

class GetTaggedTokensListData(BaseModel):
    """
        Model used to identify the data of the GET "Tagged Tokens List" endpoint.
    """
    token: str = Field(alias = "tokenHash")
    data: GetTaggedTokensListDataData

class GetTaggedTokensListResult(BaseModel):
    """
        Model used to identify the result of the GET "Tagged Tokens List" endpoint.
    """
    data: list[GetTaggedTokensListData]
    pagination: GetTaggedTokensListPagination

class GetTaggedTokensListResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Tagged Tokens List" endpoint.
    """
    result: GetTaggedTokensListResult

# classes used on GET "Token Info (v0)" endpoint
# Response
class GetTokenInfoV0Result(GetTaggedTokensListData):
    """
        Model used to identify the data of the GET "Token Info (v0)" endpoint.
    """
    pass

class GetTokenInfoV0Response(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Token Info (v0)" endpoint.
    """
    result: GetTokenInfoV0Result

# classes used on POST "Token Multiple Info (v0)" endpoint
# Response
class PostTokenMultipleInfoV0Result(GetTaggedTokensListData):
    """
        Model used to identify the data of the POST "Token Multiple Info (v0)" endpoint
    """
    pass

class PostTokenMultipleInfoV0Response(SolanaFMBaseResponse):
    """
        Model used to identify the response of the POST "Token Multiple Info (v0)" endpoint.
    """
    result: list[PostTokenMultipleInfoV0Result]

# classes used on GET "Token Info (v1)" endpoint
# Response
class GetTokenInfoV1ChainInfo(BaseModel):
    """
        Model used to identify the chain metadata of the token in the GET "Token Info (v1)" endpoint.
    """
    name: str
    symbol: str
    metadata: str
    update_authority: str = Field(alias = "updateAuthority")
    is_master_edition: bool | None = Field(default = None, alias = "isMasterEdition")
    edition: str | None = None
    uri: str
    seller_fee_basis_points: int = Field(alias = "sellerFeeBasisPoints")
    primary_sale_happened: bool = Field(alias = "primarySaleHappened")
    is_mutable: bool = Field(alias = "isMutable")
    creators: list[str]
    rule_set: str | None = Field(default = None, alias = "ruleSet")
    collection: str | None = None
    collection_details: str | None = Field(default = None, alias = "collectionDetails")
    uses: str | None = None

class GetTokenInfoV1OffChainInfo(GetTokenInfoV1ChainInfo):
    """
        Model used to identify the off-chain metadata of the token in the GET "Token Info (v1)" endpoint.
    """
    pass

class GetTokenInfoV1OnChainInfo(GetTokenInfoV1ChainInfo):
    """
        Model used to identify the on-chain metadata of the token in the GET "Token Info (v1)" endpoint.
    """
    pass

class GetTokenInfoV1TokenMetadata(BaseModel):
    """
        Model used to identify the metadata of the token in the GET "Token Info (v1)" endpoint.
    """
    on_chain_info: GetTokenInfoV1OnChainInfo | None = Field(default = None, alias = "onChainInfo")
    off_chain_info: GetTokenInfoV1OffChainInfo | None = Field(default = None, alias = "offChainInfo")

class GetTokenInfoV1TokenList(BaseModel):
    """
        Model used to identify the token list in the GET "Token Info (v1)" endpoint.
    """
    name: str
    symbol: str
    image: str
    extensions: dict[str, str]
    chain_id: int = Field(alias = "chainId")

class GetTokenInfoV1Response(BaseModel):
    """
        Model used to identify the response of the GET "Token Info (v0)" endpoint.
    """
    mint: str
    decimals: int
    freeze_authority: str | None = Field(default = None, alias = "freezeAuthority")
    mint_authority: str | None = Field(default = None, alias = "mintAuthority")
    token_type: str = Field(alias = "tokenType")
    token_list: GetTokenInfoV1TokenList = Field(alias = "tokenList")
    token_metadata: GetTokenInfoV1TokenMetadata = Field(alias = "tokenMetadata")

# classes used on POST "Token Multiple Info (v1)" endpoint
# Response
class PostTokenMultipleInfoV1Response(BaseModel):
    """
        Model used to identify the response of the POST "Token Multiple Info (v1)" endpoint.
    """
    tokens: dict[str, GetTokenInfoV1Response]

# classes used on POST "User's Token Accounts" endpoint
# Response
class PostUserTokenAccountsInfoExtensionStateTransferFee(BaseModel):
    """
        Model used to identify the transfer fee of the extension state of the token in the POST "User's Token Accounts" endpoint.
    """
    epoch: int
    maximum_fee: int = Field(alias = "maximumFee")
    transfer_fee_basis_points: int = Field(alias = "transferFeeBasisPoints")

class PostUserTokenAccountsInfoExtensionState(BaseModel):
    """
        Model used to identify the state of the extension of the token in the POST "User's Token Accounts" endpoint.
    """
    newer_transfer_fee: PostUserTokenAccountsInfoExtensionStateTransferFee | None = Field(default = None, alias = "newerTransferFee")
    older_transfer_fee: PostUserTokenAccountsInfoExtensionStateTransferFee | None = Field(default = None, alias = "olderTransferFee")
    withheld_amount: int | None = Field(default = None, alias = "withheldAmount")
    withdraw_withheld_authority: str | None = Field(default = None, alias = "withdrawWithheldAuthority")
    transfer_fee_config_authority: str | None = Field(default = None, alias = "transferFeeConfigAuthority")

class PostUserTokenAccountsInfoExtension(BaseModel):
    """
        Model used to identify the extension of the token in the POST "User's Token Accounts" endpoint.
    """
    extension: str
    state: PostUserTokenAccountsInfoExtensionState | None = None

class PostUserTokenAccountsInfoTokenAmount(BaseModel):
    """
        Model used to identify the token amount of the token in the POST "User's Token Accounts" endpoint.
    """
    amount: int
    decimals: int
    ui_amount: float = Field(alias = "uiAmount")
    ui_amount_string: str = Field(alias = "uiAmountString")

class PostUserTokenAccountsInfo(BaseModel):
    """
        Model used to identify the info of the token of the POST "User's Token Accounts" endpoint.
    """
    extensions: list[PostUserTokenAccountsInfoExtension] | None = None
    is_native: bool = Field(alias = "isNative")
    mint: str
    owner: str
    state: str
    token_amount: PostUserTokenAccountsInfoTokenAmount = Field(alias = "tokenAmount")

class PostUserTokenAccounts(BaseModel):
    """
        Model used to identify the token's account of the POST "User's Token Accounts" endpoint.
    """
    id: str = Field(alias = "_id")
    info: PostUserTokenAccountsInfo
    slot: int

class PostUserTokenAccountsResponse(BaseModel):
    """
        Model used to identify the response of the POST "User's Token Accounts" endpoint.
    """
    sol_balance: int | None = Field(default = None, alias = "solBalance")
    token_accounts: list[PostUserTokenAccounts] = Field(alias = "tokenAccounts")

# classes used on GET "Mint Token Accounts" endpoint
# Response
class GetMintTokenAccountsTokenAccounts(PostUserTokenAccounts):
    """
        Model used to identify the token accounts of the GET "Mint Token Accounts" endpoint.
    """
    pass

class GetMintTokenAccountsResponse(BaseModel):
    """
        Model used to identify the response of the GET "Mint Token Accounts" endpoint.
    """
    token_accounts: list[GetMintTokenAccountsTokenAccounts] = Field(alias = "tokenAccounts")
    total_item_count: int = Field(alias = "totalItemCount")

# classes used on GET "On-Chain Token Data" endpoint
# Response
class GetOnChainTokenDataInfoExtension(PostUserTokenAccountsInfoExtension):
    """
        Model used to identify the extension of the token in the GET "On-Chain Token Data" endpoint.
    """
    pass

class GetOnChainTokenDataInfo(BaseModel):
    """
        Model used to identify the info of the token in the GET "On-Chain Token Data" endpoint.
    """
    decimals: int
    extensions: list[GetOnChainTokenDataInfoExtension] | None = None
    freeze_authority: str | None = Field(default = None, alias = "freezeAuthority")
    is_initialized: bool = Field(alias = "isInitialized")
    mint_authority: str | None = Field(default = None, alias = "mintAuthority")
    supply: str

class GetOnChainTokenDataResponse(BaseModel):
    """
        Model used to identify the response of the GET "On-Chain Token Data" endpoint.
    """
    id: str
    info: GetOnChainTokenDataInfo
    slot: int
    type: str | None = None

# classes used on GET "Token Supply" endpoint
# Response
class GetTokenSupplyResponse(BaseModel):
    """
        Model used to identify the response of the GET "Token Supply" endpoint.
    """
    circulating_supply: float = Field(alias = "circulatingSupply")
    token_withheld_amount: int | None = Field(default = None, alias = "tokenWithheldAmount")
    user_total_withheld_amount: int = Field(alias = "userTotalWithheldAmount")
    total_withheld_amount: int = Field(alias = "totalWithheldAmount")
    real_circulating_supply: float = Field(alias = "realCirculatingSupply")
    decimals: int

# classes used on GET "Transfer Transactions" endpoint
# Response
class GetTransferTransactionsResult(GetAccountTransfersResults):
    """
        Model used to identify the result of the GET "Transfer Transactions" endpoint.
    """
    pass

class GetTransferTransactionsResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the GET "Transfer Transactions" endpoint.
    """
    result: GetTransferTransactionsResult

# classes used on POST "Multiple Transfer Transactions" endpoint
# Response
class PostMultipleTransferTransactionsResult(GetAccountTransfersResults):
    """
        Model used to identify the result of the POST "Multiple Transfer Transactions" endpoint.
    """
    pass

class PostMultipleTransferTransactionsResponse(SolanaFMBaseResponse):
    """
        Model used to identify the response of the POST "Multiple Transfer Transactions" endpoint.
    """
    result: list[PostMultipleTransferTransactionsResult]

# classes used on GET "All Transfer Actions" endpoint
# Response
class GetAllTransferActionsResponse(BaseModel):
    """
        Model used to identify the response of the GET "All Transfer Actions" endpoint.
    """
    actions: list[str]