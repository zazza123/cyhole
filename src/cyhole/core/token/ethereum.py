from ...core.token import CyholeToken

class EthereumToken(CyholeToken):
    """Model used to identify a Ethereum token on `cyhole` library."""
    pass

# **************************
# Ethereum Token Definitions
# **************************
WETH = EthereumToken(
    address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    decimals = 18,
    name = "Wrapped Ether",
    symbol = "WETH"
)
"""Wrapped Ether token."""

USDC = EthereumToken(
    address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    decimals = 6,
    name = "USD Coin",
    symbol = "USDC"
)
"""USD Coin token."""

USDT = EthereumToken(
    address = "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    decimals = 6,
    name = "Tether USD",
    symbol = "USDT"
)
"""Tether USD token."""

BNB = EthereumToken(
    address = "0xB8c77482e45F1F44dE1745F52C74426C631bDD52",
    decimals = 18,
    name = "Binance Coin",
    symbol = "BNB"
)
"""Binance Coin token."""