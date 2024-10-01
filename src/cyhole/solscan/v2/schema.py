from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel, Field, field_validator, field_serializer

from ...solscan.v2.param import (
    SolscanNFTCollectionPageSizeType,
    SolscanNFTDaysRangeType,
    SolscanNFTSortType,
    SolscanActivityTransferType,
    SolscanActivityDefiType,
    SolscanActivityNFTType,
    SolscanPageSizeType,
    SolscanOrderType,
    SolscanFlowType
)
from ...solscan.v2.exception import SolscanInvalidAmountRange, SolscanInvalidTimeRange

# General

class SolscanBaseResponse(BaseModel):
    """
        Model used to identify the base response of the Solscan API.
    """
    success: bool

# class used on Solscan HTTPErrors
class SolscanError(BaseModel):
    code: int
    message: str

class SolscanHTTPError(SolscanBaseResponse):
    """
        Solscan API returns an error schema on failed request 
        that can be used to investigated the error. This schema 
        is used to strandardise the HTTPErrors.
    """
    errors: SolscanError

class SolscanTransferParam(BaseModel):
    """
        Model used to identify the parameters of the Solscan transfer (Account/Token).
    """

    activity_type: str | list[str] | None = Field(default = None, serialization_alias = "activity_type[]")
    """
        Activity type of the account transfer.
        The supported types are available on [`SolscanActivityTransferType`][cyhole.solscan.v2.param.SolscanActivityTransferType].
    """

    from_address: str | None = Field(default = None, serialization_alias = "from")
    """From address to filter."""

    to_address: str | None = Field(default = None, serialization_alias = "to")
    """To address to filter."""

    amount_range: tuple[int, int] | None = Field(default = None, serialization_alias = "amount[]")
    """Amount range to filter for the account transfers (from, to)."""

    time_range: tuple[datetime, datetime] | None = Field(default = None, serialization_alias = "block_time[]")
    """Block times to filter by (from, to)."""

    exclude_amount_zero: bool | None = None
    """Exclude transfers with zero amount."""

    page: int = Field(default = 1, ge = 1)
    """Page number to get the account transfers."""

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of account transfers per page. 
        The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
    """

    # Validators
    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value: list[str] | str | None) -> str | list[str] | None:
        if isinstance(value, str):
            SolscanActivityTransferType.check(value)
        elif isinstance(value, list):
            for item in value:
                SolscanActivityTransferType.check(item)
        return value

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, value: int) -> int:
        SolscanPageSizeType.check(value)
        return value

    @field_validator("amount_range")
    @classmethod
    def validate_amount_range(cls, value: tuple[int, int] | None) -> tuple[int, int] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidAmountRange(f"Invalid amount range: {value}")
        return value

    @field_validator("time_range")
    @classmethod
    def validate_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[datetime, datetime] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidTimeRange(f"Invalid time range: {value}")
        return value

    # Serializers
    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

    @field_serializer("exclude_amount_zero")
    @classmethod
    def serialize_exclude_amount_zero(cls, value: bool | None) -> str | None:
        if value is not None:
            return "true" if value else "false"
        return

class SolscanTransferData(BaseModel):
    """
        Model used to parse the data of the Solscan transfer (Account/Token).
    """
    block_id: int
    transaction_id: str = Field(alias = "trans_id")
    block_time_unix_utc: int = Field(alias = "block_time")
    activity_type: str
    from_address: str
    to_address: str
    token_address: str
    token_decimals: int
    amount: int
    time: datetime

class SolscanDefiActivitiesParam(BaseModel):
    """
        Model used to identify the parameters of the Solscan defi activities (Account/Token).
    """

    activity_type: str | list[str] | None = Field(default = None, serialization_alias = "activity_type[]")
    """
        Activity type of the account defi activities.
        The supported types are available on [`SolscanActivityDefiType`][cyhole.solscan.v2.param.SolscanActivityDefiType].
    """

    from_address: str | None = Field(default = None, serialization_alias = "from")
    """From address to filter."""

    platform_address: str | list[str] | None = Field(default = None, serialization_alias = "platform[]")
    """Platform addresses to filter."""

    source_address: str | list[str] | None = Field(default = None, serialization_alias = "source[]")
    """Source addresses to filter."""

    time_range: tuple[datetime, datetime] | None = Field(default = None, serialization_alias = "block_time[]")
    """Block times to filter by (from, to)."""

    page: int = Field(default = 1, ge = 1)
    """Page number to get the account transfers."""

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of account defi activities per page. 
        The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
    """

    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value: list[str] | str | None) -> str | list[str] | None:
        if isinstance(value, str):
            SolscanActivityDefiType.check(value)
        elif isinstance(value, list):
            for item in value:
                SolscanActivityDefiType.check(item)
        return value

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, value: int) -> int:
        SolscanPageSizeType.check(value)
        return value

    @field_validator("time_range")
    @classmethod
    def validate_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[datetime, datetime] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidTimeRange(f"Invalid time range: {value}")
        return value

    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

