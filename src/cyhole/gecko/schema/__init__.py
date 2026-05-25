"""Gecko response schemas, grouped by API domain."""

from .common import (
    LinksResponse,
    RelationshipData,
    RelationshipList,
    ResourceRef,
    TimeBucketedStr,
    TokenFullInfoAttributes,
    TokenHoldersDistribution,
    TokenHoldersInfo,
    TokenImageSet,
    TokenScoreDetails,
    TransactionStats,
    TransactionsTimeBuckets,
)
from .networks import (
    GetNetworksResponse,
    NetworkAttributes,
    NetworkData,
)
from .dexes import (
    DexAttributes,
    DexData,
    GetDexesResponse,
)
from .ohlcv import (
    GetPoolOhlcvQuery,
    GetPoolOHLCVResponse,
    GetTokenOhlcvQuery,
    GetTokenOHLCVResponse,
    OhlcvAttributes,
    OhlcvData,
    OhlcvMeta,
    OhlcvMetaToken,
)
from .trades import (
    GetPoolTradesResponse,
    GetTokenTradesResponse,
    TokenTradeAttributes,
    TokenTradeData,
    TradeAttributes,
    TradeData,
)
from .pool_info import (
    GetPoolTokenInfoResponse,
    PoolTokenInfoData,
    PoolTokenInfoRelationships,
)
from .tokens import (
    GetRecentlyUpdatedTokensResponse,
    GetTokenDataMultipleResponse,
    GetTokenDataResponse,
    LaunchpadDetails,
    PoolIncluded,
    PoolIncludedAttributes,
    PoolIncludedRelationships,
    RecentlyUpdatedTokenAttributes,
    RecentlyUpdatedTokenData,
    RecentlyUpdatedTokenRelationships,
    TokenDataAttributes,
    TokenDataMultipleAttributes,
    TokenDataMultipleResource,
    TokenDataRelationships,
    TokenDataResource,
    TokenDataVolumeUsd,
)
from .token_info import (
    GetTokenInfoResponse,
    TokenInfoData,
)
from .holders import (
    GetTokenHoldersChartResponse,
    GetTopTokenHoldersResponse,
    TokenHoldersChartAttributes,
    TokenHoldersChartData,
    TokenHoldersChartMeta,
    TokenHoldersChartMetaToken,
    TopTokenHolder,
    TopTokenHoldersAttributes,
    TopTokenHoldersData,
)
from .traders import (
    GetTopTokenTradersResponse,
    TopTokenTrader,
    TopTokenTradersAttributes,
    TopTokenTradersData,
)
from .simple_price import (
    GetSimpleTokenPriceQuery,
    GetSimpleTokenPriceResponse,
    SimpleTokenPriceAttributes,
    SimpleTokenPriceData,
)
from .search import (
    GetSearchPoolsResponse,
    SearchIncluded,
    SearchIncludedAttributes,
    SearchPoolAttributes,
    SearchPoolData,
    SearchPoolRelationships,
)

__all__ = [
    # common
    "LinksResponse",
    "RelationshipData",
    "RelationshipList",
    "ResourceRef",
    "TimeBucketedStr",
    "TokenFullInfoAttributes",
    "TokenHoldersDistribution",
    "TokenHoldersInfo",
    "TokenImageSet",
    "TokenScoreDetails",
    "TransactionStats",
    "TransactionsTimeBuckets",
    # networks
    "GetNetworksResponse",
    "NetworkAttributes",
    "NetworkData",
    # dexes
    "DexAttributes",
    "DexData",
    "GetDexesResponse",
    # ohlcv
    "GetPoolOhlcvQuery",
    "GetPoolOHLCVResponse",
    "GetTokenOhlcvQuery",
    "GetTokenOHLCVResponse",
    "OhlcvAttributes",
    "OhlcvData",
    "OhlcvMeta",
    "OhlcvMetaToken",
    # trades
    "GetPoolTradesResponse",
    "GetTokenTradesResponse",
    "TokenTradeAttributes",
    "TokenTradeData",
    "TradeAttributes",
    "TradeData",
    # pool_info
    "GetPoolTokenInfoResponse",
    "PoolTokenInfoData",
    "PoolTokenInfoRelationships",
    # tokens
    "GetRecentlyUpdatedTokensResponse",
    "GetTokenDataMultipleResponse",
    "GetTokenDataResponse",
    "LaunchpadDetails",
    "PoolIncluded",
    "PoolIncludedAttributes",
    "PoolIncludedRelationships",
    "RecentlyUpdatedTokenAttributes",
    "RecentlyUpdatedTokenData",
    "RecentlyUpdatedTokenRelationships",
    "TokenDataAttributes",
    "TokenDataMultipleAttributes",
    "TokenDataMultipleResource",
    "TokenDataRelationships",
    "TokenDataResource",
    "TokenDataVolumeUsd",
    # token_info
    "GetTokenInfoResponse",
    "TokenInfoData",
    # holders
    "GetTokenHoldersChartResponse",
    "GetTopTokenHoldersResponse",
    "TokenHoldersChartAttributes",
    "TokenHoldersChartData",
    "TokenHoldersChartMeta",
    "TokenHoldersChartMetaToken",
    "TopTokenHolder",
    "TopTokenHoldersAttributes",
    "TopTokenHoldersData",
    # traders
    "GetTopTokenTradersResponse",
    "TopTokenTrader",
    "TopTokenTradersAttributes",
    "TopTokenTradersData",
    # simple_price
    "GetSimpleTokenPriceQuery",
    "GetSimpleTokenPriceResponse",
    "SimpleTokenPriceAttributes",
    "SimpleTokenPriceData",
    # search
    "GetSearchPoolsResponse",
    "SearchIncluded",
    "SearchIncludedAttributes",
    "SearchPoolAttributes",
    "SearchPoolData",
    "SearchPoolRelationships",
]
