from datetime import datetime

from pydantic import BaseModel, Field, field_validator, field_serializer

from ..jupiter.param import JupiterSwapMode, JupiterSwapDex, JupiterLimitOrderState

# class used on Jupiter HTTPErrors
class JupiterHTTPError(BaseModel):
    """
        Jupiter API returns an error schema on failed request 
        that can be used to investigated the error. This schema 
        is used to strandardise the HTTPErrors.
    """
    code: str = Field(alias = "errorCode")
    msg: str = Field(alias = "error")

# classes used on GET "Price" endpoint
class GetPriceData(BaseModel):
    id: str
    mint_symbol: str = Field(alias = "mintSymbol")
    vs_token: str = Field(alias = "vsToken")
    vs_token_symbol: str = Field(alias = "vsTokenSymbol")
    price: float

class GetPriceResponse(BaseModel):
    """
        Model used to represent the **Price** endpoint from Jupiter API.
    """
    data: dict[str, GetPriceData]
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
    """The amount to swap, factoring in the token decimals."""

    slippage_base_points: int = Field(default = 50, serialization_alias = "slippageBps")
    """Slippage tolerance in basis points (the default is used unless `auto_slippage` is set to `True`).  
        Observe that if the slippage exeeded this value, then the swap will fail."""

    swap_mode: str = Field(default = JupiterSwapMode.EXACT_IN.value, serialization_alias = "swapMode")
    """Define if the slippage is on the input or output token."""

    dexes: list[str] | None = None
    """List of DEXes to include; by default, all the DEXes are included.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    exclude_dexes: list[str] | None = Field(default = None, serialization_alias = "excludeDexes")
    """List of DEXes to exclude.  
        See [`JupiterSwapDex`][cyhole.jupiter.param.JupiterSwapDex] for all the supported DEXs"""

    restrict_intermediate_tokens: bool | None = Field(default = None, serialization_alias = "restrictIntermediateTokens")
    """Restrict to a top token set for stable liquidity."""

    only_direct_routes: bool = Field(default = False, serialization_alias = "onlyDirectRoutes")
    """Limit to single hop routes only."""

    as_legacy_transaction: bool = Field(default = False, serialization_alias = "asLegacyTransaction")
    """Use legacy transactions instead of versioned ones."""

    platform_fee_base_points: int | None = Field(default = None, serialization_alias = "platformFeeBps")
    """Fee to charge. The value is in percent and taken from output token."""

    max_accounts: int | None = Field(default = None, serialization_alias = "maxAccounts")
    """Max accounts to be used for the quote."""

    auto_slippage: bool = Field(default = False, serialization_alias = "autoSlippage")
    """Enable smart/auto slippage proposed by API."""

    max_auto_slippage_base_points: int | None = Field(default = None, serialization_alias = "maxAutoSlippageBps")
    """Max slippage for smart/auto slippage."""

    auto_slippage_collision_usd_value: int | None = Field(default = None, serialization_alias = "autoSlippageCollisionUsdValue")
    """Custom USD value for calculating slippage impact.  
        By default, the API sets 1000 USD if `auto_slippage` is set to `True`."""

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

# classes used on GET "Quote/Token" endpoint
class GetQuoteTokensResponse(BaseModel):
    """
        Model used to represent the **Quote/Token** endpoint from Jupiter API.
    """
    tokens: list[str]

# classes used on GET "Quote/Program ID to Label" endpoint
class GetQuoteProgramIdLabelResponse(BaseModel):
    """
        Model used to represent the **Quote/Program ID to Label** endpoint from Jupiter API.
    """
    dexes: dict[str, str]

# classes used on POST "Swap" endpoint
# Body
class PostSwapBody(BaseModel):
    """
        Model used to identify the body required by a POST **Swap** request.
    """
    user_public_key: str = Field(serialization_alias = "userPublicKey")
    wrap_unwrap_sol: bool = Field(default = None, serialization_alias = "wrapAndUnwrapSol")
    use_shared_accounts: bool= Field(default = None, serialization_alias = "useSharedAccounts")
    fee_account: str = Field(default = None, serialization_alias = "feeAccount")
    tracking_account: str = Field(default = None, serialization_alias = "trackingAccount")
    compute_unit_price_micro_lamports: int = Field(default = None, serialization_alias = "computeUnitPriceMicroLamports")
    prioritization_fee_lamports: int = Field(default = None, serialization_alias = "prioritizationFeeLamports")
    as_legacy_transaction: bool = Field(default = None, serialization_alias = "asLegacyTransaction")
    use_token_ledger: bool = Field(default = None, serialization_alias = "useTokenLedger")
    destination_token_account: str = Field(default = None, serialization_alias = "destinationTokenAccount")
    dynamic_compute_unit_limit: bool = Field(default = None, serialization_alias = "dynamicComputeUnitLimit")
    skip_user_accounts_rpc_calls: bool = Field(default = None, serialization_alias = "skipUserAccountsRpcCalls")
    quote_response: GetQuoteResponse = Field(serialization_alias = "quoteResponse")

# Output
class PostSwapResponse(BaseModel):
    swap_transaction: str = Field(alias = "swapTransaction")
    last_valid_block_height: int = Field(alias = "lastValidBlockHeight")
    prioritization_fee_lamports: int = Field(default = 0, alias = "prioritizationFeeLamports")

# classes used on GET "Token List" endpoint
class GetTokenListToken(BaseModel):
    address: str
    chain_id: int = Field(alias = "chainId")
    decimals: int
    name: str
    symbol: str
    logo_uri: str = Field(alias = "logoURI")
    tags: list[str]
    extensions: dict[str, str] | None = None

class GetTokenListResponse(BaseModel):
    """
        Model used to represent the **Token List** endpoint from Jupiter API.
    """
    tokens: list[GetTokenListToken]

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