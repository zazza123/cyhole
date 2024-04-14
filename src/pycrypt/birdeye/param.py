from enum import Enum

class BirdeyeChain(Enum):
    """
        Enum class to get the supported Birdeye's chains.
    """
    SOLANA = "solana"
    """Identifier of the Solana chain in Birdeye API."""
    ETHEREUM = "ethereum"
    """Identifier of the Ethereum chain in Birdeye API."""
    ARBITRUM = "arbitrum"
    """Identifier of the Arbitrum chain in Birdeye API."""
    AVALANCHE = "avalanche"
    """Identifier of the Avalanche chain in Birdeye API."""
    BSC = "bsc"
    """Identifier of the BSC (Binance Smart Chain) chain in Birdeye API."""
    OPTIMISM = "optimism"
    """Identifier of the Optimism chain in Birdeye API."""
    POLYGON = "polygon"
    """Identifier of the Polygon chain in Birdeye API."""
    BASE = "base"
    """Identifier of the Base chain in Birdeye API."""
    ZKSYNC = "zksync"
    """Identifier of the zkSync chain in Birdeye API."""

class BirdeyeOrder(Enum):
    """
        Enum class to get the supported Birdeye's orders.
    """
    ASCENDING = "asc"
    """Ascending sort order."""
    DESCENDING = "desc"
    """Descending sort order."""

class BirdeyeSort(Enum):
    """
        Enum class to get the supported Birdeye's sorting types.
    """
    SORT_MC = "mc"
    """Sort the results by Market Cap (MC)"""
    SORT_V24HUSD = "v24hUSD"
    """Sort the results by USD Volume in the last 24h"""
    SORT_V24HCHANGEPERCENT = "v24hChangePercent"
    """Sort the results by percent changing in the last 24h"""