class SolscanDefiActivitiesChildRoute(BaseModel):
    token_1: str = Field(alias = "token1")
    token_1_decimals: int = Field(alias = "token1_decimals")
    amount_1: int = Field(alias= "amount1")
    token_2: str | None = Field(default = None, alias = "token2")
    token_2_decimals: int | None = Field(default = None, alias = "token2_decimals")
    amount_2: int | None = Field(default = None, alias = "amount2")

class SolscanDefiActivitiesRoute(SolscanDefiActivitiesChildRoute):
    child_routes: list[SolscanDefiActivitiesChildRoute] | None = None

class SolscanDefiActivitiesData(BaseModel):
    """
        Model used to parse the data of the Solscan defi activities (Account/Token).
    """
    block_id: int
    transaction_id: str = Field(alias = "trans_id")
    block_time_unix_utc: int = Field(alias = "block_time")
    activity_type: str
    from_address: str
    source_addresses: list[str] = Field(alias = "sources")
    platform_address: str = Field(alias = "platform")
    routes: list[SolscanDefiActivitiesRoute] | None = None
    time: datetime

# GET - Account Transfer
# Param
class GetAccountTransferParam(SolscanTransferParam):
    """
        Model used to identify the parameters of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """

    token_account: str | None = None
    """Token account address to filter."""

    token_address: str | None = Field(default = None, serialization_alias = "token")
    """Token address to filter."""

    flow_direction: str | None = Field(default = None, serialization_alias = "flow")
    """
        Flow direction to filter.
        The supported types are available on [`SolscanFlowType`][cyhole.solscan.v2.param.SolscanFlowType].
    """

    # Validators

    @field_validator("flow_direction")
    @classmethod
    def validate_flow_direction(cls, value: str | None) -> str | None:
        if value:
            SolscanFlowType.check(value)
        return value

# Response
class GetAccountTransferData(SolscanTransferData):
    """
        Model used to parse the data of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """
    flow_type: str = Field(alias = "flow")

class GetAccountTransferResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """
    data: list[GetAccountTransferData]

# GET - Account Token/NFT Account
class GetAccountTokenNFTAccountData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Token/NFT Account](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-token-accounts)** of **V2** API endpoint.
    """
    token_account: str
    token_address: str
    amount: int
    token_decimals: int
    owner: str

class GetAccountTokenNFTAccountResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Token/NFT Account](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-token-accounts)** of **V2** API endpoint.
    """
    data: list[GetAccountTokenNFTAccountData]

# GET - Account Defi Activities
# Param
class GetAccountDefiActivitiesParam(SolscanDefiActivitiesParam):
    """
        Model used to identify the parameters of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    pass

