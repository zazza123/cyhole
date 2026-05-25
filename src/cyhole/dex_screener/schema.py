from pydantic import BaseModel, ConfigDict, Field, RootModel


# ---------------------------------------------------------------------------
# Base model
# ---------------------------------------------------------------------------

class _DexScreenerBase(BaseModel):
    """Base for every DexScreener schema model.

    ``populate_by_name = True`` lets callers construct or validate models
    using either the Python field name (snake_case) or the API alias
    (camelCase). ``serialize_by_alias = True`` makes ``model_dump()``
    emit the alias (camelCase) form, so the dumped dict has the same
    shape as the upstream JSON payload — consumers can read the same
    keys they would read from a raw HTTP response.

    The local ``_DexScreenerBase`` keeps the scope of this configuration
    explicit to the DexScreener schema package; whether to extend it
    project-wide is tracked as a separate discussion.
    """

    model_config = ConfigDict(populate_by_name = True, serialize_by_alias = True)


# ---------------------------------------------------------------------------
# Shared sub-schemas
# ---------------------------------------------------------------------------

class DexScreenerTokenProfileLink(_DexScreenerBase):
    """A single link entry attached to a token profile."""

    type: str | None = None
    label: str | None = None
    url: str


class DexScreenerTokenProfile(_DexScreenerBase):
    """Token profile metadata returned by the token-profiles endpoints."""

    url: str
    chain_id: str = Field(alias = "chainId")
    token_address: str = Field(alias = "tokenAddress")
    icon: str
    header: str | None = None
    description: str | None = None
    links: list[DexScreenerTokenProfileLink] | None = None


class DexScreenerCommunityTakeover(_DexScreenerBase):
    """Community takeover record, extending token profile with a claim date."""

    url: str
    chain_id: str = Field(alias = "chainId")
    token_address: str = Field(alias = "tokenAddress")
    icon: str
    header: str | None = None
    description: str | None = None
    links: list[DexScreenerTokenProfileLink] | None = None
    claim_date: str = Field(alias = "claimDate")


class DexScreenerAd(_DexScreenerBase):
    """Advertisement record from the ads endpoint."""

    url: str
    chain_id: str = Field(alias = "chainId")
    token_address: str = Field(alias = "tokenAddress")
    date: str
    type: str
    duration_hours: float | None = Field(default = None, alias = "durationHours")
    impressions: float | None = None


class DexScreenerTokenBoost(_DexScreenerBase):
    """Token boost record from the token-boosts endpoints."""

    url: str
    chain_id: str = Field(alias = "chainId")
    token_address: str = Field(alias = "tokenAddress")
    amount: float
    total_amount: float = Field(alias = "totalAmount")
    icon: str | None = None
    header: str | None = None
    description: str | None = None
    links: list[DexScreenerTokenProfileLink] | None = None


class DexScreenerOrder(_DexScreenerBase):
    """Paid order record for a token."""

    type: str
    status: str
    payment_timestamp: float = Field(alias = "paymentTimestamp")


class DexScreenerBaseToken(_DexScreenerBase):
    """Base token in a trading pair."""

    address: str
    name: str
    symbol: str


class DexScreenerQuoteToken(_DexScreenerBase):
    """Quote token in a trading pair (fields may be absent for some pairs)."""

    address: str | None = None
    name: str | None = None
    symbol: str | None = None


class DexScreenerPairTxns(_DexScreenerBase):
    """Buy/sell transaction counts for a time window."""

    buys: int
    sells: int


class DexScreenerPairLiquidity(_DexScreenerBase):
    """Liquidity values for a trading pair."""

    usd: float | None = None
    base: float
    quote: float


class DexScreenerPairWebsite(_DexScreenerBase):
    """Website URL associated with a pair's token."""

    url: str


class DexScreenerPairSocial(_DexScreenerBase):
    """Social media link associated with a pair's token.

    The DexScreener API returns each social entry as ``{"type", "url"}``,
    where ``type`` identifies the platform (e.g. ``"twitter"``,
    ``"telegram"``, ``"discord"``) and ``url`` is the full social link.
    """

    type: str
    url: str


class DexScreenerPairInfo(_DexScreenerBase):
    """Extended info (image, websites, socials) attached to a pair."""

    image_url: str | None = Field(default = None, alias = "imageUrl")
    websites: list[DexScreenerPairWebsite] | None = None
    socials: list[DexScreenerPairSocial] | None = None


class DexScreenerPairBoosts(_DexScreenerBase):
    """Active boost count for a pair."""

    active: int


class DexScreenerPair(_DexScreenerBase):
    """
    Full trading pair object returned by multiple DEX endpoints.

    `txns` and `volume` keys are time-window labels (e.g. ``"m5"``, ``"h1"``, ``"h6"``, ``"h24"``).
    """

    chain_id: str = Field(alias = "chainId")
    dex_id: str = Field(alias = "dexId")
    url: str
    pair_address: str = Field(alias = "pairAddress")
    labels: list[str] | None = None
    base_token: DexScreenerBaseToken = Field(alias = "baseToken")
    quote_token: DexScreenerQuoteToken = Field(alias = "quoteToken")
    price_native: str = Field(alias = "priceNative")
    price_usd: str | None = Field(default = None, alias = "priceUsd")
    txns: dict[str, DexScreenerPairTxns]
    volume: dict[str, float]
    price_change: dict[str, float] | None = Field(default = None, alias = "priceChange")
    liquidity: DexScreenerPairLiquidity | None = None
    fdv: float | None = None
    market_cap: float | None = Field(default = None, alias = "marketCap")
    pair_created_at: int | None = Field(default = None, alias = "pairCreatedAt")
    info: DexScreenerPairInfo | None = None
    boosts: DexScreenerPairBoosts | None = None


# ---------------------------------------------------------------------------
# Response models — array roots use RootModel
# ---------------------------------------------------------------------------

class GetTokenProfilesLatestResponse(RootModel[list[DexScreenerTokenProfile]]):
    """Response for GET /token-profiles/latest/v1."""
    pass


class GetCommunityTakeoverResponse(RootModel[list[DexScreenerCommunityTakeover]]):
    """Response for GET /community-takeovers/latest/v1."""
    pass


class GetAdsLatestResponse(RootModel[list[DexScreenerAd]]):
    """Response for GET /ads/latest/v1."""
    pass


class GetTokenBoostsLatestResponse(RootModel[list[DexScreenerTokenBoost]]):
    """Response for GET /token-boosts/latest/v1."""
    pass


class GetTokenBoostsTopResponse(RootModel[list[DexScreenerTokenBoost]]):
    """Response for GET /token-boosts/top/v1."""
    pass


class GetOrdersResponse(RootModel[list[DexScreenerOrder]]):
    """Response for GET /orders/v1/{chainId}/{tokenAddress}."""
    pass


class GetTokensResponse(RootModel[list[DexScreenerPair]]):
    """Response for GET /tokens/v1/{chainId}/{tokenAddresses}."""
    pass


class GetTokenPairsResponse(RootModel[list[DexScreenerPair]]):
    """Response for GET /token-pairs/v1/{chainId}/{tokenAddress}."""
    pass


class GetPairsResponse(_DexScreenerBase):
    """Response for GET /latest/dex/pairs/{chainId}/{pairId}."""

    schema_version: str = Field(alias = "schemaVersion")
    pairs: list[DexScreenerPair] | None = None


class GetSearchResponse(_DexScreenerBase):
    """Response for GET /latest/dex/search."""

    schema_version: str = Field(alias = "schemaVersion")
    pairs: list[DexScreenerPair]
