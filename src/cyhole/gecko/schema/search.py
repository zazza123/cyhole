"""Schema for the Search Pools endpoint."""

from pydantic import BaseModel

from .common import (
    IncludedResource,
    IncludedResourceAttributes,
    LinksResponse,
    PoolAttributes,
    PoolRelationships,
)


class SearchPoolAttributes(PoolAttributes):
    """
    Attributes block of a pool resource returned by the Search Pools endpoint.

    Same fields as the shared [`PoolAttributes`][cyhole.gecko.schema.PoolAttributes]; kept as a
    named subclass so existing imports keep working.
    """


class SearchPoolRelationships(PoolRelationships):
    """
    Relationships block of a search-pools entry (base token, quote token, network and DEX).

    Same fields as the shared [`PoolRelationships`][cyhole.gecko.schema.PoolRelationships]; kept as
    a named subclass so existing imports keep working.
    """


class SearchPoolData(BaseModel):
    """
    Single pool resource returned by the Search Pools endpoint.

    Attributes:
        id: GeckoTerminal pool identifier (e.g. `"eth_0x...."`).
        type: JSON:API resource type, always `"pool"`.
        attributes: pool-stats payload.
        relationships: pointers to base/quote token, network, and DEX.
    """
    id: str
    type: str
    attributes: SearchPoolAttributes
    relationships: SearchPoolRelationships | None = None


class SearchIncludedAttributes(IncludedResourceAttributes):
    """
    Attributes block of a resource embedded inside the search response's `included` array (token or
    DEX). Fields not relevant to a given resource type are `None`.

    Same fields as the shared [`IncludedResourceAttributes`][cyhole.gecko.schema.IncludedResourceAttributes];
    kept as a named subclass so existing imports keep working.
    """


class SearchIncluded(IncludedResource):
    """
    Single resource embedded in the search response's `included` array (typed `"token"` or `"dex"`).

    Attributes:
        attributes: resource attributes.
    """
    attributes: SearchIncludedAttributes


class GetSearchPoolsResponse(BaseModel):
    """
    Response payload from the **Search Pools** endpoint, returning the pools matching the requested
    query (pool address, token name, symbol, or token contract address) optionally constrained to a
    given network. When `include` is provided, the linked token/DEX resources are expanded inline.

    Attributes:
        data: list of matching pool resources.
        included: embedded token/DEX resources for the requested `include` relationships; `None` otherwise.
        links: JSON:API pagination links.
    """
    data: list[SearchPoolData]
    included: list[SearchIncluded] | None = None
    links: LinksResponse | None = None
