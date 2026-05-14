from datetime import datetime

from pydantic import BaseModel, Field, field_validator

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



# classes used on GET "Token - Trending List" endpoint
class GetTokenTrendingItem(BaseModel):
    """
        Single trending-token entry returned by the Birdeye Token - Trending List endpoint.

        Attributes:
            rank: Birdeye's internal trending rank (1 = top trending).
            address: contract address of the token on the selected chain.
            symbol: ticker symbol of the token.
            name: human-readable name of the token.
            decimals: number of decimal places used by the token.
            logo_uri: URL of the token logo (alias `logoURI`); `None` when Birdeye does not have a
                logo for the token.
            price: latest known price of the token in USD.
            liquidity: total on-chain liquidity in USD.
            marketcap: current market capitalisation in USD.
            fdv: fully-diluted valuation in USD.
            volume_24h_usd: USD traded volume over the trailing 24h window (alias `volume24hUSD`).
            volume_24h_change_percent: percent change of 24h USD volume vs the previous 24h window
                (alias `volume24hChangePercent`).
            price_24h_change_percent: percent price change vs 24h ago (alias `price24hChangePercent`).
    """
    rank: int
    address: str
    symbol: str
    name: str
    decimals: int
    logo_uri: str | None = Field(alias = "logoURI", default = None)
    price: float
    liquidity: float
    marketcap: float
    fdv: float
    volume_24h_usd: float = Field(alias = "volume24hUSD")
    volume_24h_change_percent: float = Field(alias = "volume24hChangePercent")
    price_24h_change_percent: float = Field(alias = "price24hChangePercent")

class GetTokenTrendingData(BaseModel):
    """
        Payload of the Token - Trending List response.

        Attributes:
            update_unix_time: unix-second timestamp at which Birdeye last refreshed the trending list
                (alias `updateUnixTime`).
            update_time: human-readable timestamp matching `update_unix_time` (alias `updateTime`).
            total: total number of tokens in Birdeye's trending universe (not the page size).
            tokens: ranked list of trending tokens returned in this page.
    """
    update_unix_time: int = Field(alias = "updateUnixTime")
    update_time: str = Field(alias = "updateTime")
    total: int
    tokens: list[GetTokenTrendingItem]

class GetTokenTrendingResponse(BaseModel):
    """
        Model used to represent the **Token - Trending List** endpoint from birdeye API.

        Attributes:
            data: trending-list payload (refresh timestamp + ranked tokens).
            success: `True` when the API call completed without errors.
    """
    data: GetTokenTrendingData
    success: bool
