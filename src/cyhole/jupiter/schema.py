from datetime import datetime

from pydantic import BaseModel, RootModel, Field, AliasChoices, field_validator, field_serializer, model_serializer

from ..jupiter.param import (
    JupiterSwapMode,
    JupiterSwapDex,
    JupiterBroadcastFeeType,
    JupiterOrderState,
    JupiterRouter,
    JupiterSwapExecutionStatus,
    JupiterOrderStatus,
    JupiterOrganicScore
)

# class used on Jupiter HTTPErrors
class JupiterHTTPError(BaseModel):
    """
        Jupiter API returns an error schema on failed request 
        that can be used to investigated the error. This schema 
        is used to strandardise the HTTPErrors.
    """

    code: str = Field(validation_alias = AliasChoices("errorCode", "error_code"))
    """Error code returned by the API."""

    msg: str = Field(alias = "error")
    """Error message returned by the API."""

# *************
# * Price API *
# *************

# classes used on GET "Price" endpoint
class GetPriceData(BaseModel):
    """
        Model with the price information for a single token
        returned by the GET "**Price**" endpoint from Jupiter Price V3 API.
    """

    usd_price: float = Field(alias = "usdPrice")
    """Token price in USD."""

    block_id: int = Field(alias = "blockId")
    """Solana block height at which the price was recorded, used to verify recency."""

    decimals: int
    """Token decimal places, used for UI display purposes."""

    price_change_24h: float = Field(alias = "priceChange24h")
    """24-hour percentage price change. Negative values indicate a price decrease."""

class GetPriceResponse(RootModel[dict[str, GetPriceData | None]]):
    """
        Model referring to the response schema of the GET
        "**Price**" endpoint from Jupiter Price V3 API.
        The response is a flat mapping of token mint address to price data.
        A value of `None` indicates the price is unavailable or unreliable for that token.
    """

    @property
    def data(self) -> dict[str, GetPriceData | None]:
        """Dictionary of token prices. Key is the mint address."""
        return self.root

# ************
# * Swap API *
# ************

# Output
class GetQuotePlatformFees(BaseModel):
    """
        Model refering to the platform fees of a route plan in
        GET "**Quote**" endpoint from Jupiter API.
    """

    amount_raw: int | None = Field(default = None, alias = "amount")
    """Raw amount of platform fee token to buy (before decimals)."""

    fee_base_points: int = Field(alias = "feeBps")
    """
        Amount of fees collected.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

class GetQuoteSwapInfo(BaseModel):
    """
        Model defining all the SWAP info of a route plan in
        GET "**Quote**" endpoint from Jupiter API.
    """

    amm_key: str = Field(alias = "ammKey")
    """Address of the AMM (Automated Market Maker) used for the swap."""

    amm_label: str | None = Field(default = None, alias = "label")
    """Label of the AMM used for the swap."""

    input_token: str = Field(alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw amount of input token to use to buy (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """The address of the output token on the chain that will bought."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw amount of output token to buy (before decimals)."""

    fee_token: str | None = Field(default = None, alias = "feeMint")
    """Fee token address."""

    fee_amount_raw: str | None = Field(default = None, alias = "feeAmount")
    """Raw amount of fee token to buy (before decimals)."""

    @property
    def input_amount(self) -> int:
        return int(self.input_amount_raw)

    @property
    def output_amount(self) -> int:
        return int(self.output_amount_raw)

    @property
    def fee_amount(self) -> int | None:
        return int(self.fee_amount_raw) if self.fee_amount_raw is not None else None

class GetQuoteRoutePlan(BaseModel):
    """
        Model refering to the schema of a route plan in the GET 
        "**Quote**" endpoint from Jupiter API.
    """

    swap_info: GetQuoteSwapInfo = Field(alias = "swapInfo")
    """Information about the swap."""

    percent: int | None = None
    """Percentage of the swap."""

# classes used on GET "Swap v2 - Order" endpoint
# Input
class GetSwapOrderParams(BaseModel):
    """
        Model referring to the input params schema of the GET
        "**Swap - Order**" endpoint from Jupiter Swap v2 API.
    """

    input_token: str = Field(serialization_alias = "inputMint")
    """Address of the input token mint."""

    output_token: str = Field(serialization_alias = "outputMint")
    """Address of the output token mint."""

    amount: int
    """Amount to swap in the smallest unit of the input token (factoring in token decimals)."""

    taker: str | None = None
    """Public key of the wallet signing the transaction. Required to receive a non-null transaction in the response."""

    receiver: str | None = None
    """Public key of the account receiving the output tokens. Must differ from taker when provided."""

    swap_mode: str = Field(default = "ExactIn", serialization_alias = "swapMode")
    """Swap mode. Currently only `ExactIn` is supported."""

    slippage_bps: int | None = Field(default = None, serialization_alias = "slippageBps")
    """Slippage tolerance in basis points (0–10000). Auto-determined by RTSE if unset."""

    referral_account: str | None = Field(default = None, serialization_alias = "referralAccount")
    """Referral account address. Requires referral_fee to be set."""

    referral_fee: int | None = Field(default = None, serialization_alias = "referralFee")
    """Referral fee in basis points (50–255). Requires referral_account to be set."""

    payer: str | None = None
    """Public key of the account covering gas fees on behalf of the taker."""

    priority_fee_lamports: int | None = Field(default = None, serialization_alias = "priorityFeeLamports")
    """Priority fee in lamports. Auto-optimised if unset."""

    jito_tip_lamports: int | None = Field(default = None, serialization_alias = "jitoTipLamports")
    """Jito MEV tip in lamports for faster block inclusion."""

    broadcast_fee_type: JupiterBroadcastFeeType | None = Field(default = None, serialization_alias = "broadcastFeeType")
    """Fee strategy. See [`JupiterBroadcastFeeType`][cyhole.jupiter.param.JupiterBroadcastFeeType] for valid values."""

    exclude_routers: list[JupiterRouter] | None = Field(default = None, serialization_alias = "excludeRouters")
    """Routers to exclude from competition. See [`JupiterRouter`][cyhole.jupiter.param.JupiterRouter] for valid values."""

    exclude_dexes: str | None = Field(default = None, serialization_alias = "excludeDexes")
    """Comma-separated list of DEXes to exclude from the Metis router (e.g. "Raydium,Orca V2")."""

    @field_serializer("amount")
    @classmethod
    def serialize_amount(cls, amount: int) -> str:
        return str(amount)

    @field_serializer("exclude_routers")
    @classmethod
    def serialize_exclude_routers(cls, routers: list[JupiterRouter] | None) -> str | None:
        return ",".join(r.value for r in routers) if routers else None

    @field_serializer("broadcast_fee_type")
    @classmethod
    def serialize_broadcast_fee_type(cls, fee_type: JupiterBroadcastFeeType | None) -> str | None:
        return fee_type.value if fee_type else None

