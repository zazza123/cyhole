from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, AliasChoices, field_validator, field_serializer, model_serializer

from ..jupiter.param import (
    JupiterSwapMode,
    JupiterSwapDex,
    JupiterOrderState,
    JupiterRouter,
    JupiterSwapExecutionStatus,
    JupiterOrderStatus,
    JupiterOrganicScore,
    JupiterShieldWarningType,
    JupiterShieldWarningSeverity,
    JupiterShieldWarningSource
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

class GetPriceData(BaseModel):
    """
        Model with all the information about a token data
        returned by the GET "**Price**" endpoint from Jupiter API.
    """

    price: float = Field(alias = "usdPrice")
    """The price of the token compared to the `USDC` token."""

    decimals: int
    """Decimal of the token on the chain."""

    block_id: int | None = Field(default = None, alias = "blockId")
    """The block ID of the token."""

    price_change_24h: float | None = Field(default = None, alias = "priceChange24h")
    """Price change in percentage in the last 24h."""

class GetPriceResponse(BaseModel):
    """
        Model refering to the response schema of the GET 
        "**Price**" endpoint from Jupiter API.
    """
    data: dict[str, GetPriceData]
    """Dictionary of token prices. The key is the token address."""

    time_unix: int
    """UNIX timestamp of the price data."""

# ************
# * Swap API *
# ************

# classes used on GET "Quote" endpoint
# Input
class GetQuoteParams(BaseModel):
    """
        Model refering to the input schema of the GET 
        "**Quote**" endpoint from Jupiter API.
    """

    input_token: str = Field(serialization_alias = "inputMint")
    """The address of the input token on the chain."""

    output_token: str = Field(serialization_alias = "outputMint")
    """The address of the output token on the chain."""

    amount: int
    """The amount to swap, factoring in the token decimals.
        For example, if the token has 6 decimals, then `1.0` = `1_000_000`. 
        The amount refers to the input/output token depending on the `swap_mode` 
        parameter. Since by default the `swap_mode` is set to `EXACT_IN`, then 
        the amount refers to the **input** token if not specified.
    """

    slippage_base_points: int = Field(default = 50, serialization_alias = "slippageBps")
    """Slippage tolerance in basis points. Observe that if the slippage exeeded this value, then the swap will fail."""

    swap_mode: JupiterSwapMode = Field(default = JupiterSwapMode.EXACT_IN, serialization_alias = "swapMode")
    """Define if the slippage is on the input or output token."""

    dexes: list[str] | None = None
    """List of DEXes to include; by default, all the DEXes are included.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    exclude_dexes: list[str] | None = Field(default = None, serialization_alias = "excludeDexes")
    """List of DEXes to exclude.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    restrict_intermediate_tokens: bool = Field(default = True, serialization_alias = "restrictIntermediateTokens")
    """Restrict to a top token set for stable liquidity. This will help to reduce exposure to potential high slippage routes."""

    only_direct_routes: bool = Field(default = False, serialization_alias = "onlyDirectRoutes")
    """Limit to single hop routes only."""

    as_legacy_transaction: bool = Field(default = False, serialization_alias = "asLegacyTransaction")
    """Use legacy transactions instead of versioned ones."""

    platform_fee_base_points: int | None = Field(default = None, serialization_alias = "platformFeeBps")
    """Fee to charge. The value is in percent and taken from output token."""

    max_accounts: int = Field(default = 64, serialization_alias = "maxAccounts")
    """Max accounts to be used for the quote. Jupiter Frontend uses a maxAccounts of 64."""

    @field_validator("dexes", "exclude_dexes")
    @classmethod
    def validator_dexes(cls, dexes: list[str]) -> list[str]:
        for dex in dexes:
            JupiterSwapDex.check(dex)
        return dexes

    @field_serializer("dexes", "exclude_dexes")
    @classmethod
    def serialize_dexes(cls, dexes: list[str] | None) -> str | None:
        return ",".join(dexes) if dexes else None

    @field_serializer("swap_mode")
    @classmethod
    def serialize_swap_mode(cls, mode: JupiterSwapMode) -> str:
        return mode.value

    @field_validator("swap_mode")
    @classmethod
    def validator_swap_mode(cls, mode: str) -> str:
        JupiterSwapMode.check(mode)
        return mode

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

class GetQuoteResponse(BaseModel):
    """
        Model refering to the response schema of the GET 
        "**Quote**" endpoint from Jupiter API.
    """

    input_token: str = Field(alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    input_amount_raw: str = Field(alias = "inAmount")
    """Raw amount of input token to use to buy (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """The address of the output token on the chain that will bought."""

    output_amount_raw: str = Field(alias = "outAmount")
    """Raw amount of output token to buy (before decimals)."""

    other_amount_threshold_raw: str = Field(alias = "otherAmountThreshold")
    """Raw calculated minimum output amount after accounting for `slippage_base_points` and `platform_fees` (before decimals)."""

    swap_mode: JupiterSwapMode = Field(alias = "swapMode")
    """Mode of the swap."""

    slippage_base_points: int = Field(alias = "slippageBps")
    """
        Amount of slippage the order can be executed with.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    platform_fees: GetQuotePlatformFees | None = Field(default = None, alias = "platformFee")
    """Platform fees for the swap."""

    price_impact_pct: float = Field(alias = "priceImpactPct")
    """Percentage of price impact for the swap."""

    route_plan: list[GetQuoteRoutePlan] = Field(alias = "routePlan")
    """List of route plans for the swap."""

    context_slot: int = Field(alias = "contextSlot")
    """Slot number of the context."""

    time_taken: float = Field(alias = "timeTaken")
    """Time taken to process the request."""

    @field_serializer("swap_mode")
    @classmethod
    def serialize_swap_mode(cls, mode: JupiterSwapMode) -> str:
        return mode.value

    @property
    def input_amount(self) -> int:
        return int(self.input_amount_raw)

    @property
    def output_amount(self) -> int:
        return int(self.output_amount_raw)

    @property
    def other_amount_threshold(self) -> int:
        return int(self.other_amount_threshold_raw)

# classes used on GET "Quote/Program ID to Label" endpoint
class GetQuoteProgramIdLabelResponse(BaseModel):
    """
        Model representing the GET **Quote/Program ID to Label** 
        endpoint response from Jupiter API.
    """

    dexes: dict[str, str]
    """List of dexes with their program ID and label (public_key: name)."""

# classes used on POST "Swap" endpoint
# Body
class PostSwapPriorityLevelWithMaxLamports(BaseModel):
    """
        Model used to identify the priority level with max lamports.
    """

    priority_level: Literal["low", "medium", "high"] | None = Field(default = None, alias = "priorityLevel")
    """Priority level."""

    max_lamports: int | None = Field(default = None, alias = "maxLamports")
    """Maximum lamports to cap the priority fee estimation, to prevent overpaying."""

    global_flag: bool = Field(default = False, alias = "global")
    """A boolean to choose between using a global or local fee market to estimate.
        If global is set to false, the estimation focuses on fees relevant to the writable accounts involved in the instruction."""

class PostSwapPrioritizationFeeLamports(BaseModel):
    """
        Model used to identify the prioritization fee lamports.
    """
    priority_level_with_max_lamports: PostSwapPriorityLevelWithMaxLamports | None = Field(default = None, alias = "priorityLevelWithMaxLamports")
    """Priority level with max lamports."""

    jito_tip_lamports: int | None = Field(default = None, alias = "jitoTipLamports")
    """Exact amount of tip to use in a tip instruction.  
        Estimate how much to set using Jito tip percentiles endpoint.  
        It has to be used together with a connection to a Jito RPC"""

class PostSwapBody(BaseModel):
    """
        Model used to identify the body required by a POST **Swap** request.
    """

    user_public_key: str = Field(serialization_alias = "userPublicKey")
    """Public Key of the User wallet"""

    quote_response: GetQuoteResponse = Field(serialization_alias = "quoteResponse")
    """The quote response object from the quote endpoint."""

    wrap_unwrap_sol: bool = Field(default = True, serialization_alias = "wrapAndUnwrapSol")
    """To automatically wrap/unwrap SOL in the transaction.  
        Parameter will be ignored if `destination_token_account` is set because it may belong to a 
        different user that Jupiter has no authority to close."""

    use_shared_accounts: bool= Field(default = True, serialization_alias = "useSharedAccounts")
    """This enables the usage of shared program accounts, it is essential as complex routing 
        will require multiple intermediate token accounts which the user might not have."""

    fee_account: str | None = Field(default = None, serialization_alias = "feeAccount")
    """An associated Token Address (ATA) of specific mints depending on SwapMode to collect fees."""

    tracking_account: str | None = Field(default = None, serialization_alias = "trackingAccount")
    """Specify any public key that belongs to you to track the transactions.  
        Useful for integrators to get all the swap transactions from this public key."""

    compute_unit_price_micro_lamports: int | None = Field(default = None, serialization_alias = "computeUnitPriceMicroLamports")
    """This number is used to specify a compute unit price to calculate priority fee; 
        `computeUnitLimit` (1400000) * `compute_unit_price_micro_lamports`.  
        Jupiter recommends using `prioritization_fee_lamports` and `dynamic_compute_unit_limit` instead of passing in a compute unit price."""

    prioritization_fee_lamports: PostSwapPrioritizationFeeLamports | None = Field(default = None, serialization_alias = "prioritizationFeeLamports")
    """This object is used to specify a level or amount of additional fees to prioritize the transaction.
        It can be used for EITHER priority fee OR Jito tip."""

    as_legacy_transaction: bool = Field(default = False, serialization_alias = "asLegacyTransaction")
    """Request a legacy transaction rather than the default versioned transaction.  
        Used together with `GetQuoteParams.as_legacy_transaction` in quote, otherwise the transaction might be too large."""

    destination_token_account: str | None = Field(default = None, serialization_alias = "destinationTokenAccount")
    """Public key of a token account that will be used to receive the token out of the swap.  
        If not provided, the signer's ATA will be used. If provided, Jupiter assumes that the token account is already initialized."""

    dynamic_compute_unit_limit: bool = Field(default = False, serialization_alias = "dynamicComputeUnitLimit")
    """When enabled, it will do a swap simulation to get the compute unit used and set it in ComputeBudget's compute unit limit.  
        This will increase latency slightly since there will be one extra RPC call to simulate this.  
        This can be useful to estimate compute unit correctly and reduce priority fees needed or have higher chance to be included in a block."""

    skip_user_accounts_rpc_calls: bool = Field(default = False, serialization_alias = "skipUserAccountsRpcCalls")
    """When enabled, it will not do any additional RPC calls to check on user's accounts.  
        Enable it only when you already setup all the accounts needed for the trasaction, 
        like wrapping or unwrapping sol, or destination account is already created."""

    dynamic_slippage: bool = Field(default = False, serialization_alias = "dynamicSlippage")
    """When enabled, it estimates slippage and apply it in the swap transaction directly, 
        overwriting the `GetQuoteResponse.slippage_base_points` parameter in the quote response."""

    compute_unit_price_micro_lamports: int | None = Field(default = None, serialization_alias = "computeUnitPriceMicroLamports")
    """To use an exact compute unit price to calculate priority fee: `computeUnitLimit (1400000) * computeUnitPriceMicroLamports`.  
        It is recommended using `prioritizationFeeLamports` and `dynamicComputeUnitLimit` instead of passing in your own compute unit price."""

    blockhash_slots_to_expiry: int | None = Field(default = None, serialization_alias = "blockhashSlotsToExpiry")
    """Number of slots until the blockhash expires.  
        Example: If you pass in 10 slots, the transaction will be valid for ~400ms * 10 = approximately 4 seconds before it expires."""

# Output
class PostSwapResponse(BaseModel):
    """
        Model representing the POST **Swap** endpoint 
        response from Jupiter API.
    """

    swap_transaction: str = Field(alias = "swapTransaction")
    """Base-64 encoded transaction."""

    last_valid_block_height: int = Field(alias = "lastValidBlockHeight")
    """Last valid block height for the transaction."""

    prioritization_fee_lamports: int = Field(default = 0, alias = "prioritizationFeeLamports")
    """Amount of prioritization fee in lamports."""

# Output (Instructions)
class PostSwapAccount(BaseModel):
    """Model describing a generic account in the swap transaction."""

    public_key: str = Field(alias = "pubkey")
    """Public key of the account."""

    is_signer: bool = Field(alias = "isSigner")
    """Flag indicating if the account is a signer."""

    is_writable: bool = Field(alias = "isWritable")
    """Flag indicating if the account is writable."""

class PostSwapInstruction(BaseModel):
    """Model describing a generic instruction in the swap transaction."""

    program_id: str = Field(alias = "programId")
    """Program ID of the instruction."""

    accounts: list[PostSwapAccount]
    """List of accounts used in the instruction."""

    data: str
    """Data of the instruction."""

class PostSwapInstructionsResponse(BaseModel):
    """
        Model used to represent the **Swap Instructions** endpoint response from 
        Jupiter API in the case of instructions are requested.
    """

    swap: PostSwapInstruction = Field(alias = "swapInstruction")
    """Swap instruction."""

    setup: list[PostSwapInstruction] = Field(alias = "setupInstructions")
    """Setup instructions."""

    compute_budget: list[PostSwapInstruction] = Field(alias = "computeBudgetInstructions")
    """Compute budget instructions."""

    cleanup: PostSwapInstruction | None = Field(default = None, alias = "cleanupInstruction")
    """Cleanup instruction."""

    other: list[PostSwapInstruction] | None = Field(default = None, alias = "otherInstructions")
    """Other instructions."""

    address_lookup_table_addresses: list[str] = Field(alias = "addressLookupTableAddresses")
    """Address lookup table addresses."""

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

# *************
# * Ultra API *
# *************

# classes used on GET "Ultra - Order" endpoint
class GetUltraOrderDynamicSlippageReport(BaseModel):
    """
        Model used to represent the **Ultra - Order** endpoint dynamic slippage report from Jupiter API.
    """
    amplification_ratio: str | None = Field(default = None, alias = "amplificationRatio")
    other_amount: int | None = Field(default = None, alias = "otherAmount")
    simulated_incurred_slippage_base_points: int | None = Field(default = None, alias = "simulatedIncurredSlippageBps")
    slippage_base_points: int = Field(alias = "slippageBps")
    """
        Amount of slippage the order can be executed with.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    category_name: str = Field(alias = "categoryName")
    heuristic_max_slippage_base_points: int = Field(alias = "heuristicMaxSlippageBps")

class GetUltraOrderPlatformFee(GetQuotePlatformFees):
    pass

class GetUltraOrderRoutePlan(GetQuoteRoutePlan):
    pass

class GetUltraOrderBody(BaseModel):
    """
        Model refering to the body schema of the GET
        "**Ultra - Order**" endpoint from Jupiter API.
    """

    input_token: str = Field(serialization_alias = "inputMint")
    """Address of the input token."""

    output_token: str = Field(serialization_alias = "outputMint")
    """Address of the output token."""

    input_amount: int = Field(serialization_alias = "amount")
    """
        Amount of input token to swap.
        The amount to swap **must** be factored in the token decimals. 
        For example, if the token has 6 decimals, then `1.0` = `1_000_000`.
    """

    taker_wallet_key: str = Field(default = "vBXNsd5SRtTPpW7GWv3wREA6Ztm2jCWp5eqqTsVhyG5", serialization_alias = "taker")
    """
        Address of the taker wallet. 
        If the `taker_wallet_key` is not provided, then the response will have `transaction_id` equals `None`.
    """

    receiver: str | None = None
    """
        The public key of the account that will receive the output tokens.
        If not provided, the output tokens will be sent to the taker.
    """

    payer: str | None = None
    """
        The public key of an account that will be used to cover gas-related fees on behalf of the taker.
        When `payer` is passed in, `close_authority` is required.
    """

    close_authority: str | None = Field(default = None, serialization_alias = "closeAuthority")
    """
        The public key of an account to set as the close authority of ATAs created during the swap.
        When `payer` is passed in, `close_authority` is required.
    """

    referral_account: str | None = Field(default = None, serialization_alias = "referralAccount")
    """Referral account address for integrator fees."""

    referral_fee: int | None = Field(default = None, serialization_alias = "referralFee")
    """Referral fee in basis points. Required range: 50 <= x <= 255."""

    exclude_routers: list[JupiterRouter] | None = Field(default = None, serialization_alias = "excludeRouters")
    """List of routers to exclude from the swap. Available options: `iris`, `jupiterz`, `dflow`, `okx`."""

    exclude_dexes: str | None = Field(default = None, serialization_alias = "excludeDexes")
    """
        Comma-separated list of DEXes to exclude (e.g., "Raydium,Orca V2,Meteora DLMM").
        This only excludes DEXes on the Iris router.
    """

    @field_serializer("input_amount")
    @classmethod
    def serialize_input_amount(cls, amount: int) -> str:
        return str(amount)
    
    @field_validator("exclude_routers")
    @classmethod
    def validator_exclude_routers(cls, routers: list[JupiterRouter]) -> list[str]:
        return [router.value for router in routers]

class GetUltraOrderResponse(BaseModel):
    """
        Model refering to the response schema of the GET
        "**Ultra - Order**" endpoint from Jupiter API.
    """

    mode: str
    """Mode of the order."""

    input_token: str = Field(alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    output_token: str = Field(alias = "outputMint")
    """The address of the output token on the chain that will bought."""

    input_amount_raw: int = Field(alias = "inAmount")
    """Raw amount of input token to use to buy (before decimals)."""

    output_amount_raw: int = Field(alias = "outAmount")
    """Raw amount of output token to buy (before decimals)."""

    other_amount_threshold_raw: int = Field(alias = "otherAmountThreshold")
    """Raw calculated minimum output amount after accounting for `slippage_base_points` and `platform_fees` (before decimals)."""

    swap_mode: JupiterSwapMode = Field(alias = "swapMode")
    """Mode of the swap."""

    slippage_base_points: int = Field(alias = "slippageBps")
    """
        Amount of slippage the order can be executed with.  
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    price_impact_percent: float = Field(alias = "priceImpactPct")
    """Percentage of price impact for the swap (deprecated, use price_impact instead)."""

    route_plan: list[GetUltraOrderRoutePlan] = Field(alias = "routePlan")
    """List of route plans for the swap."""

    fee_base_points: int = Field(alias = "feeBps")
    """
        Amount of fee that the `referral_public_key` collects.
        **1%** = `100`, **50%** = `5_000`, **100%** = `10_000`.
    """

    platform_fee: GetUltraOrderPlatformFee = Field(alias = "platformFee")
    """Platform fees for the swap."""

    signature_fee_lamports: int = Field(alias = "signatureFeeLamports")
    """The number of lamports the taker, maker or payer has to pay for the base network fee."""

    signature_fee_payer: str | None = Field(default = None, alias = "signatureFeePayer")
    """The public key of the account that will cover the signature fee."""

    prioritization_fee_lamports: int = Field(alias = "prioritizationFeeLamports")
    """The number of lamports the taker, maker or payer has to pay for higher priority landing."""

    prioritization_fee_payer: str | None = Field(default = None, alias = "prioritizationFeePayer")
    """The public key of the account that will cover the prioritization fee."""

    rent_fee_lamports: int = Field(alias = "rentFeeLamports")
    """The number of lamports the taker or payer has to pay for account rent."""

    rent_fee_payer: str | None = Field(default = None, alias = "rentFeePayer")
    """The public key of the account that will cover the rent fee."""

    swap_type: str = Field(default = "", alias = "swapType")
    """Type of the swap (deprecated, in favour of router)."""

    router: JupiterRouter = Field(alias = "router")
    """Router used for the swap."""

    transaction_id: str | None = Field(default = None, alias = "transaction")
    """Base-64 encoded transaction."""

    gasless: bool
    """Flag indicating if the order is gasless."""

    request_id: str = Field(alias = "requestId")
    """Unique ID required to make a request to `post_ultra_execute`."""

    total_time: int = Field(alias = "totalTime")
    """Total time taken to process the request."""

    taker_wallet_key: str | None = Field(default = None, alias = "taker")
    """Wallet address of the user who wants to create an order."""

    input_usd_value: float | None = Field(default = None, alias = "inUsdValue")
    """USD value of the input amount."""

    output_usd_value: float | None = Field(default = None, alias = "outUsdValue")
    """USD value of the output amount."""

    price_impact: float | None = Field(default = None, alias = "priceImpact")
    """Price impact of the swap."""

    swap_usd_value: float | None = Field(default = None, alias = "swapUsdValue")
    """USD value of the swap."""

    referral_account: str | None = Field(default = None, alias = "referralAccount")
    """Referral account address."""

    fee_mint: str | None = Field(default = None, alias = "feeMint")
    """Token mint address for the fee."""

    quote_id: str | None = Field(default = None, alias = "quoteId")
    """Unique ID of the quote."""

    maker_wallet_key: str | None = Field(default = None, alias = "maker")
    """Wallet address of the maker."""

    expire_at: str | None = Field(default = None, alias = "expireAt")
    """Expiration time for the order."""

    error_code: int | None = Field(default = None, alias = "errorCode")
    """Error code if transaction field is empty."""

    error_message: str | None = Field(default = None, alias = "errorMessage")
    """Error message if transaction field is empty."""

    @field_serializer("swap_mode")
    @classmethod
    def serialize_swap_mode(cls, mode: JupiterSwapMode) -> str:
        return mode.value

# classes used on POST "Ultra - Execute Order" endpoint
class PostUltraExecuteOrderSwapEvent(BaseModel):
    """
        Model refering to the schema of a swap event in the POST 
        "**Ultra - Execute Order**" endpoint from Jupiter API.
    """

    input_token: str = Field(alias = "inputMint")
    """Input token address."""

    input_amount_raw: int = Field(alias = "inputAmount")
    """Raw amount of input token used to buy (before decimals)."""

    output_token: str = Field(alias = "outputMint")
    """Output token address."""

    output_amount_raw: int = Field(alias = "outputAmount")
    """Raw amount of output token bought (before decimals)."""

class PostUltraExecuteOrderResponse(BaseModel):
    """
        Model refering to the response schema of the POST 
        "**Ultra - Execute Order**" endpoint from Jupiter API.
    """

    status: JupiterSwapExecutionStatus
    """Status of the order."""

    code: int
    """Code indicating the status of the operation."""

    signature_transaction_id: str | None = Field(default = None, alias = "signature")
    """Signature of the successful transaction."""

    slot: int | None = None
    """Slot number of the transaction."""

    input_amount_result_raw: int | None = Field(default = None, alias = "inputAmountResult")
    """Raw amount of input token used to buy (before decimals)."""

    total_input_amount_raw: int | None = Field(default = None, alias = "totalInputAmount")
    """Raw total amount of input token used to buy (before decimals)."""

    output_amount_result_raw: int | None = Field(default = None, alias = "outputAmountResult")
    """Raw amount of output token bought (before decimals)."""

    total_output_amount_raw: int | None = Field(default = None, alias = "totalOutputAmount")
    """Raw total amount of output token bought (before decimals)."""

    swap_events: PostUltraExecuteOrderSwapEvent | None = Field(default = None, alias = "swapEvents")
    """List of swap events."""

    error: str | None = None
    """Error message in case of failure."""

# classes used on GET "Ultra - Holdings" endpoint
class GetUltraHoldingsToken(BaseModel):
    """
        Model representing a specific token holding coming 
        from the GET "**Ultra - Holdings**" endpoint of Jupiter API.
    """

    address: str = Field(alias = "account")
    """The token account address."""

    amount_raw: str = Field(alias = "amount")
    """Amount of the token in raw format as string; i.e., lamports for SOL."""

    amount: float = Field(alias = "uiAmount")
    """Amount of the token in UI units after applying decimals."""

    amount_string: str = Field(alias = "uiAmountString")
    """Amount of the token as string in UI units after applying decimals."""

    is_frozen: bool = Field(alias = "isFrozen")
    """Flag indicating if the token account is frozen."""

    is_associated_token_account: bool = Field(alias = "isAssociatedTokenAccount")
    """Flag indicating if this is an associated token account."""

    decimals: int
    """Number of decimal places for the token."""

    program_id: str = Field(alias = "programId")
    """The token program ID."""

    exclude_from_net_worth: bool | None = Field(default = None, alias = "excludeFromNetWorth")
    """Flag indicating if the token should be excluded from net worth calculations."""

class GetUltraHoldingsResponse(BaseModel):
    """
        Model representing the response object from the 
        GET "**Ultra - Holdings**" endpoint from Jupiter API.
    """

    amount_raw: str = Field(alias = "amount")
    """Total SOL in lamports as string."""

    amount: float = Field(alias = "uiAmount")
    """Total SOL in UI units after applying decimals."""

    amount_string: str = Field(alias = "uiAmountString")
    """Total SOL as string in UI units after applying decimals."""

    tokens: dict[str, list[GetUltraHoldingsToken]]
    """Other token holdings organized by mint address as keys."""

# classes used on GET "Ultra - Shield" endpoint
class GetUltraShieldWarning(BaseModel):
    """
        Model representing a specific warning for a token mint 
        from the GET "**Ultra - Shield**" endpoint of Jupiter API.
    """

    type: str
    """
        Type of warning for the token.  
        See [`JupiterShieldWarningType`][cyhole.jupiter.param.JupiterShieldWarningType] for all the supported types.
    """

    message: str
    """Human-readable warning message."""

    severity: str
    """
        Severity level of the warning.  
        See [`JupiterShieldWarningSeverity`][cyhole.jupiter.param.JupiterShieldWarningSeverity] for all the supported severity levels.
    """

    source: str | None = None
    """
        Optional external source of the warning.  
        See [`JupiterShieldWarningSource`][cyhole.jupiter.param.JupiterShieldWarningSource] for all the supported sources.
    """

    @field_validator("type")
    @classmethod
    def validator_type(cls, warning_type: str) -> str:
        JupiterShieldWarningType.check(warning_type)
        return warning_type

    @field_validator("severity")
    @classmethod
    def validator_severity(cls, severity: str) -> str:
        JupiterShieldWarningSeverity.check(severity)
        return severity

    @field_validator("source")
    @classmethod
    def validator_source(cls, source: str | None) -> str | None:
        if source is not None:
            JupiterShieldWarningSource.check(source)
        return source

class GetUltraShieldResponse(BaseModel):
    """
        Model representing the response object from the 
        GET "**Ultra - Shield**" endpoint from Jupiter API.
    """

    warnings: dict[str, list[GetUltraShieldWarning]]
    """Dictionary containing lists of warnings for each mint address as keys."""

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

# classes used on POST "Recurring - Withdraw Price" endpoint
class PostRecurringWithdrawPriceResponse(PostRecurringTransactionResponse):
    """
        Model refering to the response schema of the POST 
        "**Recurring - Withdraw Price**" endpoint from Jupiter API.
    """
    pass

# classes used on POST "Recurring - Deposit Price" endpoint
class PostRecurringDepositPriceResponse(PostRecurringTransactionResponse):
    """
        Model refering to the response schema of the POST 
        "**Recurring - Deposit Price**" endpoint from Jupiter API.
    """
    pass

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