"""Request sub-schemas shared by more than one Helius endpoint."""

from pydantic import BaseModel


# ─── Comparison filters (getTransfersByAddress, getTransactionsForAddress) ────

class HeliusComparisonFilter(BaseModel):
    """
    Numeric range filter used by
    [`PostGetTransfersByAddressFilters`][cyhole.helius.schema.PostGetTransfersByAddressFilters]
    and [`PostGetTransactionsForAddressFilters`][cyhole.helius.schema.PostGetTransactionsForAddressFilters].

    All operators are optional and can be combined freely; an omitted bound
    means the value is unconstrained on that side.

    Attributes:
        gt: greater than this value (exclusive). `None` if no lower bound.
        gte: greater than or equal to this value (inclusive). `None` if no lower bound.
        lt: less than this value (exclusive). `None` if no upper bound.
        lte: less than or equal to this value (inclusive). `None` if no upper bound.
        eq: exact match. `None` when no equality match is required. Only honored by the
            `blockTime` filter of the `getTransactionsForAddress` RPC endpoint.
    """
    gt: int | None = None
    gte: int | None = None
    lt: int | None = None
    lte: int | None = None
    eq: int | None = None


class HeliusSignatureComparisonFilter(BaseModel):
    """
    Lexicographic range filter on a transaction signature, used by the `signature`
    filter of [`PostGetTransactionsForAddressFilters`][cyhole.helius.schema.PostGetTransactionsForAddressFilters].

    Values are base58-encoded signature strings; comparison is performed
    lexicographically by the API.

    Attributes:
        gt: greater than this signature (exclusive). `None` if no lower bound.
        gte: greater than or equal to this signature (inclusive). `None` if no lower bound.
        lt: less than this signature (exclusive). `None` if no upper bound.
        lte: less than or equal to this signature (inclusive). `None` if no upper bound.
    """
    gt: str | None = None
    gte: str | None = None
    lt: str | None = None
    lte: str | None = None
