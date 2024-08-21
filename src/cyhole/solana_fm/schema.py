from pydantic import BaseModel, Field, field_serializer

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

    limit: int = Field(default = 1, le = 1000, gt = 1)
    """The number of transactions to return."""

    page: int = Field(default = 1, gt = 1)
    """The page number to return."""

    @field_serializer("mint")
    @classmethod
    def serialize_str_list_input(cls, str_input: str | list[str] | None) -> str | None:
        return ",".join(str_input) if str_input else None

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