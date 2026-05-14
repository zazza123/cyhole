from ..core.param import CyholeParam


class HeliusNetwork(CyholeParam):
    """
    Network environment for the Helius RPC endpoint.

    Used to select between mainnet and devnet when initialising a [`Helius`][cyhole.helius.interaction.Helius] instance.
    """
    MAINNET = "mainnet"
    DEVNET = "devnet"


class HeliusSortBy(CyholeParam):
    """
    Sort criteria available for DAS asset collection queries (e.g. `getAssetsByOwner`).

    Pass the `.value` to [`HeliusSortConfig`][cyhole.helius.schema.HeliusSortConfig] when building a request body.
    """
    CREATED = "created"
    UPDATED = "updated"
    RECENT_ACTION = "recent_action"
    NONE = "none"


class HeliusSortDirection(CyholeParam):
    """
    Sort direction for DAS asset collection queries.

    Pass the `.value` to [`HeliusSortConfig`][cyhole.helius.schema.HeliusSortConfig] when building a request body.
    """
    ASC = "asc"
    DESC = "desc"


class HeliusTokenType(CyholeParam):
    """
    Token type filter for the `searchAssets` DAS endpoint.

    Pass the `.value` to [`PostSearchAssetsBody`][cyhole.helius.schema.PostSearchAssetsBody]
    as the `token_type` parameter.
    """
    FUNGIBLE = "fungible"
    NON_FUNGIBLE = "nonFungible"
    REGULAR_NFT = "regularNft"
    COMPRESSED_NFT = "compressedNft"
    ALL = "all"


class HeliusTransferDirection(CyholeParam):
    """
    Direction filter for the `getTransfersByAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody]
    as the `direction` parameter.
    """
    IN = "in"
    """Transfers received by the queried address."""
    OUT = "out"
    """Transfers sent by the queried address."""
    ANY = "any"
    """Both incoming and outgoing transfers (API default)."""


class HeliusSolMode(CyholeParam):
    """
    SOL/WSOL representation mode for the `getTransfersByAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody]
    as the `sol_mode` parameter.
    """
    MERGED = "merged"
    """Treat WSOL as native SOL: WSOL mints are rewritten to the native SOL mint and wrap/unwrap lifecycle rows are excluded (API default)."""
    SEPARATE = "separate"
    """Keep WSOL as a distinct SPL mint and include wrap/unwrap lifecycle rows."""


class HeliusCommitment(CyholeParam):
    """
    Commitment level for the `getTransfersByAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody]
    as the `commitment` parameter.
    """
    FINALIZED = "finalized"
    """Only include transfers from finalized blocks (API default)."""
    CONFIRMED = "confirmed"
    """Include transfers from confirmed (not yet finalized) blocks."""


class HeliusSortOrder(CyholeParam):
    """
    Result ordering for the `getTransfersByAddress` and `getTransactionsForAddress`
    RPC endpoints.

    Pass the `.value` to
    [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody]
    or [`PostGetTransactionsForAddressBody`][cyhole.helius.schema.PostGetTransactionsForAddressBody]
    as the `sort_order` parameter.
    """
    DESC = "desc"
    """Newest first (API default)."""
    ASC = "asc"
    """Oldest first."""


class HeliusTransactionDetails(CyholeParam):
    """
    Transaction detail level for the `getTransactionsForAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransactionsForAddressBody`][cyhole.helius.schema.PostGetTransactionsForAddressBody]
    as the `transaction_details` parameter.
    """
    SIGNATURES = "signatures"
    """Return only signature-level info — faster, default mode (limit up to 1,000)."""
    FULL = "full"
    """Return the complete transaction payload — eliminates the need for follow-up `getTransaction` calls (limit must be `<= 100`)."""


class HeliusTransactionStatus(CyholeParam):
    """
    Transaction status filter for the `getTransactionsForAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransactionsForAddressFilters`][cyhole.helius.schema.PostGetTransactionsForAddressFilters]
    as the `status` parameter.
    """
    SUCCEEDED = "succeeded"
    """Only successful transactions."""
    FAILED = "failed"
    """Only failed transactions."""
    ANY = "any"
    """Both successful and failed transactions (API default)."""


class HeliusTokenAccountFilter(CyholeParam):
    """
    Token-account inclusion filter for the `getTransactionsForAddress` RPC endpoint.

    Pass the `.value` to [`PostGetTransactionsForAddressFilters`][cyhole.helius.schema.PostGetTransactionsForAddressFilters]
    as the `token_accounts` parameter.

    Not supported for transactions older than December 2022.
    """
    NONE = "none"
    """Only return transactions that directly reference the wallet address (API default)."""
    BALANCE_CHANGED = "balanceChanged"
    """Include transactions that reference the address or modify the balance of a token account it owns (recommended)."""
    ALL = "all"
    """Include any transaction that references the address or any token account it owns."""


class HeliusEncoding(CyholeParam):
    """
    Encoding format for the transaction payload, used by the
    `getTransactionsForAddress` RPC endpoint when `transaction_details = "full"`.

    Pass the `.value` to [`PostGetTransactionsForAddressBody`][cyhole.helius.schema.PostGetTransactionsForAddressBody]
    as the `encoding` parameter.
    """
    JSON = "json"
    """Default JSON encoding (raw account keys and instruction data)."""
    JSON_PARSED = "jsonParsed"
    """JSON encoding with parsed instructions for known programs (SPL Token, System, etc.)."""
    BASE64 = "base64"
    """Base64 encoding of the raw transaction bytes."""
    BASE58 = "base58"
    """Base58 encoding of the raw transaction bytes."""
