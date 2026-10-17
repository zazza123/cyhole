"""Schemas for the Helius RPC methods: getTransactionsForAddress, getSignaturesForAddress, getTransaction, getAccountInfo and getMultipleAccounts."""

from typing import Any

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
            Always present. Helius also returns it from `getSignaturesForAddress` and
            `getTransaction`, where it is not part of the standard Solana response.
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


# ─── getSignaturesForAddress schemas ───────────────────────────────────────────

class PostGetSignaturesForAddressBody(BaseModel):
    """
    Request body (the `config` object) for the standard Solana `getSignaturesForAddress`
    RPC method.

    The queried `address` is passed as the first positional parameter of the JSON-RPC
    call and is therefore handled separately by the
    [`Helius._post_get_signatures_for_address`][cyhole.helius.interaction.Helius._post_get_signatures_for_address]
    method; every field of this body model is optional.

    Results are always returned newest first; walk further back in time by passing the
    last signature of a page as `before` on the next call.

    Attributes:
        limit: maximum number of signatures returned, between `1` and `1000`.
            API default: `1000`.
        before: base58-encoded transaction signature to start searching backwards from
            (exclusive). `None` starts from the most recent confirmed transaction.
        until: base58-encoded transaction signature to stop at (exclusive): the search
            stops **before** reaching it, so the signature itself is not returned.
            `None` searches until `limit` is reached or the history ends.
        commitment: data commitment level. Accepts the values of
            [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment] (`"finalized"`,
            `"confirmed"`). API default: `"finalized"` (`"processed"` is **not** supported).
        min_context_slot: minimum slot at which the request may be evaluated.
            `None` means no constraint.
    """
    model_config = ConfigDict(populate_by_name = True)

    limit: int | None = Field(default = None, ge = 1, le = 1000)
    before: str | None = None
    until: str | None = None
    commitment: str | None = None
    min_context_slot: int | None = Field(default = None, alias = "minContextSlot")


class SignatureForAddressItem(BaseModel):
    """
    A single signature record returned by `getSignaturesForAddress`.

    It identifies one transaction that referenced the queried address, without its
    payload; fetch the full transaction with `getTransaction` when needed.

    Attributes:
        signature: base58-encoded transaction signature.
        slot: slot containing the block with this transaction.
        err: transaction error, or `None` if the transaction succeeded. Its shape follows
            Solana's `TransactionError`: a string (e.g. `"AccountInUse"`) or an object
            (e.g. `{"InstructionError": [0, {"Custom": 1}]}`).
        memo: memo attached to the transaction, or `None` if no memo is present.
        block_time: estimated production time as a Unix timestamp (seconds).
            `None` when the block time is not available.
        confirmation_status: cluster confirmation status of the transaction
            (`"processed"`, `"confirmed"`, `"finalized"`). `None` when the node does
            not report it.
        transaction_index: zero-based index of the transaction within its block.
            Returned by Helius on top of the standard Solana fields; `None` when the
            node does not report it.
    """
    model_config = ConfigDict(populate_by_name = True)

    signature: str
    slot: int
    err: Any | None = None
    memo: str | None = None
    block_time: int | None = Field(default = None, alias = "blockTime")
    confirmation_status: str | None = Field(default = None, alias = "confirmationStatus")
    transaction_index: int | None = Field(default = None, alias = "transactionIndex")


class PostGetSignaturesForAddressResponse(BaseModel):
    """
    JSON-RPC 2.0 response for the `getSignaturesForAddress` RPC method.

    Attributes:
        jsonrpc: JSON-RPC protocol version (`"2.0"`).
        id: identifier of the request this response answers.
        result: signatures of the transactions that referenced the address, newest
            first. Empty when the address has no transactions in the requested range.
    """
    jsonrpc: str
    id: str | int
    result: list[SignatureForAddressItem]


# ─── getTransaction schemas ────────────────────────────────────────────────────

class PostGetTransactionBody(BaseModel):
    """
    Request body (the `config` object) for the standard Solana `getTransaction` RPC method.

    The `signature` is passed as the first positional parameter of the JSON-RPC call and
    is therefore handled separately by the
    [`Helius._post_get_transaction`][cyhole.helius.interaction.Helius._post_get_transaction]
    method; every field of this body model is optional.

    Attributes:
        encoding: encoding of the returned `transaction`. Accepts `"json"` or
            `"jsonParsed"` from [`HeliusEncoding`][cyhole.helius.param.HeliusEncoding].
            API default: `"json"`. `"jsonParsed"` decodes the instructions of known
            programs (System, SPL Token, ...). The binary encodings (`"base58"`,
            `"base64"`) return the transaction as a `[data, encoding]` array, which
            [`TransactionWithMeta`][cyhole.helius.schema.TransactionWithMeta] does not
            model: do not use them with this method.
        commitment: data commitment level. Accepts the values of
            [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment] (`"finalized"`,
            `"confirmed"`). API default: `"finalized"` (`"processed"` is **not** supported).
        max_supported_transaction_version: highest transaction version to return. Set it
            to `0` to receive both legacy and versioned (v0) transactions. When `None`,
            only legacy transactions are returned and requesting a versioned one makes
            the RPC answer with an error instead of a result.
    """
    model_config = ConfigDict(populate_by_name = True)

    encoding: str | None = None
    commitment: str | None = None
    max_supported_transaction_version: int | None = Field(default = None, alias = "maxSupportedTransactionVersion")