# Response
class GetAccountDefiActivitiesData(SolscanDefiActivitiesData):
    """
        Model used to parse the data of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    pass

class GetAccountDefiActivitiesResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    data: list[GetAccountDefiActivitiesData]

# GET - Account Balance Change Activities
# Param
class GetAccountBalanceChangeActivitiesParam(BaseModel):
    """
        Model used to identify the parameters of the GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** of **V2** API endpoint.
    """

    token_address: str | None = Field(default = None, serialization_alias = "token")
    """Token address to filter."""

    time_range: tuple[datetime, datetime] | None = Field(default = None, serialization_alias = "block_time[]")
    """Block times to filter by (from, to)."""

    remove_spam: bool | None = None
    """The query parameter to determine if spam activities have been removed or not."""

    amount_range: tuple[int, int] | None = Field(default = None, serialization_alias = "amount[]")
    """Amount range to filter for the account transfers (from, to)."""

    flow_direction: str | None = Field(default = None, serialization_alias = "flow")
    """
        Flow direction to filter.
        The supported types are available on [`SolscanFlowType`][cyhole.solscan.v2.param.SolscanFlowType].
    """

    page: int = Field(default = 1, ge = 1)
    """Page number to get the account transfers."""

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of account balance change activities per page. 
        The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
    """

    # Validators
    @field_validator("flow_direction")
    @classmethod
    def validate_flow_direction(cls, value: str | None) -> str | None:
        if value:
            SolscanFlowType.check(value)
        return value

    @field_validator("amount_range")
    @classmethod
    def validate_amount_range(cls, value: tuple[int, int] | None) -> tuple[int, int] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidAmountRange(f"Invalid amount range: {value}")
        return value

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, value: int) -> int:
        SolscanPageSizeType.check(value)
        return value

    @field_validator("time_range")
    @classmethod
    def validate_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[datetime, datetime] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidTimeRange(f"Invalid time range: {value}")
        return value

    # Serializers
    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

    @field_serializer("remove_spam")
    @classmethod
    def serialize_remove_spam(cls, value: bool | None) -> str | None:
        if value is not None:
            return "true" if value else "false"
        return

# Response
class GetAccountBalanceChangeActivitiesData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** of **V2** API endpoint.
    """
    block_id: int
    block_time_unix_utc: int = Field(alias = "block_time")
    transaction_id: str = Field(alias = "trans_id")
    address: str
    token_address: str
    token_account: str
    token_decimals: int
    amount: int
    pre_balance: int
    post_balance: int
    change_type: str
    fee: int
    time: datetime

class GetAccountBalanceChangeActivitiesResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** of **V2** API endpoint.
    """
    data: list[GetAccountBalanceChangeActivitiesData]

# GET - Account Transactions
# Response
class GetAccountTransactionsInstruction(BaseModel):
    """
        Model used to parse the instructions of the GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** of **V2** API endpoint.
    """
    type: str
    program: str
    program_id: str

class GetAccountTransactionsData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** of **V2** API endpoint.
    """
    slot: int
    fee: int
    status: str
    signer: list[str]
    block_time_unix_utc: int = Field(alias = "block_time")
    transaction_id: str = Field(alias = "tx_hash")
    parsed_instructions: list[GetAccountTransactionsInstruction]
    program_ids: list[str]
    time: datetime

class GetAccountTransactionsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** of **V2** API endpoint.
    """
    data: list[GetAccountTransactionsData]

# GET - Account Stake
# Response
class GetAccountStakeData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** of **V2** API endpoint.
    """
    amount: int
    role: list[str]
    status: str
    type: str
    voter: str
    active_stake_amount: int
    delegated_stake_amount: int
    sol_balance: int
    total_reward: str
    stake_account: str
    activation_epoch: int
    stake_type: int

class GetAccountStakeResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** of **V2** API endpoint.
    """
    data: list[GetAccountStakeData]

# GET - Account Detail
# Response
class GetAccountDetailData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** of **V2** API endpoint.
    """
    account: str
    lamports: int
    type: str
    executable: bool
    owner_program: str
    rent_epoch: int
    is_oncurve: bool

class GetAccountDetailResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** of **V2** API endpoint.
    """
    data: GetAccountDetailData

