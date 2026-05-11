from typing import Any
from pydantic import BaseModel, Field, RootModel


# ---------------------------------------------------------------------------
# Shared sub-schemas
# ---------------------------------------------------------------------------

class RugcheckRisk(BaseModel):
    """A single risk factor identified during a token report."""

    name: str
    value: str
    description: str
    score: int
    level: str


class RugcheckTokenInfo(BaseModel):
    """On-chain token mint account data."""

    mint_authority: str | None = Field(default=None, alias="mintAuthority")
    supply: int
    decimals: int
    is_initialized: bool = Field(alias="isInitialized")
    freeze_authority: str | None = Field(default=None, alias="freezeAuthority")


class RugcheckTokenMeta(BaseModel):
    """Token metadata stored on-chain (Metaplex standard)."""

    name: str
    symbol: str
    uri: str
    mutable: bool
    update_authority: str = Field(alias="updateAuthority")


class RugcheckHolder(BaseModel):
    """A single top-holder entry for a token."""

    address: str
    amount: int
    decimals: int
    pct: float
    ui_amount: float = Field(alias="uiAmount")
    ui_amount_string: str = Field(alias="uiAmountString")
    owner: str
    insider: bool


class RugcheckFileMeta(BaseModel):
    """Off-chain file metadata for a token (e.g. from Arweave/IPFS)."""

    description: str
    name: str
    symbol: str
    image: str


class RugcheckLocker(BaseModel):
    """A single liquidity locker entry."""

    program_id: str = Field(alias="programID")
    token_account: str = Field(alias="tokenAccount")
    owner: str
    uri: str
    unlock_date: int = Field(alias="unlockDate")
    usdc_locked: float = Field(alias="usdcLocked")
    type: str


class RugcheckVaultSummary(BaseModel):
    """Aggregated totals for a vault response."""

    total_usdc: float = Field(alias="totalUSDC")
    pct: float


class RugcheckTokenAccount(BaseModel):
    """SPL token mint account info (embedded in market data)."""

    mint_authority: str | None = Field(default=None, alias="mintAuthority")
    supply: int
    decimals: int
    is_initialized: bool = Field(alias="isInitialized")
    freeze_authority: str | None = Field(default=None, alias="freezeAuthority")


class RugcheckLiquidityAccount(BaseModel):
    """SPL token account holding liquidity for a market."""

    mint: str
    owner: str
    amount: int
    delegate: str | None = None
    state: int
    delegated_amount: int = Field(alias="delegatedAmount")
    close_authority: str | None = Field(default=None, alias="closeAuthority")


class RugcheckLPInfo(BaseModel):
    """Liquidity pool breakdown for a market."""

    base_mint: str = Field(alias="baseMint")
    quote_mint: str = Field(alias="quoteMint")
    lp_mint: str = Field(alias="lpMint")
    quote_price: float = Field(alias="quotePrice")
    base_price: float = Field(alias="basePrice")
    base: float
    quote: float
    reserve_supply: int = Field(alias="reserveSupply")
    current_supply: int = Field(alias="currentSupply")
    quote_usd: float = Field(alias="quoteUSD")
    base_usd: float = Field(alias="baseUSD")
    pct_reserve: int = Field(alias="pctReserve")
    pct_supply: int = Field(alias="pctSupply")
    holders: Any | None = None
    total_tokens_unlocked: int = Field(alias="totalTokensUnlocked")
    token_supply: int = Field(alias="tokenSupply")
    lp_locked: int = Field(alias="lpLocked")
    lp_unlocked: int = Field(alias="lpUnlocked")
    lp_locked_pct: int = Field(alias="lpLockedPct")
    lp_locked_usd: int = Field(alias="lpLockedUSD")
    lp_max_supply: int = Field(alias="lpMaxSupply")
    lp_current_supply: int = Field(alias="lpCurrentSupply")
    lp_total_supply: int = Field(alias="lpTotalSupply")


