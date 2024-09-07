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

class SolscanActivityNFTType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT activities types.
    """
    SOLD = "ACTIVITY_NFT_SOLD"
    """Export only NFT sold."""
    LISTING = "ACTIVITY_NFT_LISTING"
    """Export only NFT listing."""
    BIDDING = "ACTIVITY_NFT_BIDDING"
    """Export only NFT bidding."""
    CANCEL_BID = "ACTIVITY_NFT_CANCEL_BID"
    """Export only NFT cancel bid."""
    CANCEL_LIST = "ACTIVITY_NFT_CANCEL_LIST"
    """Export only NFT cancel list."""
    REJECT_BID = "ACTIVITY_NFT_REJECT_BID"
    """Export only NFT reject bid."""
    UPDATE_PRICE = "ACTIVITY_NFT_UPDATE_PRICE"
    """Export only NFT update price."""
    LIST_AUCTION = "ACTIVITY_NFT_LIST_AUCTION"
    """Export only NFT list auction."""

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

class SolscanNFTPageSizeType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT page size types.
    """
    SIZE_12 = 12
    """Export only 12 items per page."""
    SIZE_24 = 24
    """Export only 24 items per page."""
    SIZE_36 = 36
    """Export only 36 items per page."""

class SolscanNFTCollectionPageSizeType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT collection page size types.
    """
    SIZE_10 = 10
    """Export only 10 items per page."""
    SIZE_18 = 18
    """Export only 18 items per page."""
    SIZE_20 = 20
    """Export only 20 items per page."""
    SIZE_30 = 30
    """Export only 30 items per page."""
    SIZE_40 = 40
    """Export only 40 items per page."""

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

class SolscanOrderType(CyholeParam):
    """
        Enum class to get the supported Solscan's orders.
    """
    ASCENDING = "asc"
    """Ascending sort order."""
    DESCENDING = "desc"
    """Descending sort order."""

class SolscanSortType(CyholeParam):
    """
        Enum class to get the supported Solscan's sorting types.
    """
    PRICE = "price"
    """Sort by price."""
    HOLDER = "holder"
    """Sort by holder."""
    MARKET_CAP = "market_cap"
    """Sort by market cap."""
    CREATED_TIME = "created_time"
    """Sort by created time."""

class SolscanNFTSortType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT sorting types.
    """
    ITEMS = "items"
    """Sort by items."""
    FLOOR_PRICE = "floor_price"
    """Sort by floor price."""
    VOLUMES = "volumes"
    """Sort by volumes."""

class SolscanNFTItemSortType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT item sorting types.
    """
    LAST_TRADE = "last_trade"
    """Sort by last trade."""
    LISTING_PRICE = "listing_price"
    """Sort by listing price."""

class SolscanNFTDaysRangeType(CyholeParam):
    """
        Enum class to get the supported Solscan's NFT days range types.
    """
    DAYS_1 = 1
    """Export only 1 day."""
    DAYS_7 = 7
    """Export only 7 days."""
    DAYS_30 = 30
    """Export only 30 days."""

class SolscanTransactionFilterType(CyholeParam):
    """
        Enum class to get the supported Solscan's transaction filter types.
    """
    ALL = "all"
    """Export all transactions."""
    EXCEPT_VOTE = "exceptVote"
    """Export all transactions except votes."""