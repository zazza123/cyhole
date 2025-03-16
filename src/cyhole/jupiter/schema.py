from datetime import datetime

from pydantic import BaseModel, Field, AliasChoices, field_validator, field_serializer

from ..jupiter.param import JupiterSwapMode, JupiterSwapDex, JupiterLimitOrderState

# class used on Jupiter HTTPErrors
class JupiterHTTPError(BaseModel):
    """
        Jupiter API returns an error schema on failed request 
        that can be used to investigated the error. This schema 
        is used to strandardise the HTTPErrors.
    """
    code: str = Field(validation_alias = AliasChoices("errorCode", "error_code"))
    msg: str = Field(alias = "error")

# classes used on GET "Price" endpoint
class GetPriceDepthValues(BaseModel):
    """Depth values."""

    amount_10_sol: float = Field(alias = "10")
    amount_100_sol: float = Field(alias = "100")
    amount_1000_sol: float = Field(alias = "1000")

class GetPriceDepthRatio(BaseModel):
    """Depth ratio information."""

    timestamp_unix: int = Field(alias = "timestamp")
    depth: GetPriceDepthValues

class GetPriceDepth(BaseModel):
    """Depth information."""

    buy_price_impact_ratio: GetPriceDepthRatio | None = Field(default = None, alias = "buyPriceImpactRatio")
    sell_price_impact_ratio: GetPriceDepthRatio | None = Field(default = None, alias = "sellPriceImpactRatio")

class GetPriceLastSwappedPrice(BaseModel):
    """Last swapped price information."""

    last_jupiter_sell_at_unix: int = Field(alias = "lastJupiterSellAt")
    last_jupiter_sell_price: str = Field(alias = "lastJupiterSellPrice")
    last_jupiter_buy_at_unix: int = Field(alias = "lastJupiterBuyAt")
    last_jupiter_buy_price: str = Field(alias = "lastJupiterBuyPrice")

class GetPriceQuotedPrice(BaseModel):
    """Last quoted price information."""

    buy_price: str = Field(alias = "buyPrice")
    buy_at_unix: int = Field(alias = "buyAt")
    sell_price: str | None = Field(default = None, alias = "sellPrice")
    sell_at_unix: int | None = Field(default = None, alias = "sellAt")

class GetPriceExtraInfo(BaseModel):
    """Extra information about the price."""

    last_swapped_price: GetPriceLastSwappedPrice | None = Field(default = None, alias = "lastSwappedPrice")
    quoted_price: GetPriceQuotedPrice = Field(alias = "quotedPrice")
    confidence_level: str = Field(alias = "confidenceLevel")
    depth: GetPriceDepth

class GetPriceData(BaseModel):
    id: str
    """Chain address of the token."""

    type: str
    """The type of the token."""

    price: str
    """The price of the token."""

    extra_info: None | GetPriceExtraInfo = Field(default = None, alias = "extraInfo")
    """Extra information about the price. Only available if request param `extra_info` is set to `True`."""

class GetPriceResponse(BaseModel):
    """
        Model used to represent the **Price** endpoint from Jupiter API.
    """
    data: dict[str, GetPriceData | None]
    time_taken: float = Field(alias = "timeTaken")

# classes used on GET "Quote" endpoint
# Input
class GetQuoteInput(BaseModel):
    """
        Model used to identify the inputs params required by 
        a GET Quote request.
    """

    input_token: str = Field(serialization_alias = "inputMint")
    """The address of the input token on the chain."""

    output_token: str = Field(serialization_alias = "outputMint")
    """The address of the output token on the chain."""

    amount: int
    """The amount to swap, factoring in the token decimals.
        For example, if the token has 6 decimals, then `1.0` = `1_000_000`."""

    slippage_base_points: int = Field(default = 50, serialization_alias = "slippageBps")
    """Slippage tolerance in basis points. Observe that if the slippage exeeded this value, then the swap will fail."""

    swap_mode: str = Field(default = JupiterSwapMode.EXACT_IN.value, serialization_alias = "swapMode")
    """Define if the slippage is on the input or output token."""

    dexes: list[str] | None = None
    """List of DEXes to include; by default, all the DEXes are included.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    exclude_dexes: list[str] | None = Field(default = None, serialization_alias = "excludeDexes")
    """List of DEXes to exclude.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    restrict_intermediate_tokens: bool | None = Field(default = None, serialization_alias = "restrictIntermediateTokens")
    """Restrict to a top token set for stable liquidity. This will help to reduce exposure to potential high slippage routes."""

    only_direct_routes: bool = Field(default = False, serialization_alias = "onlyDirectRoutes")
    """Limit to single hop routes only."""

    as_legacy_transaction: bool = Field(default = False, serialization_alias = "asLegacyTransaction")
    """Use legacy transactions instead of versioned ones."""

    platform_fee_base_points: int | None = Field(default = None, serialization_alias = "platformFeeBps")
    """Fee to charge. The value is in percent and taken from output token."""

    max_accounts: int | None = Field(default = None, serialization_alias = "maxAccounts")
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

    @field_validator("swap_mode")
    @classmethod
    def validator_swap_mode(cls, mode: str) -> str:
        JupiterSwapMode.check(mode)
        return mode

