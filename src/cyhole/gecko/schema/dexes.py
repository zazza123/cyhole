"""Schemas for the Dexes-by-network endpoint."""

from pydantic import BaseModel

from .common import LinksResponse


class DexAttributes(BaseModel):
    """
    Attributes block of a single DEX resource.

    Attributes:
        name: human-readable DEX name (e.g. `"Uniswap V3"`).
    """
    name: str


class DexData(BaseModel):
    """
    Single DEX resource returned by the Dexes-by-network endpoint.

    Attributes:
        id: GeckoTerminal DEX identifier (e.g. `"uniswap_v3"`).
        type: JSON:API resource type, always `"dex"`.
        attributes: per-DEX metadata block.
    """
    id: str
    type: str
    attributes: DexAttributes


class GetDexesResponse(BaseModel):
    """
    Response payload from the **Dexes by Network** endpoint, returning the paginated list of every
    decentralized exchange indexed by GeckoTerminal on the requested network.

    Attributes:
        data: list of supported DEXes for the current page.
        links: JSON:API pagination links.
    """
    data: list[DexData]
    links: LinksResponse | None = None