# GET - Account Rewards Export
class GetAccountRewardsExportResponse(BaseModel):
    """
        This class refers to the response model of GET **[Account ExportRewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** of **V2** API endpoint.
    """
    csv: str

# GET - Token Transfer
# Param
class GetTokenTransferParam(SolscanTransferParam):
    """
        Model used to identify the parameters of the GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** of **V2** API endpoint.
    """
    pass

# Response
class GetTokenTransferData(SolscanTransferData):
    """
        Model used to parse the data of the GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** of **V2** API endpoint.
    """
    pass

class GetTokenTransferResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** of **V2** API endpoint.
    """
    data: list[GetTokenTransferData]

# Get - Token Defi Activities
# Param
class GetTokenDefiActivitiesParam(SolscanDefiActivitiesParam):
    """
        Model used to identify the parameters of the GET **[Token Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** of **V2** API endpoint.
    """

    token_address: str | None = Field(default = None, serialization_alias = "token")
    """Token address to filter."""

# Response
class GetTokenDefiActivitiesData(SolscanDefiActivitiesData):
    """
        Model used to parse the data of the GET **[Token Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** of **V2** API endpoint.
    """
    pass

class GetTokenDefiActivitiesResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** of **V2** API endpoint.
    """
    data: list[GetTokenDefiActivitiesData]

# GET - Token Markets
# Response
class GetTokenMarketsData(BaseModel):
    """
        Model used to parse the data of the GET **[Token Markets](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-markets)** of **V2** API endpoint.
    """
    pool_id: str
    program_id: str
    token_1: str
    token_2: str
    token_account_1: str
    token_account_2: str
    total_trades_24h: int
    total_trades_prev_24h: int
    total_volume_24h: int
    total_volume_prev_24h: int

class GetTokenMarketsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Markets](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-markets)** of **V2** API endpoint.
    """
    data: list[GetTokenMarketsData]

# GET - Token List
# Response
class GetTokenListData(BaseModel):
    """
        Model used to parse the data of the GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-list)** of **V2** API endpoint.
    """
    address: str
    decimals: int
    name: str | None = None
    symbol: str | None = None
    market_cap: int | None = None
    price: float | None = None
    price_24h_change: float | None = None
    holder: int | None = None
    created_time_unix_utc: int | None = Field(default = None, alias = "created_time")

class GetTokenListResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-list)** of **V2** API endpoint.
    """
    data: list[GetTokenListData]

# GET - Token Trending
# Response
class GetTokenTrendingData(BaseModel):
    """
        Model used to parse the data of the GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** of **V2** API endpoint.
    """
    address: str
    decimals: int
    name: str | None = None
    symbol: str | None = None

class GetTokenTrendingResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** of **V2** API endpoint.
    """
    data: list[GetTokenTrendingData]

# GET - Token Price
# Response
class GetTokenPriceData(BaseModel):
    """
        Model used to parse the data of the GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** of **V2** API endpoint.
    """
    date: datetime = Field(strict = True)
    price: float

    # Validators
    @field_validator("date", mode = "before")
    @classmethod
    def validate_date(cls, value: int) -> datetime:
        return datetime.strptime(str(value), "%Y%m%d")

    # Serializers
    @field_serializer("date")
    @classmethod
    def serialize_date(cls, value: datetime) -> int:
        return int(value.strftime("%Y%m%d"))

class GetTokenPriceResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** of **V2** API endpoint.
    """
    data: list[GetTokenPriceData]

# GET - Token Holders
# Response
class GetTokenHoldersHolder(BaseModel):
    """
        Model used to parse the holder data of the GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** of **V2** API endpoint.
    """
    address: str
    amount: int
    decimals: int
    owner: str
    rank: int

class GetTokenHoldersData(BaseModel):
    """
        Model used to parse the data of the GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** of **V2** API endpoint.
    """
    total_holders: int = Field(alias = "total")
    holders: list[GetTokenHoldersHolder] = Field(alias = "items")

class GetTokenHoldersResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** of **V2** API endpoint.
    """
    data: GetTokenHoldersData

# GET - Token Meta
# Response
class GetTokenMetaData(BaseModel):
    """
        Model used to parse the meta data of the GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** of **V2** API endpoint.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    icon: str | None = None
    decimals: int
    price: float
    volume_24h: int
    market_cap: int
    market_cap_rank: int
    price_change_24h: float
    supply: int
    holder: int

class GetTokenMetaResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** of **V2** API endpoint.
    """
    data: GetTokenMetaData

# GET - NFT News
# Response
class GetNFTNewsNftInfoMetaAttribute(BaseModel):
    trait_type: str
    value: str | int

class GetNFTNewsNftInfoMetaCollection(BaseModel):
    name: str
    family: str

class GetNFTNewsNftInfoMetaFile(BaseModel):
    uri: str
    type: str

class GetNFTNewsNftInfoMetaCreator(BaseModel):
    address: str
    share: int

class GetNFTNewsNftInfoMetaProperty(BaseModel):
    files: list[GetNFTNewsNftInfoMetaFile]
    category: str | None = None
    creators: list[GetNFTNewsNftInfoMetaCreator] | None = None

class GetNFTNewsNftInfoMeta(BaseModel):
    name: str
    symbol: str | None = None
    description: str
    seller_fee_basis_points: int | None = None
    image: str
    animation_url: str | None = None
    external_url: str | None = None
    attributes: list[GetNFTNewsNftInfoMetaAttribute] | None = None
    tags: list[str] | None = None
    collection: GetNFTNewsNftInfoMetaCollection | None = None
    properties: GetNFTNewsNftInfoMetaProperty | None = None
    edition: int | None = None
    creators: list[GetNFTNewsNftInfoMetaCreator] | None = None
    compiler: str | None = None
    dna: str | None = None
    date: int | None = None
    process_video: str | None = Field(default = None, alias = "processVideo")

class GetNFTNewsNftInfoDataCreator(BaseModel):
    address: str
    verified: int
    share: int

class GetNFTNewsNftInfoData(BaseModel):
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int = Field(alias = "sellerFeeBasisPoints")
    creators: list[GetNFTNewsNftInfoDataCreator]
    id: int

class GetNFTNewsNftInfo(BaseModel):
    address: str
    created_time_unix_utc: int = Field(alias = "createdTime")
    mint_transaction: str = Field(alias = "mintTx")
    collection: str
    collection_id: str = Field(alias = "collectionId")
    collection_key: str | None = Field(default = None, alias = "collectionKey")
    data: GetNFTNewsNftInfoData
    meta: GetNFTNewsNftInfoMeta

class GetNFTNewsNft(BaseModel):
    info: GetNFTNewsNftInfo

class GetNFTNewsData(BaseModel):
    """
        Model used to parse the data of the GET **[NFT News](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-news)** of **V2** API endpoint.
    """
    nfts: list[GetNFTNewsNft] = Field(alias = "data")
    total: int

class GetNFTNewsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[NFT News](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-news)** of **V2** API endpoint.
    """
    data: GetNFTNewsData

