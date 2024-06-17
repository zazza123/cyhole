from pydantic import BaseModel, Field, field_validator, field_serializer

from ..jupiter.param import JupiterSwapMode, JupiterSwapDex

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
    amount: float
    fee_base_points: str = Field(alias = "feeBps")

class GetQuoteSwapInfo(BaseModel):
    amm_key: str = Field(alias = "ammKey")
    amm_label: str | None = Field(default = None, alias = "label")
    input_token: str = Field(alias = "inputMint")
    input_amount: float = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: float = Field(alias = "outAmount")
    fee_token: str = Field(alias = "feeMint")
    fee_amount: float = Field(alias = "feeAmount")

class GetQuoteRoutePlan(BaseModel):
    swap_info: GetQuoteSwapInfo = Field(alias = "swapInfo")
    percent: int

class GetQuoteResponse(BaseModel):
    """
        Model used to represent the **Quote** endpoint from Jupiter API.
    """
    input_token: str = Field(alias = "inputMint")
    input_amount: float = Field(alias = "inAmount")
    output_token: str = Field(alias = "outputMint")
    output_amount: float = Field(alias = "outAmount")
    other_amount_threshold: float = Field(alias = "otherAmountThreshold")
    swap_mode: str = Field(alias = "swapMode")
    slippage_base_points: int = Field(alias = "slippageBps")
    platform_fees: GetQuotePlatformFees | None = Field(alias = "platformFee")
    price_impact_pct: float = Field(alias = "priceImpactPct")
    route_plan: list[GetQuoteRoutePlan] = Field(alias = "routePlan")
    context_slot: float = Field(alias = "contextSlot")
    time_taken: float = Field(alias = "timeTaken")