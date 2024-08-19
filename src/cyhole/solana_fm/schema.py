from pydantic import BaseModel, Field, field_serializer

class SolanaFMPagination(BaseModel):
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

    limit: int = Field(default = 1, le = 1000, gt = 1)
    """The number of transactions to return."""

    page: int = Field(default = 1, gt = 1)
    """The page number to return."""

    @field_serializer("mints", "programs")
    @classmethod
    def serialize_str_list_input(cls, str_input: str | list[str] | None) -> str | None:
        return ",".join(str_input) if str_input else None

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

class GetAccountTransactionsResponse(BaseModel):
    """
        Model used to identify the response of the GET "Account - Transactions" endpoint.
    """
    status: str
    message: str
    result: GetAccountTransactionsResult