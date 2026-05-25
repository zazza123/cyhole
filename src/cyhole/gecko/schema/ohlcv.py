"""Schemas for the Pool OHLCV and Token OHLCV endpoints."""

from pydantic import BaseModel


class GetPoolOhlcvQuery(BaseModel):
    """
    Query-string bundle for the Pool OHLCV endpoint, exposed as a single model because the endpoint
    accepts more than three meaningful inputs. Pass it through and any field left at `None` will be
    omitted from the request.

    Attributes:
        aggregate: candle aggregation step within the chosen timeframe. Allowed values depend on the
            timeframe — `day`: `"1"`; `hour`: `"1"`, `"4"`, `"12"`; `minute`: `"1"`, `"5"`, `"15"`;
            `second`: `"1"`, `"15"`, `"30"`. Defaults to `"1"` server-side.
        before_timestamp: unix timestamp (seconds) used as an upper bound on the returned candles;
            useful to walk backwards through history.
        limit: maximum number of candles to return. Server default is `100`; valid range is 1–1000.
        currency: candle denomination, either `"usd"` (default) or `"token"`; see
            [`GeckoCurrency`][cyhole.gecko.param.GeckoCurrency].
        token: which side of the pool to quote prices on. `"base"`, `"quote"` (see
            [`GeckoTokenSide`][cyhole.gecko.param.GeckoTokenSide]) or a token contract address.
        include_empty_intervals: when `True`, the server returns zero-volume candles in periods with
            no trades; when `False` (default) these intervals are omitted.
    """
    aggregate: str | None = None
    before_timestamp: int | None = None
    limit: int | None = None
    currency: str | None = None
    token: str | None = None
    include_empty_intervals: bool | None = None


class GetTokenOhlcvQuery(BaseModel):
    """
    Query-string bundle for the Token OHLCV endpoint.

    Attributes:
        aggregate: candle aggregation step — same allowed values as
            [`GetPoolOhlcvQuery.aggregate`][cyhole.gecko.schema.GetPoolOhlcvQuery].
        before_timestamp: unix timestamp (seconds) used as an upper bound on the returned candles.
        limit: maximum number of candles to return. Server default is `100`; valid range is 1–1000.
        currency: candle denomination, either `"usd"` (default) or `"token"`.
        include_empty_intervals: when `True`, the server returns zero-volume candles in periods with
            no trades; defaults to `False` server-side.
        include_inactive_source: when `True`, include data from sources GeckoTerminal has flagged as
            inactive; defaults to `False`.
    """
    aggregate: str | None = None
    before_timestamp: int | None = None
    limit: int | None = None
    currency: str | None = None
    include_empty_intervals: bool | None = None
    include_inactive_source: bool | None = None


class OhlcvAttributes(BaseModel):
    """
    Attributes block of an OHLCV resource.

    Attributes:
        ohlcv_list: ordered list of candles; each candle is a 6-element list
            `[timestamp_unix_seconds, open, high, low, close, volume]` with the timestamp as an integer
            and the four price components plus volume as floats.
    """
    ohlcv_list: list[list[float]]


class OhlcvData(BaseModel):
    """
    Top-level `data` block of an OHLCV response.

    Attributes:
        id: identifier of the OHLCV series.
        type: JSON:API resource type.
        attributes: candle list payload.
    """
    id: str
    type: str
    attributes: OhlcvAttributes


class OhlcvMetaToken(BaseModel):
    """
    Reference info for one side (base or quote) of an OHLCV series.

    Attributes:
        address: token contract address.
        name: human-readable token name.
        symbol: token ticker symbol.
        coingecko_coin_id: CoinGecko coin id mapped to this token; `None` when not mapped.
    """
    address: str
    name: str
    symbol: str
    coingecko_coin_id: str | None = None


class OhlcvMeta(BaseModel):
    """
    `meta` block of an OHLCV response identifying the base and quote tokens.

    Attributes:
        base: metadata of the base token of the underlying pool.
        quote: metadata of the quote token of the underlying pool.
    """
    base: OhlcvMetaToken
    quote: OhlcvMetaToken


class GetPoolOHLCVResponse(BaseModel):
    """
    Response payload from the **Pool OHLCV** endpoint, returning historical candlestick data for the
    requested pool at the chosen timeframe. The candles are returned newest-first up to the
    configured `limit` and can be denominated in USD or quoted in the pool's token.

    Attributes:
        data: candle series payload.
        meta: base/quote reference info for the underlying pool.
    """
    data: OhlcvData
    meta: OhlcvMeta


class GetTokenOHLCVResponse(BaseModel):
    """
    Response payload from the **Token OHLCV** endpoint, returning aggregated candlestick data for the
    requested token across the most-relevant pool on the network. The shape mirrors the Pool OHLCV
    response.

    Attributes:
        data: candle series payload.
        meta: base/quote reference info for the underlying pool selected by GeckoTerminal.
    """
    data: OhlcvData
    meta: OhlcvMeta