# Output
class GetQuotePlatformFees(BaseModel):
    amount: str
    fee_base_points: str = Field(alias = "feeBps")

class GetQuoteSwapInfo(BaseModel):
    amm_key: str = Field(alias = "ammKey")
    amm_label: str | None = Field(default = None, alias = "label")
    input_token: str = Field(alias = "inputMint")
    input_amount: str = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: str = Field(alias = "outAmount")
    fee_token: str = Field(alias = "feeMint")
    fee_amount: str = Field(alias = "feeAmount")

class GetQuoteRoutePlan(BaseModel):
    swap_info: GetQuoteSwapInfo = Field(alias = "swapInfo")
    percent: int

class GetQuoteResponse(BaseModel):
    """
        Model used to represent the **Quote** endpoint from Jupiter API.
    """
    input_token: str = Field(alias = "inputMint")
    input_amount: str = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: str = Field(alias = "outAmount")
    other_amount_threshold: str = Field(alias = "otherAmountThreshold")
    swap_mode: str = Field(alias = "swapMode")
    slippage_base_points: int = Field(alias = "slippageBps")
    platform_fees: GetQuotePlatformFees | None = Field(default = None, alias = "platformFee")
    price_impact_pct: str = Field(alias = "priceImpactPct")
    route_plan: list[GetQuoteRoutePlan] = Field(alias = "routePlan")
    context_slot: int = Field(alias = "contextSlot")
    time_taken: float = Field(alias = "timeTaken")

# classes used on GET "Quote/Program ID to Label" endpoint
class GetQuoteProgramIdLabelResponse(BaseModel):
    """
        Model used to represent the **Quote/Program ID to Label** endpoint from Jupiter API.
    """
    dexes: dict[str, str]

# classes used on POST "Swap" endpoint
# Body
class PostSwapPriorityLevelWithMaxLamports(BaseModel):
    """
        Model used to identify the priority level with max lamports.
    """
    priority_level: int = Field(default = None, alias = "priorityLevel")
    """Priority level."""

    max_lamports: int = Field(default = None, alias = "maxLamports")
    """Max lamports."""