# Output
class GetSwapOrderPlatformFee(BaseModel):
    """Platform fee details in the GET "Swap - Order" response."""

    amount: str | None = None
    """Raw platform fee amount (before decimals). None when no platform fee."""

    fee_bps: int = Field(alias = "feeBps")
    """Platform fee in basis points."""

    fee_mint: str | None = Field(default = None, alias = "feeMint")
    """Token mint address for the fee. None when no platform fee."""

class GetSwapOrderSwapInfo(BaseModel):
    """Swap info for a single step in the route plan of the GET "Swap - Order" response."""

    amm_key: str = Field(alias = "ammKey")
    """Address of the AMM used for this swap step."""

    amm_label: str | None = Field(default = None, alias = "label")
    """Human-readable label of the AMM."""

    input_token: str = Field(alias = "inputMint")
    """Input token address for this swap step."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw input amount for this step (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """Output token address for this swap step."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw output amount for this step (before decimals)."""

class GetSwapOrderRoutePlan(BaseModel):
    """A single step in the route plan of the GET "Swap - Order" response."""

    swap_info: GetSwapOrderSwapInfo = Field(alias = "swapInfo")
    """Swap details for this step."""

    percent: int | None = None
    """Percentage of the total swap routed through this step."""

    bps: int | None = None
    """Routing basis points for this step."""

    usd_value: float | None = Field(default = None, alias = "usdValue")
    """Estimated USD value routed through this step."""

class GetSwapOrderResponse(BaseModel):
    """
        Model referring to the response schema of the GET
        "**Swap - Order**" endpoint from Jupiter Swap v2 API.
    """

    mode: str | None = None
    """Order mode: "ultra" or "manual"."""

    input_token: str = Field(alias = "inputMint")
    """Input token mint address."""

    output_token: str = Field(alias = "outputMint")
    """Output token mint address."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw input amount (before decimals)."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw output amount (before decimals)."""

    input_usd_value: float | None = Field(default = None, alias = "inUsdValue")
    """USD value of the input amount."""

    output_usd_value: float | None = Field(default = None, alias = "outUsdValue")
    """USD value of the output amount."""

    price_impact: float | None = Field(default = None, alias = "priceImpact")
    """Price impact as a decimal (e.g. -0.001 = -0.1%)."""

    swap_usd_value: float | None = Field(default = None, alias = "swapUsdValue")
    """USD value of the entire swap."""

    other_amount_threshold: str = Field(alias = "otherAmountThreshold")
    """Minimum output amount after slippage."""

    swap_mode: str = Field(alias = "swapMode")
    """Swap mode used (currently only ExactIn)."""

    slippage_bps: int = Field(alias = "slippageBps")
    """Slippage tolerance applied in basis points."""

    route_plan: list[GetSwapOrderRoutePlan] = Field(alias = "routePlan")
    """Execution route broken into individual swap steps."""

    referral_account: str | None = Field(default = None, alias = "referralAccount")
    """Referral account address, if provided."""

    fee_mint: str | None = Field(default = None, alias = "feeMint")
    """Token mint used for fees."""

    fee_bps: int | None = Field(default = None, alias = "feeBps")
    """Total fees in basis points, including platform fee and other fees."""

    platform_fee: GetSwapOrderPlatformFee | None = Field(default = None, alias = "platformFee")
    """Platform fee breakdown."""

    signature_fee_lamports: int | None = Field(default = None, alias = "signatureFeeLamports")
    """Lamports required for the base network signature fee."""

    signature_fee_payer: str | None = Field(default = None, alias = "signatureFeePayer")
    """Account paying the signature fee. None when taker pays."""

    prioritization_fee_lamports: int | None = Field(default = None, alias = "prioritizationFeeLamports")
    """Lamports required for priority fees and tips (Jito, Nozomi)."""

    prioritization_fee_payer: str | None = Field(default = None, alias = "prioritizationFeePayer")
    """Account paying the prioritization fee. None when taker pays."""

    rent_fee_lamports: int | None = Field(default = None, alias = "rentFeeLamports")
    """Estimated rent fee in lamports."""

    rent_fee_payer: str | None = Field(default = None, alias = "rentFeePayer")
    """Account paying the rent fee. None when taker pays."""

    router: JupiterRouter | None = None
    """Router that won the quote competition."""

    transaction: str | None = None
    """Base64-encoded assembled transaction. None when taker is not provided."""

    last_valid_block_height: str | None = Field(default = None, alias = "lastValidBlockHeight")
    """Last valid block height for the transaction."""

    gasless: bool | None = None
    """True when the swap is executed gasless."""

    request_id: str = Field(alias = "requestId")
    """Unique request ID required to call post_swap_execute."""

    total_time: int | None = Field(default = None, alias = "totalTime")
    """Total response time in milliseconds."""

    taker: str | None = None
    """Public key of the taker wallet."""

    quote_id: str | None = Field(default = None, alias = "quoteId")
    """Quote ID for RFQ swaps. None for non-RFQ routes."""

    maker: str | None = None
    """Market maker address for RFQ swaps. None for non-RFQ routes."""

    expire_at: str | None = Field(default = None, alias = "expireAt")
    """Quote expiration timestamp for RFQ swaps. None for non-RFQ routes."""

    error_code: int | None = Field(default = None, alias = "errorCode")
    """Error code when the transaction could not be built."""

    error_message: str | None = Field(default = None, alias = "errorMessage")
    """Human-readable error description when the transaction could not be built."""


# classes used on POST "Swap v2 - Execute" endpoint
# Body
class PostSwapExecuteBody(BaseModel):
    """
        Model referring to the body schema of the POST
        "**Swap - Execute**" endpoint from Jupiter Swap v2 API.
    """

    signed_transaction: str = Field(serialization_alias = "signedTransaction")
    """Base64-encoded signed transaction from get_swap_order."""

    request_id: str = Field(serialization_alias = "requestId")
    """Request ID from the get_swap_order response."""

    last_valid_block_height: str | None = Field(default = None, serialization_alias = "lastValidBlockHeight")
    """Optional block height for nonce validation."""

# Output
class PostSwapExecuteSwapEvent(BaseModel):
    """A single swap event in the POST "Swap - Execute" response."""

    input_token: str = Field(alias = "inputMint")
    """Input token address for this swap event."""

    input_amount: str = Field(alias = "inputAmount")
    """Input token amount used."""

    output_token: str = Field(alias = "outputMint")
    """Output token address for this swap event."""

    output_amount: str = Field(alias = "outputAmount")
    """Output token amount received."""

