from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# classes used on GET "Price" endpoint
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
        Model used to represent the **Price** endpoint from birdeye API.
    """
    data: GetPriceData
    success: bool

# classes used on GET "Price - Multiple" endpoint
class GetPriceMultipleData(GetPriceData):
    price_change_24h: float = Field(alias = "priceChange24h")

class GetPriceMultipleResponse(BaseModel):
    """
        Model used to represent the **Price - Multiple** endpoint from birdeye API.
    """
    data: dict[str, GetPriceMultipleData]
    success: bool

# classes used on GET "Price - Historical" endpoint
class GetPriceHistoricalMeasure(BaseModel):
    unix_time: int = Field(alias = "unixTime")
    value: float

class GetPriceHistoricalData(BaseModel):
    items: list[GetPriceHistoricalMeasure]

class GetPriceHistoricalResponse(BaseModel):
    """
        Model used to represent the **Price - Historical** endpoint from birdeye API.
    """
    data: GetPriceHistoricalData
    success: bool

# classes used on GET "Price Volume - Single Token" endpoint
class GetPriceVolumeSingleData(BaseModel):
    price: float
    update_unix_time: int = Field(alias = "updateUnixTime")
    update_human_time: datetime = Field(alias = "updateHumanTime")
    volume_usd: float = Field(alias = "volumeUSD")
    volume_change_percent: float = Field(alias = "volumeChangePercent")
    price_change_percent: float = Field(alias = "priceChangePercent")

    @field_validator("update_human_time")
    def parse_update_human_time(cls, update_human_time_raw: str | datetime) -> datetime:
        if isinstance(update_human_time_raw, str):
            return datetime.strptime(update_human_time_raw, "%Y-%m-%dT%H:%M:%S")
        return update_human_time_raw

class GetPriceVolumeSingleResponse(BaseModel):
    """
        Model used to represent the **Price Volume - Single Token** endpoint from birdeye API.
    """
    data: GetPriceVolumeSingleData
    success: bool

# classes used on POST "Price Volume - Multiple Token" endpoint
class PostPriceVolumeMultiData(GetPriceVolumeSingleData):
    address: str

class PostPriceVolumeMultiResponse(BaseModel):
    """
        Model used to represent the **Price Volume - Multiple Token** endpoint from birdeye API.
    """
    data: list[PostPriceVolumeMultiData]

