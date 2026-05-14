from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# classes used on GET "Trades - Token" endpoint
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
    icon: str | None = None

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
        Model used to represent the **Trades - Token** endpoint from birdeye API.
    """
    data: GetTradesTokenData
    success: bool

# classes used on GET "Trades - Pair" endpoint
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
        Model used to represent the **Trades - Pair** endpoint from birdeye API.
    """
    data: GetTradesPairData
    success: bool

# classes used on GET "OHLCV - Token/Pair" endpoint
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
        Model used to represent the **OHLCV - Token/Pair** endpoint from birdeye API.
    """
    data: GetOHLCVTokenPairData
    success: bool

# classes used on GET "OHLCV - Base/Quote" endpoint
class GetOHLCVBaseQuoteInterval(GetOHLCVInterval):
    base_address: str = Field(alias = "baseAddress")
    quote_address: str = Field(alias = "quoteAddress")
    base_volume: float = Field(alias = "vBase")
    quote_volume: float = Field(alias = "vQuote")

class GetOHLCVBaseQuoteData(BaseModel):
    items: list[GetOHLCVBaseQuoteInterval]

class GetOHLCVBaseQuoteResponse(BaseModel):
    """
        Model used to represent the **OHLCV - Token/Pair** endpoint from birdeye API.
    """
    data: GetOHLCVBaseQuoteData



# classes used on GET "Token - Mint/Burn" endpoint
class GetV3TokenMintBurnTxsItem(BaseModel):
    """
        Single mint or burn transaction returned by the v3 Token - Mint/Burn endpoint.

        Attributes:
            common_type: kind of supply change, either `"mint"` or `"burn"`.
            tx_hash: signature of the on-chain transaction that performed the mint/burn.
            slot: Solana slot at which the transaction was processed.
            block_time: unix-second timestamp of the block containing the transaction.
            block_human_time: ISO-8601 timestamp of the same block as `block_time`.
            mint: contract address of the affected SPL token mint.
            program_id: address of the on-chain program that emitted the mint/burn instruction
                (usually the SPL Token program).
            amount: raw amount minted or burned, expressed in the token's smallest units (string).
            decimals: number of decimal places used by the token.
            ui_amount: UI-formatted amount (i.e. `amount` divided by `10 ** decimals`) as a number.
            ui_amount_string: UI-formatted amount as a string (preserves precision for very large values).
    """
    common_type: str
    tx_hash: str
    slot: int
    block_time: int
    block_human_time: str
    mint: str
    program_id: str
    amount: str
    decimals: int
    ui_amount: float
    ui_amount_string: str

class GetV3TokenMintBurnTxsData(BaseModel):
    """
        Payload of the v3 Token - Mint/Burn response.

        Attributes:
            items: list of mint/burn transactions matching the request, ranked per `sort_by` /
                `sort_type` (default: most recent first).
    """
    items: list[GetV3TokenMintBurnTxsItem]

class GetV3TokenMintBurnTxsResponse(BaseModel):
    """
        Model used to represent the **Token - Mint/Burn** endpoint from birdeye API.

        Attributes:
            data: payload containing the list of mint/burn transactions.
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenMintBurnTxsData
    success: bool
