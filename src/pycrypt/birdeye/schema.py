from datetime import datetime

from pydantic import BaseModel, Field, validator

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

    @validator("update_time", pre = True)
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