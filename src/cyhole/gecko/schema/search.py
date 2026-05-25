"""Schema for the Search Pools endpoint."""

from pydantic import BaseModel

from .common import (
    LinksResponse,
    RelationshipData,
    TimeBucketedStr,
    TransactionsTimeBuckets,
)


class SearchPoolAttributes(BaseModel):
    """
    Attributes block of a pool resource returned by the Search Pools endpoint.

    Attributes:
        base_token_price_usd: USD price of the pool's base token.
        base_token_price_native_currency: base-token price expressed in the network native currency.
        quote_token_price_usd: USD price of the pool's quote token.
        quote_token_price_native_currency: quote-token price expressed in the network native currency.
        base_token_price_quote_token: base/quote price ratio.
        quote_token_price_base_token: quote/base price ratio.
        address: pool contract address.
        name: human-readable pool name.
        pool_created_at: ISO-8601 creation timestamp.
        fdv_usd: fully-diluted valuation in USD; `None` when not computable.
        market_cap_usd: market cap in USD; `None` when supply data is unavailable.
        price_change_percentage: % change of the base price per time window.
        transactions: transaction-count breakdown per time window.
        volume_usd: USD volume per time window.
        reserve_in_usd: aggregate USD reserve.
    """
    base_token_price_usd: str | None = None
    base_token_price_native_currency: str | None = None
    quote_token_price_usd: str | None = None
    quote_token_price_native_currency: str | None = None
    base_token_price_quote_token: str | None = None
    quote_token_price_base_token: str | None = None
    address: str | None = None
    name: str | None = None
    pool_created_at: str | None = None
    fdv_usd: str | None = None
    market_cap_usd: str | None = None
    price_change_percentage: TimeBucketedStr | None = None
    transactions: TransactionsTimeBuckets | None = None
    volume_usd: TimeBucketedStr | None = None
    reserve_in_usd: str | None = None


class SearchPoolRelationships(BaseModel):
    """
    Relationships block of a search-pools entry.

    Attributes:
        base_token: pointer to the base token resource.
        quote_token: pointer to the quote token resource.
        network: pointer to the network resource.
        dex: pointer to the DEX resource.
    """
    base_token: RelationshipData | None = None
    quote_token: RelationshipData | None = None
    network: RelationshipData | None = None
    dex: RelationshipData | None = None


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


class SearchIncludedAttributes(BaseModel):
    """
    Attributes block of a resource embedded inside the search response's `included` array (token or
    DEX). Fields not relevant to a given resource type are `None`.

    Attributes:
        address: token contract address; `None` for DEX resources.
        name: human-readable name (token or DEX).
        symbol: token ticker symbol; `None` for DEX resources.
        decimals: token decimals; `None` for DEX resources.
        image_url: token image URL; `None` for DEX resources.
        coingecko_coin_id: CoinGecko coin id mapped to the token; `None` for DEX resources or unmapped tokens.
    """
    address: str | None = None
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    image_url: str | None = None
    coingecko_coin_id: str | None = None


class SearchIncluded(BaseModel):
    """
    Single resource embedded in the search response's `included` array (typed `"token"` or `"dex"`).

    Attributes:
        id: resource identifier.
        type: JSON:API resource type (`"token"` or `"dex"`).
        attributes: resource attributes.
    """
    id: str
    type: str
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
