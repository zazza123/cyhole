from typing import Any
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

# classes used on GET 'Token - Security' endpoint
class GetTokenSecurityDataSolana(BaseModel):
    """
        Data specific only for Solana chain
    """
    creator_address: str | None = Field(alias = "creatorAddress", default = None)
    owner_address: str | None = Field(alias = "ownerAddress", default = None)
    creation_transaction: str | None = Field(alias = "creationTx", default = None)
    creation_time_unix: int | None = Field(alias = "creationTime", default = None)
    creation_slot: int | None = Field(alias = "creationSlot", default = None)
    mint_transaction: str | None = Field(alias = "mintTx", default = None)
    mint_time_unix: int | None = Field(alias = "mintTime", default = None)
    mint_slot: int | None = Field(alias = "mintSlot", default = None)
    mintable: bool | None = None
    renounce: bool | None = None
    creator_balance: float | None = Field(alias = "creatorBalance", default = None)
    creator_percentage: float | None = Field(alias = "creatorPercentage", default = None)
    owner_balance: float | None = Field(alias = "ownerBalance", default = None)
    owner_percentage: float | None = Field(alias = "ownerPercentage", default = None)
    metaplex_update_authority: str = Field(alias = "metaplexUpdateAuthority")
    metaplex_update_balance: float = Field(alias = "metaplexUpdateAuthorityBalance")
    metaplex_update_percentage: float = Field(alias = "metaplexUpdateAuthorityPercent")
    mutable_metadata: bool = Field(alias = "mutableMetadata")
    top_10_holder_balance: float = Field(alias = "top10HolderBalance")
    top_10_holder_percentage: float = Field(alias = "top10HolderPercent")
    top_10_user_balance: float = Field(alias = "top10UserBalance")
    top_10_user_percentage: float = Field(alias = "top10UserPercent")
    is_true_token: bool | None = Field(alias = "isTrueToken", default = None)
    total_supply: float = Field(alias = "totalSupply")
    pre_market_holder: list[str] = Field(alias = "preMarketHolder")
    lock_info: Any | None = Field(alias = "lockInfo", default = None)
    freezeable: bool | None = None
    freeze_authority: str | None = Field(alias = "freezeAuthority", default = None)
    transfer_fee_enable: bool | None = Field(alias = "transferFeeEnable", default = None)
    transfer_fee_data: Any | None = Field(alias = "transferFeeData", default = None)
    is_token_2022: bool = Field(alias = "isToken2022")
    non_transferable: bool | None = Field(alias = "nonTransferable", default = None)

class GetTokenSecurityResponse(BaseModel):
    """
        Model used to represent the 'Token - Security' endpoint from birdeye API.
    """
    data: GetTokenSecurityDataSolana | dict[str, Any]
    success: bool

# classes used on GET 'Token - Creation Token Info' endpoint
class GetTokenCreationInfoData(BaseModel):
    transaction_hash: str = Field(alias = "txHash")
    slot: int
    token_address: str = Field(alias = "tokenAddress")
    decimals: int
    owner: str

class GetTokenCreationInfoResponse(BaseModel):
    """
        Model used to represent the 'Token - Creation Token Info' endpoint from birdeye API.
    """
    data: GetTokenCreationInfoData
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

# classes used on GET 'Trades - Token' endpoint
class GetTradesTokenTradeToken(BaseModel):
    symbol: str
    decimals: int
    address: str
    amount: int
    type: str
    type_swap: str = Field(alias = "typeSwap")
    ui_amount: float = Field(alias = "uiAmount")
    price: float | None = None
    nearest_price: float = Field(alias = "nearestPrice")
    change_amount: float = Field(alias = "changeAmount")
    ui_change_amount: float = Field(alias = "uiChangeAmount")
    icon: str