class PostSwapExecuteResponse(BaseModel):
    """
        Model referring to the response schema of the POST
        "**Swap - Execute**" endpoint from Jupiter Swap v2 API.
    """

    status: JupiterSwapExecutionStatus
    """Execution status: Success or Failed."""

    code: int | None = None
    """Status code (0 = success; non-zero values indicate specific failure types)."""

    signature: str | None = None
    """Transaction signature on success."""

    slot: str | None = None
    """Confirmed slot number."""

    total_input_amount: str | None = Field(default = None, alias = "totalInputAmount")
    """Total input token amount before fees."""

    total_output_amount: str | None = Field(default = None, alias = "totalOutputAmount")
    """Total output token amount after fees."""

    input_amount_result: str | None = Field(default = None, alias = "inputAmountResult")
    """Input token amount used for the swap."""

    output_amount_result: str | None = Field(default = None, alias = "outputAmountResult")
    """Output token amount received from the swap."""

    swap_events: list[PostSwapExecuteSwapEvent] | None = Field(default = None, alias = "swapEvents")
    """Individual swap events comprising the transaction."""

    error: str | None = None
    """Error message when status is Failed."""


# classes used on GET "Swap v2 - Build" endpoint
# Input
class GetSwapBuildParams(BaseModel):
    """
        Model referring to the input params schema of the GET
        "**Swap - Build**" endpoint from Jupiter Swap v2 API.
    """

    input_token: str = Field(serialization_alias = "inputMint")
    """Address of the input token mint."""

    output_token: str = Field(serialization_alias = "outputMint")
    """Address of the output token mint."""

    amount: int
    """Amount to swap in the smallest unit of the input token (factoring in token decimals)."""

    taker: str | None = None
    """Public key of the wallet initiating the swap."""

    slippage_bps: int | None = Field(default = None, serialization_alias = "slippageBps")
    """Slippage tolerance in basis points (0–10000). Defaults to 50 when unset."""

    mode: str | None = None
    """Quoting mode. Pass "fast" for reduced latency."""

    dexes: str | None = None
    """Comma-separated list of DEXes to restrict routing to. See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for valid values."""

    exclude_dexes: str | None = Field(default = None, serialization_alias = "excludeDexes")
    """Comma-separated list of DEXes to exclude from routing."""

    platform_fee_bps: int | None = Field(default = None, serialization_alias = "platformFeeBps")
    """Platform fee in basis points (0–10000). Requires fee_account."""

    fee_account: str | None = Field(default = None, serialization_alias = "feeAccount")
    """Token account for collecting platform fees."""

    max_accounts: int | None = Field(default = None, serialization_alias = "maxAccounts")
    """Maximum accounts for the swap route (1–64). Defaults to 64."""

    payer: str | None = None
    """Account paying transaction and rent fees. Defaults to taker."""

    wrap_unwrap_sol: bool | None = Field(default = None, serialization_alias = "wrapAndUnwrapSol")
    """Whether to automatically wrap/unwrap SOL. Defaults to True."""

    destination_token_account: str | None = Field(default = None, serialization_alias = "destinationTokenAccount")
    """SPL token account for receiving output tokens."""

    blockhash_slots_to_expiry: int | None = Field(default = None, serialization_alias = "blockhashSlotsToExpiry")
    """Slots until the blockhash expires (1–300). Defaults to 150."""

    tip_amount: str | None = Field(default = None, serialization_alias = "tipAmount")
    """SOL tip in lamports added as a tip instruction."""

    compute_unit_price_percentile: str | None = Field(default = None, serialization_alias = "computeUnitPricePercentile")
    """Named priority level ("medium", "high", "veryHigh") or basis points (0–10000) for compute unit price."""

    @field_serializer("amount")
    @classmethod
    def serialize_amount(cls, amount: int) -> str:
        return str(amount)

# Output
class GetSwapBuildAccount(BaseModel):
    """A single account entry in a swap instruction."""

    public_key: str = Field(alias = "pubkey")
    """Public key of the account."""

    is_signer: bool = Field(alias = "isSigner")
    """True when this account must sign the transaction."""

    is_writable: bool = Field(alias = "isWritable")
    """True when this account is modified by the instruction."""

class GetSwapBuildInstruction(BaseModel):
    """A single Solana instruction in the swap transaction."""

    program_id: str = Field(alias = "programId")
    """Program ID executing this instruction."""

    accounts: list[GetSwapBuildAccount]
    """Accounts referenced by this instruction."""

    data: str
    """Base64-encoded instruction data."""

class GetSwapBuildBlockhashMetadata(BaseModel):
    """Blockhash metadata in the GET "Swap - Build" response."""

    blockhash: list[int]
    """Blockhash represented as a byte array."""

    last_valid_block_height: int = Field(alias = "lastValidBlockHeight")
    """Block height at which this blockhash expires."""

class GetSwapBuildSwapInfo(BaseModel):
    """Swap info for a single step in the route plan of the GET "Swap - Build" response."""

    amm_key: str = Field(alias = "ammKey")
    """Address of the AMM used for this swap step."""

    amm_label: str | None = Field(default = None, alias = "label")
    """Human-readable label of the AMM."""

    input_token: str = Field(alias = "inputMint")
    """Input token address for this swap step."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw input amount for this step (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """Output token address for this swap step."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw output amount for this step (before decimals)."""

class GetSwapBuildRoutePlan(BaseModel):
    """A single step in the route plan of the GET "Swap - Build" response."""

    swap_info: GetSwapBuildSwapInfo = Field(alias = "swapInfo")
    """Swap details for this step."""

    percent: int | None = None
    """Percentage of the total swap routed through this step."""

    bps: int | None = None
    """Routing basis points for this step."""

    usd_value: float | None = Field(default = None, alias = "usdValue")
    """Estimated USD value routed through this step."""

class GetSwapBuildResponse(BaseModel):
    """
        Model referring to the response schema of the GET
        "**Swap - Build**" endpoint from Jupiter Swap v2 API.
    """

    input_token: str = Field(alias = "inputMint")
    """Input token mint address."""

    output_token: str = Field(alias = "outputMint")
    """Output token mint address."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw input amount (before decimals)."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw output amount (before decimals)."""

    other_amount_threshold: str = Field(alias = "otherAmountThreshold")
    """Minimum output amount after slippage."""

    swap_mode: str = Field(alias = "swapMode")
    """Swap mode used."""

    slippage_bps: int = Field(alias = "slippageBps")
    """Slippage tolerance applied in basis points."""

    route_plan: list[GetSwapBuildRoutePlan] = Field(alias = "routePlan")
    """Execution route broken into individual swap steps."""

    compute_budget_instructions: list[GetSwapBuildInstruction] = Field(alias = "computeBudgetInstructions")
    """Compute unit price instructions."""

    setup_instructions: list[GetSwapBuildInstruction] = Field(alias = "setupInstructions")
    """Pre-swap setup instructions (e.g. ATA creation)."""

    swap_instruction: GetSwapBuildInstruction = Field(alias = "swapInstruction")
    """Primary swap instruction."""

    cleanup_instruction: GetSwapBuildInstruction | None = Field(default = None, alias = "cleanupInstruction")
    """Post-swap cleanup instruction. None when not needed."""

    other_instructions: list[GetSwapBuildInstruction] | None = Field(default = None, alias = "otherInstructions")
    """Additional instructions. None when not applicable."""

    tip_instruction: GetSwapBuildInstruction | None = Field(default = None, alias = "tipInstruction")
    """SOL tip instruction. None when tipAmount was not provided."""

    addresses_by_lookup_table: dict[str, list[str]] | None = Field(default = None, alias = "addressesByLookupTableAddress")
    """Address lookup table mappings for v0 transactions. None when not needed."""

    blockhash_with_metadata: GetSwapBuildBlockhashMetadata | None = Field(default = None, alias = "blockhashWithMetadata")
    """Blockhash and expiry metadata for the transaction."""


