from datetime import datetime
from pydantic import BaseModel, Field, field_validator, field_serializer

from ...solscan.v2.param import SolscanActivityTransferType, SolscanPageSizeType, SolscanFlowType
from ...solscan.v2.exception import SolscanAccountTransferInvalidAmountRange, SolscanAccountTransferInvalidTimeRange

# GET - Account Transfer
# Param
class GetAccountTransferParam(BaseModel):
    """
        Model used to identify the parameters of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """

    activity_type: str | list[str] | None = Field(default = None, serialization_alias = "activity_type[]")
    """
        Activity type of the account transfer.
        The supported types are available on [`SolscanActivityTransferType`][cyhole.solscan.v2.param.SolscanActivityTransferType].
    """

    token_account: str | None = None
    """Token account address to filter."""

    from_address: str | None = Field(default = None, serialization_alias = "from")
    """From address to filter."""

    to_address: str | None = Field(default = None, serialization_alias = "to")
    """To address to filter."""

    token_address: str | None = Field(default = None, serialization_alias = "token")
    """Token address to filter."""

    amount_range: tuple[int, int] | None = Field(default = None, serialization_alias = "amount[]")
    """Amount range to filter for the account transfers (from, to)."""

    time_range: tuple[datetime, datetime] | None = Field(default = None, serialization_alias = "block_time[]")
    """Block times to filter by (from, to)."""

    exclude_amount_zero: bool | None = None
    """Exclude transfers with zero amount."""

    flow_direction: str | None = Field(default = None, serialization_alias = "flow")
    """Flow direction to filter."""

    page: int = Field(default = 1, ge = 1)
    """
        Page number to get the account transfers.
        The supported types are available on [`SolscanFlowType`][cyhole.solscan.v2.param.SolscanFlowType].
    """

    page_size: int = Field(default = SolscanPageSizeType.SIZE_10.value)
    """
        Number of account transfers per page. 
        The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
    """

    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value: list[str] | str | None) -> str | list[str] | None:
        if isinstance(value, str):
            SolscanActivityTransferType.check(value)
        elif isinstance(value, list):
            for item in value:
                SolscanActivityTransferType.check(item)
        return value

    @field_validator("flow_direction")
    @classmethod
    def validate_flow_direction(cls, value: str | None) -> str | None:
        if value:
            SolscanFlowType.check(value)
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

    @field_serializer("time_range")
    @classmethod
    def serialize_time_range(cls, value: tuple[datetime, datetime] | None) -> tuple[int, int] | None:
        if value:
            return (int(value[0].timestamp()), int(value[1].timestamp()))
        return

# Response
class GetAccountTransferData(BaseModel):
    """
        Model used to parse the data of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """
    block_id: int
    transaction_id: str = Field(alias= "trans_id")
    block_time_unix_utc: int = Field(alias= "block_time")
    activity_type: str
    from_address: str
    to_address: str
    token_address: str
    token_decimals: int
    amount: int
    flow_type: str = Field(alias= "flow")
    time: datetime

class GetAccountTransferResponse(BaseModel):
    """
        Model used to parse the response of the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint.
    """
    success: bool
    data: list[GetAccountTransferData]