# GET - NFT Activities
# Param
class GetNFTActivitiesParam(BaseModel):
    """
        Model used to identify the parameters of the GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** of **V2** API endpoint.
    """

    from_address: str | None = Field(default = None, serialization_alias = "from")
    """From address to filter."""

    to_address: str | None = Field(default = None, serialization_alias = "to")
    """To address to filter."""

    source_address: str | list[str] | None = Field(default = None, serialization_alias = "source[]")
    """Source addresses to filter."""

    activity_type: str | list[str] | None = Field(default = None, serialization_alias = "activity_type[]")
    """
        Activity type of the NFT activities.
        The supported types are available on [`SolscanActivityNFTType`][cyhole.solscan.v2.param.SolscanActivityNFTType].
    """

    token_address: str | None = Field(default = None, serialization_alias = "token")
    """Token address to filter."""

    collection_address: str | None = Field(default = None, serialization_alias = "collection")
    """Collection address to filter."""

    currency_token_address: str | None = Field(default = None, serialization_alias = "currency_token")
    """Currency token address to filter."""

    amount_range: tuple[int, int] | None = Field(default = None, serialization_alias = "price[]")
    """Amount range to filter for the NFT activities (from, to)."""

    time_range: tuple[datetime, datetime] | None = Field(default = None, serialization_alias = "block_time[]")
    """Block times to filter by (from, to)."""

    page: int = Field(default = 1, ge = 1)
    """Page number to get the NFT activities."""

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of NFT activities per page. 
        The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
    """

    # Validators
    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value: list[str] | str | None) -> str | list[str] | None:
        if isinstance(value, str):
            SolscanActivityNFTType.check(value)
        elif isinstance(value, list):
            for item in value:
                SolscanActivityNFTType.check(item)
        return value

    @field_validator("amount_range")
    @classmethod
    def validate_amount_range(cls, value: tuple[int, int] | None) -> tuple[int, int] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidAmountRange(f"Invalid amount range: {value}")
        return value

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, value: int) -> int:
        SolscanPageSizeType.check(value)
        return value

    @field_validator("time_range")
    @classmethod
    def validate_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[datetime, datetime] | None:
        if value and value[0] > value[1]:
            raise SolscanInvalidTimeRange(f"Invalid time range: {value}")
        return value

    # Serializers
    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

# Response
class GetNFTActivitiesData(BaseModel):
    """
        Model used to parse the data of the GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** of **V2** API endpoint.
    """
    block_id: int
    transaction_id: str = Field(alias = "trans_id")
    block_time_unix_utc: int = Field(alias = "block_time")
    activity_type: str
    from_address: str
    to_address: str
    token_address: str
    marketplace_address: str
    collection_address: str
    amount: int
    price: int
    currency_token: str
    currency_decimals: int
    time: datetime

class GetNFTActivitiesResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** of **V2** API endpoint.
    """
    data: list[GetNFTActivitiesData]

# GET - NFT Collection Lists
# Param
class GetNFTCollectionListsParam(BaseModel):
    """
        Model used to identify the parameters of the GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** of **V2** API endpoint.
    """

    days_range: int | None = Field(default = None, serialization_alias = "range")
    """
        Number of days to filter the NFT collection lists.
        The supported types are available on [`SolscanNFTDaysRangeType`][cyhole.solscan.v2.param.SolscanNFTDaysRangeType].
    """

    order_by: str | None = Field(default = None, serialization_alias = "sort_order")
    """
        Order by to filter the NFT collection lists.
        The supported types are available on [`SolscanOrderType`][cyhole.solscan.v2.param.SolscanOrderType].
    """

    sort_by: str | None = Field(default = None, serialization_alias = "sort_by")
    """
        Sort by to filter the NFT collection lists.
        The supported types are available on [`SolscanNFTSortType`][cyhole.solscan.v2.param.SolscanNFTSortType].
    """

    page: int = Field(default = 1, ge = 1)
    """Page number to get the NFT collection lists."""

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of NFT activities per page. 
        The supported types are available on [`SolscanNFTCollectionPageSizeType`][cyhole.solscan.v2.param.SolscanNFTCollectionPageSizeType].
    """

    collection_address: str | None = Field(default = None, serialization_alias = "collection")
    """Collection address to filter."""

    # Validators
    @field_validator("days_range")
    @classmethod
    def validate_days_range(cls, value: int | None) -> int | None:
        if value:
            SolscanNFTDaysRangeType.check(value)
        return value

    @field_validator("order_by")
    @classmethod
    def validate_order_by(cls, value: str | None) -> str | None:
        if value:
            SolscanOrderType.check(value)
        return value

    @field_validator("sort_by")
    @classmethod
    def validate_sort_by(cls, value: str | None) -> str | None:
        if value:
            SolscanNFTSortType.check(value)
        return value

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, value: int) -> int:
        SolscanNFTCollectionPageSizeType.check(value)
        return value

# Response
class GetNFTCollectionListsData(BaseModel):
    """
        Model used to parse the data of the GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** of **V2** API endpoint.
    """
    collection_address: str = Field(alias = "collection_id")
    floor_price: float
    items: int
    marketplaces: list[str]
    volumes: float
    volumes_change_24h: str | None = None

class GetNFTCollectionListsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** of **V2** API endpoint.
    """
    data: list[GetNFTCollectionListsData]