# classes used on POST "Swap - Submit" endpoint
# Body
class PostSwapSubmitBody(BaseModel):
    """
        Model referring to the body schema of the POST
        "**Swap - Submit**" endpoint from Jupiter.
    """

    signed_transaction: str = Field(serialization_alias = "signedTransaction")
    """Base64-encoded signed Solana transaction."""

# Output
class PostSwapSubmitResponse(BaseModel):
    """
        Model referring to the response schema of the POST
        "**Swap - Submit**" endpoint from Jupiter.
    """

    signature: str
    """Transaction signature returned after successful submission."""

# *************
# * Token API *
# *************

class GetTokenInfoAudit(BaseModel):
    """General class holding audit information about a token."""

    is_suspicious: bool | None = Field(default = None, alias = "isSus")
    """The token is considered suspicious."""

    mint_authority_disabled: bool | None = Field(default = None, alias = "mintAuthorityDisabled")
    """Check if the mint authority is disabled."""

    freeze_authority_disabled: bool | None = Field(default = None, alias = "freezeAuthorityDisabled")
    """Check if the freeze authority is disabled."""

    top_holders_percentage: float | None = Field(default = None, alias = "topHoldersPercentage")
    """Percentage of the top holders."""

    dev_balance_percentage: float | None = Field(default = None, alias = "devBalancePercentage")
    """Percentage of the developer balance."""

    dev_migrations: float | None = Field(default = None, alias = "devMigrations")
    """Number of developer migrations."""

class GetTokenInfoFirstPool(BaseModel):
    """General class holding information about the first pool of a token."""

    id: str
    """The pool's ID."""

    created_at: str = Field(alias = "createdAt")
    """The pool's creation timestamp."""

class GetTokenInfoStatistics(BaseModel):
    """General class holding statistics information about a token in a period of time."""

    price_change: float | None = Field(default = None, alias = "priceChange")
    """Price change in percentage."""

    holder_change: float | None = Field(default = None, alias = "holderChange")
    """Holder change in percentage."""

    liquidity_change: float | None = Field(default = None, alias = "liquidityChange")
    """Liquidity change in percentage."""

    volume_change: float | None = Field(default = None, alias = "volumeChange")
    """Volume change in percentage."""

    buy_volume: float | None = Field(default = None, alias = "buyVolume")
    """Buy volume in percentage."""

    sell_volume: float | None = Field(default = None, alias = "sellVolume")
    """Sell volume in percentage."""

    buy_organic_volume: float | None = Field(default = None, alias = "buyOrganicVolume")
    """Buy organic volume in percentage."""

    sell_organic_volume: float | None = Field(default = None, alias = "sellOrganicVolume")
    """Sell organic volume in percentage."""

    num_buys: int | None = Field(default = None, alias = "numBuys")
    """Number of buys."""

    num_sells: int | None = Field(default = None, alias = "numSells")
    """Number of sells."""

    num_traders: int | None = Field(default = None, alias = "numTraders")
    """Number of traders."""

    num_organic_buyers: int | None = Field(default = None, alias = "numOrganicBuyers")
    """Number of organic buyers."""

    num_net_buyers: int | None = Field(default = None, alias = "numNetBuyers")
    """Number of net buyers."""

class GetTokenInfo(BaseModel):
    """General class identifing a token on the chain and all its information."""

    id: str
    """The token's mint address."""

    name: str
    """The token's name."""

    symbol: str
    """The token's symbol."""

    icon: str | None = None
    """The token's icon URL."""

    decimals: int
    """The token's decimals."""

    twitter: str | None = None
    """The token's Twitter URL."""

    telegram: str | None = None
    """The token's Telegram URL."""

    website: str | None = None
    """The token's website URL."""

    dev: str | None = None
    """The token's developer URL."""

    circ_supply: float | None = Field(default = None, alias = "circSupply")
    """The token's circulating supply."""

    total_supply: float | None = Field(default = None, alias = "totalSupply")
    """The token's total supply."""

    token_program: str | None = Field(default = None, alias = "tokenProgram")
    """The token program address."""

    launchpad: str | None = Field(default = None, alias = "launchpad")
    """The token launchpad address."""

    partner_config: str | None = Field(default = None, alias = "partnerConfig")
    """The token partner config address."""

    graduated_pool: str | None = Field(default = None, alias = "graduatedPool")
    """The token graduated pool address."""

    graduated_at: str | None = Field(default = None, alias = "graduatedAt")
    """The token graduated at timestamp."""

    holder_count: int | None = Field(default = None, alias = "holderCount")
    """The token holder count."""

    fully_diluted_valuation: float | None = Field(default = None, alias = "fdv")
    """The token fully diluted valuation."""

    market_cap: float | None = Field(default = None, alias = "mcap")
    """The token market capitalization."""

    usd_price: float | None = Field(default = None, alias = "usdPrice")
    """The token price in USD."""

    price_block_id: int | None = Field(default = None, alias = "priceBlockId")
    """The block ID of the token price."""

    liquidity: float | None = Field(default = None, alias = "liquidity")
    """The token liquidity."""

    stats_5m: GetTokenInfoStatistics | None = Field(default = None, alias = "stats5m")
    """The token statistics over the last 5 minutes."""

    stats_1h: GetTokenInfoStatistics | None = Field(default = None, alias = "stats1h")
    """The token statistics over the last 1 hour."""

    stats_6h: GetTokenInfoStatistics | None = Field(default = None, alias = "stats6h")
    """The token statistics over the last 6 hours."""

    stats_24h: GetTokenInfoStatistics | None = Field(default = None, alias = "stats24h")
    """The token statistics over the last 24 hours."""

    stats_7d: GetTokenInfoStatistics | None = Field(default = None, alias = "stats7d")
    """The token statistics over the last 7 days."""

    stats_30d: GetTokenInfoStatistics | None = Field(default = None, alias = "stats30d")
    """The token statistics over the last 30 days."""

    first_pool: GetTokenInfoFirstPool | None = Field(default = None, alias = "firstPool")
    """The token first pool information."""

    audit: GetTokenInfoAudit | None = None
    """The token audit information."""

    organic_score: float = Field(alias = "organicScore")
    """The token organic score."""

    organic_score_label: JupiterOrganicScore = Field(alias = "organicScoreLabel")
    """The token organic score label."""

    is_verified: bool | None = Field(default = None, alias = "isVerified")
    """Whether the token is verified."""

    cexes: list[str] | None = Field(default = None, alias = "cexes")
    """List of centralized exchanges where the token is listed."""

    tags: list[str] | None = Field(default = None, alias = "tags")
    """List of tags associated with the token."""

    updated_at: str | None = Field(default = None, alias = "updatedAt")
    """Date and time when the token was last updated."""

