from ..core.param import CyholeParam

class JupiterApiTier(CyholeParam):
    """
        Enum class to get the supported Jupiter's API tiers.
    """
    LITE = "lite"
    PRO = "pro"
    ULTRA = "ultra"

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

class JupiterOrderStatus(CyholeParam):
    """
        Enum class to get the supported Jupiter's order statuses.
    """
    ACTIVE = "active"
    """The order is active."""
    HISTORY = "history"
    """The order is in history."""

class JupiterOrderState(CyholeParam):
    """
        Enum class to get the supported Jupiter's order states.
    """
    OPEN = "Open"
    """The order is still open."""
    COMPLETED = "Completed"
    """The order is completed."""
    CANCELLED = "Cancelled"
    """The order was cancelled."""
    CLOSE = "Close"
    """The order was closed."""

class JupiterTokenTagType(CyholeParam):
    """
        Enum class to get the supported Jupiter's token tag types.
    """
    LST = "lst"
    """Latest tokens added to Jupiter."""
    VERIFIED = "verified"
    """
        A list of verified tokens, consisting of community-verified tokens 
        via [catdetlist.jup.ag](https://catdetlist.jup.ag/) and the previous 
        standard of Jupiter Strict.
    """

class JupiterTokenCategory(CyholeParam):
    """
        Enum class to get the supported Jupiter's token category types.
    """
    TOP_ORGANIC_SCORE = "toporganicscore"
    TOP_TRADED = "toptraded"
    TOP_TRENDING = "toptrending"

class JupiterTokenInterval(CyholeParam):
    """
        Enum class to get the supported Jupiter's token interval types.
    """
    FIVE_MINUTES = "5m"
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"
    TWENTY_FOUR_HOURS = "24h"

class JupiterRecurringType(CyholeParam):
    """
        Enum class to get the supported Jupiter's 
        recurring order types, that can be used in 
        "**Recurring - Orders**" endpoint.
    """
    ALL = "all"
    """All recurring orders."""
    PRICE = "price"
    """Recurring price-based orders."""
    TIME = "time"
    """Recurring time-based orders."""

class JupiterWithdrawMode(CyholeParam):
    """
        Enum class to get the supported Jupiter's withdraw modes.
    """
    IN = "In"
    """Withdraw in mode."""
    OUT = "Out"
    """Withdraw out mode."""

class JupiterOrganicScore(CyholeParam):
    """
        Enum class to get the supported Jupiter's 
        organic score types.
    """
    HIGH = "high"
    """Tokens with high organic score."""
    MEDIUM = "medium"
    """Tokens with medium organic score."""
    LOW = "low"
    """Tokens with low organic score."""

class JupiterBroadcastFeeType(CyholeParam):
    """
        Enum class to get the supported Jupiter's broadcast fee type strategies
        in the Swap v2 "**Order**" endpoint.
    """
    MAX_CAP = "maxCap"
    """Treat the fee as a maximum cap; actual fee may be lower."""
    EXACT_FEE = "exactFee"
    """Use the exact fee amount specified."""

class JupiterRouter(CyholeParam):
    """
        Enum class to get the supported Jupiter's router types.
    """
    IRIS = "iris"
    """Iris router."""
    JUPITERZ = "jupiterz"
    """JupiterZ router."""
    DFLOW = "dflow"
    """DFlow router."""
    OKX = "okx"
    """OKX router."""

class JupiterShieldWarningType(CyholeParam):
    """
        Enum class to get the supported Jupiter's shield warning types.
    """
    NOT_VERIFIED = "NOT_VERIFIED"
    """Token is not verified."""
    LOW_LIQUIDITY = "LOW_LIQUIDITY"
    """Token has low liquidity."""
    NOT_SELLABLE = "NOT_SELLABLE"
    """Token is not sellable."""
    LOW_ORGANIC_ACTIVITY = "LOW_ORGANIC_ACTIVITY"
    """Token has low organic activity."""
    HAS_MINT_AUTHORITY = "HAS_MINT_AUTHORITY"
    """Token has mint authority enabled."""
    HAS_FREEZE_AUTHORITY = "HAS_FREEZE_AUTHORITY"
    """Token has freeze authority enabled."""
    HAS_PERMANENT_DELEGATE = "HAS_PERMANENT_DELEGATE"
    """Token has a permanent delegate."""
    NEW_LISTING = "NEW_LISTING"
    """Token is a new listing."""
    VERY_LOW_TRADING_ACTIVITY = "VERY_LOW_TRADING_ACTIVITY"
    """Token has very low trading activity."""
    HIGH_SUPPLY_CONCENTRATION = "HIGH_SUPPLY_CONCENTRATION"
    """Token has high supply concentration."""
    NON_TRANSFERABLE = "NON_TRANSFERABLE"
    """Token is non-transferable."""
    MUTABLE_TRANSFER_FEES = "MUTABLE_TRANSFER_FEES"
    """Token has mutable transfer fees."""
    SUSPICIOUS_DEV_ACTIVITY = "SUSPICIOUS_DEV_ACTIVITY"
    """Token has suspicious developer activity."""
    SUSPICIOUS_TOP_HOLDER_ACTIVITY = "SUSPICIOUS_TOP_HOLDER_ACTIVITY"
    """Token has suspicious top holder activity."""
    HIGH_SINGLE_OWNERSHIP = "HIGH_SINGLE_OWNERSHIP"
    """Token has high single ownership concentration."""

class JupiterShieldWarningSeverity(CyholeParam):
    """
        Enum class to get the supported Jupiter's shield warning severity levels.
    """
    INFO = "info"
    """Informational severity level."""
    WARNING = "warning"
    """Warning severity level."""
    CRITICAL = "critical"
    """Critical severity level."""

class JupiterShieldWarningSource(CyholeParam):
    """
        Enum class to get the supported Jupiter's shield warning sources.
    """
    RUG_CHECK = "RugCheck"
    """Warning source from RugCheck."""