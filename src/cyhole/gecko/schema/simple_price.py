"""Schema for the Onchain Simple Token Price endpoint."""

from pydantic import BaseModel


class GetSimpleTokenPriceQuery(BaseModel):
    """
    Query-string bundle for the Onchain Simple Token Price endpoint, exposed as a model because the
    endpoint accepts six optional `include_*` flags.

    Attributes:
        include_market_cap: when `True`, the response carries a `market_cap_usd` map keyed by address.
        mcap_fdv_fallback: when `True` together with `include_market_cap`, the server returns FDV
            for tokens lacking a market cap so the field is never missing.
        include_24hr_vol: when `True`, the response carries a `h24_volume_usd` map keyed by address.
        include_24hr_price_change: when `True`, the response carries a `h24_price_change_percentage` map.
        include_total_reserve_in_usd: when `True`, the response carries a `total_reserve_in_usd` map.
        include_inactive_source: when `True`, include data from sources GeckoTerminal has flagged as inactive.
    """
    include_market_cap: bool | None = None
    mcap_fdv_fallback: bool | None = None
    include_24hr_vol: bool | None = None
    include_24hr_price_change: bool | None = None
    include_total_reserve_in_usd: bool | None = None
    include_inactive_source: bool | None = None


class SimpleTokenPriceAttributes(BaseModel):
    """
    Attributes block of the Simple Token Price response.

    Every map is keyed by the lower-cased token contract address. Optional maps are only present
    when the corresponding `include_*` query flag is set on the request.

    Attributes:
        token_prices: USD price per token (decimal string).
        market_cap_usd: USD market cap per token; present when `include_market_cap=true`.
            With `mcap_fdv_fallback=true` returns FDV when market cap is unavailable.
        h24_volume_usd: trailing-24h USD volume per token; present when `include_24hr_vol=true`.
        h24_price_change_percentage: trailing-24h price change per token (percentage string);
            present when `include_24hr_price_change=true`.
        total_reserve_in_usd: aggregate pool reserve in USD per token; present when
            `include_total_reserve_in_usd=true`.
        last_trade_timestamp: unix timestamp (seconds) of the latest trade per token.
    """
    token_prices: dict[str, str | None] | None = None
    market_cap_usd: dict[str, str | None] | None = None
    h24_volume_usd: dict[str, str | None] | None = None
    h24_price_change_percentage: dict[str, str | None] | None = None
    total_reserve_in_usd: dict[str, str | None] | None = None
    last_trade_timestamp: dict[str, int | None] | None = None


class SimpleTokenPriceData(BaseModel):
    """
    Top-level `data` block of the Simple Token Price response.

    Attributes:
        id: identifier of the response.
        type: JSON:API resource type.
        attributes: per-address price + optional metric maps.
    """
    id: str
    type: str
    attributes: SimpleTokenPriceAttributes


class GetSimpleTokenPriceResponse(BaseModel):
    """
    Response payload from the **Onchain Simple Token Price** endpoint, returning current USD prices
    (and optional metrics) for up to 100 tokens on a single network in one request. Designed for
    lightweight quote lookups when the full Token Data payload is not needed.

    Attributes:
        data: per-token price and metric maps.
    """
    data: SimpleTokenPriceData
