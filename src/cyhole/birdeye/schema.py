from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

# classes used on GET "Token List" endpoint
class GetTokenListInfo(BaseModel):
    name: str | None                = None
    symbol: str | None              = None
    price: float
    address: str
    decimals: int
    liquidity: float
    volume_24h_usd: float           = Field(alias = "v24hUSD")
    market_cap: float               = Field(alias = "mc")
    volume_24h_change: float | None = Field(alias = "v24hChangePercent", default = None)
    last_trade_unix_time: float     = Field(alias = "lastTradeUnixTime")
    logo_uri: str  | None           = Field(alias = "logoURI", default = None)

class GetTokenListData(BaseModel):
    total: int | None = None
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
        Solana-specific security/risk profile of a token returned by the Birdeye
        **Token - Security** endpoint.

        All ownership and authority fields are optional because Birdeye returns
        `null` for them when the token has renounced/cleared the corresponding
        on-chain authority. Balance and percentage fields refer to the holdings
        of the related authority over the token's total supply.

        Attributes:
            creator_address: address that created the token (alias `creatorAddress`); `None` if unknown.
            creator_owner_address: owner of `creator_address` at the time of token creation
                (alias `creatorOwnerAddress`); `None` if the creator was an EOA or no longer tracked.
            owner_address: current on-chain owner of the token authority (alias `ownerAddress`);
                `None` when ownership has been renounced.
            owner_of_owner_address: owner of `owner_address` (alias `ownerOfOwnerAddress`);
                `None` if owner is an EOA or ownership has been renounced.
            creation_transaction: signature of the transaction that created the token
                (alias `creationTx`); `None` if unknown.
            creation_time_unix: unix-second timestamp of the creation transaction (alias `creationTime`).
            creation_slot: slot of the creation transaction (alias `creationSlot`).
            mint_transaction: signature of the mint transaction (alias `mintTx`).
            mint_time_unix: unix-second timestamp of the mint transaction (alias `mintTime`).
            mint_slot: slot of the mint transaction (alias `mintSlot`).
            mintable: whether the token can still be minted; `None` if the API cannot determine it.
            renounce: whether the mint authority has been renounced; `None` if undetermined.
            creator_balance: token balance currently held by the creator address (alias `creatorBalance`).
            creator_percentage: creator balance expressed as a fraction (0..1) of total supply
                (alias `creatorPercentage`).
            owner_balance: token balance currently held by the owner address (alias `ownerBalance`).
            owner_percentage: owner balance expressed as a fraction (0..1) of total supply
                (alias `ownerPercentage`).
            metaplex_update_authority: Metaplex metadata update authority (alias `metaplexUpdateAuthority`).
            metaplex_owner_update_authority: owner of the Metaplex update authority address
                (alias `metaplexOwnerUpdateAuthority`); `None` when no upstream owner is tracked.
            metaplex_update_balance: token balance held by the Metaplex update authority
                (alias `metaplexUpdateAuthorityBalance`).
            metaplex_update_percentage: Metaplex update authority balance expressed as a fraction (0..1)
                of total supply (alias `metaplexUpdateAuthorityPercent`).
            mutable_metadata: whether the on-chain Metaplex metadata of the token is still mutable
                (alias `mutableMetadata`).
            top_10_holder_balance: cumulative token balance of the top-10 holders (alias `top10HolderBalance`).
            top_10_holder_percentage: top-10 holders' cumulative balance as a fraction (0..1) of total
                supply (alias `top10HolderPercent`).
            top_10_user_balance: cumulative token balance of the top-10 *user* wallets (excluding programs)
                (alias `top10UserBalance`).
            top_10_user_percentage: top-10 users' cumulative balance as a fraction (0..1) of total supply
                (alias `top10UserPercent`).
            is_true_token: Birdeye flag marking the token as one of its verified entries
                (alias `isTrueToken`); `None` when unverified.
            fake_token: Birdeye flag marking the token as a known scam/fake (alias `fakeToken`);
                `None` when Birdeye has not categorised it.
            total_supply: total on-chain supply of the token, expressed in UI units (alias `totalSupply`).
            pre_market_holder: list of addresses that received tokens before any public market existed
                (alias `preMarketHolder`).
            lock_info: free-form payload describing on-chain locks (e.g. team vesting); `None` when no
                lock information is known (alias `lockInfo`).
            freezeable: whether the SPL freeze authority can still freeze accounts; `None` if undetermined.
            freeze_authority: address that owns the freeze authority (alias `freezeAuthority`);
                `None` when the freeze authority has been renounced.
            transfer_fee_enable: whether the Token-2022 transfer-fee extension is active
                (alias `transferFeeEnable`); `None` if the extension is absent or undetermined.
            transfer_fee_data: free-form payload describing the active transfer-fee parameters
                (alias `transferFeeData`); `None` when no fee data is available.
            is_token_2022: whether the token is an SPL Token-2022 mint (alias `isToken2022`).
            non_transferable: whether the Token-2022 non-transferable extension is active
                (alias `nonTransferable`); `None` if undetermined.
            jup_strict_list: whether the token is part of Jupiter's strict token list
                (alias `jupStrictList`); `None` when Birdeye did not populate the flag.
    """
    creator_address: str | None = Field(alias = "creatorAddress", default = None)
    creator_owner_address: str | None = Field(alias = "creatorOwnerAddress", default = None)
    owner_address: str | None = Field(alias = "ownerAddress", default = None)
    owner_of_owner_address: str | None = Field(alias = "ownerOfOwnerAddress", default = None)
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
    metaplex_owner_update_authority: str | None = Field(alias = "metaplexOwnerUpdateAuthority", default = None)
    metaplex_update_balance: float = Field(alias = "metaplexUpdateAuthorityBalance")
    metaplex_update_percentage: float = Field(alias = "metaplexUpdateAuthorityPercent")
    mutable_metadata: bool = Field(alias = "mutableMetadata")
    top_10_holder_balance: float = Field(alias = "top10HolderBalance")
    top_10_holder_percentage: float = Field(alias = "top10HolderPercent")
    top_10_user_balance: float = Field(alias = "top10UserBalance")
    top_10_user_percentage: float = Field(alias = "top10UserPercent")
    is_true_token: bool | None = Field(alias = "isTrueToken", default = None)
    fake_token: bool | None = Field(alias = "fakeToken", default = None)
    total_supply: float = Field(alias = "totalSupply")
    pre_market_holder: list[str] = Field(alias = "preMarketHolder")
    lock_info: Any | None = Field(alias = "lockInfo", default = None)
    freezeable: bool | None = None
    freeze_authority: str | None = Field(alias = "freezeAuthority", default = None)
    transfer_fee_enable: bool | None = Field(alias = "transferFeeEnable", default = None)
    transfer_fee_data: Any | None = Field(alias = "transferFeeData", default = None)
    is_token_2022: bool = Field(alias = "isToken2022")
    non_transferable: bool | None = Field(alias = "nonTransferable", default = None)
    jup_strict_list: bool | None = Field(alias = "jupStrictList", default = None)

class GetTokenSecurityResponse(BaseModel):
    """
        Model used to represent the **Token - Security** endpoint from birdeye API.

        Attributes:
            data: security profile of the token. When the request targets Solana the payload is
                parsed into the typed [`GetTokenSecurityDataSolana`][cyhole.birdeye.schema.GetTokenSecurityDataSolana]
                schema; for every other supported chain the payload is left as a free-form
                dictionary because Birdeye returns a chain-specific (EVM-style) shape.
            success: `True` when the API call completed without errors.
    """
    data: GetTokenSecurityDataSolana | dict[str, Any]
    success: bool

# classes used on GET "Token - Overview" endpoint
class GetTokenOverviewData(BaseModel):
    """
        Token-level analytics payload returned by the Birdeye **Token - Overview** endpoint.

        The payload bundles identity (address, symbol, name, social links), pricing (current
        price plus history snapshots at 1m, 5m, 30m, 1h, 2h, 4h, 6h, 8h, 12h and 24h),
        liquidity, supply (total, circulating, number of holders), unique-wallet counts and
        per-side trade activity (sell, buy, volume both in token UI units and USD) for the
        trailing 1m, 5m, 30m, 1h, 2h, 4h, 8h and 24h windows. For every activity window
        Birdeye also returns the equivalent metric over the immediately preceding window
        (the `*_history` fields) and a precomputed percent change between the two.

        Attributes:
            address: contract address of the token.
            decimals: number of decimal places used by the token.
            symbol: ticker symbol of the token.
            name: human-readable name of the token.
            market_cap: current market capitalisation of the token in USD; `None` when Birdeye cannot compute it. (alias `marketCap`)
            fdv: fully-diluted valuation of the token in USD; `None` when Birdeye cannot compute it.
            extensions: free-form dictionary of optional metadata (CoinGecko id, website, social links, etc.); individual values may be `None`, and the whole dict can be `None` when Birdeye has no extra metadata for the token.
            logo_uri: URL of the token logo; `None` if Birdeye does not have a logo for the token. (alias `logoURI`)
            liquidity: total on-chain liquidity of the token expressed in USD.
            last_trade_unix_time: unix-second timestamp of the last observed trade involving the token. (alias `lastTradeUnixTime`)
            last_trade_human_time: ISO-8601 timestamp of the last observed trade involving the token. (alias `lastTradeHumanTime`)
            price: latest known price of the token expressed in USD.
            history_1m_price: snapshot price of the token in USD at the start of the trailing 1m window; `None` if the API has no price datapoint for the start of that window. (alias `history1mPrice`)
            price_change_1m_percent: price change versus the start of the trailing 1m window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange1mPercent`)
            history_5m_price: snapshot price of the token in USD at the start of the trailing 5m window; `None` if the API has no price datapoint for the start of that window. (alias `history5mPrice`)
            price_change_5m_percent: price change versus the start of the trailing 5m window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange5mPercent`)
            history_30m_price: snapshot price of the token in USD at the start of the trailing 30m window; `None` if the API has no price datapoint for the start of that window. (alias `history30mPrice`)
            price_change_30m_percent: price change versus the start of the trailing 30m window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange30mPercent`)
            history_1h_price: snapshot price of the token in USD at the start of the trailing 1h window; `None` if the API has no price datapoint for the start of that window. (alias `history1hPrice`)
            price_change_1h_percent: price change versus the start of the trailing 1h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange1hPercent`)
            history_2h_price: snapshot price of the token in USD at the start of the trailing 2h window; `None` if the API has no price datapoint for the start of that window. (alias `history2hPrice`)
            price_change_2h_percent: price change versus the start of the trailing 2h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange2hPercent`)
            history_4h_price: snapshot price of the token in USD at the start of the trailing 4h window; `None` if the API has no price datapoint for the start of that window. (alias `history4hPrice`)
            price_change_4h_percent: price change versus the start of the trailing 4h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange4hPercent`)
            history_6h_price: snapshot price of the token in USD at the start of the trailing 6h window; `None` if the API has no price datapoint for the start of that window. (alias `history6hPrice`)
            price_change_6h_percent: price change versus the start of the trailing 6h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange6hPercent`)
            history_8h_price: snapshot price of the token in USD at the start of the trailing 8h window; `None` if the API has no price datapoint for the start of that window. (alias `history8hPrice`)
            price_change_8h_percent: price change versus the start of the trailing 8h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange8hPercent`)
            history_12h_price: snapshot price of the token in USD at the start of the trailing 12h window; `None` if the API has no price datapoint for the start of that window. (alias `history12hPrice`)
            price_change_12h_percent: price change versus the start of the trailing 12h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange12hPercent`)
            history_24h_price: snapshot price of the token in USD at the start of the trailing 24h window; `None` if the API has no price datapoint for the start of that window. (alias `history24hPrice`)
            price_change_24h_percent: price change versus the start of the trailing 24h window, expressed in percent; `None` if the change cannot be computed. (alias `priceChange24hPercent`)
            unique_wallet_1m: count of unique wallets that traded the token during the trailing 1m window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet1m`)
            unique_wallet_history_1m: count of unique wallets that traded the token during the previous 1m window; `None` if not available. (alias `uniqueWalletHistory1m`)
            unique_wallet_1m_change_percent: percent change of unique wallets between the current and previous 1m windows; `None` if either window is missing. (alias `uniqueWallet1mChangePercent`)
            unique_wallet_5m: count of unique wallets that traded the token during the trailing 5m window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet5m`)
            unique_wallet_history_5m: count of unique wallets that traded the token during the previous 5m window; `None` if not available. (alias `uniqueWalletHistory5m`)
            unique_wallet_5m_change_percent: percent change of unique wallets between the current and previous 5m windows; `None` if either window is missing. (alias `uniqueWallet5mChangePercent`)
            unique_wallet_30m: count of unique wallets that traded the token during the trailing 30m window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet30m`)
            unique_wallet_history_30m: count of unique wallets that traded the token during the previous 30m window; `None` if not available. (alias `uniqueWalletHistory30m`)
            unique_wallet_30m_change_percent: percent change of unique wallets between the current and previous 30m windows; `None` if either window is missing. (alias `uniqueWallet30mChangePercent`)
            unique_wallet_1h: count of unique wallets that traded the token during the trailing 1h window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet1h`)
            unique_wallet_history_1h: count of unique wallets that traded the token during the previous 1h window; `None` if not available. (alias `uniqueWalletHistory1h`)
            unique_wallet_1h_change_percent: percent change of unique wallets between the current and previous 1h windows; `None` if either window is missing. (alias `uniqueWallet1hChangePercent`)
            unique_wallet_2h: count of unique wallets that traded the token during the trailing 2h window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet2h`)
            unique_wallet_history_2h: count of unique wallets that traded the token during the previous 2h window; `None` if not available. (alias `uniqueWalletHistory2h`)
            unique_wallet_2h_change_percent: percent change of unique wallets between the current and previous 2h windows; `None` if either window is missing. (alias `uniqueWallet2hChangePercent`)
            unique_wallet_4h: count of unique wallets that traded the token during the trailing 4h window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet4h`)
            unique_wallet_history_4h: count of unique wallets that traded the token during the previous 4h window; `None` if not available. (alias `uniqueWalletHistory4h`)
            unique_wallet_4h_change_percent: percent change of unique wallets between the current and previous 4h windows; `None` if either window is missing. (alias `uniqueWallet4hChangePercent`)
            unique_wallet_8h: count of unique wallets that traded the token during the trailing 8h window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet8h`)
            unique_wallet_history_8h: count of unique wallets that traded the token during the previous 8h window; `None` if not available. (alias `uniqueWalletHistory8h`)
            unique_wallet_8h_change_percent: percent change of unique wallets between the current and previous 8h windows; `None` if either window is missing. (alias `uniqueWallet8hChangePercent`)
            unique_wallet_24h: count of unique wallets that traded the token during the trailing 24h window; `None` if Birdeye has not computed the metric for that window. (alias `uniqueWallet24h`)
            unique_wallet_history_24h: count of unique wallets that traded the token during the previous 24h window; `None` if not available. (alias `uniqueWalletHistory24h`)
            unique_wallet_24h_change_percent: percent change of unique wallets between the current and previous 24h windows; `None` if either window is missing. (alias `uniqueWallet24hChangePercent`)
            total_supply: total on-chain supply of the token in UI units; `None` if undetermined. (alias `totalSupply`)
            circulating_supply: currently circulating supply of the token in UI units; `None` if undetermined. (alias `circulatingSupply`)
            holder: number of distinct holders of the token on the chain; `None` if undetermined.
            trade_1m: total number of trades involving the token during the trailing 1m window. (alias `trade1m`)
            trade_history_1m: total number of trades during the previous 1m window. (alias `tradeHistory1m`)
            trade_1m_change_percent: percent change of trade count between the current and previous 1m windows. (alias `trade1mChangePercent`)
            sell_1m: number of sell trades during the trailing 1m window. (alias `sell1m`)
            sell_history_1m: number of sell trades during the previous 1m window. (alias `sellHistory1m`)
            sell_1m_change_percent: percent change of sell count between the current and previous 1m windows. (alias `sell1mChangePercent`)
            buy_1m: number of buy trades during the trailing 1m window. (alias `buy1m`)
            buy_history_1m: number of buy trades during the previous 1m window. (alias `buyHistory1m`)
            buy_1m_change_percent: percent change of buy count between the current and previous 1m windows. (alias `buy1mChangePercent`)
            volume_1m: traded volume during the trailing 1m window, expressed in the token UI units. (alias `v1m`)
            volume_1m_usd: traded volume during the trailing 1m window, expressed in USD. (alias `v1mUSD`)
            volume_history_1m: traded volume during the previous 1m window, expressed in the token UI units. (alias `vHistory1m`)
            volume_history_1m_usd: traded volume during the previous 1m window, expressed in USD. (alias `vHistory1mUSD`)
            volume_1m_change_percent: percent change of traded volume between the current and previous 1m windows. (alias `v1mChangePercent`)
            volume_buy_1m: buy-side traded volume during the trailing 1m window, in the token UI units. (alias `vBuy1m`)
            volume_buy_1m_usd: buy-side traded volume during the trailing 1m window, in USD. (alias `vBuy1mUSD`)
            volume_buy_history_1m: buy-side traded volume during the previous 1m window, in the token UI units. (alias `vBuyHistory1m`)
            volume_buy_history_1m_usd: buy-side traded volume during the previous 1m window, in USD. (alias `vBuyHistory1mUSD`)
            volume_buy_1m_change_percent: percent change of buy-side traded volume between the current and previous 1m windows. (alias `vBuy1mChangePercent`)
            volume_sell_1m: sell-side traded volume during the trailing 1m window, in the token UI units. (alias `vSell1m`)
            volume_sell_1m_usd: sell-side traded volume during the trailing 1m window, in USD. (alias `vSell1mUSD`)
            volume_sell_history_1m: sell-side traded volume during the previous 1m window, in the token UI units. (alias `vSellHistory1m`)
            volume_sell_history_1m_usd: sell-side traded volume during the previous 1m window, in USD. (alias `vSellHistory1mUSD`)
            volume_sell_1m_change_percent: percent change of sell-side traded volume between the current and previous 1m windows. (alias `vSell1mChangePercent`)
            trade_5m: total number of trades involving the token during the trailing 5m window. (alias `trade5m`)
            trade_history_5m: total number of trades during the previous 5m window. (alias `tradeHistory5m`)
            trade_5m_change_percent: percent change of trade count between the current and previous 5m windows. (alias `trade5mChangePercent`)
            sell_5m: number of sell trades during the trailing 5m window. (alias `sell5m`)
            sell_history_5m: number of sell trades during the previous 5m window. (alias `sellHistory5m`)
            sell_5m_change_percent: percent change of sell count between the current and previous 5m windows. (alias `sell5mChangePercent`)
            buy_5m: number of buy trades during the trailing 5m window. (alias `buy5m`)
            buy_history_5m: number of buy trades during the previous 5m window. (alias `buyHistory5m`)
            buy_5m_change_percent: percent change of buy count between the current and previous 5m windows. (alias `buy5mChangePercent`)
            volume_5m: traded volume during the trailing 5m window, expressed in the token UI units. (alias `v5m`)
            volume_5m_usd: traded volume during the trailing 5m window, expressed in USD. (alias `v5mUSD`)
            volume_history_5m: traded volume during the previous 5m window, expressed in the token UI units. (alias `vHistory5m`)
            volume_history_5m_usd: traded volume during the previous 5m window, expressed in USD. (alias `vHistory5mUSD`)
            volume_5m_change_percent: percent change of traded volume between the current and previous 5m windows. (alias `v5mChangePercent`)
            volume_buy_5m: buy-side traded volume during the trailing 5m window, in the token UI units. (alias `vBuy5m`)
            volume_buy_5m_usd: buy-side traded volume during the trailing 5m window, in USD. (alias `vBuy5mUSD`)
            volume_buy_history_5m: buy-side traded volume during the previous 5m window, in the token UI units. (alias `vBuyHistory5m`)
            volume_buy_history_5m_usd: buy-side traded volume during the previous 5m window, in USD. (alias `vBuyHistory5mUSD`)
            volume_buy_5m_change_percent: percent change of buy-side traded volume between the current and previous 5m windows. (alias `vBuy5mChangePercent`)
            volume_sell_5m: sell-side traded volume during the trailing 5m window, in the token UI units. (alias `vSell5m`)
            volume_sell_5m_usd: sell-side traded volume during the trailing 5m window, in USD. (alias `vSell5mUSD`)
            volume_sell_history_5m: sell-side traded volume during the previous 5m window, in the token UI units. (alias `vSellHistory5m`)
            volume_sell_history_5m_usd: sell-side traded volume during the previous 5m window, in USD. (alias `vSellHistory5mUSD`)
            volume_sell_5m_change_percent: percent change of sell-side traded volume between the current and previous 5m windows. (alias `vSell5mChangePercent`)
            trade_30m: total number of trades involving the token during the trailing 30m window. (alias `trade30m`)
            trade_history_30m: total number of trades during the previous 30m window. (alias `tradeHistory30m`)
            trade_30m_change_percent: percent change of trade count between the current and previous 30m windows. (alias `trade30mChangePercent`)
            sell_30m: number of sell trades during the trailing 30m window. (alias `sell30m`)
            sell_history_30m: number of sell trades during the previous 30m window. (alias `sellHistory30m`)
            sell_30m_change_percent: percent change of sell count between the current and previous 30m windows. (alias `sell30mChangePercent`)
            buy_30m: number of buy trades during the trailing 30m window. (alias `buy30m`)
            buy_history_30m: number of buy trades during the previous 30m window. (alias `buyHistory30m`)
            buy_30m_change_percent: percent change of buy count between the current and previous 30m windows. (alias `buy30mChangePercent`)
            volume_30m: traded volume during the trailing 30m window, expressed in the token UI units. (alias `v30m`)
            volume_30m_usd: traded volume during the trailing 30m window, expressed in USD. (alias `v30mUSD`)
            volume_history_30m: traded volume during the previous 30m window, expressed in the token UI units. (alias `vHistory30m`)
            volume_history_30m_usd: traded volume during the previous 30m window, expressed in USD. (alias `vHistory30mUSD`)
            volume_30m_change_percent: percent change of traded volume between the current and previous 30m windows. (alias `v30mChangePercent`)
            volume_buy_30m: buy-side traded volume during the trailing 30m window, in the token UI units. (alias `vBuy30m`)
            volume_buy_30m_usd: buy-side traded volume during the trailing 30m window, in USD. (alias `vBuy30mUSD`)
            volume_buy_history_30m: buy-side traded volume during the previous 30m window, in the token UI units. (alias `vBuyHistory30m`)
            volume_buy_history_30m_usd: buy-side traded volume during the previous 30m window, in USD. (alias `vBuyHistory30mUSD`)
            volume_buy_30m_change_percent: percent change of buy-side traded volume between the current and previous 30m windows. (alias `vBuy30mChangePercent`)
            volume_sell_30m: sell-side traded volume during the trailing 30m window, in the token UI units. (alias `vSell30m`)
            volume_sell_30m_usd: sell-side traded volume during the trailing 30m window, in USD. (alias `vSell30mUSD`)
            volume_sell_history_30m: sell-side traded volume during the previous 30m window, in the token UI units. (alias `vSellHistory30m`)
            volume_sell_history_30m_usd: sell-side traded volume during the previous 30m window, in USD. (alias `vSellHistory30mUSD`)
            volume_sell_30m_change_percent: percent change of sell-side traded volume between the current and previous 30m windows. (alias `vSell30mChangePercent`)
            trade_1h: total number of trades involving the token during the trailing 1h window. (alias `trade1h`)
            trade_history_1h: total number of trades during the previous 1h window. (alias `tradeHistory1h`)
            trade_1h_change_percent: percent change of trade count between the current and previous 1h windows. (alias `trade1hChangePercent`)
            sell_1h: number of sell trades during the trailing 1h window. (alias `sell1h`)
            sell_history_1h: number of sell trades during the previous 1h window. (alias `sellHistory1h`)
            sell_1h_change_percent: percent change of sell count between the current and previous 1h windows. (alias `sell1hChangePercent`)
            buy_1h: number of buy trades during the trailing 1h window. (alias `buy1h`)
            buy_history_1h: number of buy trades during the previous 1h window. (alias `buyHistory1h`)
            buy_1h_change_percent: percent change of buy count between the current and previous 1h windows. (alias `buy1hChangePercent`)
            volume_1h: traded volume during the trailing 1h window, expressed in the token UI units. (alias `v1h`)
            volume_1h_usd: traded volume during the trailing 1h window, expressed in USD. (alias `v1hUSD`)
            volume_history_1h: traded volume during the previous 1h window, expressed in the token UI units. (alias `vHistory1h`)
            volume_history_1h_usd: traded volume during the previous 1h window, expressed in USD. (alias `vHistory1hUSD`)
            volume_1h_change_percent: percent change of traded volume between the current and previous 1h windows. (alias `v1hChangePercent`)
            volume_buy_1h: buy-side traded volume during the trailing 1h window, in the token UI units. (alias `vBuy1h`)
            volume_buy_1h_usd: buy-side traded volume during the trailing 1h window, in USD. (alias `vBuy1hUSD`)
            volume_buy_history_1h: buy-side traded volume during the previous 1h window, in the token UI units. (alias `vBuyHistory1h`)
            volume_buy_history_1h_usd: buy-side traded volume during the previous 1h window, in USD. (alias `vBuyHistory1hUSD`)
            volume_buy_1h_change_percent: percent change of buy-side traded volume between the current and previous 1h windows. (alias `vBuy1hChangePercent`)
            volume_sell_1h: sell-side traded volume during the trailing 1h window, in the token UI units. (alias `vSell1h`)
            volume_sell_1h_usd: sell-side traded volume during the trailing 1h window, in USD. (alias `vSell1hUSD`)
            volume_sell_history_1h: sell-side traded volume during the previous 1h window, in the token UI units. (alias `vSellHistory1h`)
            volume_sell_history_1h_usd: sell-side traded volume during the previous 1h window, in USD. (alias `vSellHistory1hUSD`)
            volume_sell_1h_change_percent: percent change of sell-side traded volume between the current and previous 1h windows. (alias `vSell1hChangePercent`)
            trade_2h: total number of trades involving the token during the trailing 2h window. (alias `trade2h`)
            trade_history_2h: total number of trades during the previous 2h window. (alias `tradeHistory2h`)
            trade_2h_change_percent: percent change of trade count between the current and previous 2h windows. (alias `trade2hChangePercent`)
            sell_2h: number of sell trades during the trailing 2h window. (alias `sell2h`)
            sell_history_2h: number of sell trades during the previous 2h window. (alias `sellHistory2h`)
            sell_2h_change_percent: percent change of sell count between the current and previous 2h windows. (alias `sell2hChangePercent`)
            buy_2h: number of buy trades during the trailing 2h window. (alias `buy2h`)
            buy_history_2h: number of buy trades during the previous 2h window. (alias `buyHistory2h`)
            buy_2h_change_percent: percent change of buy count between the current and previous 2h windows. (alias `buy2hChangePercent`)
            volume_2h: traded volume during the trailing 2h window, expressed in the token UI units. (alias `v2h`)
            volume_2h_usd: traded volume during the trailing 2h window, expressed in USD. (alias `v2hUSD`)
            volume_history_2h: traded volume during the previous 2h window, expressed in the token UI units. (alias `vHistory2h`)
            volume_history_2h_usd: traded volume during the previous 2h window, expressed in USD. (alias `vHistory2hUSD`)
            volume_2h_change_percent: percent change of traded volume between the current and previous 2h windows. (alias `v2hChangePercent`)
            volume_buy_2h: buy-side traded volume during the trailing 2h window, in the token UI units. (alias `vBuy2h`)
            volume_buy_2h_usd: buy-side traded volume during the trailing 2h window, in USD. (alias `vBuy2hUSD`)
            volume_buy_history_2h: buy-side traded volume during the previous 2h window, in the token UI units. (alias `vBuyHistory2h`)
            volume_buy_history_2h_usd: buy-side traded volume during the previous 2h window, in USD. (alias `vBuyHistory2hUSD`)
            volume_buy_2h_change_percent: percent change of buy-side traded volume between the current and previous 2h windows. (alias `vBuy2hChangePercent`)
            volume_sell_2h: sell-side traded volume during the trailing 2h window, in the token UI units. (alias `vSell2h`)
            volume_sell_2h_usd: sell-side traded volume during the trailing 2h window, in USD. (alias `vSell2hUSD`)
            volume_sell_history_2h: sell-side traded volume during the previous 2h window, in the token UI units. (alias `vSellHistory2h`)
            volume_sell_history_2h_usd: sell-side traded volume during the previous 2h window, in USD. (alias `vSellHistory2hUSD`)
            volume_sell_2h_change_percent: percent change of sell-side traded volume between the current and previous 2h windows. (alias `vSell2hChangePercent`)
            trade_4h: total number of trades involving the token during the trailing 4h window. (alias `trade4h`)
            trade_history_4h: total number of trades during the previous 4h window. (alias `tradeHistory4h`)
            trade_4h_change_percent: percent change of trade count between the current and previous 4h windows. (alias `trade4hChangePercent`)
            sell_4h: number of sell trades during the trailing 4h window. (alias `sell4h`)
            sell_history_4h: number of sell trades during the previous 4h window. (alias `sellHistory4h`)
            sell_4h_change_percent: percent change of sell count between the current and previous 4h windows. (alias `sell4hChangePercent`)
            buy_4h: number of buy trades during the trailing 4h window. (alias `buy4h`)
            buy_history_4h: number of buy trades during the previous 4h window. (alias `buyHistory4h`)
            buy_4h_change_percent: percent change of buy count between the current and previous 4h windows. (alias `buy4hChangePercent`)
            volume_4h: traded volume during the trailing 4h window, expressed in the token UI units. (alias `v4h`)
            volume_4h_usd: traded volume during the trailing 4h window, expressed in USD. (alias `v4hUSD`)
            volume_history_4h: traded volume during the previous 4h window, expressed in the token UI units. (alias `vHistory4h`)
            volume_history_4h_usd: traded volume during the previous 4h window, expressed in USD. (alias `vHistory4hUSD`)
            volume_4h_change_percent: percent change of traded volume between the current and previous 4h windows. (alias `v4hChangePercent`)
            volume_buy_4h: buy-side traded volume during the trailing 4h window, in the token UI units. (alias `vBuy4h`)
            volume_buy_4h_usd: buy-side traded volume during the trailing 4h window, in USD. (alias `vBuy4hUSD`)
            volume_buy_history_4h: buy-side traded volume during the previous 4h window, in the token UI units. (alias `vBuyHistory4h`)
            volume_buy_history_4h_usd: buy-side traded volume during the previous 4h window, in USD. (alias `vBuyHistory4hUSD`)
            volume_buy_4h_change_percent: percent change of buy-side traded volume between the current and previous 4h windows. (alias `vBuy4hChangePercent`)
            volume_sell_4h: sell-side traded volume during the trailing 4h window, in the token UI units. (alias `vSell4h`)
            volume_sell_4h_usd: sell-side traded volume during the trailing 4h window, in USD. (alias `vSell4hUSD`)
            volume_sell_history_4h: sell-side traded volume during the previous 4h window, in the token UI units. (alias `vSellHistory4h`)
            volume_sell_history_4h_usd: sell-side traded volume during the previous 4h window, in USD. (alias `vSellHistory4hUSD`)
            volume_sell_4h_change_percent: percent change of sell-side traded volume between the current and previous 4h windows. (alias `vSell4hChangePercent`)
            trade_8h: total number of trades involving the token during the trailing 8h window. (alias `trade8h`)
            trade_history_8h: total number of trades during the previous 8h window. (alias `tradeHistory8h`)
            trade_8h_change_percent: percent change of trade count between the current and previous 8h windows. (alias `trade8hChangePercent`)
            sell_8h: number of sell trades during the trailing 8h window. (alias `sell8h`)
            sell_history_8h: number of sell trades during the previous 8h window. (alias `sellHistory8h`)
            sell_8h_change_percent: percent change of sell count between the current and previous 8h windows. (alias `sell8hChangePercent`)
            buy_8h: number of buy trades during the trailing 8h window. (alias `buy8h`)
            buy_history_8h: number of buy trades during the previous 8h window. (alias `buyHistory8h`)
            buy_8h_change_percent: percent change of buy count between the current and previous 8h windows. (alias `buy8hChangePercent`)
            volume_8h: traded volume during the trailing 8h window, expressed in the token UI units. (alias `v8h`)
            volume_8h_usd: traded volume during the trailing 8h window, expressed in USD. (alias `v8hUSD`)
            volume_history_8h: traded volume during the previous 8h window, expressed in the token UI units. (alias `vHistory8h`)
            volume_history_8h_usd: traded volume during the previous 8h window, expressed in USD. (alias `vHistory8hUSD`)
            volume_8h_change_percent: percent change of traded volume between the current and previous 8h windows. (alias `v8hChangePercent`)
            volume_buy_8h: buy-side traded volume during the trailing 8h window, in the token UI units. (alias `vBuy8h`)
            volume_buy_8h_usd: buy-side traded volume during the trailing 8h window, in USD. (alias `vBuy8hUSD`)
            volume_buy_history_8h: buy-side traded volume during the previous 8h window, in the token UI units. (alias `vBuyHistory8h`)
            volume_buy_history_8h_usd: buy-side traded volume during the previous 8h window, in USD. (alias `vBuyHistory8hUSD`)
            volume_buy_8h_change_percent: percent change of buy-side traded volume between the current and previous 8h windows. (alias `vBuy8hChangePercent`)
            volume_sell_8h: sell-side traded volume during the trailing 8h window, in the token UI units. (alias `vSell8h`)
            volume_sell_8h_usd: sell-side traded volume during the trailing 8h window, in USD. (alias `vSell8hUSD`)
            volume_sell_history_8h: sell-side traded volume during the previous 8h window, in the token UI units. (alias `vSellHistory8h`)
            volume_sell_history_8h_usd: sell-side traded volume during the previous 8h window, in USD. (alias `vSellHistory8hUSD`)
            volume_sell_8h_change_percent: percent change of sell-side traded volume between the current and previous 8h windows. (alias `vSell8hChangePercent`)
            trade_24h: total number of trades involving the token during the trailing 24h window. (alias `trade24h`)
            trade_history_24h: total number of trades during the previous 24h window. (alias `tradeHistory24h`)
            trade_24h_change_percent: percent change of trade count between the current and previous 24h windows. (alias `trade24hChangePercent`)
            sell_24h: number of sell trades during the trailing 24h window. (alias `sell24h`)
            sell_history_24h: number of sell trades during the previous 24h window. (alias `sellHistory24h`)
            sell_24h_change_percent: percent change of sell count between the current and previous 24h windows. (alias `sell24hChangePercent`)
            buy_24h: number of buy trades during the trailing 24h window. (alias `buy24h`)
            buy_history_24h: number of buy trades during the previous 24h window. (alias `buyHistory24h`)
            buy_24h_change_percent: percent change of buy count between the current and previous 24h windows. (alias `buy24hChangePercent`)
            volume_24h: traded volume during the trailing 24h window, expressed in the token UI units. (alias `v24h`)
            volume_24h_usd: traded volume during the trailing 24h window, expressed in USD. (alias `v24hUSD`)
            volume_history_24h: traded volume during the previous 24h window, expressed in the token UI units. (alias `vHistory24h`)
            volume_history_24h_usd: traded volume during the previous 24h window, expressed in USD. (alias `vHistory24hUSD`)
            volume_24h_change_percent: percent change of traded volume between the current and previous 24h windows. (alias `v24hChangePercent`)
            volume_buy_24h: buy-side traded volume during the trailing 24h window, in the token UI units. (alias `vBuy24h`)
            volume_buy_24h_usd: buy-side traded volume during the trailing 24h window, in USD. (alias `vBuy24hUSD`)
            volume_buy_history_24h: buy-side traded volume during the previous 24h window, in the token UI units. (alias `vBuyHistory24h`)
            volume_buy_history_24h_usd: buy-side traded volume during the previous 24h window, in USD. (alias `vBuyHistory24hUSD`)
            volume_buy_24h_change_percent: percent change of buy-side traded volume between the current and previous 24h windows. (alias `vBuy24hChangePercent`)
            volume_sell_24h: sell-side traded volume during the trailing 24h window, in the token UI units. (alias `vSell24h`)
            volume_sell_24h_usd: sell-side traded volume during the trailing 24h window, in USD. (alias `vSell24hUSD`)
            volume_sell_history_24h: sell-side traded volume during the previous 24h window, in the token UI units. (alias `vSellHistory24h`)
            volume_sell_history_24h_usd: sell-side traded volume during the previous 24h window, in USD. (alias `vSellHistory24hUSD`)
            volume_sell_24h_change_percent: percent change of sell-side traded volume between the current and previous 24h windows. (alias `vSell24hChangePercent`)
            number_markets: number of active markets (trading pairs) Birdeye tracks for the token; `None` if undetermined. (alias `numberMarkets`)
            is_scaled_ui_token: `True` when the token is a scaled-UI-amount SPL token (Solana only); `None` outside Solana or when undetermined. (alias `isScaledUiToken`)
            multiplier: scaling multiplier applied by the API to UI amounts of scaled-UI-amount tokens; `None` when not applicable.
    """
    address: str
    decimals: int
    symbol: str
    name: str
    market_cap: float | None = Field(alias = "marketCap", default = None)
    fdv: float | None = None
    extensions: dict[str, str | None] | None = None
    logo_uri: str | None = Field(alias = "logoURI", default = None)
    liquidity: float
    last_trade_unix_time: int = Field(alias = "lastTradeUnixTime")
    last_trade_human_time: datetime = Field(alias = "lastTradeHumanTime")
    price: float
    history_1m_price: float | None = Field(alias = "history1mPrice", default = None)
    price_change_1m_percent: float | None = Field(alias = "priceChange1mPercent", default = None)
    history_5m_price: float | None = Field(alias = "history5mPrice", default = None)
    price_change_5m_percent: float | None = Field(alias = "priceChange5mPercent", default = None)
    history_30m_price: float | None = Field(alias = "history30mPrice", default = None)
    price_change_30m_percent: float | None = Field(alias = "priceChange30mPercent", default = None)
    history_1h_price: float | None = Field(alias = "history1hPrice", default = None)
    price_change_1h_percent: float | None = Field(alias = "priceChange1hPercent", default = None)
    history_2h_price: float | None = Field(alias = "history2hPrice", default = None)
    price_change_2h_percent: float | None = Field(alias = "priceChange2hPercent", default = None)
    history_4h_price: float | None = Field(alias = "history4hPrice", default = None)
    price_change_4h_percent: float | None = Field(alias = "priceChange4hPercent", default = None)
    history_6h_price: float | None = Field(alias = "history6hPrice", default = None)
    price_change_6h_percent: float | None = Field(alias = "priceChange6hPercent", default = None)
    history_8h_price: float | None = Field(alias = "history8hPrice", default = None)
    price_change_8h_percent: float | None = Field(alias = "priceChange8hPercent", default = None)
    history_12h_price: float | None = Field(alias = "history12hPrice", default = None)
    price_change_12h_percent: float | None = Field(alias = "priceChange12hPercent", default = None)
    history_24h_price: float | None = Field(alias = "history24hPrice", default = None)
    price_change_24h_percent: float | None = Field(alias = "priceChange24hPercent", default = None)
    unique_wallet_1m: int | None = Field(alias = "uniqueWallet1m", default = None)
    unique_wallet_history_1m: int | None = Field(alias = "uniqueWalletHistory1m", default = None)
    unique_wallet_1m_change_percent: float | None = Field(alias = "uniqueWallet1mChangePercent", default = None)
    unique_wallet_5m: int | None = Field(alias = "uniqueWallet5m", default = None)
    unique_wallet_history_5m: int | None = Field(alias = "uniqueWalletHistory5m", default = None)
    unique_wallet_5m_change_percent: float | None = Field(alias = "uniqueWallet5mChangePercent", default = None)
    unique_wallet_30m: int | None = Field(alias = "uniqueWallet30m", default = None)
    unique_wallet_history_30m: int | None = Field(alias = "uniqueWalletHistory30m", default = None)
    unique_wallet_30m_change_percent: float | None = Field(alias = "uniqueWallet30mChangePercent", default = None)
    unique_wallet_1h: int | None = Field(alias = "uniqueWallet1h", default = None)
    unique_wallet_history_1h: int | None = Field(alias = "uniqueWalletHistory1h", default = None)
    unique_wallet_1h_change_percent: float | None = Field(alias = "uniqueWallet1hChangePercent", default = None)
    unique_wallet_2h: int | None = Field(alias = "uniqueWallet2h", default = None)
    unique_wallet_history_2h: int | None = Field(alias = "uniqueWalletHistory2h", default = None)
    unique_wallet_2h_change_percent: float | None = Field(alias = "uniqueWallet2hChangePercent", default = None)
    unique_wallet_4h: int | None = Field(alias = "uniqueWallet4h", default = None)
    unique_wallet_history_4h: int | None = Field(alias = "uniqueWalletHistory4h", default = None)
    unique_wallet_4h_change_percent: float | None = Field(alias = "uniqueWallet4hChangePercent", default = None)
    unique_wallet_8h: int | None = Field(alias = "uniqueWallet8h", default = None)
    unique_wallet_history_8h: int | None = Field(alias = "uniqueWalletHistory8h", default = None)
    unique_wallet_8h_change_percent: float | None = Field(alias = "uniqueWallet8hChangePercent", default = None)
    unique_wallet_24h: int | None = Field(alias = "uniqueWallet24h", default = None)
    unique_wallet_history_24h: int | None = Field(alias = "uniqueWalletHistory24h", default = None)
    unique_wallet_24h_change_percent: float | None = Field(alias = "uniqueWallet24hChangePercent", default = None)
    total_supply: float | None = Field(alias = "totalSupply", default = None)
    circulating_supply: float | None = Field(alias = "circulatingSupply", default = None)
    holder: int | None = None
    trade_1m: int | None = Field(alias = "trade1m", default = None)
    trade_history_1m: int | None = Field(alias = "tradeHistory1m", default = None)
    trade_1m_change_percent: float | None = Field(alias = "trade1mChangePercent", default = None)
    sell_1m: int | None = Field(alias = "sell1m", default = None)
    sell_history_1m: int | None = Field(alias = "sellHistory1m", default = None)
    sell_1m_change_percent: float | None = Field(alias = "sell1mChangePercent", default = None)
    buy_1m: int | None = Field(alias = "buy1m", default = None)
    buy_history_1m: int | None = Field(alias = "buyHistory1m", default = None)
    buy_1m_change_percent: float | None = Field(alias = "buy1mChangePercent", default = None)
    volume_1m: float | None = Field(alias = "v1m", default = None)
    volume_1m_usd: float | None = Field(alias = "v1mUSD", default = None)
    volume_history_1m: float | None = Field(alias = "vHistory1m", default = None)
    volume_history_1m_usd: float | None = Field(alias = "vHistory1mUSD", default = None)
    volume_1m_change_percent: float | None = Field(alias = "v1mChangePercent", default = None)
    volume_buy_1m: float | None = Field(alias = "vBuy1m", default = None)
    volume_buy_1m_usd: float | None = Field(alias = "vBuy1mUSD", default = None)
    volume_buy_history_1m: float | None = Field(alias = "vBuyHistory1m", default = None)
    volume_buy_history_1m_usd: float | None = Field(alias = "vBuyHistory1mUSD", default = None)
    volume_buy_1m_change_percent: float | None = Field(alias = "vBuy1mChangePercent", default = None)
    volume_sell_1m: float | None = Field(alias = "vSell1m", default = None)
    volume_sell_1m_usd: float | None = Field(alias = "vSell1mUSD", default = None)
    volume_sell_history_1m: float | None = Field(alias = "vSellHistory1m", default = None)
    volume_sell_history_1m_usd: float | None = Field(alias = "vSellHistory1mUSD", default = None)
    volume_sell_1m_change_percent: float | None = Field(alias = "vSell1mChangePercent", default = None)
    trade_5m: int | None = Field(alias = "trade5m", default = None)
    trade_history_5m: int | None = Field(alias = "tradeHistory5m", default = None)
    trade_5m_change_percent: float | None = Field(alias = "trade5mChangePercent", default = None)
    sell_5m: int | None = Field(alias = "sell5m", default = None)
    sell_history_5m: int | None = Field(alias = "sellHistory5m", default = None)
    sell_5m_change_percent: float | None = Field(alias = "sell5mChangePercent", default = None)
    buy_5m: int | None = Field(alias = "buy5m", default = None)
    buy_history_5m: int | None = Field(alias = "buyHistory5m", default = None)
    buy_5m_change_percent: float | None = Field(alias = "buy5mChangePercent", default = None)
    volume_5m: float | None = Field(alias = "v5m", default = None)
    volume_5m_usd: float | None = Field(alias = "v5mUSD", default = None)
    volume_history_5m: float | None = Field(alias = "vHistory5m", default = None)
    volume_history_5m_usd: float | None = Field(alias = "vHistory5mUSD", default = None)
    volume_5m_change_percent: float | None = Field(alias = "v5mChangePercent", default = None)
    volume_buy_5m: float | None = Field(alias = "vBuy5m", default = None)
    volume_buy_5m_usd: float | None = Field(alias = "vBuy5mUSD", default = None)
    volume_buy_history_5m: float | None = Field(alias = "vBuyHistory5m", default = None)
    volume_buy_history_5m_usd: float | None = Field(alias = "vBuyHistory5mUSD", default = None)
    volume_buy_5m_change_percent: float | None = Field(alias = "vBuy5mChangePercent", default = None)
    volume_sell_5m: float | None = Field(alias = "vSell5m", default = None)
    volume_sell_5m_usd: float | None = Field(alias = "vSell5mUSD", default = None)
    volume_sell_history_5m: float | None = Field(alias = "vSellHistory5m", default = None)
    volume_sell_history_5m_usd: float | None = Field(alias = "vSellHistory5mUSD", default = None)
    volume_sell_5m_change_percent: float | None = Field(alias = "vSell5mChangePercent", default = None)
    trade_30m: int | None = Field(alias = "trade30m", default = None)
    trade_history_30m: int | None = Field(alias = "tradeHistory30m", default = None)
    trade_30m_change_percent: float | None = Field(alias = "trade30mChangePercent", default = None)
    sell_30m: int | None = Field(alias = "sell30m", default = None)
    sell_history_30m: int | None = Field(alias = "sellHistory30m", default = None)
    sell_30m_change_percent: float | None = Field(alias = "sell30mChangePercent", default = None)
    buy_30m: int | None = Field(alias = "buy30m", default = None)
    buy_history_30m: int | None = Field(alias = "buyHistory30m", default = None)
    buy_30m_change_percent: float | None = Field(alias = "buy30mChangePercent", default = None)
    volume_30m: float | None = Field(alias = "v30m", default = None)
    volume_30m_usd: float | None = Field(alias = "v30mUSD", default = None)
    volume_history_30m: float | None = Field(alias = "vHistory30m", default = None)
    volume_history_30m_usd: float | None = Field(alias = "vHistory30mUSD", default = None)
    volume_30m_change_percent: float | None = Field(alias = "v30mChangePercent", default = None)
    volume_buy_30m: float | None = Field(alias = "vBuy30m", default = None)
    volume_buy_30m_usd: float | None = Field(alias = "vBuy30mUSD", default = None)
    volume_buy_history_30m: float | None = Field(alias = "vBuyHistory30m", default = None)
    volume_buy_history_30m_usd: float | None = Field(alias = "vBuyHistory30mUSD", default = None)
    volume_buy_30m_change_percent: float | None = Field(alias = "vBuy30mChangePercent", default = None)
    volume_sell_30m: float | None = Field(alias = "vSell30m", default = None)
    volume_sell_30m_usd: float | None = Field(alias = "vSell30mUSD", default = None)
    volume_sell_history_30m: float | None = Field(alias = "vSellHistory30m", default = None)
    volume_sell_history_30m_usd: float | None = Field(alias = "vSellHistory30mUSD", default = None)
    volume_sell_30m_change_percent: float | None = Field(alias = "vSell30mChangePercent", default = None)
    trade_1h: int | None = Field(alias = "trade1h", default = None)
    trade_history_1h: int | None = Field(alias = "tradeHistory1h", default = None)
    trade_1h_change_percent: float | None = Field(alias = "trade1hChangePercent", default = None)
    sell_1h: int | None = Field(alias = "sell1h", default = None)
    sell_history_1h: int | None = Field(alias = "sellHistory1h", default = None)
    sell_1h_change_percent: float | None = Field(alias = "sell1hChangePercent", default = None)
    buy_1h: int | None = Field(alias = "buy1h", default = None)
    buy_history_1h: int | None = Field(alias = "buyHistory1h", default = None)
    buy_1h_change_percent: float | None = Field(alias = "buy1hChangePercent", default = None)
    volume_1h: float | None = Field(alias = "v1h", default = None)
    volume_1h_usd: float | None = Field(alias = "v1hUSD", default = None)
    volume_history_1h: float | None = Field(alias = "vHistory1h", default = None)
    volume_history_1h_usd: float | None = Field(alias = "vHistory1hUSD", default = None)
    volume_1h_change_percent: float | None = Field(alias = "v1hChangePercent", default = None)
    volume_buy_1h: float | None = Field(alias = "vBuy1h", default = None)
    volume_buy_1h_usd: float | None = Field(alias = "vBuy1hUSD", default = None)
    volume_buy_history_1h: float | None = Field(alias = "vBuyHistory1h", default = None)
    volume_buy_history_1h_usd: float | None = Field(alias = "vBuyHistory1hUSD", default = None)
    volume_buy_1h_change_percent: float | None = Field(alias = "vBuy1hChangePercent", default = None)
    volume_sell_1h: float | None = Field(alias = "vSell1h", default = None)
    volume_sell_1h_usd: float | None = Field(alias = "vSell1hUSD", default = None)
    volume_sell_history_1h: float | None = Field(alias = "vSellHistory1h", default = None)
    volume_sell_history_1h_usd: float | None = Field(alias = "vSellHistory1hUSD", default = None)
    volume_sell_1h_change_percent: float | None = Field(alias = "vSell1hChangePercent", default = None)
    trade_2h: int | None = Field(alias = "trade2h", default = None)
    trade_history_2h: int | None = Field(alias = "tradeHistory2h", default = None)
    trade_2h_change_percent: float | None = Field(alias = "trade2hChangePercent", default = None)
    sell_2h: int | None = Field(alias = "sell2h", default = None)
    sell_history_2h: int | None = Field(alias = "sellHistory2h", default = None)
    sell_2h_change_percent: float | None = Field(alias = "sell2hChangePercent", default = None)
    buy_2h: int | None = Field(alias = "buy2h", default = None)
    buy_history_2h: int | None = Field(alias = "buyHistory2h", default = None)
    buy_2h_change_percent: float | None = Field(alias = "buy2hChangePercent", default = None)
    volume_2h: float | None = Field(alias = "v2h", default = None)
    volume_2h_usd: float | None = Field(alias = "v2hUSD", default = None)
    volume_history_2h: float | None = Field(alias = "vHistory2h", default = None)
    volume_history_2h_usd: float | None = Field(alias = "vHistory2hUSD", default = None)
    volume_2h_change_percent: float | None = Field(alias = "v2hChangePercent", default = None)
    volume_buy_2h: float | None = Field(alias = "vBuy2h", default = None)
    volume_buy_2h_usd: float | None = Field(alias = "vBuy2hUSD", default = None)
    volume_buy_history_2h: float | None = Field(alias = "vBuyHistory2h", default = None)
    volume_buy_history_2h_usd: float | None = Field(alias = "vBuyHistory2hUSD", default = None)
    volume_buy_2h_change_percent: float | None = Field(alias = "vBuy2hChangePercent", default = None)
    volume_sell_2h: float | None = Field(alias = "vSell2h", default = None)
    volume_sell_2h_usd: float | None = Field(alias = "vSell2hUSD", default = None)
    volume_sell_history_2h: float | None = Field(alias = "vSellHistory2h", default = None)
    volume_sell_history_2h_usd: float | None = Field(alias = "vSellHistory2hUSD", default = None)
    volume_sell_2h_change_percent: float | None = Field(alias = "vSell2hChangePercent", default = None)
    trade_4h: int | None = Field(alias = "trade4h", default = None)
    trade_history_4h: int | None = Field(alias = "tradeHistory4h", default = None)
    trade_4h_change_percent: float | None = Field(alias = "trade4hChangePercent", default = None)
    sell_4h: int | None = Field(alias = "sell4h", default = None)
    sell_history_4h: int | None = Field(alias = "sellHistory4h", default = None)
    sell_4h_change_percent: float | None = Field(alias = "sell4hChangePercent", default = None)
    buy_4h: int | None = Field(alias = "buy4h", default = None)
    buy_history_4h: int | None = Field(alias = "buyHistory4h", default = None)
    buy_4h_change_percent: float | None = Field(alias = "buy4hChangePercent", default = None)
    volume_4h: float | None = Field(alias = "v4h", default = None)
    volume_4h_usd: float | None = Field(alias = "v4hUSD", default = None)
    volume_history_4h: float | None = Field(alias = "vHistory4h", default = None)
    volume_history_4h_usd: float | None = Field(alias = "vHistory4hUSD", default = None)
    volume_4h_change_percent: float | None = Field(alias = "v4hChangePercent", default = None)
    volume_buy_4h: float | None = Field(alias = "vBuy4h", default = None)
    volume_buy_4h_usd: float | None = Field(alias = "vBuy4hUSD", default = None)
    volume_buy_history_4h: float | None = Field(alias = "vBuyHistory4h", default = None)
    volume_buy_history_4h_usd: float | None = Field(alias = "vBuyHistory4hUSD", default = None)
    volume_buy_4h_change_percent: float | None = Field(alias = "vBuy4hChangePercent", default = None)
    volume_sell_4h: float | None = Field(alias = "vSell4h", default = None)
    volume_sell_4h_usd: float | None = Field(alias = "vSell4hUSD", default = None)
    volume_sell_history_4h: float | None = Field(alias = "vSellHistory4h", default = None)
    volume_sell_history_4h_usd: float | None = Field(alias = "vSellHistory4hUSD", default = None)
    volume_sell_4h_change_percent: float | None = Field(alias = "vSell4hChangePercent", default = None)
    trade_8h: int | None = Field(alias = "trade8h", default = None)
    trade_history_8h: int | None = Field(alias = "tradeHistory8h", default = None)
    trade_8h_change_percent: float | None = Field(alias = "trade8hChangePercent", default = None)
    sell_8h: int | None = Field(alias = "sell8h", default = None)
    sell_history_8h: int | None = Field(alias = "sellHistory8h", default = None)
    sell_8h_change_percent: float | None = Field(alias = "sell8hChangePercent", default = None)
    buy_8h: int | None = Field(alias = "buy8h", default = None)
    buy_history_8h: int | None = Field(alias = "buyHistory8h", default = None)
    buy_8h_change_percent: float | None = Field(alias = "buy8hChangePercent", default = None)
    volume_8h: float | None = Field(alias = "v8h", default = None)
    volume_8h_usd: float | None = Field(alias = "v8hUSD", default = None)
    volume_history_8h: float | None = Field(alias = "vHistory8h", default = None)
    volume_history_8h_usd: float | None = Field(alias = "vHistory8hUSD", default = None)
    volume_8h_change_percent: float | None = Field(alias = "v8hChangePercent", default = None)
    volume_buy_8h: float | None = Field(alias = "vBuy8h", default = None)
    volume_buy_8h_usd: float | None = Field(alias = "vBuy8hUSD", default = None)
    volume_buy_history_8h: float | None = Field(alias = "vBuyHistory8h", default = None)
    volume_buy_history_8h_usd: float | None = Field(alias = "vBuyHistory8hUSD", default = None)
    volume_buy_8h_change_percent: float | None = Field(alias = "vBuy8hChangePercent", default = None)
    volume_sell_8h: float | None = Field(alias = "vSell8h", default = None)
    volume_sell_8h_usd: float | None = Field(alias = "vSell8hUSD", default = None)
    volume_sell_history_8h: float | None = Field(alias = "vSellHistory8h", default = None)
    volume_sell_history_8h_usd: float | None = Field(alias = "vSellHistory8hUSD", default = None)
    volume_sell_8h_change_percent: float | None = Field(alias = "vSell8hChangePercent", default = None)
    trade_24h: int | None = Field(alias = "trade24h", default = None)
    trade_history_24h: int | None = Field(alias = "tradeHistory24h", default = None)
    trade_24h_change_percent: float | None = Field(alias = "trade24hChangePercent", default = None)
    sell_24h: int | None = Field(alias = "sell24h", default = None)
    sell_history_24h: int | None = Field(alias = "sellHistory24h", default = None)
    sell_24h_change_percent: float | None = Field(alias = "sell24hChangePercent", default = None)
    buy_24h: int | None = Field(alias = "buy24h", default = None)
    buy_history_24h: int | None = Field(alias = "buyHistory24h", default = None)
    buy_24h_change_percent: float | None = Field(alias = "buy24hChangePercent", default = None)
    volume_24h: float | None = Field(alias = "v24h", default = None)
    volume_24h_usd: float | None = Field(alias = "v24hUSD", default = None)
    volume_history_24h: float | None = Field(alias = "vHistory24h", default = None)
    volume_history_24h_usd: float | None = Field(alias = "vHistory24hUSD", default = None)
    volume_24h_change_percent: float | None = Field(alias = "v24hChangePercent", default = None)
    volume_buy_24h: float | None = Field(alias = "vBuy24h", default = None)
    volume_buy_24h_usd: float | None = Field(alias = "vBuy24hUSD", default = None)
    volume_buy_history_24h: float | None = Field(alias = "vBuyHistory24h", default = None)
    volume_buy_history_24h_usd: float | None = Field(alias = "vBuyHistory24hUSD", default = None)
    volume_buy_24h_change_percent: float | None = Field(alias = "vBuy24hChangePercent", default = None)
    volume_sell_24h: float | None = Field(alias = "vSell24h", default = None)
    volume_sell_24h_usd: float | None = Field(alias = "vSell24hUSD", default = None)
    volume_sell_history_24h: float | None = Field(alias = "vSellHistory24h", default = None)
    volume_sell_history_24h_usd: float | None = Field(alias = "vSellHistory24hUSD", default = None)
    volume_sell_24h_change_percent: float | None = Field(alias = "vSell24hChangePercent", default = None)
    number_markets: int | None = Field(alias = "numberMarkets", default = None)
    is_scaled_ui_token: bool | None = Field(alias = "isScaledUiToken", default = None)
    multiplier: float | None = None

    @field_validator("last_trade_human_time")
    def parse_last_trade_human_time(cls, dt_raw: str | datetime) -> datetime:
        if isinstance(dt_raw, str):
            return datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
        return dt_raw

class GetTokenOverviewResponse(BaseModel):
    """
        Model used to represent the **Token - Overview** endpoint from birdeye API.

        Attributes:
            data: token analytics payload (identity, price, liquidity, supply, per-window
                trade/volume activity, etc.).
            success: `True` when the API call completed without errors.
    """
    data: GetTokenOverviewData
    success: bool

# classes used on GET "Token - Creation Token Info" endpoint
class GetTokenCreationInfoData(BaseModel):
    """
        Creation metadata of a token returned by the Birdeye
        **Token - Creation Token Info** endpoint.

        Attributes:
            transaction_hash: hash of the on-chain transaction that minted the token
                (alias `txHash`).
            slot: slot in which the mint transaction was processed (Solana-style ordinal).
            token_address: contract address of the freshly created token (alias `tokenAddress`).
            decimals: number of decimal places used by the token.
            owner: address that signed and paid for the creation transaction.
            block_unix_time: timestamp of the block containing the creation transaction,
                expressed as unix seconds (alias `blockUnixTime`).
            block_human_time: human-readable ISO-8601 timestamp of the same block as
                `block_unix_time` (alias `blockHumanTime`).
    """
    transaction_hash: str = Field(alias = "txHash")
    slot: int
    token_address: str = Field(alias = "tokenAddress")
    decimals: int
    owner: str
    block_unix_time: int = Field(alias = "blockUnixTime")
    block_human_time: datetime = Field(alias = "blockHumanTime")

    @field_validator("block_human_time")
    def parse_block_human_time(cls, dt_raw: str | datetime) -> datetime:
        if isinstance(dt_raw, str):
            # Birdeye returns ISO timestamps with a trailing "Z" and optional milliseconds.
            return datetime.fromisoformat(dt_raw.replace("Z", "+00:00"))
        return dt_raw

class GetTokenCreationInfoResponse(BaseModel):
    """
        Model used to represent the **Token - Creation Token Info** endpoint from birdeye API.

        Attributes:
            data: token creation metadata payload.
            success: `True` when the API call completed without errors.
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