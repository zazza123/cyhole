from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# classes used on GET "Token List" endpoint
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
        Model used to represent the **Token - List** endpoint from birdeye API.
    """
    data: GetTokenListData
    success: bool

# classes used on GET "Token - Security" endpoint
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
        Model used to represent the **Token - Security** endpoint from birdeye API.
    """
    data: GetTokenSecurityDataSolana | dict[str, Any]
    success: bool

# classes used on GET "Token - Overview" endpoint
class GetTokenOverviewData(BaseModel):
    address: str
    decimals: int
    symbol: str
    name: str
    extensions: dict[str, str | None]
    logo_uri: str = Field(alias = "logoURI")
    liquidity: float
    price: float
    supply: float | None = None
    market_cap: float | None = Field(alias = "mc", default = None)
    history_30m_price: float = Field(alias = "history30mPrice")
    price_change_30m_percent: float = Field(alias = "priceChange30mPercent")
    history_1h_price: float = Field(alias = "history1hPrice")
    price_change_1h_percent: float = Field(alias = "priceChange1hPercent")
    history_2h_price: float = Field(alias = "history2hPrice")
    price_change_2h_percent: float = Field(alias = "priceChange2hPercent")
    history_4h_price: float = Field(alias = "history4hPrice")
    price_change_4h_percent: float = Field(alias = "priceChange4hPercent")
    history_6h_price: float = Field(alias = "history6hPrice")
    price_change_6h_percent: float = Field(alias = "priceChange6hPercent")
    history_8h_price: float = Field(alias = "history8hPrice")
    price_change_8h_percent: float = Field(alias = "priceChange8hPercent")
    history_12h_price: float = Field(alias = "history12hPrice")
    price_change_12h_percent: float = Field(alias = "priceChange12hPercent")
    history_24h_price: float = Field(alias = "history24hPrice")
    price_change_24h_percent: float = Field(alias = "priceChange24hPercent")
    unique_wallet_30m: int = Field(alias = "uniqueWallet30m")
    unique_wallet_history_30m: int = Field(alias = "uniqueWalletHistory30m")
    unique_wallet_30m_change_percent: float = Field(alias = "uniqueWallet30mChangePercent")
    unique_wallet_1h: int = Field(alias = "uniqueWallet1h")
    unique_wallet_history_1h: int = Field(alias = "uniqueWalletHistory1h")
    unique_wallet_1h_change_percent: float = Field(alias = "uniqueWallet1hChangePercent")
    unique_wallet_2h: int = Field(alias = "uniqueWallet2h")
    unique_wallet_history_2h: int = Field(alias = "uniqueWalletHistory2h")
    unique_wallet_2h_change_percent: float = Field(alias = "uniqueWallet2hChangePercent")
    unique_wallet_4h: int = Field(alias = "uniqueWallet4h")
    unique_wallet_history_4h: int = Field(alias = "uniqueWalletHistory4h")
    unique_wallet_4h_change_percent: float = Field(alias = "uniqueWallet4hChangePercent")
    unique_wallet_6h: int = Field(alias = "uniqueWallet6h")
    unique_wallet_history_6h: int = Field(alias = "uniqueWalletHistory6h")
    unique_wallet_6h_change_percent: float = Field(alias = "uniqueWallet6hChangePercent")
    unique_wallet_8h: int = Field(alias = "uniqueWallet8h")
    unique_wallet_history_8h: int = Field(alias = "uniqueWalletHistory8h")
    unique_wallet_8h_change_percent: float = Field(alias = "uniqueWallet8hChangePercent")
    unique_wallet_12h: int = Field(alias = "uniqueWallet12h")
    unique_wallet_history_12h: int = Field(alias = "uniqueWalletHistory12h")
    unique_wallet_12h_change_percent: float = Field(alias = "uniqueWallet12hChangePercent")
    unique_wallet_24h: int = Field(alias = "uniqueWallet24h")
    unique_wallet_history_24h: int = Field(alias = "uniqueWalletHistory24h")
    unique_wallet_24h_change_percent: float = Field(alias = "uniqueWallet24hChangePercent")
    last_trade_unix_time: int = Field(alias = "lastTradeUnixTime")
    last_trade_human_time: datetime = Field(alias = "lastTradeHumanTime")
    trade_30m: int = Field(alias = "trade30m")
    trade_history_30m: int = Field(alias = "tradeHistory30m")
    trade_30m_change_percent: float = Field(alias = "trade30mChangePercent")
    sell_30m: int = Field(alias = "sell30m")
    sell_history_30m: int = Field(alias = "sellHistory30m")
    sell_30m_change_percent: float = Field(alias = "sell30mChangePercent")
    buy_30m: int = Field(alias = "buy30m")
    buy_history_30m: int = Field(alias = "buyHistory30m")
    buy_30m_change_percent: float = Field(alias = "buy30mChangePercent")
    volume_30m: float = Field(alias = "v30m")
    volume_30m_usd: float = Field(alias = "v30mUSD")
    volume_history_30m: float = Field(alias = "vHistory30m")
    volume_history_30m_usd: float = Field(alias = "vHistory30mUSD")
    volume_30m_change_percent: float = Field(alias = "v30mChangePercent")
    volume_buy_30m: float = Field(alias = "vBuy30m")
    volume_buy_30m_usd: float = Field(alias = "vBuy30mUSD")
    volume_buy_history_30m: float = Field(alias = "vBuyHistory30m")
    volume_buy_history_30m_usd: float = Field(alias = "vBuyHistory30mUSD")
    volume_buy_30m_change_percent: float = Field(alias = "vBuy30mChangePercent")
    volume_sell_30m: float = Field(alias = "vSell30m")
    volume_sell_30m_usd: float = Field(alias = "vSell30mUSD")
    volume_sell_history_30m: float = Field(alias = "vSellHistory30m")
    volume_sell_history_30m_usd: float = Field(alias = "vSellHistory30mUSD")
    volume_sell_30m_change_percent: float = Field(alias = "vSell30mChangePercent")
    trade_1h: int = Field(alias = "trade1h")
    trade_history_1h: int = Field(alias = "tradeHistory1h")
    trade_1h_change_percent: float = Field(alias = "trade1hChangePercent")
    sell_1h: int = Field(alias = "sell1h")
    sell_history_1h: int = Field(alias = "sellHistory1h")
    sell_1h_change_percent: float = Field(alias = "sell1hChangePercent")
    buy_1h: int = Field(alias = "buy1h")
    buy_history_1h: int = Field(alias = "buyHistory1h")
    buy_1h_change_percent: float = Field(alias = "buy1hChangePercent")
    volume_1h: float = Field(alias = "v1h")
    volume_1h_usd: float = Field(alias = "v1hUSD")
    volume_history_1h: float = Field(alias = "vHistory1h")
    volume_history_1h_usd: float = Field(alias = "vHistory1hUSD")
    volume_1h_change_percent: float = Field(alias = "v1hChangePercent")
    volume_buy_1h: float = Field(alias = "vBuy1h")
    volume_buy_1h_usd: float = Field(alias = "vBuy1hUSD")
    volume_buy_history_1h: float = Field(alias = "vBuyHistory1h")
    volume_buy_history_1h_usd: float = Field(alias = "vBuyHistory1hUSD")
    volume_buy_1h_change_percent: float = Field(alias = "vBuy1hChangePercent")
    volume_sell_1h: float = Field(alias = "vSell1h")
    volume_sell_1h_usd: float = Field(alias = "vSell1hUSD")
    volume_sell_history_1h: float = Field(alias = "vSellHistory1h")
    volume_sell_history_1h_usd: float = Field(alias = "vSellHistory1hUSD")
    volume_sell_1h_change_percent: float = Field(alias = "vSell1hChangePercent")
    trade_2h: int = Field(alias = "trade2h")
    trade_history_2h: int = Field(alias = "tradeHistory2h")
    trade_2h_change_percent: float = Field(alias = "trade2hChangePercent")
    sell_2h: int = Field(alias = "sell2h")
    sell_history_2h: int = Field(alias = "sellHistory2h")
    sell_2h_change_percent: float = Field(alias = "sell2hChangePercent")
    buy_2h: int = Field(alias = "buy2h")
    buy_history_2h: int = Field(alias = "buyHistory2h")
    buy_2h_change_percent: float = Field(alias = "buy2hChangePercent")
    volume_2h: float = Field(alias = "v2h")
    volume_2h_usd: float = Field(alias = "v2hUSD")
    volume_history_2h: float = Field(alias = "vHistory2h")
    volume_history_2h_usd: float = Field(alias = "vHistory2hUSD")
    volume_2h_change_percent: float = Field(alias = "v2hChangePercent")
    volume_buy_2h: float = Field(alias = "vBuy2h")
    volume_buy_2h_usd: float = Field(alias = "vBuy2hUSD")
    volume_buy_history_2h: float = Field(alias = "vBuyHistory2h")
    volume_buy_history_2h_usd: float = Field(alias = "vBuyHistory2hUSD")
    volume_buy_2h_change_percent: float = Field(alias = "vBuy2hChangePercent")
    volume_sell_2h: float = Field(alias = "vSell2h")
    volume_sell_2h_usd: float = Field(alias = "vSell2hUSD")
    volume_sell_history_2h: float = Field(alias = "vSellHistory2h")
    volume_sell_history_2h_usd: float = Field(alias = "vSellHistory2hUSD")
    volume_sell_2h_change_percent: float = Field(alias = "vSell2hChangePercent")
    trade_4h: int = Field(alias = "trade4h")
    trade_history_4h: int = Field(alias = "tradeHistory4h")
    trade_4h_change_percent: float = Field(alias = "trade4hChangePercent")
    sell_4h: int = Field(alias = "sell4h")
    sell_history_4h: int = Field(alias = "sellHistory4h")
    sell_4h_change_percent: float = Field(alias = "sell4hChangePercent")
    buy_4h: int = Field(alias = "buy4h")
    buy_history_4h: int = Field(alias = "buyHistory4h")
    buy_4h_change_percent: float = Field(alias = "buy4hChangePercent")
    volume_4h: float = Field(alias = "v4h")
    volume_4h_usd: float = Field(alias = "v4hUSD")
    volume_history_4h: float = Field(alias = "vHistory4h")
    volume_history_4h_usd: float = Field(alias = "vHistory4hUSD")
    volume_4h_change_percent: float = Field(alias = "v4hChangePercent")
    volume_buy_4h: float = Field(alias = "vBuy4h")
    volume_buy_4h_usd: float = Field(alias = "vBuy4hUSD")
    volume_buy_history_4h: float = Field(alias = "vBuyHistory4h")
    volume_buy_history_4h_usd: float = Field(alias = "vBuyHistory4hUSD")
    volume_buy_4h_change_percent: float = Field(alias = "vBuy4hChangePercent")
    volume_sell_4h: float = Field(alias = "vSell4h")
    volume_sell_4h_usd: float = Field(alias = "vSell4hUSD")
    volume_sell_history_4h: float = Field(alias = "vSellHistory4h")
    volume_sell_history_4h_usd: float = Field(alias = "vSellHistory4hUSD")
    volume_sell_4h_change_percent: float = Field(alias = "vSell4hChangePercent")
    trade_6h: int = Field(alias = "trade6h")
    trade_history_6h: int = Field(alias = "tradeHistory6h")
    trade_6h_change_percent: float = Field(alias = "trade6hChangePercent")
    sell_6h: int = Field(alias = "sell6h")
    sell_history_6h: int = Field(alias = "sellHistory6h")
    sell_6h_change_percent: float = Field(alias = "sell6hChangePercent")
    buy_6h: int = Field(alias = "buy6h")
    buy_history_6h: int = Field(alias = "buyHistory6h")
    buy_6h_change_percent: float = Field(alias = "buy6hChangePercent")
    volume_6h: float = Field(alias = "v6h")
    volume_6h_usd: float = Field(alias = "v6hUSD")
    volume_history_6h: float = Field(alias = "vHistory6h")
    volume_history_6h_usd: float = Field(alias = "vHistory6hUSD")
    volume_6h_change_percent: float = Field(alias = "v6hChangePercent")
    volume_buy_6h: float = Field(alias = "vBuy6h")
    volume_buy_6h_usd: float = Field(alias = "vBuy6hUSD")
    volume_buy_history_6h: float = Field(alias = "vBuyHistory6h")
    volume_buy_history_6h_usd: float = Field(alias = "vBuyHistory6hUSD")
    volume_buy_6h_change_percent: float = Field(alias = "vBuy6hChangePercent")
    volume_sell_6h: float = Field(alias = "vSell6h")
    volume_sell_6h_usd: float = Field(alias = "vSell6hUSD")
    volume_sell_history_6h: float = Field(alias = "vSellHistory6h")
    volume_sell_history_6h_usd: float = Field(alias = "vSellHistory6hUSD")
    volume_sell_6h_change_percent: float = Field(alias = "vSell6hChangePercent")
    trade_8h: int = Field(alias = "trade8h")
    trade_history_8h: int = Field(alias = "tradeHistory8h")
    trade_8h_change_percent: float = Field(alias = "trade8hChangePercent")
    sell_8h: int = Field(alias = "sell8h")
    sell_history_8h: int = Field(alias = "sellHistory8h")
    sell_8h_change_percent: float = Field(alias = "sell8hChangePercent")
    buy_8h: int = Field(alias = "buy8h")
    buy_history_8h: int = Field(alias = "buyHistory8h")
    buy_8h_change_percent: float = Field(alias = "buy8hChangePercent")
    volume_8h: float = Field(alias = "v8h")
    volume_8h_usd: float = Field(alias = "v8hUSD")
    volume_history_8h: float = Field(alias = "vHistory8h")
    volume_history_8h_usd: float = Field(alias = "vHistory8hUSD")
    volume_8h_change_percent: float = Field(alias = "v8hChangePercent")
    volume_buy_8h: float = Field(alias = "vBuy8h")
    volume_buy_8h_usd: float = Field(alias = "vBuy8hUSD")
    volume_buy_history_8h: float = Field(alias = "vBuyHistory8h")
    volume_buy_history_8h_usd: float = Field(alias = "vBuyHistory8hUSD")
    volume_buy_8h_change_percent: float = Field(alias = "vBuy8hChangePercent")
    volume_sell_8h: float = Field(alias = "vSell8h")
    volume_sell_8h_usd: float = Field(alias = "vSell8hUSD")
    volume_sell_history_8h: float = Field(alias = "vSellHistory8h")
    volume_sell_history_8h_usd: float = Field(alias = "vSellHistory8hUSD")
    volume_sell_8h_change_percent: float = Field(alias = "vSell8hChangePercent")
    trade_12h: int = Field(alias = "trade12h")
    trade_history_12h: int = Field(alias = "tradeHistory12h")
    trade_12h_change_percent: float = Field(alias = "trade12hChangePercent")
    sell_12h: int = Field(alias = "sell12h")
    sell_history_12h: int = Field(alias = "sellHistory12h")
    sell_12h_change_percent: float = Field(alias = "sell12hChangePercent")
    buy_12h: int = Field(alias = "buy12h")
    buy_history_12h: int = Field(alias = "buyHistory12h")
    buy_12h_change_percent: float = Field(alias = "buy12hChangePercent")
    volume_12h: float = Field(alias = "v12h")
    volume_12h_usd: float = Field(alias = "v12hUSD")
    volume_history_12h: float = Field(alias = "vHistory12h")
    volume_history_12h_usd: float = Field(alias = "vHistory12hUSD")
    volume_12h_change_percent: float = Field(alias = "v12hChangePercent")
    volume_buy_12h: float = Field(alias = "vBuy12h")
    volume_buy_12h_usd: float = Field(alias = "vBuy12hUSD")
    volume_buy_history_12h: float = Field(alias = "vBuyHistory12h")
    volume_buy_history_12h_usd: float = Field(alias = "vBuyHistory12hUSD")
    volume_buy_12h_change_percent: float = Field(alias = "vBuy12hChangePercent")
    volume_sell_12h: float = Field(alias = "vSell12h")
    volume_sell_12h_usd: float = Field(alias = "vSell12hUSD")
    volume_sell_history_12h: float = Field(alias = "vSellHistory12h")
    volume_sell_history_12h_usd: float = Field(alias = "vSellHistory12hUSD")
    volume_sell_12h_change_percent: float = Field(alias = "vSell12hChangePercent")
    trade_24h: int = Field(alias = "trade24h")
    trade_history_24h: int = Field(alias = "tradeHistory24h")
    trade_24h_change_percent: float = Field(alias = "trade24hChangePercent")
    sell_24h: int = Field(alias = "sell24h")
    sell_history_24h: int = Field(alias = "sellHistory24h")
    sell_24h_change_percent: float = Field(alias = "sell24hChangePercent")
    buy_24h: int = Field(alias = "buy24h")
    buy_history_24h: int = Field(alias = "buyHistory24h")
    buy_24h_change_percent: float = Field(alias = "buy24hChangePercent")
    volume_24h: float = Field(alias = "v24h")
    volume_24h_usd: float = Field(alias = "v24hUSD")
    volume_history_24h: float = Field(alias = "vHistory24h")
    volume_history_24h_usd: float = Field(alias = "vHistory24hUSD")
    volume_24h_change_percent: float = Field(alias = "v24hChangePercent")
    volume_buy_24h: float = Field(alias = "vBuy24h")
    volume_buy_24h_usd: float = Field(alias = "vBuy24hUSD")
    volume_buy_history_24h: float = Field(alias = "vBuyHistory24h")
    volume_buy_history_24h_usd: float = Field(alias = "vBuyHistory24hUSD")
    volume_buy_24h_change_percent: float = Field(alias = "vBuy24hChangePercent")
    volume_sell_24h: float = Field(alias = "vSell24h")
    volume_sell_24h_usd: float = Field(alias = "vSell24hUSD")
    volume_sell_history_24h: float = Field(alias = "vSellHistory24h")
    volume_sell_history_24h_usd: float = Field(alias = "vSellHistory24hUSD")
    volume_sell_24h_change_percent: float = Field(alias = "vSell24hChangePercent")
    watch: int = Field(alias = "watch")
    view_30m: int = Field(alias = "view30m")
    view_history_30m: int = Field(alias = "viewHistory30m")
    view_30m_change_percent: float = Field(alias = "view30mChangePercent")
    view_1h: int = Field(alias = "view1h")
    view_history_1h: int = Field(alias = "viewHistory1h")
    view_1h_change_percent: float = Field(alias = "view1hChangePercent")
    view_2h: int = Field(alias = "view2h")
    view_history_2h: int = Field(alias = "viewHistory2h")
    view_2h_change_percent: float = Field(alias = "view2hChangePercent")
    view_4h: int = Field(alias = "view4h")
    view_history_4h: int = Field(alias = "viewHistory4h")
    view_4h_change_percent: float = Field(alias = "view4hChangePercent")
    view_6h: int = Field(alias = "view6h")
    view_history_6h: int = Field(alias = "viewHistory6h")
    view_6h_change_percent: float = Field(alias = "view6hChangePercent")
    view_8h: int = Field(alias = "view8h")
    view_history_8h: int = Field(alias = "viewHistory8h")
    view_8h_change_percent: float = Field(alias = "view8hChangePercent")
    view_12h: int = Field(alias = "view12h")
    view_history_12h: int = Field(alias = "viewHistory12h")
    view_12h_change_percent: float = Field(alias = "view12hChangePercent")
    view_24h: int = Field(alias = "view24h")
    view_history_24h: int = Field(alias = "viewHistory24h")
    view_24h_change_percent: float = Field(alias = "view24hChangePercent")
    unique_view_30m: int = Field(alias = "uniqueView30m")
    unique_view_history_30m: int = Field(alias = "uniqueViewHistory30m")
    unique_view_30m_change_percent: float = Field(alias = "uniqueView30mChangePercent")
    unique_view_1h: int = Field(alias = "uniqueView1h")
    unique_view_history_1h: int = Field(alias = "uniqueViewHistory1h")
    unique_view_1h_change_percent: float = Field(alias = "uniqueView1hChangePercent")
    unique_view_2h: int = Field(alias = "uniqueView2h")
    unique_view_history_2h: int = Field(alias = "uniqueViewHistory2h")
    unique_view_2h_change_percent: float = Field(alias = "uniqueView2hChangePercent")
    unique_view_4h: int = Field(alias = "uniqueView4h")
    unique_view_history_4h: int = Field(alias = "uniqueViewHistory4h")
    unique_view_4h_change_percent: float = Field(alias = "uniqueView4hChangePercent")
    unique_view_6h: int = Field(alias = "uniqueView6h")
    unique_view_history_6h: int = Field(alias = "uniqueViewHistory6h")
    unique_view_6h_change_percent: float = Field(alias = "uniqueView6hChangePercent")
    unique_view_8h: int = Field(alias = "uniqueView8h")
    unique_view_history_8h: int = Field(alias = "uniqueViewHistory8h")
    unique_view_8h_change_percent: float = Field(alias = "uniqueView8hChangePercent")
    unique_view_12h: int = Field(alias = "uniqueView12h")
    unique_view_history_12h: int = Field(alias = "uniqueViewHistory12h")
    unique_view_12h_change_percent: float = Field(alias = "uniqueView12hChangePercent")
    unique_view_24h: int = Field(alias = "uniqueView24h")
    unique_view_history_24h: int = Field(alias = "uniqueViewHistory24h")
    unique_view_24h_change_percent: float = Field(alias = "uniqueView24hChangePercent")

class GetTokenOverviewResponse(BaseModel):
    """
        Model used to represent the **Token - Overview** endpoint from birdeye API.
    """
    data: GetTokenOverviewData
    success: bool

# classes used on GET "Token - Creation Token Info" endpoint
class GetTokenCreationInfoData(BaseModel):
    transaction_hash: str = Field(alias = "txHash")
    slot: int
    token_address: str = Field(alias = "tokenAddress")
    decimals: int
    owner: str

class GetTokenCreationInfoResponse(BaseModel):
    """
        Model used to represent the **Token - Creation Token Info** endpoint from birdeye API.
    """
    data: GetTokenCreationInfoData
    success: bool


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

# classes used on GET "History" endpoint
class GetHistoryData(BaseModel):
    items: list[str]
    reset_in_seconds: int = Field(alias = "resetInSeconds")

class GetHistoryResponse(BaseModel):
    """
        Model used to represent the **History** endpoint from birdeye API.
    """
    data: GetHistoryData
    success: bool

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
    success: bool

# classes used on GET "Wallet - Supported Networks" endpoint
class GetWalletSupportedNetworksResponse(BaseModel):
    """
        Model used to represent the **Wallet - Supported Networks** endpoint from birdeye API.
    """
    data: list[str]
    success: bool