# GET - NFT Collection Items
# Response
class GetNFTCollectionItemData(GetNFTNewsNftInfoData):
    pass

class GetNFTCollectionItemMeta(GetNFTNewsNftInfoMeta):
    pass

class GetNFTCollectionItemInfo(BaseModel):
    address: str
    token_name: str
    token_symbol: str
    collection_id: str
    data: GetNFTCollectionItemData
    meta: GetNFTCollectionItemMeta

class GetNFTCollectionItemStats(BaseModel):
    trade_time_unix_utc: int = Field(alias = "trade_time")
    signature: str
    market_id: str
    type: str
    price: int
    currency_token: str
    currency_decimals: int
    seller: str
    buyer: str

class GetNFTCollectionItemsData(BaseModel):
    """
        Model used to parse the data of the GET **[NFT Collection Items](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-items)** of **V2** API endpoint.
    """
    info: GetNFTCollectionItemInfo
    stats: GetNFTCollectionItemStats

class GetNFTCollectionItemsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[NFT Collection Items](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-items)** of **V2** API endpoint.
    """
    data: list[GetNFTCollectionItemsData]

# GET - Transaction Last
# Response
class GetTransactionLastInstruction(GetAccountTransactionsInstruction):
    pass

class GetTransactionLastData(BaseModel):
    """
        Model used to parse the data of the GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-last)** of **V2** API endpoint.
    """
    slot: int
    fee: int
    status: str
    signer: list[str]
    block_time_unix_utc: int = Field(alias = "block_time")
    transaction_id: str = Field(alias = "tx_hash")
    parsed_instructions: list[GetTransactionLastInstruction]
    program_ids: list[str]
    time: datetime

class GetTransactionLastResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-last)** of **V2** API endpoint.
    """
    data: list[GetTransactionLastData]

# GET - Transaction Actions
# Response
class GetTransactionActionsTransfer(BaseModel):
    source_owner: str | None = None
    source: str | None = None
    destination_owner: str | None = None
    destination: str | None = None
    transfer_type: str
    token_address: str
    decimals: int
    amount_str: str
    amount: int
    program_id: str
    outer_program_id: str | None = None
    ins_index: int
    outer_ins_index: int

class GetTransactionActionsActivityDataRouter(BaseModel):
    amm_program_id: str
    token_1: str
    token_decimal_1: int
    amount_1: int
    amount_1_str: str
    token_2: str
    token_decimal_2: int
    amount_2: int
    amount_2_str: str

# Data Unit Limit
class GetTransactionActionsActivityDataUnitLimit(BaseModel):
    compute_unit_limit: str

# Data Unit Price
class GetTransactionActionsActivityDataUnitPrice(BaseModel):
    compute_unit_price_by_microlamport: str

# Data Spl Common
class GetTransactionActionsActivityDataSplCommon(BaseModel):
    amount: int | None = None
    amount_str: str | None = None
    token_address: str
    token_decimals: int | None = None
    closed_account: str | None = None
    authority: str | None = None
    destination: str | None = None
    sync_account: str | None = None
    init_account: str | None = None
    owner: str | None = None

# Data Spl Mint/Burn
class GetTransactionActionsActivityDataSplMintBurn(BaseModel):
    account: str
    authority: str
    token_address: str
    token_decimals: int
    amount: int
    amount_str: str