# classes used on GET "Token Search" endpoint
class GetTokenSearchResponse(BaseModel):
    """
        Model representing the response object from the GET
        "**Token Search**" endpoint from Jupiter API.
    """

    tokens: list[GetTokenInfo]
    """List of token addresses matching the search query."""

# classes used on GET "Token Tag" endpoint
class GetTokenTagResponse(GetTokenSearchResponse):
    """
        Model used to represent the GET **Token Tag** 
        endpoint from Jupiter API.
    """
    pass

# classes used on GET "Token Category" endpoint
class GetTokenCategoryResponse(GetTokenSearchResponse):
    """
        Model used to represent the GET **Token Category** 
        endpoint from Jupiter API.
    """
    pass

# classes used on GET "Token New" endpoint
class GetTokenRecentResponse(GetTokenSearchResponse):
    """
        Model used to represent a token information
        on the GET **Token Recent** endpoint.
    """
    pass

# classes used on GET "Token Verify - Check Eligibility" endpoint
class GetTokenVerifyCheckEligibilityResponse(BaseModel):
    """
        Model representing the response object from the GET
        "**Token Verify - Check Eligibility**" endpoint from Jupiter API.
    """

    token_exists: bool = Field(alias = "tokenExists")
    """Whether Jupiter recognises the token."""

    is_verified: bool = Field(alias = "isVerified")
    """Whether the token already has verified status."""

    can_verify: bool = Field(alias = "canVerify")
    """Whether a verification submission is currently permitted."""

    can_metadata: bool = Field(alias = "canMetadata")
    """Whether a metadata update submission is currently permitted."""

    verification_error: str | None = Field(default = None, alias = "verificationError")
    """Reason verification is blocked; `None` when verification is permitted."""

    metadata_error: str | None = Field(default = None, alias = "metadataError")
    """Reason metadata update is blocked; `None` when metadata update is permitted."""

# classes used on GET "Token Verify - Craft Transaction" endpoint
class GetTokenVerifyCraftTxnResponse(BaseModel):
    """
        Model representing the response object from the GET
        "**Token Verify - Craft Transaction**" endpoint from Jupiter API.
    """

    transaction: str
    """Base64-encoded unsigned transaction for the 1000 JUP payment."""

    request_id: str = Field(alias = "requestId")
    """Unique identifier to be passed to the execute step."""

    mint: str
    """JUP token mint address used for the payment."""

    amount: str
    """Payment amount in the smallest JUP units (1000 JUP = `1000000000`)."""

    expire_at: str = Field(alias = "expireAt")
    """ISO-8601 timestamp after which the transaction is no longer valid."""

    gasless: bool
    """Whether the transaction requires no SOL fees."""

# classes used on POST "Token Verify - Execute" endpoint
class PostTokenVerifyExecuteTokenMetadata(BaseModel):
    """Optional token metadata fields submitted alongside a verification request."""

    token_id: str = Field(serialization_alias = "tokenId")
    """Mint address of the token being updated."""

    name: str | None = None
    """Display name of the token."""

    symbol: str | None = None
    """Ticker symbol of the token."""

    icon: str | None = None
    """URL to the token icon image."""

    website: str | None = None
    """Official website URL."""

    twitter: str | None = None
    """Official Twitter/X profile URL."""

    twitter_community: str | None = Field(default = None, serialization_alias = "twitterCommunity")
    """Twitter/X community URL."""

    telegram: str | None = None
    """Official Telegram URL."""

    discord: str | None = None
    """Official Discord URL."""

    instagram: str | None = None
    """Official Instagram URL."""

    tiktok: str | None = None
    """Official TikTok URL."""

    token_description: str | None = Field(default = None, serialization_alias = "tokenDescription")
    """Short description of the token."""

    circulating_supply: str | None = Field(default = None, serialization_alias = "circulatingSupply")
    """Current circulating supply as a string."""

    circulating_supply_url: str | None = Field(default = None, serialization_alias = "circulatingSupplyUrl")
    """URL to a data source for circulating supply."""

    coingecko_coin_id: str | None = Field(default = None, serialization_alias = "coingeckoCoinId")
    """CoinGecko coin identifier for the token."""

    other_url: str | None = Field(default = None, serialization_alias = "otherUrl")
    """Any additional reference URL."""

class PostTokenVerifyExecuteBody(BaseModel):
    """
        Model referring to the body schema of the POST
        "**Token Verify - Execute**" endpoint from Jupiter API.
    """

    transaction: str
    """Base64-encoded signed transaction from the craft-txn step."""

    request_id: str = Field(serialization_alias = "requestId")
    """Request ID from the craft-txn response."""

    sender_address: str = Field(serialization_alias = "senderAddress")
    """Wallet address that signed and submitted the payment."""

    token_id: str = Field(serialization_alias = "tokenId")
    """Mint address of the token to verify."""

    twitter_handle: str = Field(serialization_alias = "twitterHandle")
    """X profile URL of the project."""

    description: str
    """Rationale for the verification submission."""

    token_metadata: PostTokenVerifyExecuteTokenMetadata | None = Field(default = None, serialization_alias = "tokenMetadata")
    """Optional metadata to update alongside the verification request."""

class PostTokenVerifyExecuteResponse(BaseModel):
    """
        Model representing the response object from the POST
        "**Token Verify - Execute**" endpoint from Jupiter API.
    """

    status: str
    """Execution result: `Success` or `Failed`."""

    signature: str
    """On-chain transaction signature."""

    verification_created: bool = Field(alias = "verificationCreated")
    """Whether a verification request was submitted."""

    metadata_created: bool = Field(alias = "metadataCreated")
    """Whether a metadata update request was submitted."""

# ***************
# * Trigger API *
# ***************

