"""Shared building-block schemas reused across multiple Gecko endpoints."""

from pydantic import BaseModel, Field


class LinksResponse(BaseModel):
    """
    JSON:API pagination block returned by list endpoints (`networks`, `dexes`, `search/pools`).

    Attributes:
        first: URL of the first page of results.
        prev: URL of the previous page; `None` when on the first page.
        next: URL of the next page; `None` when on the last page.
        last: URL of the last page of results.
    """
    first: str | None = None
    prev: str | None = None
    next: str | None = None
    last: str | None = None


class ResourceRef(BaseModel):
    """
    JSON:API resource identifier used inside `relationships` blocks (e.g. `{ id: "...", type: "token" }`).

    Attributes:
        id: identifier of the referenced resource.
        type: type tag of the referenced resource (e.g. `"token"`, `"pool"`, `"dex"`, `"network"`).
    """
    id: str
    type: str


class RelationshipData(BaseModel):
    """
    JSON:API single-relationship wrapper of shape `{ "data": { id, type } }`.

    Attributes:
        data: resource identifier of the related entity.
    """
    data: ResourceRef


class RelationshipList(BaseModel):
    """
    JSON:API to-many relationship wrapper of shape `{ "data": [ { id, type }, ... ] }`.

    Attributes:
        data: list of resource identifiers of the related entities.
    """
    data: list[ResourceRef]


class TransactionStats(BaseModel):
    """
    Per-window transaction count breakdown used in pool/search responses.

    Attributes:
        buys: number of buy trades observed in the window.
        sells: number of sell trades observed in the window.
        buyers: number of distinct buyer addresses observed in the window.
        sellers: number of distinct seller addresses observed in the window.
    """
    buys: int
    sells: int
    buyers: int
    sellers: int


class TransactionsTimeBuckets(BaseModel):
    """
    Transaction stats bucketed by the standard GeckoTerminal time windows.

    Each bucket carries the [`TransactionStats`][cyhole.gecko.schema.TransactionStats] aggregates for the
    corresponding rolling window. All buckets are populated for pool resources.

    Attributes:
        m5: stats for the trailing 5 minutes.
        m15: stats for the trailing 15 minutes.
        m30: stats for the trailing 30 minutes.
        h1: stats for the trailing 1 hour.
        h6: stats for the trailing 6 hours.
        h24: stats for the trailing 24 hours.
    """
    m5: TransactionStats
    m15: TransactionStats
    m30: TransactionStats
    h1: TransactionStats
    h6: TransactionStats
    h24: TransactionStats


class TimeBucketedStr(BaseModel):
    """
    String-valued metric bucketed by the standard GeckoTerminal time windows.

    Used for `price_change_percentage` and `volume_usd` (USD strings) on pool/search resources, and
    for the `volume_usd` block on token resources where typically only `h24` is populated.

    Attributes:
        m5: value for the trailing 5 minutes; `None` when not reported.
        m15: value for the trailing 15 minutes; `None` when not reported.
        m30: value for the trailing 30 minutes; `None` when not reported.
        h1: value for the trailing 1 hour; `None` when not reported.
        h6: value for the trailing 6 hours; `None` when not reported.
        h24: value for the trailing 24 hours; `None` when not reported.
    """
    m5: str | None = None
    m15: str | None = None
    m30: str | None = None
    h1: str | None = None
    h6: str | None = None
    h24: str | None = None


class TokenImageSet(BaseModel):
    """
    Token image URLs at multiple sizes, as returned by token-info-style endpoints.

    Attributes:
        thumb: URL of the thumbnail image.
        small: URL of the small image.
        large: URL of the large image.
    """
    thumb: str | None = None
    small: str | None = None
    large: str | None = None


class TokenScoreDetails(BaseModel):
    """
    Breakdown of the GeckoTerminal trust score (`gt_score`) by contributing dimension.

    Attributes:
        pool: subscore from pool quality (liquidity, age, etc.).
        transaction: subscore from on-chain transaction activity.
        creation: subscore from contract-creation signals.
        info: subscore from metadata completeness.
        holders: subscore from holder distribution.
    """
    pool: float
    transaction: float
    creation: float
    info: float
    holders: float


class TokenHoldersDistribution(BaseModel):
    """
    Percentage split of token supply across holder buckets, as percentage strings (e.g. `"15.4"`).

    Attributes:
        top_10: percentage owned by the top 10 holders.
        holders_11_30: percentage owned by holders ranked 11 through 30 (JSON key `"11_30"`).
        holders_31_50: percentage owned by holders ranked 31 through 50 (JSON key `"31_50"`).
        rest: percentage owned by every other holder.
    """
    top_10: str | None = None
    holders_11_30: str | None = Field(default = None, alias = "11_30")
    holders_31_50: str | None = Field(default = None, alias = "31_50")
    rest: str | None = None


class TokenHoldersInfo(BaseModel):
    """
    Aggregate token-holder snapshot embedded in token-info-style responses.

    Attributes:
        count: total number of holders.
        distribution_percentage: split of supply across holder rank buckets.
        last_updated: ISO-8601 timestamp of the last snapshot.
    """
    count: int | None = None
    distribution_percentage: TokenHoldersDistribution | None = None
    last_updated: str | None = None


class TokenFullInfoAttributes(BaseModel):
    """
    Full token metadata block returned by the standalone Token Info endpoint and embedded in every
    entry of the Pool Tokens Info endpoint.

    Attributes:
        address: token contract address.
        name: human-readable token name.
        symbol: token ticker symbol.
        decimals: number of decimal places used by the token.
        image_url: legacy single image URL; superseded by `image`.
        image: image URLs at thumb/small/large sizes.
        coingecko_coin_id: CoinGecko coin id linked to this token; `None` when not mapped.
        websites: list of official website URLs declared by the project.
        discord_url: project Discord invite URL; `None` when not provided.
        farcaster_url: project Farcaster URL; `None` when not provided.
        zora_url: project Zora URL; `None` when not provided.
        telegram_handle: project Telegram handle; `None` when not provided.
        twitter_handle: project Twitter/X handle; `None` when not provided.
        description: free-text project description.
        gt_score: aggregate GeckoTerminal trust score (0–100).
        gt_score_details: per-dimension breakdown of the trust score.
        gt_verified: whether GeckoTerminal has marked the token as verified.
        categories: human-readable category labels.
        gt_category_ids: GeckoTerminal category ids.
        holders: aggregate holders snapshot.
        mint_authority: address with mint authority on the underlying network; `None` if not applicable.
        freeze_authority: address with freeze authority; `None` if not applicable.
        is_honeypot: honeypot flag; the API occasionally returns this as a string instead of a bool.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    image_url: str | None = None
    image: TokenImageSet | None = None
    coingecko_coin_id: str | None = None
    websites: list[str] | None = None
    discord_url: str | None = None
    farcaster_url: str | None = None
    zora_url: str | None = None
    telegram_handle: str | None = None
    twitter_handle: str | None = None
    description: str | None = None
    gt_score: float | None = None
    gt_score_details: TokenScoreDetails | None = None
    gt_verified: bool | None = None
    categories: list[str] | None = None
    gt_category_ids: list[str] | None = None
    holders: TokenHoldersInfo | None = None
    mint_authority: str | None = None
    freeze_authority: str | None = None
    is_honeypot: bool | str | None = None
