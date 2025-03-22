from ..core.param import CyholeParam

class JupiterSwapMode(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap modes.
    """
    EXACT_IN = "ExactIn"
    EXACT_OUT = "ExactOut"

class JupiterSwapType(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap types.
    """
    AGGREGATOR = "aggregator"
    RFQ = "rfq"

class JupiterSwapExecutionStatus(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap execution statuses.
    """
    SUCCESS = "Success"
    FAILED = "Failed"

class JupiterEnvironmentType(CyholeParam):
    """
        Enum class to get the supported Jupiter's environment types.
    """
    PRODUCTION = "production"
    CANARY = "canary"

class JupiterPrioritizationType(CyholeParam):
    """
        Enum class to get the supported Jupiter's prioritization types.
    """
    NONE = "None"
    COMPUTE_BUDGET = "ComputeBudget"
    JITO = "Jito"

class JupiterSwapDex(CyholeParam):
    """
        Enum class to get the supported Jupiter's swap DEXes.
    """
    ALDRIN = "Aldrin"
    ALDRIN_V2 = "Aldrin V2"
    BONKSWAP = "Bonkswap"
    #CLONE = "Clone Protocol"
    CREMA = "Crema"
    CROPPER = "Cropper"
    #CROPPER_LEGACY = "Cropper Legacy"
    DAOS_FUN = "Daos.fun"
    DEXLAB = "Dexlab"
    DEX1 = "1DEX"
    FLUX = "FluxBeam"
    #GOOSEFX = "GooseFX"
    GUACSWAP = "Guacswap"
    HELIUM = "Helium Network"
    INVARIANT = "Invariant"
    #LIFINITY_V1 = "Lifinity V1"
    LIFINITY_V2 = "Lifinity V2"
    #MARINADE = "Marinade"
    MERCURIAL = "Mercurial"
    METEORA = "Meteora"
    METEORA_DLMM = "Meteora DLMM"
    MOONSHOT = "Moonshot"
    OASIS = "Oasis"
    OBRIC_V2 = "Obric V2"
    ONE_DEX = "1DEX"
    OPENBOOK = "Openbook"
    OPENBOOK_V2 = "OpenBook V2"
    ORCA_V1 = "Orca V1"
    ORCA_V2 = "Orca V2"
    PENGUIN = "Penguin"
    PERENA = "Perena"
    PERPS = "Perps"
    PHOENIX = "Phoenix"
    PUMP_FUN = "Pump.fun"
    PUMP_FUN_AMM = "Pump.fun AMM"
    RAYDIUM = "Raydium"
    RAYDIUM_CLMM = "Raydium CLMM"
    RAYDIUM_CP = "Raydium CP"
    SABER = "Saber"
    SABER_DECIMALS = "Saber (Decimals)"
    SANCTUM = "Sanctum"
    SANCTUM_INFINITY = "Sanctum Infinity"
    SAROS = "Saros"
    SOLAYER = "Solayer"
    SOLFI = "SolFi"
    STABBLE_STABLE_SWAP = "Stabble Stable Swap"
    STABBLE_WEIGHTED_SWAP = "Stabble Weighted Swap"
    STEP = "StepN"
    TOKEN_MILL = "Token Mill"
    TOKEN_SWAP = "Token Swap"
    WHIRLPOOL = "Whirlpool"
    VIRTUALS = "Virtuals"
    ZERO_FI = "ZeroFi"

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

class JupiterTokenTagType(CyholeParam):
    """
        Enum class to get the supported Jupiter's token tag types.
    """
    MOONSHOT = "moonshot"
    """A list of tokens minted via Moonshot."""
    PUMPFUN = "pump"
    """	A list of tokens minted via Pump.fun."""
    TOKEN_2022 = "token-2022"
    """A list of all token-2022 tokens."""
    LIQUID_STAKED = "lst"
    """A list of liquid staked tokens, maintained with Sanctum."""
    VERIFIED = "verified"
    """
        A list of verified tokens, consisting of community-verified tokens 
        via [catdetlist.jup.ag](https://catdetlist.jup.ag/) and the previous 
        standard of Jupiter Strict.
    """