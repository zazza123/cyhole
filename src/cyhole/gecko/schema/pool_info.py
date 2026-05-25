"""Schemas for the Pool Tokens Info endpoint."""

from pydantic import BaseModel

from .common import RelationshipData, TokenFullInfoAttributes


class PoolTokenInfoRelationships(BaseModel):
    """
    Relationships block of a Pool Tokens Info entry.

    Attributes:
        pool: pointer to the parent pool resource.
    """
    pool: RelationshipData


class PoolTokenInfoData(BaseModel):
    """
    Single token entry inside the Pool Tokens Info response (one per side of the pool).

    Attributes:
        id: GeckoTerminal token identifier (e.g. `"eth_0x...."`).
        type: JSON:API resource type, always `"token"`.
        attributes: full token metadata payload.
        relationships: link back to the parent pool.
    """
    id: str
    type: str
    attributes: TokenFullInfoAttributes
    relationships: PoolTokenInfoRelationships | None = None


class GetPoolTokenInfoResponse(BaseModel):
    """
    Response payload from the **Pool Tokens Info** endpoint, returning the full metadata of every
    token that participates in the requested pool (base + quote). Useful to enrich a pool view with
    social links, trust scores, and holder distribution without making a separate request per token.

    Attributes:
        data: list of token entries (typically two — base and quote — for standard pools).
    """
    data: list[PoolTokenInfoData]
