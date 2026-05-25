from ..core.param import CyholeParam


class GeckoTimeframe(CyholeParam):
    """
    Timeframe granularity used by the OHLCV endpoints (pool and token).

    `aggregate` query parameter values depend on the chosen timeframe:

    - `DAY`: `"1"`.
    - `HOUR`: `"1"`, `"4"`, `"12"`.
    - `MINUTE`: `"1"`, `"5"`, `"15"`.
    - `SECOND`: `"1"`, `"15"`, `"30"`.
    """
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"


class GeckoCurrency(CyholeParam):
    """Currency unit for OHLCV candle values (`usd` or quoted in `token`)."""
    USD = "usd"
    TOKEN = "token"


class GeckoTokenSide(CyholeParam):
    """Token side used by OHLCV/trades endpoints to indicate which side of the pool a price refers to."""
    BASE = "base"
    QUOTE = "quote"


class GeckoHoldersChartDays(CyholeParam):
    """Window covered by the token-holders chart endpoint."""
    DAYS_7 = "7"
    DAYS_30 = "30"
    MAX = "max"


class GeckoTopTradersSort(CyholeParam):
    """Sorting criterion accepted by the top-traders endpoint."""
    REALIZED_PNL_DESC = "realized_pnl_usd_desc"
    UNREALIZED_PNL_DESC = "unrealized_pnl_usd_desc"
    TOTAL_BUY_USD_DESC = "total_buy_usd_desc"
    TOTAL_SELL_USD_DESC = "total_sell_usd_desc"


class GeckoTokenDataInclude(CyholeParam):
    """`include` query value used by the token-data endpoints to embed related pools in the response."""
    TOP_POOLS = "top_pools"


class GeckoRecentlyUpdatedInclude(CyholeParam):
    """`include` query value for the recently-updated-tokens endpoint to embed the network resource."""
    NETWORK = "network"


class GeckoSearchInclude(CyholeParam):
    """`include` query values accepted by the search-pools endpoint; pass any combination as comma-separated."""
    BASE_TOKEN = "base_token"
    QUOTE_TOKEN = "quote_token"
    DEX = "dex"
