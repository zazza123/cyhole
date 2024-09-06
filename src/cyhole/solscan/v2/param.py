from ...core.param import CyholeParam

class SolscanActivityTransferType(CyholeParam):
    """
        Enum class to get the supported Solscan's transfters activities types.
    """
    SPL_TRANSFER = "ACTIVITY_SPL_TRANSFER"
    """Export only SPL transfers."""
    SPL_BURN = "ACTIVITY_SPL_BURN"
    """Export only SPL burns."""
    SPL_MINT = "ACTIVITY_SPL_MINT"
    """Export only SPL mints."""
    SPL_CREATE_ACCOUNT = "ACTIVITY_SPL_CREATE_ACCOUNT"
    """Export only SPL create account."""

class SolscanPageSizeType(CyholeParam):
    """
        Enum class to get the supported Solscan's page size types.
    """
    SIZE_10 = 10
    """Export only 10 items per page."""
    SIZE_20 = 20
    """Export only 20 items per page."""
    SIZE_30 = 30
    """Export only 30 items per page."""
    SIZE_40 = 40
    """Export only 40 items per page."""
    SIZE_60 = 60
    """Export only 60 items per page."""
    SIZE_100 = 100
    """Export only 100 items per page."""

class SolscanReturnLimitType(CyholeParam):
    """
        Enum class to get the supported Solscan's return limit types.
    """
    LIMIT_10 = 10
    """Export only 10 items."""
    LIMIT_20 = 20
    """Export only 20 items."""
    LIMIT_30 = 30
    """Export only 30 items."""
    LIMIT_40 = 40
    """Export only 40 items."""

class SolscanFlowType(CyholeParam):
    """
        Enum class to get the supported Solscan's flow types.
    """
    INCOMING = "in"
    """Export only incoming transactions."""
    OUTGOING = "out"
    """Export only outgoing transactions."""

class SolscanAccountType(CyholeParam):
    """
        Enum class to get the supported Solscan's account types.
    """
    NFT = "nft"
    """Export only NFT accounts."""
    TOKEN = "token"
    """Export only token accounts."""

class SolscanActivityDefiType(CyholeParam):
    """
        Enum class to get the supported Solscan's DeFi activities types.
    """
    TOKEN_SWAP = "ACTIVITY_TOKEN_SWAP"
    """Export only token swaps."""
    AGG_TOKEN_SWAP = "ACTIVITY_AGG_TOKEN_SWAP"
    """Export only aggregated token swaps."""
    TOKEN_ADD_LIQ = "ACTIVITY_TOKEN_ADD_LIQ"
    """Export only token add liquidity."""
    TOKEN_REMOVE_LIQ = "ACTIVITY_TOKEN_REMOVE_LIQ"
    """Export only token remove liquidity."""
    SPL_TOKEN_STAKE = "ACTIVITY_SPL_TOKEN_STAKE"
    """Export only SPL token stakes."""
    SPL_TOKEN_UNSTAKE = "ACTIVITY_SPL_TOKEN_UNSTAKE"
    """Export only SPL token unstakes."""
    SPL_TOKEN_WITHDRAW_STAKE = "ACTIVITY_SPL_TOKEN_WITHDRAW_STAKE"
    """Export only SPL token withdraw stakes."""