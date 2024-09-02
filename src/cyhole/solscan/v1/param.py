from ...core.param import CyholeParam

class SolscanExportType(CyholeParam):
    """
        Enum class to get the supported Solscan's exporting types.
    """
    TOKEN_CHANGE = "tokenchange"
    """Export only token changes."""
    SOL_TRANSFER = "soltransfer"
    """Export only Solana transfers."""
    ALL = "all"
    """Export all types of transactions."""

class SolscanSort(CyholeParam):
    """
        Enum class to get the supported Solscan's sorting types.
    """
    MARKET_CAP = "market_cap"
    """Sort the results by Market Cap (MC)"""
    VOLUME = "volume"
    """Sort the results by USD Volume in the last 24h"""
    HOLDER = "holder"
    """Sort the results by the number of holders"""
    PRICE = "price"
    """Sort the results by the price"""
    PRICE_CHANGE_24H = "price_change_24h"
    """Sort the results by percent changing in the last 24h"""
    PRICE_CHANGE_7D = "price_change_7d"
    """Sort the results by percent changing in the last 7d"""
    PRICE_CHANGE_14D = "price_change_14d"
    """Sort the results by percent changing in the last 14d"""
    PRICE_CHANGE_30D = "price_change_30d"
    """Sort the results by percent changing in the last 30d"""
    PRICE_CHANGE_60D = "price_change_60d"
    """Sort the results by percent changing in the last 60d"""
    PRICE_CHANGE_200D = "price_change_200d"
    """Sort the results by percent changing in the last 200d"""
    PRICE_CHANGE_1Y = "price_change_1y"
    """Sort the results by percent changing in the last 1y"""

class SolscanOrder(CyholeParam):
    """
        Enum class to get the supported Solscan's orders.
    """
    ASCENDING = "asc"
    """Ascending sort order."""
    DESCENDING = "desc"
    """Descending sort order."""