# classes used on POST "Trigger - Create Order" endpoint
class PostTriggerCreateOrderParams(BaseModel):
    """
        Model used to identify the amounts required by a POST **Limit Order Create** request.  
        Observe that the amounts are in raw format (integer values without decimals).
    """

    input_amount: int = Field(serialization_alias = "makingAmount")
    """Amount of input token to sell in the limit order."""

    output_amount: int = Field(serialization_alias = "takingAmount")
    """Amount of output token to buy in the limit order."""

    expired_at_unix_time: int | None = Field(default = None, serialization_alias = "expiredAt")
    """Expiring date for the Limit Order expressed in UNIX time"""

    slippage_base_points: int | None = Field(default = None, serialization_alias = "slippageBps")
    """
        Amount of slippage the order can be executed with.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    fee_base_points: int | None = Field(default = None, serialization_alias = "feeBps")
    """
        Amount of fee that the `referral_public_key` collects.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    @field_serializer("input_amount", "output_amount", "fee_base_points", "expired_at_unix_time", "slippage_base_points", when_used = "unless-none")
    @classmethod
    def serialize_amounts(cls, amount_raw: int | None) -> str | None:
        if amount_raw is not None:
            return str(amount_raw)

class PostTriggerCreateOrderBody(BaseModel):
    """
        Model refering to the input body of the POST 
        "**Trigger - Create Order**" endpoint from Jupiter API.
    """

    maker_wallet_key: str = Field(serialization_alias = "maker")
    """Wallet address of the user who wants to create an order."""

    payer_wallet_key: str = Field(serialization_alias = "payer")
    """Wallet address of who is paying to open an order (usually the `maker` wallet)."""

    input_token: str = Field(serialization_alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    output_token: str = Field(serialization_alias = "outputMint")
    """The address of the output token on the chain that will bought."""

    params: PostTriggerCreateOrderParams
    """The amounts of output-to-buy and input-to-sell tokens in the limit order."""

    compute_unit_price: str = Field(default = "auto", serialization_alias = "computeUnitPrice")
    """Used to determine a transaction's prioritization fee. Defaults to `auto`."""

    referral_public_key: str | None = Field(default = None, serialization_alias = "feeAccount")
    """A token account (via the Referral Program) that will receive the fees."""

    wrap_unwrap_sol: bool = Field(default = True, serialization_alias = "wrapAndUnwrapSol")
    """To automatically wrap/unwrap SOL in the transaction."""

class PostTriggerCreateOrderResponse(BaseModel):
    """
        Model refering to the response schema of the POST 
        "**Trigger - Create Order**" endpoint from Jupiter API.
    """

    request_id: str = Field(alias = "requestId")
    """Unique ID required to make a request to `post_trigger_execute`"""

    transaction_id: str = Field(alias = "transaction")
    """Unsigned base-64 encoded transaction."""

    order_public_key: str = Field(alias = "order")
    """Base-58 account which is the Trigger Order account."""

# classes used on POST "Trigger - Execute" endpoint
class PostTriggerExecuteResponse(BaseModel):
    """
        Model refering to the response schema of the POST 
        "**Trigger - Execute**" endpoint from Jupiter API.
    """

    status: JupiterSwapExecutionStatus
    """Status of the order."""

    code: int
    """Code of the status."""

    signature_transaction_id: str | None = Field(default = None, alias = "signature")
    """Signature of the successful transaction."""

    error: str | None = None
    """Error message in case of failure."""

# classes used on POST "Trigger - Cancel Order" endpoint
class PostTriggerCancelOrderResponse(BaseModel):
    """
        Model refering to the response schema of the POST 
        "**Trigger - Cancel Order**" endpoint from Jupiter API.
    """

    request_id: str = Field(alias = "requestId")
    """Unique ID required to make a request to `post_trigger_execute`"""

    transaction_id: str | list[str] = Field(validation_alias = AliasChoices("transaction", "transactions"))
    """Unsigned base-64 encoded transaction."""

    @model_serializer
    def serialize_response(self) -> dict[str, str | list[str]]:
        """Custom serializer to manage transaction response according to type."""

        # set root
        resonse_model: dict[str, str | list[str]] = {"requestId": self.request_id}

        # set transaction id
        if isinstance(self.transaction_id, str):
            resonse_model["transaction"] = self.transaction_id
        elif isinstance(self.transaction_id, list):
            resonse_model["transactions"] = self.transaction_id

        return resonse_model

# classes used on GET "Trigger - Orders" endpoint
class GetTriggerOrdersTrade(BaseModel):
    """
        Model refering to the schema of a trade in the GET 
        "**Trigger - Orders**" endpoint from Jupiter
    """

    order_key: str = Field(alias = "orderKey")
    """Unique identifier of the order associated with the trade."""

    keeper: str
    """Wallet address of the user who made the trade."""

    input_token: str = Field(alias = "inputMint")
    """Input token address."""

    input_amount: float = Field(alias = "inputAmount")
    """Amount of input token sent in the trade."""

    input_amount_raw: int = Field(alias = "rawInputAmount")
    """Amount of input token sent in raw format; i.e. integer value without decimals."""

    output_token: str = Field(alias = "outputMint")
    """Output token address."""

    output_amount: float = Field(alias = "outputAmount")
    """Amount of output token received in the trade."""

    output_amount_raw: int = Field(alias = "rawOutputAmount")
    """Amount of output token received in raw format; i.e. integer value without decimals."""

    fee_token: str = Field(alias = "feeMint")
    """Fee token address."""

    fee_amount: float = Field(alias = "feeAmount")
    """Amount of fee token paid in the trade."""

    fee_amount_raw: int = Field(alias = "rawFeeAmount")
    """Amount of fee token paid in raw format; i.e. integer value without decimals."""

    transaction_id: str = Field(alias = "txId")
    """Unique identifier of the transaction associated with the trade."""

    confirmed_at: datetime = Field(alias = "confirmedAt")
    """Date and time when the trade was confirmed."""

    action: str
    """Action made in the trade."""

    @field_validator("input_amount", "output_amount", "fee_amount")
    def parse_amounts(cls, amount_raw: str) -> float:
        return float(amount_raw)

    @field_validator("input_amount_raw", "output_amount_raw", "fee_amount_raw")
    def parse_amounts_raw(cls, amount_raw: str) -> int:
        return int(amount_raw)

    @field_validator("confirmed_at")
    def parse_datetime(cls, datetime_raw: str | datetime) -> datetime:
        if isinstance(datetime_raw, str):
            return datetime.strptime(datetime_raw, "%Y-%m-%dT%H:%M:%S")
        return datetime_raw

class GetTriggerOrdersOrder(BaseModel):
    """
        Model refering to the schema of an order in the GET 
        "**Trigger - Orders**" endpoint from Jupiter API.
    """

    user_public_key: str = Field(alias = "userPubkey")
    """User wallet address."""

    order_key: str = Field(alias = "orderKey")
    """Unique identifier of the order."""

    input_token: str = Field(alias = "inputMint")
    """Input token address."""

    input_amount: float = Field(alias = "makingAmount")
    """Amount of input token to sell in the order."""

    input_amount_raw: int = Field(alias = "rawMakingAmount")
    """Amount of input token to sell in raw format; i.e. integer value without decimals."""

    input_remaining_token: float = Field(alias = "remainingMakingAmount")
    """Amount of input token remaining to sell in the order."""

    input_remaining_token_raw: int = Field(alias = "rawRemainingMakingAmount")
    """Amount of input token remaining to sell in raw format; i.e. integer value without decimals."""

    output_token: str = Field(alias = "outputMint")
    """Output token address."""

    output_amount: float = Field(alias = "takingAmount")
    """Amount of output token to buy in the order."""

    output_amount_raw: int = Field(alias = "rawTakingAmount")
    """Amount of output token to buy in raw format; i.e. integer value without decimals."""

    output_remaining_amount: float = Field(alias = "remainingTakingAmount")
    """Amount of output token remaining to buy in the order."""

    output_remaining_amount_raw: int = Field(alias = "rawRemainingTakingAmount")
    """Amount of output token remaining to buy in raw format; i.e. integer value without decimals."""

    expired_at_unix_time: int | None = Field(default = None, alias = "expiredAt")
    """Expiring date for the Limit Order expressed in UNIX time"""

    created_at: datetime = Field(alias = "createdAt")
    """Date and time when the order was created."""

    updated_at: datetime = Field(alias = "updatedAt")
    """Date and time when the order was last updated."""

    status: JupiterOrderState
    """Status of the order."""

    open_transaction_id: str = Field(alias = "openTx")
    """Transaction ID of the open order."""

    close_transaction_id: str | None = Field(default = None, alias = "closeTx")
    """Transaction ID of the close order."""

    program_version_id: str = Field(alias = "programVersion")
    """Program version public key used for the order."""

    trades: list[GetTriggerOrdersTrade]
    """List of trades made in the order."""

    @field_validator("input_amount", "input_remaining_token", "output_amount", "output_remaining_amount")
    def parse_amounts(cls, amount_raw: str) -> float:
        return float(amount_raw)

    @field_validator("input_amount_raw", "input_remaining_token_raw", "output_amount_raw", "output_remaining_amount_raw")
    def parse_amounts_raw(cls, amount_raw: str) -> int:
        return int(amount_raw)

    @field_validator("created_at", "updated_at")
    def parse_datetime(cls, datetime_raw: str | datetime) -> datetime:
        if isinstance(datetime_raw, str):
            return datetime.strptime(datetime_raw, "%Y-%m-%dT%H:%M:%S")
        return datetime_raw

    @field_validator("status")
    @classmethod
    def validator_status(cls, status_raw: str | JupiterOrderState) -> JupiterOrderState:
        if isinstance(status_raw, str):
            JupiterOrderState.check(status_raw)
            return JupiterOrderState[status_raw]
        return status_raw

class GetTriggerOrdersResponse(BaseModel):
    """
        Model refering to the response schema of the GET 
        "**Trigger - Orders**" endpoint from Jupiter API.
    """

    user_public_key: str = Field(alias = "user")
    """User wallet address."""

    order_status: JupiterOrderStatus = Field(alias = "orderStatus")
    """Status of the order."""

    orders: list[GetTriggerOrdersOrder]
    """List of orders."""

    page: int
    """Current page."""

    total_pages: int = Field(alias = "totalPages")
    """Total number of pages."""

# *****************
# * Recurring API *
# *****************

class PostRecurringTransactionResponse(BaseModel):
    """
        This model is used to identify the general response 
        provided by all the endpoints of the Recurring API that 
        give an unsigned transaction that should be then sent 
        to the `post_trigger_execute` endpoint.
    """

    request_id: str = Field(alias = "requestId")
    """Unique ID required to make a request to `post_trigger_execute`"""

    transaction_id: str = Field(alias = "transaction")
    """Unsigned base-64 encoded transaction."""

# class used on POST "Recurring - Create Order" endpoint
class PostRecurringCreateOrderTime(BaseModel):
    """
        Model used to identify the parameters required by a POST 
        **Recurring - Create Order** request using **time** mode.
    """

    deposit_amount_raw: int = Field(serialization_alias = "inAmount")
    """Raw amount of input token to deposit now (before decimals)."""

    order_count: int = Field(serialization_alias = "numberOfOrders")
    """Number of orders to create."""

    interval_unix_time: int = Field(serialization_alias = "interval")
    """Time between each order in UNIX seconds."""

    min_price_raw: int | None = Field(default = None, serialization_alias = "minPrice")
    """Minimum price of the token for the order to be executed in raw format (before decimals)."""

    max_price_raw: int | None = Field(default = None, serialization_alias = "maxPrice")
    """Maximum price of the token for the order to be executed in raw format (before decimals)."""

    start_at_unix_time: int | None = Field(default = None, serialization_alias = "startAt")
    """
        Time when the first cycle will start in UNIX seconds.  
        If not provided, the first cycle will start immediately.
    """

class PostRecurringCreateOrderTimeParams(BaseModel):
    """**Recurring - Create Order** time mode."""

    time: PostRecurringCreateOrderTime
    """Time order parameters."""

class PostRecurringCreateOrderPrice(BaseModel):
    """
        Model used to identify the parameters required by a POST 
        **Recurring - Create Order** request using **price** mode.
    """

    deposit_amount_raw: int = Field(serialization_alias = "depositAmount")
    """Raw amount of input token to deposit now (before decimals)."""

    increment_usdc_value_raw: int = Field(serialization_alias = "incrementUsdcValue")
    """Raw amount of `USDC` to increment per cycle (before decimals)."""

    interval_unix_time: int = Field(serialization_alias = "interval")
    """Time between each cycle in UNIX seconds."""

    start_at_unix_time: int | None = Field(default = None, serialization_alias = "startAt")
    """
        Time when the first cycle will start in UNIX seconds.  
        If not provided, the first cycle will start immediately.
    """

class PostRecurringCreateOrderPriceParams(BaseModel):
    """**Recurring - Create Order** price mode."""

    price: PostRecurringCreateOrderPrice
    """Price order parameters."""


class PostRecurringCreateOrderBody(BaseModel):
    """
        Model refering to the input body of the POST 
        "**Recurring - Create Order**" endpoint from Jupiter API.
    """

    user_public_key: str = Field(serialization_alias = "user")
    """User wallet address."""

    input_token: str = Field(serialization_alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    output_token: str = Field(serialization_alias = "outputMint")
    """The address of the output token on the chain that will be bought."""

    params: PostRecurringCreateOrderTimeParams | PostRecurringCreateOrderPriceParams
    """The parameters of the order. It can be either a time or price parameter."""

class PostRecurringCreateOrderResponse(PostRecurringTransactionResponse):
    """
        Model refering to the response schema of the POST 
        "**Recurring - Create Order**" endpoint from Jupiter API.
    """
    pass

# classes used on GET "Recurring - Orders" endpoint
class GetRecurringOrdersTrade(GetTriggerOrdersTrade):
    """
        Model refering to the response schema of the GET 
        "**Recurring - Orders**" endpoint from Jupiter API
        identifing a trade.
    """

    product_meta: dict | None = Field(default = None, alias = "productMeta")
    """Additional metadata of the trade."""

class GetRecurringOrdersOrder(BaseModel):
    """
        Model refering to an order coming from the GET 
        "**Recurring - Orders**" endpoint from Jupiter API.
    """

    order_key: str = Field(alias = "orderKey")
    """Unique identifier of the order."""

    updated_at: datetime = Field(alias = "updatedAt")
    """Date and time when the order was last updated."""

    open_transaction_id: str = Field(alias = "openTx")
    """Transaction ID used to open the order."""

    close_transaction_id: str | None = Field(default = None, alias = "closeTx")
    """Transaction ID of the close order."""

    created_at: datetime = Field(alias = "createdAt")
    """Date and time when the order was created."""

    input_token: str = Field(alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    input_amount_deposited: float = Field(alias = "inDeposited")
    """Input token amount deposited in the order."""

    input_amount_deposited_raw: int = Field(alias = "rawInDeposited")
    """Raw input token amount deposited in the order (before decimals)."""

    input_amount_used: float = Field(alias = "inUsed")
    """Input token amount used in the order."""

    input_amount_used_raw: int = Field(alias = "rawInUsed")
    """Raw input token amount used in the order (before decimals)."""

    input_amount_withdrawn: float = Field(alias = "inWithdrawn")
    """Input token amount withdrawn in the order."""

    input_amount_withdrawn_raw: int = Field(alias = "rawInWithdrawn")
    """Raw input token amount withdrawn in the order (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """The address of the output token on the chain that will be bought."""

    output_amount_received: float = Field(alias = "outReceived")
    """Output token amount received in the order."""

    output_amount_received_raw: int = Field(alias = "rawOutReceived")
    """Raw output token amount received in the order (before decimals)."""

    output_amount_withdrawn: float = Field(alias = "outWithdrawn")
    """Output token amount withdrawn in the order."""

    output_amount_withdrawn_raw: int = Field(alias = "rawOutWithdrawn")
    """Raw output token amount withdrawn in the order (before decimals)."""

    trades: list[GetRecurringOrdersTrade]
    """List of trades made in the order."""

    user_public_key: str = Field(alias = "userPubkey")
    """User wallet address."""

class GetRecurringOrdersPrice(GetRecurringOrdersOrder):
    """
        Model refering to the response schema of the GET 
        "**Recurring - Orders**" endpoint when requesting 
        price-based orders from Jupiter API.
    """

    start_at: datetime = Field(alias = "startAt")
    """Time when the order started."""

    status: JupiterOrderState
    """Status of the order."""

    order_interval_sec: int = Field(alias = "orderInterval")
    """Interval in seconds between each order."""

    closed_by: str | None = Field(default = None, alias = "closedBy")
    """Account key of the user who closed the order."""

    estimated_usdc_value_spent: float = Field(alias = "estimatedUsdcValueSpent")
    """Estimated USDC value spent in the order."""

    estimated_usdc_value_spent_raw: int = Field(alias = "rawEstimatedUsdcValueSpent")
    """Raw estimated USDC value spent in the order (before decimals)."""

    incremental_usd_value: float = Field(alias = "incrementalUsdValue")
    """Incremental `USD` value of the order."""

    incremental_usd_value_raw: int = Field(alias = "rawIncrementalUsdValue")
    """Raw incremental `USD` value of the order (before decimals)."""

    supposed_usd_value: float = Field(alias = "supposedUsdValue")
    """Supposed `USD` value to use in the order."""

    supposed_usd_value_raw: int = Field(alias = "rawSupposedUsdValue")
    """Raw supposed `USD` value to use in the order (before decimals)."""

    input_amount_left: float = Field(alias = "inLeft")
    """Input token amount left to fulfill the orders."""

    input_amount_left_raw: int = Field(alias = "rawInLeft")
    """Raw input token amount left to fulfill the orders (before decimals)."""

class GetRecurringOrdersTime(GetRecurringOrdersOrder):
    """
        Model refering to the response schema of the GET 
        "**Recurring - Orders**" endpoint when requesting
        time-based orders from Jupiter API.
    """

    cycle_frequency_sec: int = Field(alias = "cycleFrequency")
    """Seconds count between each cycle."""

    input_amount_per_cycle: float = Field(alias = "inAmountPerCycle")
    """Input token amount required by the cycle."""

    input_amount_per_cycle_raw: int = Field(alias = "rawInAmountPerCycle")
    """Raw input token amount required by the cycle (before decimals)."""

    min_output_price: float = Field(alias = "minOutAmount")
    """Minimum price of the output token for the order to be executed."""

    min_output_price_raw: int = Field(alias = "rawMinOutAmount")
    """Raw minimum price of the output token for the order to be executed (before decimals)."""

    max_output_price: float = Field(alias = "maxOutAmount")
    """Maximum price of the output token for the order to be executed."""

    max_output_price_raw: int = Field(alias = "rawMaxOutAmount")
    """Raw maximum price of the output token for the order to be executed (before decimals)."""

    user_closed_flag: bool = Field(alias = "userClosed")
    """Flag indicating if the user closed the order."""

class GetRecurringOrdersResponse(BaseModel):
    """
        Model refering to the response schema of the GET 
        "**Recurring - Orders**" endpoint from Jupiter API.
    """

    user_public_key: str = Field(alias = "user")
    """User wallet address."""

    order_status: JupiterOrderStatus = Field(alias = "orderStatus")
    """Status of the order."""

    price: list[GetRecurringOrdersPrice] | None = None
    """List of price-based orders. Variable filled only if the request is for price-based orders."""

    time: list[GetRecurringOrdersTime] | None = None
    """List of time-based orders. Variable filled only if the request is for time-based orders."""

    all: list[GetRecurringOrdersPrice | GetRecurringOrdersTime] | None = None
    """List of both time-based and price-based orders. Variable filled only if the request is for all types of orders."""

    page: int
    """Current page."""

    total_pages: int = Field(alias = "totalPages")
    """Total number of pages."""

# classes used on POST "Recurring - Cancel Order" endpoint
class PostRecurringCancelOrderResponse(PostRecurringTransactionResponse):
    """
        Model refering to the response schema of the POST 
        "**Recurring - Cancel Order**" endpoint from Jupiter API.
    """
    pass

# classes used on POST "Recurring - Execute" endpoint
class PostRecurringExecuteResponse(BaseModel):
    """
        Model refering to the response schema of the POST 
        "**Recurring - Execute**" endpoint from Jupiter API.
    """
    signature_transaction_id: str | None = Field(default = None, alias = "signature")
    status: JupiterSwapExecutionStatus
    order_id: str | None = Field(default = None, alias = "order")
    error: str | None = None