class TransactionMeta(BaseModel):
    """
    Status metadata of a confirmed transaction returned by `getTransaction`
    (Solana's `meta` object).

    Balances are expressed in lamports (1 SOL = 10^9 lamports) and listed in the same
    order as the transaction's account keys. Fields not modelled here are ignored.

    Attributes:
        err: transaction error, or `None` if the transaction succeeded. Its shape follows
            Solana's `TransactionError`: a string or an object such as
            `{"InstructionError": [0, {"Custom": 1}]}`.
        status: legacy status object (`{"Ok": null}` or `{"Err": ...}`), deprecated by
            Solana in favour of `err`. `None` when not reported.
        fee: fee charged for the transaction, in lamports.
        pre_balances: account balances before the transaction was processed, in lamports.
        post_balances: account balances after the transaction was processed, in lamports.
        pre_token_balances: SPL token balances before the transaction, one object per
            token account touched (`accountIndex`, `mint`, `owner`, `programId`,
            `uiTokenAmount`). `None` when balance recording was disabled.
        post_token_balances: SPL token balances after the transaction, same shape as
            `pre_token_balances`. `None` when balance recording was disabled.
        inner_instructions: instructions invoked by the transaction's programs (CPIs),
            grouped by the index of the top-level instruction that issued them. `None`
            when inner-instruction recording was disabled.
        log_messages: program log lines emitted during execution. `None` when log
            recording was disabled.
        rewards: rewards credited in this transaction (`pubkey`, `lamports`,
            `postBalance`, `rewardType`, `commission`). `None` when not reported.
        loaded_addresses: accounts loaded from address lookup tables by a versioned
            transaction, as `{"writable": [...], "readonly": [...]}`. `None` for
            transactions that predate the field.
        return_data: data returned by the last program that called `set_return_data`,
            as `{"programId": ..., "data": [base64, "base64"]}`. `None` when no program
            returned data.
        compute_units_consumed: compute units consumed by the transaction. `None` for
            transactions that predate the field.
        cost_units: cost units the scheduler charged to the block for the transaction.
            `None` when not reported.
    """
    model_config = ConfigDict(populate_by_name = True)

    err: Any | None = None
    status: dict[str, Any] | None = None
    fee: int
    pre_balances: list[int] = Field(alias = "preBalances")
    post_balances: list[int] = Field(alias = "postBalances")
    pre_token_balances: list[dict[str, Any]] | None = Field(default = None, alias = "preTokenBalances")
    post_token_balances: list[dict[str, Any]] | None = Field(default = None, alias = "postTokenBalances")
    inner_instructions: list[dict[str, Any]] | None = Field(default = None, alias = "innerInstructions")
    log_messages: list[str] | None = Field(default = None, alias = "logMessages")
    rewards: list[dict[str, Any]] | None = None
    loaded_addresses: dict[str, Any] | None = Field(default = None, alias = "loadedAddresses")
    return_data: dict[str, Any] | None = Field(default = None, alias = "returnData")
    compute_units_consumed: int | None = Field(default = None, alias = "computeUnitsConsumed")
    cost_units: int | None = Field(default = None, alias = "costUnits")


class TransactionWithMeta(BaseModel):
    """
    A confirmed transaction returned by `getTransaction`, with its status metadata.

    Attributes:
        slot: slot this transaction was processed in.
        block_time: estimated production time as a Unix timestamp (seconds).
            `None` when the block time is not available.
        version: transaction version: `"legacy"` for legacy transactions, `0` for
            versioned (v0) transactions. `None` when `max_supported_transaction_version`
            was not set in the request.
        transaction_index: zero-based index of the transaction within its block.
            Returned by Helius on top of the standard Solana fields; `None` when the
            node does not report it.
        transaction: the transaction itself (`signatures` and `message`, with account
            keys, recent blockhash and instructions). Kept as a plain dictionary because
            its shape depends on the requested `encoding`: with `"jsonParsed"` the
            account keys are objects and known instructions carry a `parsed` field.
        meta: transaction status metadata — see
            [`TransactionMeta`][cyhole.helius.schema.TransactionMeta]. `None` when the
            node did not record it.
    """
    model_config = ConfigDict(populate_by_name = True)

    slot: int
    block_time: int | None = Field(default = None, alias = "blockTime")
    version: int | str | None = None
    transaction_index: int | None = Field(default = None, alias = "transactionIndex")
    transaction: dict[str, Any]
    meta: TransactionMeta | None = None


