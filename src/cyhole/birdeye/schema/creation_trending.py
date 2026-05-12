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

