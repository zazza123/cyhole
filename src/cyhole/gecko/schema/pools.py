"""Schemas for the New Pools (by network and across networks) and Multiple Pools Data endpoints."""

from pydantic import BaseModel

from .common import (
    IncludedResource,
    PoolAttributes,
    PoolRelationships,
    TimeBucketedStr,
)
from .tokens import LaunchpadDetails


class PoolData(BaseModel):
    """
    Single pool resource returned in the `data` array of the New Pools endpoints.

    Attributes:
        id: GeckoTerminal pool identifier, `<network>_<pool address>` (e.g. `"solana_GKzF..."`).
        type: JSON:API resource type, always `"pool"`.
        attributes: pool prices, valuation, liquidity, volume and transaction statistics.
        relationships: pointers to the base token, quote token, DEX and (cross-network endpoint only)
            network of the pool.
    """
    id: str
    type: str
    attributes: PoolAttributes
    relationships: PoolRelationships | None = None


class GetNewPoolsResponse(BaseModel):
    """
    Response payload from the **New Pools** endpoint, returning the most recently created pools
    across every network GeckoTerminal indexes, newest first, 20 per page. Each pool's
    `relationships` also points to its network.

    Attributes:
        data: list of pools on the requested page, newest first.
        included: token / DEX / network resources expanded for the requested `include`
            relationships; `None` when `include` was not set.
    """
    data: list[PoolData]
    included: list[IncludedResource] | None = None


class GetNetworkNewPoolsResponse(GetNewPoolsResponse):
    """
    Response payload from the **New Pools by Network** endpoint, returning the most recently created
    pools on one network, newest first, 20 per page. Same shape as
    [`GetNewPoolsResponse`][cyhole.gecko.schema.GetNewPoolsResponse]; `relationships.network` is
    `None` because the network is fixed by the request.
    """


class PoolMultiAttributes(PoolAttributes):
    """
    Attributes block of a pool returned by the **Multiple Pools Data** endpoint.

    Extends [`PoolAttributes`][cyhole.gecko.schema.PoolAttributes] with the fields only this endpoint
    returns. The fee and locked-liquidity percentages are typed to accept either a decimal string or
    a number, because the captured responses only ever carried `null` for them.

    Attributes:
        pool_name: pool name as reported by the DEX; usually equal to `name`.
        pool_fee_percentage: swap fee charged by the pool, in percent; `None` when not reported.
        locked_liquidity_percentage: share of the pool liquidity that is locked, in percent; `None`
            when not reported.
        launchpad_details: bonding-curve progress for pools of launchpad DEXes (e.g. pump.fun);
            `None` for regular AMM pools.
        net_buy_volume_usd: buy volume minus sell volume in USD per time window; returned only when
            `include_volume_breakdown=True`, `None` otherwise.
        buy_volume_usd: USD volume of buy trades per time window; returned only when
            `include_volume_breakdown=True`, `None` otherwise.
        sell_volume_usd: USD volume of sell trades per time window; returned only when
            `include_volume_breakdown=True`, `None` otherwise.
    """
    pool_name: str | None = None
    pool_fee_percentage: str | float | None = None
    locked_liquidity_percentage: str | float | None = None
    launchpad_details: LaunchpadDetails | None = None
    net_buy_volume_usd: TimeBucketedStr | None = None
    buy_volume_usd: TimeBucketedStr | None = None
    sell_volume_usd: TimeBucketedStr | None = None


class PoolMultiData(BaseModel):
    """
    Single pool resource returned in the `data` array of the Multiple Pools Data endpoint.

    Attributes:
        id: GeckoTerminal pool identifier, `<network>_<pool address>`.
        type: JSON:API resource type, always `"pool"`.
        attributes: pool statistics, extended with fee, locked liquidity, launchpad progress and the
            optional volume breakdown.
        relationships: pointers to the base token, quote token and DEX of the pool.
    """
    id: str
    type: str
    attributes: PoolMultiAttributes
    relationships: PoolRelationships | None = None


class GetPoolsMultiResponse(BaseModel):
    """
    Response payload from the **Multiple Pools Data** endpoint, returning the current statistics of
    up to 30 pools of one network in a single request. Join the entries back to the requested
    addresses through `attributes.address` rather than by position.

    Attributes:
        data: list of the requested pools.
        included: token / DEX resources expanded for the requested `include` relationships; `None`
            when `include` was not set.
    """
    data: list[PoolMultiData]
    included: list[IncludedResource] | None = None