class RugcheckMarket(BaseModel):
    """A single DEX market/pool for a token."""

    pubkey: str
    market_type: str = Field(alias="marketType")
    mint_a: str = Field(alias="mintA")
    mint_b: str = Field(alias="mintB")
    mint_lp: str = Field(alias="mintLP")
    liquidity_a: str = Field(alias="liquidityA")
    liquidity_b: str = Field(alias="liquidityB")
    mint_a_account: RugcheckTokenAccount = Field(alias="mintAAccount")
    mint_b_account: RugcheckTokenAccount = Field(alias="mintBAccount")
    mint_lp_account: RugcheckTokenAccount = Field(alias="mintLPAccount")
    liquidity_a_account: RugcheckLiquidityAccount = Field(alias="liquidityAAccount")
    liquidity_b_account: RugcheckLiquidityAccount = Field(alias="liquidityBAccount")
    lp: RugcheckLPInfo


class RugcheckKnownAccount(BaseModel):
    """A labelled on-chain account (e.g. DEX program or AMM pool)."""

    name: str
    type: str


class RugcheckTransferFee(BaseModel):
    """Transfer fee configuration for Token-2022 tokens."""

    pct: int
    max_amount: int = Field(alias="maxAmount")
    authority: str


class RugcheckTokenEvent(BaseModel):
    """A historical event recorded for a token (e.g. authority changes)."""

    created_at: str = Field(alias="createdAt")
    event: str
    new_value: str | None = Field(default=None, alias="newValue")
    old_value: str | None = Field(default=None, alias="oldValue")


class RugcheckInsiderNode(BaseModel):
    """A single wallet node in an insider network graph."""

    id: str
    participant: bool
    holdings: int


class RugcheckInsiderNetwork(BaseModel):
    """A detected insider network with its member wallet nodes."""

    net_id: str
    network_type: str
    nodes: list[RugcheckInsiderNode]


class RugcheckInsiderNetworkSummary(BaseModel):
    """Summarised metadata for a detected insider network."""

    id: str
    size: int
    activity_type: str = Field(alias="activityType")
    total_amount: int = Field(alias="totalAmount")
    num_active_accounts: int = Field(alias="numActiveAccounts")
    simple: bool


class RugcheckLeaderboardEntry(BaseModel):
    """A single entry in the vote leaderboard."""

    username: str
    votes: int
    wins: int
    weight: int


class RugcheckNewToken(BaseModel):
    """A recently created token as returned by the new-tokens stats endpoint."""

    mint: str
    decimals: int
    symbol: str
    creator: str
    mint_authority: str = Field(alias="mintAuthority")
    freeze_authority: str = Field(alias="freezeAuthority")
    program: str
    create_at: str = Field(alias="createAt")
    updated_at: str = Field(alias="updatedAt")
    events: list[RugcheckTokenEvent] | None = None


class RugcheckRecentToken(BaseModel):
    """A recently visited token as returned by the recent stats endpoint."""

    mint: str
    metadata: RugcheckTokenMeta
    user_visits: int
    visits: int
    score: int


class RugcheckTrendingToken(BaseModel):
    """A trending token with vote counts."""

    mint: str
    up_count: int
    vote_count: int


class RugcheckVerifiedToken(BaseModel):
    """A verified token with project metadata."""

    mint: str
    payer: str
    name: str
    symbol: str
    description: str
    jup_verified: bool
    jup_strict: bool
    links: list[Any] | None = None


class RugcheckDomain(BaseModel):
    """A domain-mapped token entry."""

    mint: str
    name: str
    symbol: str
    domain: str
    created_at: str = Field(alias="createdAt")


class RugcheckEligibilityCriteria(BaseModel):
    """Eligibility criteria evaluated for a token verification request."""

    exists: bool
    duplicate: bool
    created_recently: bool
    mint_authority_set: bool
    freeze_authority_set: bool
    metadata_missing: bool
    liquidity_unlocked: bool
    risk_score: int


