"""Schemas for the Helius RPC transaction-history endpoint getTransactionsForAddress."""

from pydantic import BaseModel, ConfigDict, Field

from .common import HeliusComparisonFilter, HeliusSignatureComparisonFilter


# ─── getTransactionsForAddress schemas ─────────────────────────────────────────

class PostGetTransactionsForAddressFilters(BaseModel):
    """
    Optional filters for the `getTransactionsForAddress` RPC method.

    Attributes:
        slot: filter by slot number using numeric comparison operators. `None` if not used.
        block_time: filter by block timestamp in Unix seconds. `None` if not used.
            This filter additionally accepts the `eq` operator on
            [`HeliusComparisonFilter`][cyhole.helius.schema.HeliusComparisonFilter] for exact matches.
        signature: filter by transaction signature with lexicographic comparison. `None` if not used.
        status: filter by transaction success/failure. Accepts the values of
            [`HeliusTransactionStatus`][cyhole.helius.param.HeliusTransactionStatus]
            (`"succeeded"`, `"failed"`, `"any"`). `None` means no status filter (defaults to `"any"`).
        token_accounts: include transactions for token accounts owned by the
            queried address. Accepts the values of
            [`HeliusTokenAccountFilter`][cyhole.helius.param.HeliusTokenAccountFilter]
            (`"none"`, `"balanceChanged"`, `"all"`). API default: `"none"`.
            Not supported for transactions older than December 2022.
    """
    model_config = ConfigDict(populate_by_name = True)

    slot: HeliusComparisonFilter | None = None
    block_time: HeliusComparisonFilter | None = Field(default = None, alias = "blockTime")
    signature: HeliusSignatureComparisonFilter | None = None
    status: str | None = None
    token_accounts: str | None = Field(default = None, alias = "tokenAccounts")


class PostGetTransactionsForAddressBody(BaseModel):
    """
    Request body (the `config` object) for the `getTransactionsForAddress` RPC method.

    The queried `address` is passed as the first positional parameter of the JSON-RPC
    call and is therefore handled separately by the
    [`Helius._post_get_transactions_for_address`][cyhole.helius.interaction.Helius._post_get_transactions_for_address]
    method; every field of this body model is optional.

    Attributes:
        transaction_details: level of detail returned for each transaction. Accepts the
            values of [`HeliusTransactionDetails`][cyhole.helius.param.HeliusTransactionDetails]
            (`"signatures"`, `"full"`). API default: `"signatures"`. Use `"full"` to obtain
            the complete transaction payload in a single call; full mode is billed per
            100 transactions returned, so a large `limit` costs proportionally more.
        sort_order: result ordering. Accepts the values of
            [`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder] (`"desc"`, `"asc"`).
            API default: `"desc"` (newest first).
        limit: maximum number of transactions returned. Up to `1000` in both
            `"signatures"` and `"full"` mode. API default: `1000`.
        pagination_token: cursor from the previous response — pass the value received
            in `result.pagination_token` (format `"slot:position"`) to fetch the next page.
        commitment: data commitment level. Accepts the values of
            [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment] (`"finalized"`,
            `"confirmed"`). API default: `"finalized"` (`"processed"` is **not** supported).
        filters: advanced filters — see
            [`PostGetTransactionsForAddressFilters`][cyhole.helius.schema.PostGetTransactionsForAddressFilters].
        encoding: encoding format for the transaction payload — only meaningful when
            `transaction_details = "full"`. Accepts the values of
            [`HeliusEncoding`][cyhole.helius.param.HeliusEncoding]
            (`"json"`, `"jsonParsed"`, `"base64"`, `"base58"`).
        max_supported_transaction_version: maximum transaction version to return.
            When `None`, the API only returns legacy transactions; set to `0` to include
            all versioned transactions.
        min_context_slot: minimum slot at which the request may be evaluated.
    """
    model_config = ConfigDict(populate_by_name = True)

    transaction_details: str | None = Field(default = None, alias = "transactionDetails")
    sort_order: str | None = Field(default = None, alias = "sortOrder")
    limit: int | None = None
    pagination_token: str | None = Field(default = None, alias = "paginationToken")
    commitment: str | None = None
    filters: PostGetTransactionsForAddressFilters | None = None
    encoding: str | None = None
    max_supported_transaction_version: int | None = Field(default = None, alias = "maxSupportedTransactionVersion")
    min_context_slot: int | None = Field(default = None, alias = "minContextSlot")


class TransactionForAddressItem(BaseModel):
    """
    A single transaction record returned by `getTransactionsForAddress`.

    Fields populated depend on the `transaction_details` mode requested:

    * `"signatures"` mode (API default) populates `signature`, `err`, `memo`, and `confirmation_status`.
    * `"full"` mode populates `transaction` and `meta` instead.

    Fields outside the active mode are `None`.

    Attributes:
        slot: slot containing the block with this transaction. Always present.
        transaction_index: zero-based index of the transaction within its block.
            Always present; unique to `getTransactionsForAddress` (not exposed by
            `getSignaturesForAddress` / `getTransaction`).
        block_time: estimated production time as a Unix timestamp (seconds).
            `None` when the block time cannot be determined.
        signature: base58-encoded transaction signature. Populated only in `"signatures"` mode.
        err: transaction error object, or `None` if the transaction succeeded.
            Populated only in `"signatures"` mode.
        memo: memo attached to the transaction, or `None` if no memo. Populated only
            in `"signatures"` mode.
        confirmation_status: cluster confirmation status (`"finalized"`, `"confirmed"`).
            Populated only in `"signatures"` mode.
        transaction: full transaction payload (message, signatures, instructions) in the
            shape returned by Solana's `getTransaction` RPC method. Populated only in
            `"full"` mode. Encoding follows the body's `encoding` parameter.
        meta: transaction metadata (fee, pre/post balances, inner instructions, log
            messages, etc.) in the shape returned by Solana's `getTransaction` RPC
            method. Populated only in `"full"` mode.
    """
    model_config = ConfigDict(populate_by_name = True)

    slot: int
    transaction_index: int = Field(alias = "transactionIndex")
    block_time: int | None = Field(default = None, alias = "blockTime")
    signature: str | None = None
    err: dict | None = None
    memo: str | None = None
    confirmation_status: str | None = Field(default = None, alias = "confirmationStatus")
    transaction: dict | None = None
    meta: dict | None = None


class TransactionForAddressList(BaseModel):
    """
    Paginated list of transactions returned inside the `getTransactionsForAddress`
    JSON-RPC result.

    Attributes:
        data: list of transaction items for the current page, ordered as requested
            by `sort_order`.
        pagination_token: cursor (format `"slot:position"`) to retrieve the next page,
            or `None` when no further pages remain.
    """
    model_config = ConfigDict(populate_by_name = True)

    data: list[TransactionForAddressItem]
    pagination_token: str | None = Field(default = None, alias = "paginationToken")


class PostGetTransactionsForAddressResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getTransactionsForAddress` RPC method."""
    jsonrpc: str
    id: str | int
    result: TransactionForAddressList
