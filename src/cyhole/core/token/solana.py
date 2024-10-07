from ...core.token import CyholeToken

class SolanaToken(CyholeToken):
    """Model used to identify a Solana token on `cyhole` library."""
    pass

# ************************
# Solana Token Definitions
# ************************
SOL = SolanaToken(
    address = "So11111111111111111111111111111111111111111",
    decimals = 9,
    name = "Solana",
    symbol = "SOL"
)
"""Solana token."""

WSOL = SolanaToken(
    address = "So11111111111111111111111111111111111111112",
    decimals = 9,
    name = "Wrapped SOL",
    symbol = "SOL"
)
"""Wrapped Solana token."""

USDC = SolanaToken(
    address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    decimals = 6,
    name = "USD Coin",
    symbol = "USDC"
)
"""USD Coin token."""

USDT = SolanaToken(
    address = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    decimals = 6,
    name = "Tether USD",
    symbol = "USDT"
)
"""Tether USD token."""

JUP  = SolanaToken(
    address = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    decimals = 6,
    name = "Jupiter",
    symbol = "JUP"
)
"""Jupiter token."""

BONK = SolanaToken(
    address = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    decimals = 5,
    name = "Bonk",
    symbol = "BONK"
)
"""Bonk token."""

WIF  = SolanaToken(
    address = "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
    decimals = 6,
    name = "dogwifhat",
    symbol = "$WIF"
)
"""dogwifhat token."""