class RugcheckVerifyData(BaseModel):
    """Metadata payload for a token verification submission."""

    sol_domain: str = Field(alias="solDomain")
    description: str
    terms_accepted: bool = Field(alias="termsAccepted")
    data_integrity_accepted: bool = Field(alias="dataIntegrityAccepted")
    links: dict[str, Any]


# ---------------------------------------------------------------------------
# Body schemas
# ---------------------------------------------------------------------------

class PostTokenVoteBody(BaseModel):
    """Request body for submitting a vote on a token."""

    mint: str
    side: bool


class PostBulkTokensBody(BaseModel):
    """Request body for bulk token report/summary endpoints."""

    tokens: list[str]
    cache_only: bool = Field(alias="cacheOnly")


class PostTokensVerifyEligibleBody(BaseModel):
    """Request body for checking token verification eligibility."""

    mint: str


class PostTokensVerifyBody(BaseModel):
    """Request body for submitting a full token verification."""

    mint: str
    payer: str
    signature: str
    data: RugcheckVerifyData


class PostTokensVerifyTransactionBody(BaseModel):
    """Request body for generating a verification transaction."""

    mint: str
    payer: str
    data: dict[str, Any]
    priority_fee: int


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class GetPingResponse(BaseModel):
    """Response for the ping health-check endpoint."""

    message: str


class GetMaintenanceResponse(BaseModel):
    """Response for the maintenance status endpoint."""

    message: str


class GetLeaderboardResponse(RootModel):
    """Response for the leaderboard endpoint — ordered list of top voters."""

    root: list[RugcheckLeaderboardEntry]


class GetTokenReportResponse(BaseModel):
    """Full rug-check report for a given token mint address."""

    mint: str
    token_program: str = Field(alias="tokenProgram")
    creator: str
    creator_balance: int = Field(alias="creatorBalance")
    token: RugcheckTokenInfo
    token_extensions: Any | None = Field(default=None, alias="token_extensions")
    token_meta: RugcheckTokenMeta = Field(alias="tokenMeta")
    top_holders: list[RugcheckHolder] = Field(alias="topHolders")
    freeze_authority: str | None = Field(default=None, alias="freezeAuthority")
    mint_authority: str | None = Field(default=None, alias="mintAuthority")
    risks: list[RugcheckRisk]
    score: int
    score_normalised: int
    file_meta: RugcheckFileMeta = Field(alias="fileMeta")
    locker_owners: dict[str, Any] = Field(alias="lockerOwners")
    lockers: dict[str, RugcheckLocker]
    locker_scan_status: str = Field(alias="lockerScanStatus")
    markets: list[RugcheckMarket]
    total_market_liquidity: float = Field(alias="totalMarketLiquidity")
    total_stable_liquidity: float = Field(alias="totalStableLiquidity")
    total_lp_providers: int = Field(alias="totalLPProviders")
    total_holders: int = Field(alias="totalHolders")
    price: float
    rugged: bool
    token_type: str = Field(alias="tokenType")
    transfer_fee: RugcheckTransferFee = Field(alias="transferFee")
    known_accounts: dict[str, RugcheckKnownAccount] = Field(alias="knownAccounts")


class GetTokenReportSummaryResponse(BaseModel):
    """Lightweight summary of a token report."""

    token_program: str = Field(alias="tokenProgram")
    token_type: str = Field(alias="tokenType")
    risks: list[RugcheckRisk]
    score: int
    score_normalised: int
    lp_locked_pct: float = Field(alias="lpLockedPct")
    mint: str | None = None
    error: str | None = None


class GetTokenMetadataResponse(BaseModel):
    """Token metadata including image URI."""

    mint: str
    decimals: int
    image_uri: str = Field(alias="imageUri")
    image_type: str = Field(alias="imageType")
    name: str
    symbol: str
    update_authority: str = Field(alias="updateAuthority")


class GetTokenVotesResponse(BaseModel):
    """Community vote counts for a token."""

    up: int
    down: int
    user_voted: bool = Field(alias="userVoted")


class GetTokenInsidersGraphResponse(RootModel):
    """List of insider networks with full node graph for a token."""

    root: list[RugcheckInsiderNetwork]


