from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# classes used on GET 'Token List' endpoint
class GetTokenListInfo(BaseModel):
    name: str
    symbol: str
    address: str
    decimals: int
    liquidity: float
    volume_24h_usd: float           = Field(alias = "v24hUSD")
    market_cap: float               = Field(alias = "mc")
    volume_24h_change: float | None = Field(alias = "v24hChangePercent", default = None)
    last_trade_unix_time: float     = Field(alias = "lastTradeUnixTime")
    logo_uri: str                   = Field(alias = "logoURI")

class GetTokenListData(BaseModel):
    total: int
    update_time: datetime = Field(alias = "updateTime")
    update_unix_time: int = Field(alias = "updateUnixTime")
    tokens: list[GetTokenListInfo]

    @field_validator("update_time")
    def parse_update_time(cls, update_time_raw: str | datetime) -> datetime:
        if isinstance(update_time_raw, str):
            return datetime.strptime(update_time_raw, "%Y-%m-%dT%H:%M:%S")
        return update_time_raw


class GetTokenListResponse(BaseModel):
    """
        Model used to represent the 'Token - List' endpoint from birdeye API.
    """
    data: GetTokenListData
    success: bool

# classes used on GET 'Price' endpoint
class GetPriceData(BaseModel):
    value: float
    liquidity: float | None = None
    update_human_time: datetime = Field(alias = "updateHumanTime")
    update_unix_time: int = Field(alias = "updateUnixTime")

    @field_validator("update_human_time")
    def parse_update_human_time(cls, update_human_time_raw: str | datetime) -> datetime:
        if isinstance(update_human_time_raw, str):
            return datetime.strptime(update_human_time_raw, "%Y-%m-%dT%H:%M:%S")
        return update_human_time_raw

class GetPriceResponse(BaseModel):
    """
        Model used to represent the 'Price' endpoint from birdeye API.
    """
    data: GetPriceData
    success: bool

# classes used on GET 'Price - Multiple' endpoint
class GetPriceMultipleData(GetPriceData):
    price_change_24h: float = Field(alias = "priceChange24h")

class GetPriceMultipleResponse(BaseModel):
    """
        Model used to represent the 'Price - Multiple' endpoint from birdeye API.
    """
    data: dict[str, GetPriceMultipleData]
    success: bool

# classes used on GET 'Price - Historical' endpoint
class GetPriceHistoricalMeasure(BaseModel):
    address: str
    unix_time: int = Field(alias = "unixTime")
    value: float

class GetPriceHistoricalData(BaseModel):
    items: list[GetPriceHistoricalMeasure]

class GetPriceHistoricalResponse(BaseModel):
    """
        Model used to represent the 'Price - Historical' endpoint from birdeye API.
    """
    data: GetPriceHistoricalData
    success: bool

# classes used on GET 'History' endpoint
class GetHistoryData(BaseModel):
    items: list[str]
    reset_in_seconds: int = Field(alias = "resetInSeconds")

class GetHistoryResponse(BaseModel):
    """
        Model used to represent the 'History' endpoint from birdeye API.
    """
    data: GetHistoryData
    success: bool