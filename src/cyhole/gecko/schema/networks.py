"""Schemas for the Networks endpoint."""

from pydantic import BaseModel

from .common import LinksResponse


class NetworkAttributes(BaseModel):
    """
    Attributes block of a single network resource.

    Attributes:
        name: human-readable network name (e.g. `"Ethereum"`).
        coingecko_asset_platform_id: CoinGecko asset platform id mapped to this network; `None` when not mapped.
    """
    name: str
    coingecko_asset_platform_id: str | None = None


class NetworkData(BaseModel):
    """
    Single network resource as returned in the `data` list of the Networks endpoint.

    Attributes:
        id: GeckoTerminal network identifier (e.g. `"eth"`, `"solana"`, `"bsc"`); used as path parameter in most endpoints.
        type: JSON:API resource type, always `"network"`.
        attributes: per-network metadata block.
    """
    id: str
    type: str
    attributes: NetworkAttributes


class GetNetworksResponse(BaseModel):
    """
    Response payload from the **Networks** endpoint, returning the paginated list of every network
    supported by GeckoTerminal.

    Attributes:
        data: list of supported networks for the current page.
        links: JSON:API pagination links.
    """
    data: list[NetworkData]
    links: LinksResponse | None = None