class GetTradesTokenTrade(BaseModel):
    volume: float
    volume_usd: float = Field(alias = "volumeUSD")
    trade_hash: str = Field(alias = "txHash")
    slot: int
    source: str
    block_unix_time: int = Field(alias = "blockUnixTime")
    block_human_time: datetime = Field(alias = "blockHumanTime")
    trade_type: str = Field(alias = "txType")
    address: str
    owner: str
    trade_status: str = Field(alias = "txStatus")
    outliers: bool
    nearest_price_base_coin: float = Field(alias = "nearestPriceBaseCoin")
    nearest_price_quote_coin: float = Field(alias = "nearestPriceQuoteCoin")
    ins_index: int = Field(alias = "insIndex")
    inner_ins_index: int | None = Field(alias = "innerInsIndex", default = None)
    be_bevenue: str | None = Field(alias = "beRevenue", default = None)
    event_type: str = Field(alias = "eventType")
    side: str
    price_pair: float = Field(alias = "pricePair")
    alias: str | None = None
    platform: str
    toke_price: float = Field(alias = "tokenPrice")
    proce_mark: bool = Field(alias = "priceMark")
    network: str
    trade_from: GetTradesTokenTradeToken = Field(alias = "from")
    trade_to: GetTradesTokenTradeToken = Field(alias = "to")

    @field_validator("block_human_time")
    def parse_update_human_time(cls, dt_raw: str | datetime) -> datetime:
        if isinstance(dt_raw, str):
            return datetime.strptime(dt_raw, "%Y-%m-%dT%H:%M:%S")
        return dt_raw

class GetTradesTokenData(BaseModel):
    items: list[GetTradesTokenTrade]
    has_next: bool = Field(alias = "hasNext")

class GetTradesTokenResponse(BaseModel):
    """
        Model used to represent the 'Trades - Token' endpoint from birdeye API.
    """
    data: GetTradesTokenData
    success: bool

# classes used on GET 'Trades - Pair' endpoint
class GetTradesPairTradeToken(BaseModel):
    symbol: str
    decimals: int
    address: str
    amount: int
    type: str
    type_swap: str = Field(alias = "typeSwap")
    ui_amount: float = Field(alias = "uiAmount")
    price: float | None = None
    nearest_price: float = Field(alias = "nearestPrice")
    change_amount: float = Field(alias = "changeAmount")
    ui_change_amount: float = Field(alias = "uiChangeAmount")

class GetTradesPairTrade(BaseModel):
    trade_hash: str = Field(alias = "txHash")
    source: str
    block_unix_time: int = Field(alias = "blockUnixTime")
    address: str
    owner: str
    trade_from: GetTradesPairTradeToken = Field(alias = "from")
    trade_to: GetTradesPairTradeToken = Field(alias = "to")

class GetTradesPairData(BaseModel):
    items: list[GetTradesPairTrade]
    has_next: bool = Field(alias = "hasNext")

class GetTradesPairResponse(BaseModel):
    """
        Model used to represent the 'Trades - Pair' endpoint from birdeye API.
    """
    data: GetTradesPairData
    success: bool

# classes used on GET 'OHLCV - Token/Pair' endpoint
class GetOHLCVInterval(BaseModel):
    close: float = Field(alias = "c")
    high: float  = Field(alias = "h")
    low: float  = Field(alias = "l")
    open: float  = Field(alias = "o")
    type: str
    unix_time: int  = Field(alias = "unixTime")

class GetOHLCVTokenPairInterval(GetOHLCVInterval):
    address: str
    volume: float  = Field(alias = "v")

class GetOHLCVTokenPairData(BaseModel):
    items: list[GetOHLCVTokenPairInterval]

class GetOHLCVTokenPairResponse(BaseModel):
    """
        Model used to represent the 'OHLCV - Token/Pair' endpoint from birdeye API.
    """
    data: GetOHLCVTokenPairData
    success: bool

# classes used on GET 'OHLCV - Base/Quote' endpoint
class GetOHLCVBaseQuoteInterval(GetOHLCVInterval):
    base_address: str = Field(alias = "baseAddress")
    quote_address: str = Field(alias = "quoteAddress")
    base_volume: float = Field(alias = "vBase")
    quote_volume: float = Field(alias = "vQuote")

class GetOHLCVBaseQuoteData(BaseModel):
    items: list[GetOHLCVBaseQuoteInterval]

class GetOHLCVBaseQuoteResponse(BaseModel):
    """
        Model used to represent the 'OHLCV - Token/Pair' endpoint from birdeye API.
    """
    data: GetOHLCVBaseQuoteData
    success: bool

# classes used on GET 'Wallet - Supported Networks' endpoint
class GetWalletSupportedNetworksResponse(BaseModel):
    """
        Model used to represent the 'Wallet - Supported Networks' endpoint from birdeye API.
    """
    data: list[str]
    success: bool