# Data Token Swap
class GetTransactionActionsActivityDataTokenSwap(BaseModel):
    amm_id: str
    amm_authoriy: str | None = None
    account: str
    token_1: str
    token_2: str
    amount_1: int
    amount_1_str: str
    amount_2: int
    amount_2_str: str
    token_decimal_1: int
    token_decimal_2: int
    token_account_1_1: str | None = None
    token_account_1_2: str | None = None
    token_account_2_1: str | None = None
    token_account_2_2: str | None = None
    owner_1: str | None = None
    owner_2: str | None = None
    rounters: list[GetTransactionActionsActivityDataRouter] | None = None
    exact_amount_2: int | None = None
    exact_amount_2_str: str | None = None
    platform_fee: int | None = None
    slippage: int | None = None

# Data Create Account
class GetTransactionActionsActivityDataCreateAccount(BaseModel):
    new_account: str
    source: str
    transfer_amount: int
    transfer_amount_str: str
    program_owner: str
    space: int
    common_type: str

# Data Type Alias
GetTransactionActionsActivityData: TypeAlias = \
      GetTransactionActionsActivityDataSplMintBurn \
    | GetTransactionActionsActivityDataUnitLimit \
    | GetTransactionActionsActivityDataUnitPrice \
    | GetTransactionActionsActivityDataSplCommon \
    | GetTransactionActionsActivityDataTokenSwap \
    | GetTransactionActionsActivityDataCreateAccount

class GetTransactionActionsActivity(BaseModel):
    name: str
    activity_type: str
    program_id: str
    data: GetTransactionActionsActivityData
    ins_index: int
    outer_ins_index: int
    outer_program_id: str | None = None

class GetTransactionActionsData(BaseModel):
    """
        Model used to parse the data of the GET **[Transaction Actions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-actions)** of **V2** API endpoint.
    """
    transaction_id: str = Field(alias = "tx_hash")
    block_id: int
    block_time_unix_utc: int = Field(alias = "block_time")
    time: datetime
    fee: int
    transfers: list[GetTransactionActionsTransfer] | None = None
    activities: list[GetTransactionActionsActivity] | None = None

class GetTransactionActionsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Transaction Actions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-actions)** of **V2** API endpoint.
    """
    data: GetTransactionActionsData

# GET - Block Last
# Response
class GetBlockLastData(BaseModel):
    """
        Model used to parse the data of the GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-last)** of **V2** API endpoint.
    """
    block_id: str = Field(alias = "blockhash")
    fee_rewards: int
    transactions_count: int
    current_slot: int
    block_height: int
    block_time_unix_utc: int = Field(alias = "block_time")
    time: datetime
    parent_slot: int
    previous_block_id: str = Field(alias = "previous_block_hash")

class GetBlockLastResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-last)** of **V2** API endpoint.
    """
    data: list[GetBlockLastData]

# GET - Block Transactions
# Response
class GetBlockTransactionsInstruction(GetAccountTransactionsInstruction):
    pass

class GetBlockTransactionsDataTransaction(BaseModel):
    slot: int
    fee: int
    status: str
    signer: list[str]
    block_time_unix_utc: int = Field(alias = "block_time")
    transaction_id: str = Field(alias = "tx_hash")
    parsed_instructions: list[GetBlockTransactionsInstruction]
    program_ids: list[str]
    time: datetime

class GetBlockTransactionsData(BaseModel):
    """
        Model used to parse the data of the GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-transactions)** of **V2** API endpoint.
    """
    total: int
    transactions: list[GetBlockTransactionsDataTransaction]

class GetBlockTransactionsResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-transactions)** of **V2** API endpoint.
    """
    data: GetBlockTransactionsData

# GET - Block Detail
# Response
class GetBlockDetailData(BaseModel):
    """
        Model used to parse the data of the GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-detail)** of **V2** API endpoint.
    """
    block_id: str = Field(alias = "blockhash")
    fee_rewards: int
    transactions_count: int
    block_height: int
    block_time_unix_utc: int = Field(alias = "block_time")
    time: datetime
    parent_slot: int
    previous_block_id: str = Field(alias = "previous_block_hash")

class GetBlockDetailResponse(SolscanBaseResponse):
    """
        Model used to parse the response of the GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-detail)** of **V2** API endpoint.
    """
    data: GetBlockDetailData