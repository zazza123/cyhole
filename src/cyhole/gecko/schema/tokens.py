"""Schemas for the Token Data (single + multiple) and Recently Updated Tokens endpoints."""

from pydantic import BaseModel

from .common import (
    RelationshipData,
    RelationshipList,
    TimeBucketedStr,
    TransactionsTimeBuckets,
)


class TokenDataVolumeUsd(BaseModel):
    """
    Volume bucket returned inside a token-data attributes block.

    Token Data endpoints typically return only the trailing 24-hour bucket. Modelled as
    [`TimeBucketedStr`][cyhole.gecko.schema.TimeBucketedStr] for consistency with pool resources.

    Attributes:
        h24: trailing 24-hour USD volume; `None` when not reported.
    """
    h24: str | None = None


class LaunchpadDetails(BaseModel):
    """
    Launchpad progress metadata included on the multi-token endpoint when relevant.

    Attributes:
        graduation_percentage: percentage of the launchpad bonding curve completed (0–100).
        completed: whether the launchpad sale has concluded.
        completed_at: ISO-8601 timestamp of completion; `None` while the sale is in progress.
        migrated_destination_pool_address: address of the AMM pool the token migrated to after the sale; `None` until migration occurs.
    """
    graduation_percentage: float | None = None
    completed: bool | None = None
    completed_at: str | None = None
    migrated_destination_pool_address: str | None = None


