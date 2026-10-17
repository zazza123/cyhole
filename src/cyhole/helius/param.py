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
    Commitment level for the `getTransfersByAddress`, `getSignaturesForAddress` and
    `getTransaction` RPC endpoints.

    Pass the `.value` to [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody],
    [`PostGetSignaturesForAddressBody`][cyhole.helius.schema.PostGetSignaturesForAddressBody],
    [`PostGetTransactionBody`][cyhole.helius.schema.PostGetTransactionBody]
    or [`PostGetAccountInfoBody`][cyhole.helius.schema.PostGetAccountInfoBody]
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
    """Return the complete transaction payload — eliminates the need for follow-up `getTransaction` calls (limit up to 1,000; billed per 100 transactions returned)."""


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
    `getTransactionsForAddress` RPC endpoint when `transaction_details = "full"`
    and by the `getTransaction` RPC endpoint.

    Pass the `.value` to [`PostGetTransactionsForAddressBody`][cyhole.helius.schema.PostGetTransactionsForAddressBody]
    or [`PostGetTransactionBody`][cyhole.helius.schema.PostGetTransactionBody]
    as the `encoding` parameter. `getTransaction` supports only `JSON` and `JSON_PARSED`
    in `cyhole`: its response model expects the transaction as a JSON object.
    """
    JSON = "json"
    """Default JSON encoding (raw account keys and instruction data)."""
    JSON_PARSED = "jsonParsed"
    """JSON encoding with parsed instructions for known programs (SPL Token, System, etc.)."""
    BASE64 = "base64"
    """Base64 encoding of the raw transaction bytes."""
    BASE58 = "base58"
    """Base58 encoding of the raw transaction bytes."""


class HeliusAccountEncoding(CyholeParam):
    """
    Encoding format for the account data returned by the `getAccountInfo` and
    `getMultipleAccounts` RPC endpoints.

    Pass the `.value` to [`PostGetAccountInfoBody`][cyhole.helius.schema.PostGetAccountInfoBody]
    as the `encoding` parameter. The binary encodings return the data as a
    `[data, encoding]` pair; `JSON_PARSED` returns a JSON object for the programs the
    node can decode (SPL Token accounts, for example) and falls back to base64 for the
    others.
    """
    BASE58 = "base58"
    """Base58 encoding of the raw account data (slow; limited to small accounts)."""
    BASE64 = "base64"
    """Base64 encoding of the raw account data. The usual choice for program accounts."""
    BASE64_ZSTD = "base64+zstd"
    """Base64 encoding of the zstd-compressed account data."""
    JSON_PARSED = "jsonParsed"
    """JSON object decoded by the node for known programs (SPL Token, Stake, ...)."""


class HeliusParserStatus(CyholeParam):
    """
    Per-item parsing outcome returned by the Parsed Events API.

    Compare against the `parser_status` attribute of a
    [`ParsedEventsTransactionResult`][cyhole.helius.schema.ParsedEventsTransactionResult]
    to tell the items that carry a `parsed` payload from the ones that carry a `parser_error`.
    """
    OK = "OK"
    """The transaction was found and parsed — `parsed` is populated."""
    ERROR = "ERROR"
    """The item could not be parsed (e.g. invalid or unknown signature) — `parser_error` is populated."""


class HeliusParsedEventsSummaryType(CyholeParam):
    """
    Summary types assigned by the Parsed Events API to a transaction or to a single instruction.

    Compare against the `type` attribute of a
    [`ParsedEventsSummary`][cyhole.helius.schema.ParsedEventsSummary].

    The set is **not closed**: Helius documents the first six values as the "current" ones and
    keeps adding parsers, and the API already returns values outside the documented list
    (`token_mint` was observed on mainnet). Treat an unknown string as a valid, newer type
    rather than as an error — which is why the schema types the field as a plain `str`.
    """
    SWAP = "swap"
    """A token swap; `parsed_data` carries the venue, the direction and the amounts."""
    TRANSFER = "transfer"
    """A native SOL or SPL token transfer."""
    ADD_LIQUIDITY = "add_liquidity"
    """Liquidity deposited into a pool."""
    REMOVE_LIQUIDITY = "remove_liquidity"
    """Liquidity withdrawn from a pool."""
    CREATE_ACCOUNT = "create_account"
    """A System Program account creation."""
    CREATE_TOKEN_ACCOUNT = "create_token_account"
    """An SPL token account creation."""
    TOKEN_MINT = "token_mint"
    """A token mint operation. Observed on mainnet, not listed in the Helius documentation."""

