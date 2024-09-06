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

class SolscanFlowType(CyholeParam):
    """
        Enum class to get the supported Solscan's flow types.
    """
    INCOMING = "in"
    """Export only incoming transactions."""
    OUTGOING = "out"
    """Export only outgoing transactions."""