class TokenDataAttributes(BaseModel):
    """
    Attributes block returned by the **single** Token Data endpoint.

    Attributes:
        address: token contract address.
        name: human-readable token name.
        symbol: token ticker symbol.
        decimals: number of decimal places used by the token.
        image_url: token image URL.
        coingecko_coin_id: CoinGecko coin id mapped to this token; `None` when not mapped.
        total_supply: total supply in raw integer units (decimal string).
        normalized_total_supply: total supply rescaled by `decimals` (decimal string).
        price_usd: latest USD price (decimal string).
        fdv_usd: fully-diluted valuation in USD; `None` when not computable.
        total_reserve_in_usd: aggregate USD reserve across all indexed pools.
        volume_usd: USD volume by time window (typically only `h24`).
        market_cap_usd: USD market cap; `None` when supply data is unavailable.
        last_trade_timestamp: unix timestamp (seconds) of the most recent trade.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    image_url: str | None = None
    coingecko_coin_id: str | None = None
    total_supply: str | None = None
    normalized_total_supply: str | None = None
    price_usd: str | None = None
    fdv_usd: str | None = None
    total_reserve_in_usd: str | None = None
    volume_usd: TokenDataVolumeUsd | None = None
    market_cap_usd: str | None = None
    last_trade_timestamp: int | None = None


class TokenDataMultipleAttributes(TokenDataAttributes):
    """
    Attributes block returned by the **multiple** Token Data endpoint.

    Extends [`TokenDataAttributes`][cyhole.gecko.schema.TokenDataAttributes] with launchpad metadata
    only the multi endpoint provides.

    Attributes:
        launchpad_details: launchpad progress info; `None` for tokens that were not launched via a tracked launchpad.
    """
    launchpad_details: LaunchpadDetails | None = None


class TokenDataRelationships(BaseModel):
    """
    Relationships block of a token-data resource.

    Attributes:
        top_pools: pointers to the related top pools; populated only when `include=top_pools` is set.
    """
    top_pools: RelationshipList | None = None


class TokenDataResource(BaseModel):
    """
    Single token resource for the Token Data (single) endpoint.

    Attributes:
        id: GeckoTerminal token identifier.
        type: JSON:API resource type, always `"token"`.
        attributes: token data payload.
        relationships: optional pointers to related top pools.
    """
    id: str
    type: str
    attributes: TokenDataAttributes
    relationships: TokenDataRelationships | None = None


class TokenDataMultipleResource(BaseModel):
    """
    Single token resource for the Token Data (multiple) endpoint, with `launchpad_details` available.
    """
    id: str
    type: str
    attributes: TokenDataMultipleAttributes
    relationships: TokenDataRelationships | None = None


class PoolIncludedAttributes(BaseModel):
    """
    Attributes block of a pool resource that appears in the JSON:API `included` array when callers
    request `include=top_pools` on the token-data endpoints.

    Attributes:
        base_token_price_usd: USD price of the pool's base token.
        base_token_price_native_currency: base-token price expressed in the network native currency.
        base_token_balance: pool reserve of the base token (decimal string).
        base_token_liquidity_usd: USD value of the base-token reserve.
        quote_token_price_usd: USD price of the pool's quote token.
        quote_token_price_native_currency: quote-token price expressed in the network native currency.
        quote_token_balance: pool reserve of the quote token.
        quote_token_liquidity_usd: USD value of the quote-token reserve.
        base_token_price_quote_token: base/quote price ratio.
        quote_token_price_base_token: quote/base price ratio.
        address: pool contract address.
        name: human-readable pool name.
        pool_created_at: ISO-8601 creation timestamp.
        token_price_usd: pool-level token USD price (single-endpoint only; `None` on multi responses).
        fdv_usd: pool-implied FDV in USD; `None` when not computable.
        market_cap_usd: pool-implied market cap; `None` when supply data is unavailable.
        price_change_percentage: % change of base price per time window.
        transactions: transaction-count breakdown per time window.
        volume_usd: USD volume per time window.
        reserve_in_usd: aggregate USD reserve.
    """
    base_token_price_usd: str | None = None
    base_token_price_native_currency: str | None = None
    base_token_balance: str | None = None
    base_token_liquidity_usd: str | None = None
    quote_token_price_usd: str | None = None
    quote_token_price_native_currency: str | None = None
    quote_token_balance: str | None = None
    quote_token_liquidity_usd: str | None = None
    base_token_price_quote_token: str | None = None
    quote_token_price_base_token: str | None = None
    address: str | None = None
    name: str | None = None
    pool_created_at: str | None = None
    token_price_usd: str | None = None
    fdv_usd: str | None = None
    market_cap_usd: str | None = None
    price_change_percentage: TimeBucketedStr | None = None
    transactions: TransactionsTimeBuckets | None = None
    volume_usd: TimeBucketedStr | None = None
    reserve_in_usd: str | None = None


class PoolIncludedRelationships(BaseModel):
    """
    Relationships block of a pool resource embedded in `included`.

    Attributes:
        base_token: pointer to the base token of the pool.
        quote_token: pointer to the quote token of the pool.
        dex: pointer to the DEX hosting the pool.
    """
    base_token: RelationshipData | None = None
    quote_token: RelationshipData | None = None
    dex: RelationshipData | None = None


class PoolIncluded(BaseModel):
    """
    Pool resource as it appears inside the JSON:API `included` array.

    Attributes:
        id: GeckoTerminal pool identifier.
        type: JSON:API resource type, always `"pool"`.
        attributes: pool-stats payload.
        relationships: pointers to base/quote token and DEX.
    """
    id: str
    type: str
    attributes: PoolIncludedAttributes
    relationships: PoolIncludedRelationships | None = None


class GetTokenDataResponse(BaseModel):
    """
    Response payload from the **single Token Data** endpoint, returning current price, supply,
    liquidity, and volume metrics for one token on a given network. When `include=top_pools` is set,
    the most relevant pools are listed in `relationships.top_pools` and their full details are
    expanded inside `included`.

    Attributes:
        data: token data resource.
        included: optional list of pool resources when `include=top_pools` was requested; `None` otherwise.
    """
    data: TokenDataResource
    included: list[PoolIncluded] | None = None


class GetTokenDataMultipleResponse(BaseModel):
    """
    Response payload from the **multiple Token Data** endpoint, returning the same metrics as the
    single endpoint for up to ~50 tokens at once, plus the optional `launchpad_details` block. Use
    this when you need to fetch many tokens efficiently.

    Attributes:
        data: list of token data resources.
        included: optional list of pool resources when `include=top_pools` was requested; `None` otherwise.
    """
    data: list[TokenDataMultipleResource]
    included: list[PoolIncluded] | None = None


class RecentlyUpdatedTokenAttributes(BaseModel):
    """
    Attributes block of a token returned by the Recently Updated Tokens endpoint.

    Attributes:
        address: token contract address.
        name: human-readable token name.
        symbol: token ticker symbol.
        decimals: number of decimal places used by the token.
        image_url: token image URL.
        coingecko_coin_id: CoinGecko coin id mapped to this token; `None` when not mapped.
        websites: list of official website URLs.
        discord_url: project Discord invite; `None` when not provided.
        farcaster_url: project Farcaster URL; `None` when not provided.
        zora_url: project Zora URL; `None` when not provided.
        telegram_handle: project Telegram handle; `None` when not provided.
        twitter_handle: project Twitter/X handle; `None` when not provided.
        description: free-text project description.
        gt_score: aggregate GeckoTerminal trust score.
        metadata_updated_at: ISO-8601 timestamp of the latest metadata update.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    image_url: str | None = None
    coingecko_coin_id: str | None = None
    websites: list[str] | None = None
    discord_url: str | None = None
    farcaster_url: str | None = None
    zora_url: str | None = None
    telegram_handle: str | None = None
    twitter_handle: str | None = None
    description: str | None = None
    gt_score: float | None = None
    metadata_updated_at: str | None = None


class RecentlyUpdatedTokenRelationships(BaseModel):
    """
    Relationships block of a recently-updated-tokens entry.

    Attributes:
        network: pointer to the network the token belongs to.
    """
    network: RelationshipData | None = None


class RecentlyUpdatedTokenData(BaseModel):
    """
    Single token entry returned by the Recently Updated Tokens endpoint.

    Attributes:
        id: GeckoTerminal token identifier.
        type: JSON:API resource type, always `"token"`.
        attributes: token metadata payload.
        relationships: pointer to the network resource.
    """
    id: str
    type: str
    attributes: RecentlyUpdatedTokenAttributes
    relationships: RecentlyUpdatedTokenRelationships | None = None


class GetRecentlyUpdatedTokensResponse(BaseModel):
    """
    Response payload from the **Recently Updated Tokens** endpoint, returning tokens whose
    metadata (description, links, score, etc.) was updated most recently on the requested network.
    Useful for surfacing newly enriched projects.

    Attributes:
        data: list of recently updated tokens.
    """
    data: list[RecentlyUpdatedTokenData]