class PostSwapPrioritizationFeeLamports(BaseModel):
    """
        Model used to identify the prioritization fee lamports.
    """
    priority_level_with_max_lamports: PostSwapPriorityLevelWithMaxLamports = Field(default = None, alias = "priorityLevelWithMaxLamports")
    """Priority level with max lamports."""

    jito_tip_lamports: int = Field(default = None, alias = "jitoTipLamports")
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
        different user that Jupitere has no authority to close."""

    use_shared_accounts: bool= Field(default = True, serialization_alias = "useSharedAccounts")
    """This enables the usage of shared program accounts, it is essential as complex routing 
        will require multiple intermediate token accounts which the user might not have."""

    fee_account: str = Field(default = None, serialization_alias = "feeAccount")
    """An Associated Token Address (ATA) of specific mints depending on SwapMode to collect fees."""

    tracking_account: str = Field(default = None, serialization_alias = "trackingAccount")
    """Specify any public key that belongs to you to track the transactions.  
        Useful for integrators to get all the swap transactions from this public key."""

    compute_unit_price_micro_lamports: int = Field(default = None, serialization_alias = "computeUnitPriceMicroLamports")
    """This number is used to specify a compute unit price to calculate priority fee; 
        `computeUnitLimit` (1400000) * `compute_unit_price_micro_lamports`.  
        Jupiter recommends using `prioritization_fee_lamports` and `dynamic_compute_unit_limit` instead of passing in a compute unit price."""

    prioritization_fee_lamports: PostSwapPrioritizationFeeLamports = Field(default = None, serialization_alias = "prioritizationFeeLamports")
    """This object is used to specify a level or amount of additional fees to prioritize the transaction.
        It can be used for EITHER priority fee OR Jito tip."""

    as_legacy_transaction: bool = Field(default = False, serialization_alias = "asLegacyTransaction")
    """Request a legacy transaction rather than the default versioned transaction.  
        Used together with `GetQuoteInput.as_legacy_transaction` in quote, otherwise the transaction might be too large."""

    destination_token_account: str = Field(default = None, serialization_alias = "destinationTokenAccount")
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

# Output
class PostSwapResponse(BaseModel):
    swap_transaction: str = Field(alias = "swapTransaction")
    last_valid_block_height: int = Field(alias = "lastValidBlockHeight")
    prioritization_fee_lamports: int = Field(default = 0, alias = "prioritizationFeeLamports")

# classes used on GET "Token Info" endpoint
class GetTokenInfoResponse(BaseModel):
    """
        Model used to represent the **Token** endpoint from Jupiter API
        focused on retrieving information about a token.
    """
    name: str
    address: str
    symbol: str
    decimals: int
    created_at: str
    logoURI: str | None = None
    tags: list[str] | None = None
    daily_volume: float | None = None
    freeze_authority: str | None = None
    mint_authority: str | None = None
    minted_at: str | None = None
    permanent_delegate: str | None = None
    extensions: dict[str, str] | None = None

# classes used on GET "Token Market Mints" endpoint
class GetTokenMarketMintsResponse(BaseModel):
    """
        Model used to represent the **Token Market Mints** endpoint from Jupiter API.
    """
    mints: list[str]

# classes used on GET "Token Tagged" endpoint
class GetTokenTaggedToken(GetTokenInfoResponse):
    pass

class GetTokenTaggedResponse(BaseModel):
    """
        Model used to represent the **Token Tagged** endpoint from Jupiter API.
    """
    tokens: list[GetTokenTaggedToken]

# classes used on GET "Token New" endpoint
class GetTokenNewToken(BaseModel):
    """Model used to represent a token information on the **Token New** endpoint."""
    mint: str
    name: str
    symbol: str
    decimals: int
    created_at: str
    known_markets: list[str]
    metadata_updated_at: int
    logo_uri: str | None = None
    mint_authority: str | None = None
    freeze_authority: str | None = None

class GetTokenNewResponse(BaseModel):
    """
        Model used to represent the **Token New** endpoint from Jupiter API.
    """
    tokens: list[GetTokenNewToken]

# classes used on POST "Limit Order Create" endpoint
# Body
class PostLimitOrderCreateBody(BaseModel):
    """
        Model used to identify the body required by a POST **Limit Order Create** request.
    """
    user_public_key: str = Field(serialization_alias = "owner")
    """Public Key of the Owner wallet"""

    input_token: str = Field(serialization_alias = "inputMint")
    """The address of the input token on the chain used to buy."""

    input_amount: int = Field(serialization_alias = "inAmount")
    """The amount of input token to use for the limit order."""

    output_token: str = Field(serialization_alias = "outputMint")
    """The address of the output token on the chain that will bought."""

    output_amount: int = Field(serialization_alias = "outAmount")
    """The amount of output token to buy in the limit order."""

    base: str
    """Public Key used to initiate the Limit Order"""

    expired_at_unix_time: int | None = Field(default = None, serialization_alias = "expiredAt")
    """Expiring date for the Limit Order expressed in UNIX time"""

    referral_public_key: str | None = Field(default = None, serialization_alias = "referralAccount")
    """The address of the account used to get referral fees."""

    referral_name: str | None = Field(default = None, serialization_alias = "referralName")

# Output
class PostLimitOrderCreateResponse(BaseModel):
    """
        Model used to represent the **Limit Order Create** endpoint from Jupiter API.
    """
    transaction: str = Field(alias = "tx")
    order_public_key: str = Field(alias = "orderPubkey")

# classes used on POST "Limit Order Cancel" endpoint
# Body
class PostLimitOrderCancelBody(BaseModel):
    """
        Model used to identify the body required by a POST **Limit Order Cancel** request.
    """
    user_public_key: str = Field(serialization_alias = "owner")
    """Public Key of the Owner wallet"""

    fee_payer_public_key: str = Field(serialization_alias = "feePayer")
    """Public Key of the fee payer."""

    orders: list[str]
    """List of orders Public Keys to cancel."""

# Output
class PostLimitOrderCancelResponse(BaseModel):
    """
        Model used to represent the **Limit Order Cancel** endpoint from Jupiter API.
    """
    transaction: str = Field(alias = "tx")

# classes used on GET "Limit Order Opens" endpoint
class GetLimitOrderOpenAccount(BaseModel):
    maker: str
    input_token: str = Field(alias = "inputMint")
    input_amount: str = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: str = Field(alias = "outAmount")
    ori_input_token: str = Field(alias = "oriInAmount")
    ori_output_amount: str = Field(alias = "oriOutAmount")
    expired_at_unix_time: int | None = Field(default = None, alias = "expiredAt")
    base: str

class GetLimitOrderOpen(BaseModel):
    public_key: str = Field(alias = "publicKey")
    account: GetLimitOrderOpenAccount

class GetLimitOrderOpenResponse(BaseModel):
    """
        Model used to represent the **Limit Order Opens** endpoint from Jupiter API.
    """
    orders: list[GetLimitOrderOpen]

# classes used on GET "Limit Order History" endpoint
class GetLimitOrderHistory(BaseModel):
    id: int
    maker: str
    order_key: str = Field(alias = "orderKey")
    input_token: str = Field(alias = "inputMint")
    input_amount: str = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: str = Field(alias = "outAmount")
    ori_input_token: str = Field(alias = "oriInAmount")
    ori_output_amount: str = Field(alias = "oriOutAmount")
    expired_at_unix_time: int | None = Field(default = None, alias = "expiredAt")
    state: str
    create_transaction_id: str = Field(alias = "createTxid")
    cancel_transaction_id: str | None = Field(default = None, alias = "cancelTxid")
    updated_at: datetime = Field(alias = "updatedAt")
    created_at: datetime = Field(alias = "createdAt")

    @field_validator("created_at", "updated_at")
    def parse_datetime(cls, datetime_raw: str | datetime) -> datetime:
        if isinstance(datetime_raw, str):
            return datetime.strptime(datetime_raw, "%Y-%m-%dT%H:%M:%S")
        return datetime_raw

    @field_validator("state")
    @classmethod
    def validator_state(cls, state: str) -> str:
        JupiterLimitOrderState.check(state)
        return state

class GetLimitOrderHistoryResponse(BaseModel):
    """
        Model used to represent the **Limit Order History** endpoint from Jupiter API.
    """
    orders: list[GetLimitOrderHistory]

# classes used on GET "Limit Order Trade History" endpoint
class GetLimitOrderTradeHistoryOrder(BaseModel):
    id: int
    order_key: str = Field(alias = "orderKey")
    input_token: str = Field(alias = "inputMint")
    output_token: str = Field(alias = "outputMint")

class GetLimitOrderTradeHistory(BaseModel):
    id: int
    input_amount: str = Field(alias = "inAmount")
    output_amount: str = Field(alias = "outAmount")
    transaction_id: str = Field(alias = "txid")
    updated_at: datetime = Field(alias = "updatedAt")
    created_at: datetime = Field(alias = "createdAt")
    order: GetLimitOrderTradeHistoryOrder

    @field_validator("created_at", "updated_at")
    def parse_datetime(cls, datetime_raw: str | datetime) -> datetime:
        if isinstance(datetime_raw, str):
            return datetime.strptime(datetime_raw, "%Y-%m-%dT%H:%M:%S")
        return datetime_raw

class GetLimitOrderTradeHistoryResponse(BaseModel):
    """
        Model used to represent the **Limit Order Trade History** endpoint from Jupiter API.
    """
    orders: list[GetLimitOrderTradeHistory]