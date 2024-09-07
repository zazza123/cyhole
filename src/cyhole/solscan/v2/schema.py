from datetime import datetime
from pydantic import BaseModel, Field, field_validator, field_serializer

from ...solscan.v2.param import (
    SolscanActivityTransferType,
    SolscanActivityDefiType,
    SolscanPageSizeType,
    SolscanFlowType
)
from ...solscan.v2.exception import SolscanAccountTransferInvalidAmountRange, SolscanAccountTransferInvalidTimeRange

# General

class SolscanBaseResponse(BaseModel):
    """
        Model used to identify the base response of the Solscan API.
    """
    success: bool

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
            raise SolscanAccountTransferInvalidAmountRange(f"Invalid amount range: {value}")
        return value

    @field_validator("time_range")
    @classmethod
    def validate_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[datetime, datetime] | None:
        if value and value[0] > value[1]:
            raise SolscanAccountTransferInvalidTimeRange(f"Invalid time range: {value}")
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
        if value:
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
class GetAccountDefiActivitiesParam(BaseModel):
    """
        Model used to identify the parameters of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
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
            raise SolscanAccountTransferInvalidTimeRange(f"Invalid time range: {value}")
        return value

    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

# Response
class GetAccountDefiActivitiesChildRoute(BaseModel):
    """
        Model used to parse the route of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    token_1: str = Field(alias = "token1")
    token_1_decimals: int = Field(alias = "token1_decimals")
    amount_1: int = Field(alias= "amount1")
    token_2: str | None = Field(default = None, alias = "token2")
    token_2_decimals: int | None = Field(default = None, alias = "token2_decimals")
    amount_2: int | None = Field(default = None, alias = "amount2")

class GetAccountDefiActivitiesRoute(GetAccountDefiActivitiesChildRoute):
    """
        Model used to parse the route of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    child_routes: list[GetAccountDefiActivitiesChildRoute] | None = None

class GetAccountDefiActivitiesData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Defi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint.
    """
    block_id: int
    transaction_id: str = Field(alias = "trans_id")
    block_time_unix_utc: int = Field(alias = "block_time")
    activity_type: str
    from_address: str
    source_addresses: list[str] = Field(alias = "sources")
    platform_address: str = Field(alias = "platform")
    routes: list[GetAccountDefiActivitiesRoute] | None = None
    time: datetime

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
            raise SolscanAccountTransferInvalidAmountRange(f"Invalid amount range: {value}")
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
            raise SolscanAccountTransferInvalidTimeRange(f"Invalid time range: {value}")
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
        if value:
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