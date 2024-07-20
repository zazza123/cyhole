from ..core.param import CyholeParam

class JupiterSwapMode(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap modes.
    """
    EXACT_IN = "ExactIn"
    EXACT_OUT = "ExactOut"

class JupiterSwapDex(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap DEXes.
    """
    ALDRIN = "Aldrin"
    ALDRIN_V2 = "Aldrin V2"
    BONKSWAP = "Bonkswap"
    CLONE = "Clone Protocol"
    CREMA = "Crema"
    CROPPER = "Cropper"
    CROPPER_LEGACY = "Cropper Legacy"
    DEXLAB = "Dexlab"
    DEX1 = "1DEX"
    FLUX = "FluxBeam"
    GOOSEFX = "GooseFX"
    GUACSWAP = "Guacswap"
    HELIUM = "Helium Network"
    INVARIANT = "Invariant"
    LIFINITY_V1 = "Lifinity V1"
    LIFINITY_V2 = "Lifinity V2"
    MARINADE = "Marinade"
    MERCURIAL = "Mercurial"
    METEORA = "Meteora"
    METEORA_DLMM = "Meteora DLMM"
    OASIS = "Oasis"
    OPENBOOK = "Openbook"
    OPENBOOK_V2 = "OpenBook V2"
    ORCA_V1 = "Orca V1"
    ORCA_V2 = "Orca V2"
    PENGUIN = "Penguin"
    PERPS = "Perps"
    PHOENIX = "Phoenix"
    RAYDIUM = "Raydium"
    RAYDIUM_CLMM = "Raydium CLMM"
    RAYDIUM_CP = "Raydium CP"
    SABER = "Saber"
    SABER_DECIMALS = "Saber (Decimals)"
    SANCTUM = "Sanctum"
    SANCTUM_INFINITY = "Sanctum Infinity"
    SAROS = "Saros"
    STEP = "StepN"
    TOKEN_SWAP = "Token Swap"
    WHIRLPOOL = "Whirlpool"

class JupiterTokenListType(CyholeParam):
    """
        Enum class to get the supported Jupiter's token lists.
    """
    STRICT = "strict"
    """Extract only the tokens with tags `old-registry`, `community`, or `wormhole` verified"""
    ALL = "all"
    """Extract **all** non banned tokens."""

class JupiterLimitOrderState(CyholeParam):
    """
        Enum class to get the supported Jupiter's limit order states.
    """
    OPEN = "Open"
    """The limit order is still open."""
    COMPLETED = "Completed"
    """The limit order is completed."""
    CANCELLED = "Cancelled"
    """The limit order was cancelled."""