class GetTokenInsidersNetworksResponse(RootModel):
    """Summarised list of insider network metadata for a token."""

    root: list[RugcheckInsiderNetworkSummary]


class GetStatsNewTokensResponse(RootModel):
    """List of recently created tokens."""

    root: list[RugcheckNewToken]


class GetStatsRecentResponse(RootModel):
    """List of recently visited/checked tokens."""

    root: list[RugcheckRecentToken]


class GetStatsTrendingResponse(RootModel):
    """List of trending tokens by vote activity (may be empty/null)."""

    root: list[RugcheckTrendingToken] | None


class GetStatsVerifiedResponse(RootModel):
    """List of verified tokens with project metadata."""

    root: list[RugcheckVerifiedToken]


class GetStatsAnalyticsResponse(BaseModel):
    """Aggregate analytics statistics for a given time window."""

    avg_launch_score: float = Field(alias="avgLaunchScore")
    avg_time_to_rug_minutes: dict[str, Any] = Field(alias="avgTimeToRugMinutes")
    avg_rug_score: float = Field(alias="avgRugScore")
    window: str
    avg_token_score: float = Field(alias="avgTokenScore")
    tokens_launched: dict[str, Any] = Field(alias="tokensLaunched")
    rug_pull_count: dict[str, Any] = Field(alias="rugPullCount")
    insider_stats: dict[str, Any] = Field(alias="insiderStats")
    avg_insider_network_size: float = Field(alias="avgInsiderNetworkSize")
    rug_market_cap_usd: float = Field(alias="rugMarketCapUSD")


class GetStatsRugsTickerResponse(BaseModel):
    """Recent rug-pull ticker items."""

    items: list[Any]


class GetCreatorResponse(BaseModel):
    """Creator wallet statistics including rug history."""

    wallet: str
    total_tokens: int = Field(alias="totalTokens")
    rugged_tokens: int = Field(alias="ruggedTokens")
    avg_launch_score: float = Field(alias="avgLaunchScore")
    last_token_at: str | None = Field(default=None, alias="lastTokenAt")
    last_rug_at: str | None = Field(default=None, alias="lastRugAt")
    auto_blacklisted: bool = Field(alias="autoBlacklisted")
    manual_blacklisted: bool = Field(alias="manualBlacklisted")
    updated_at: str = Field(alias="updatedAt")


class GetDomainsResponse(RootModel):
    """List of domain-mapped tokens."""

    root: list[RugcheckDomain]


class GetDomainLookupResponse(RootModel):
    """Resolved mint address for a given domain."""

    root: str


class PostTokenReportResponse(BaseModel):
    """Response confirming a token report generation was queued."""

    ok: bool


class PostTokenVoteResponse(BaseModel):
    """Updated vote counts after casting a vote."""

    up: int
    down: int
    user_voted: bool = Field(alias="userVoted")


class GetTokenLockersResponse(BaseModel):
    """Vault response containing locker details and aggregate totals."""

    lockers: dict[str, RugcheckLocker]
    total: RugcheckVaultSummary


class GetTokenLockersFluxResponse(BaseModel):
    """Flux vault response containing locker details and aggregate totals."""

    lockers: dict[str, RugcheckLocker]
    total: RugcheckVaultSummary


class PostBulkTokensReportResponse(RootModel):
    """Detailed reports for multiple tokens requested in bulk."""

    root: list[GetTokenReportResponse]


class PostBulkTokensSummaryResponse(BaseModel):
    """Summary reports for multiple tokens requested in bulk."""

    reports: list[GetTokenReportSummaryResponse]


class PostTokensVerifyEligibleResponse(BaseModel):
    """Eligibility check result for a token verification request."""

    mint: str
    eligible: bool
    criteria: RugcheckEligibilityCriteria


class PostTokensVerifyResponse(BaseModel):
    """Response confirming a token verification was submitted."""

    ok: bool


class PostTokensVerifyTransactionResponse(BaseModel):
    """Serialised transaction for on-chain token verification."""

    transaction: str