class PostGetTransactionResponse(BaseModel):
    """
    JSON-RPC 2.0 response for the `getTransaction` RPC method.

    Attributes:
        jsonrpc: JSON-RPC protocol version (`"2.0"`).
        id: identifier of the request this response answers.
        result: the confirmed transaction, or `None` when the signature is not found
            (unknown signature, or a transaction not yet confirmed at the requested
            commitment). The field is required: a JSON-RPC error answer, which carries
            no `result`, fails validation instead of reading as "not found".
    """
    jsonrpc: str
    id: str | int
    result: TransactionWithMeta | None


# ─── getAccountInfo / getMultipleAccounts schemas ──────────────────────────────

class AccountDataSlice(BaseModel):
    """
    Part of the account data to return, for the `getAccountInfo` and
    `getMultipleAccounts` RPC methods. Only available with the binary encodings.

    Attributes:
        offset: byte offset where the returned data starts.
        length: number of bytes to return.
    """
    offset: int = Field(ge = 0)
    length: int = Field(ge = 0)


class PostGetAccountInfoBody(BaseModel):
    """
    Request body (the `config` object) for the standard Solana `getAccountInfo` and
    `getMultipleAccounts` RPC methods.

    The address (or the list of addresses) is passed as the first positional parameter
    of the JSON-RPC call and is therefore handled separately by the
    [`Helius._post_get_account_info`][cyhole.helius.interaction.Helius._post_get_account_info]
    method; every field of this body model is optional.

    Attributes:
        encoding: encoding of the returned account `data`. Accepts the values of
            [`HeliusAccountEncoding`][cyhole.helius.param.HeliusAccountEncoding]
            (`"base58"`, `"base64"`, `"base64+zstd"`, `"jsonParsed"`). API default:
            `"base58"`, which fails on accounts larger than 129 bytes: set it explicitly.
        commitment: data commitment level. Accepts the values of
            [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment]. API default:
            `"finalized"`.
        data_slice: return only part of the data — see
            [`AccountDataSlice`][cyhole.helius.schema.AccountDataSlice]. `None` returns
            the whole data. Only available with the binary encodings.
        min_context_slot: minimum slot the request can be evaluated at. `None` if not used.
    """
    model_config = ConfigDict(populate_by_name = True)

    encoding: str | None = None
    commitment: str | None = None
    data_slice: AccountDataSlice | None = Field(default = None, alias = "dataSlice")
    min_context_slot: int | None = Field(default = None, alias = "minContextSlot")


class RpcResponseContext(BaseModel):
    """
    Context of a standard Solana RPC answer: the slot the answer was read at.

    Attributes:
        slot: slot at which the node evaluated the request.
        api_version: version of the node software. `None` when the node does not report it.
    """
    model_config = ConfigDict(populate_by_name = True)

    slot: int
    api_version: str | None = Field(default = None, alias = "apiVersion")


class AccountInfo(BaseModel):
    """
    State of one Solana account, as returned by `getAccountInfo` and `getMultipleAccounts`.

    Attributes:
        lamports: balance of the account in lamports (1 SOL = 10^9 lamports).
        owner: base58-encoded address of the program that owns the account.
        data: the account data. A `[data, encoding]` pair for the binary encodings
            (`"base58"`, `"base64"`, `"base64+zstd"`); a JSON object with `program`,
            `parsed` and `space` for `"jsonParsed"` when the node can decode the account,
            otherwise the base64 pair; a plain string for legacy binary answers.
        executable: whether the account holds a program.
        rent_epoch: epoch at which the account next owes rent. Rent-exempt accounts
            report the u64 maximum (`18446744073709551615`).
        space: size of the account data in bytes. `None` when the node does not report it.
    """
    model_config = ConfigDict(populate_by_name = True)

    lamports: int
    owner: str
    data: list[str] | dict[str, Any] | str
    executable: bool
    rent_epoch: int = Field(alias = "rentEpoch")
    space: int | None = None


class AccountInfoResult(BaseModel):
    """
    Result of the `getAccountInfo` RPC method.

    Attributes:
        context: slot the answer was read at — see
            [`RpcResponseContext`][cyhole.helius.schema.RpcResponseContext].
        value: the account — see [`AccountInfo`][cyhole.helius.schema.AccountInfo] — or
            `None` when the account does not exist (never funded, or closed).
    """
    context: RpcResponseContext
    value: AccountInfo | None


class PostGetAccountInfoResponse(BaseModel):
    """
    JSON-RPC 2.0 response for the `getAccountInfo` RPC method.

    Attributes:
        jsonrpc: JSON-RPC protocol version (`"2.0"`).
        id: identifier of the request this response answers.
        result: context and account — see
            [`AccountInfoResult`][cyhole.helius.schema.AccountInfoResult]. The field is
            required: a JSON-RPC error answer, which carries no `result`, fails validation
            instead of reading as a missing account.
    """
    jsonrpc: str
    id: str | int
    result: AccountInfoResult
