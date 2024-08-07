from ..core.param import CyholeParam

class BirdeyeChain(CyholeParam):
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

class BirdeyeOrder(CyholeParam):
    """
        Enum class to get the supported Birdeye's orders.
    """
    ASCENDING = "asc"
    """Ascending sort order."""
    DESCENDING = "desc"
    """Descending sort order."""

class BirdeyeSort(CyholeParam):
    """
        Enum class to get the supported Birdeye's sorting types.
    """
    SORT_MC = "mc"
    """Sort the results by Market Cap (MC)"""
    SORT_V24HUSD = "v24hUSD"
    """Sort the results by USD Volume in the last 24h"""
    SORT_V24HCHANGEPERCENT = "v24hChangePercent"
    """Sort the results by percent changing in the last 24h"""

class BirdeyeTimeFrame(CyholeParam):
    """
        Enum class to get the supported Birdeye's timeframe sizes.
    """
    MIN1 = "1m"
    """1 minute"""
    MIN3 = "3m"
    """3 minute"""
    MIN5 = "5m"
    """5 minute"""
    MIN15 = "15m"
    """15 minute"""
    MIN30 = "30m"
    """30 minute"""
    H1 = "1H"
    """1 hour"""
    H2 = "2H"
    """2 hour"""
    H4 = "4H"
    """4 hour"""
    H6 = "6H"
    """6 hour"""
    H8 = "8H"
    """8 hour"""
    H12 = "12H"
    """12 hour"""
    D1 = "1D"
    """1 day"""
    D3 = "3D"
    """3 day"""
    W1 = "1W"
    """1 week"""
    M1 = "1M"
    """1 month"""

class BirdeyeHourTimeFrame(CyholeParam):
    """
        Enum class to get the supported Birdeye's timeframe sizes with hour as unit size.
    """
    H1 = "1h"
    """1 hour"""
    H2 = "2h"
    """2 hour"""
    H4 = "4h"
    """4 hour"""
    H8 = "8h"
    """8 hour"""
    H24 = "24h"
    """24 hour"""

class BirdeyeAddressType(CyholeParam):
    """
        Enum class to get the supported Birdeye's address' types.
    """
    TOKEN = "token"
    """The address is refering to a token on the chain."""
    PAIR = "pair"
    """The address is refering to a token pair on the chain. (e.g. SOL/USDT)"""

class BirdeyeTradeType(CyholeParam):
    """
        Enum class to get the supported Birdeye's transactions' types.
    """
    SWAP = "swap"
    """A classic exchange between two currencies."""
    ADD = "add"
    """Transactions that add liquidity."""
    REMOVE = "remove"
    """Transactions that remove liquidity."""
    ALL = "all"
    """All type of transactions (swap, add, remove)."""