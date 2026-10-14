"""Schemas for the getTransfersByAddress endpoint."""

from pydantic import BaseModel, ConfigDict, Field

from .common import HeliusComparisonFilter


# ─── getTransfersByAddress schemas ─────────────────────────────────────────────


class PostGetTransfersByAddressFilters(BaseModel):
    """
    Optional numeric filters for the `getTransfersByAddress` RPC method.

    Attributes:
        amount: filter by raw transfer amount (not UI amount). `None` means no constraint on amount.
        block_time: filter by block timestamp in Unix seconds. `None` means no time bound.
        slot: filter by slot number. `None` means no slot bound.
    """
    model_config = ConfigDict(populate_by_name = True)

    amount: HeliusComparisonFilter | None = None
    block_time: HeliusComparisonFilter | None = Field(default = None, alias = "blockTime")
    slot: HeliusComparisonFilter | None = None


class PostGetTransfersByAddressBody(BaseModel):
    """
    Request body (the `config` object) for the `getTransfersByAddress` RPC method.

    The owner `address` is passed as the first positional parameter of the JSON-RPC
    call and is therefore handled separately by the
    [`Helius._post_get_transfers_by_address`][cyhole.helius.interaction.Helius._post_get_transfers_by_address]
    method; every field of this body model is optional.

    Attributes:
        with_address: counterparty address — return only transfers to or from this wallet.
            `None` means no counterparty filter.
        direction: transfer direction relative to the queried address. Accepts the
            values of [`HeliusTransferDirection`][cyhole.helius.param.HeliusTransferDirection]
            (`"in"`, `"out"`, `"any"`). API default: `"any"`.
        mint: token mint address to filter by. Use `So11111111111111111111111111111111111111111`
            for native SOL and `So11111111111111111111111111111111111111112` for WSOL.
            `None` means no mint filter.
        sol_mode: how native SOL and WSOL are represented. Accepts the values of
            [`HeliusSolMode`][cyhole.helius.param.HeliusSolMode] (`"merged"`, `"separate"`).
            API default: `"merged"` (WSOL is collapsed into native SOL, wrap/unwrap
            lifecycle rows are excluded).
        filters: optional numeric filters for amount, block time, and slot.
        limit: maximum number of transfers returned per page (range `1`–`100`).
            API default: `100`.
        pagination_token: cursor from the previous response — pass the value
            received in `result.pagination_token` to fetch the next page.
        commitment: data commitment level. Accepts the values of
            [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment] (`"finalized"`,
            `"confirmed"`). API default: `"finalized"`.
        sort_order: result ordering. Accepts the values of
            [`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder] (`"desc"`, `"asc"`).
            API default: `"desc"` (newest first).
    """
    model_config = ConfigDict(populate_by_name = True)

    with_address: str | None = Field(default = None, alias = "with")
    direction: str | None = None
    mint: str | None = None
    sol_mode: str | None = Field(default = None, alias = "solMode")
    filters: PostGetTransfersByAddressFilters | None = None
    limit: int | None = None
    pagination_token: str | None = Field(default = None, alias = "paginationToken")
    commitment: str | None = None
    sort_order: str | None = Field(default = None, alias = "sortOrder")


class Transfer(BaseModel):
    """
    A single parsed transfer record returned by the `getTransfersByAddress` RPC method.

    Attributes:
        signature: transaction signature this transfer belongs to.
        slot: slot at which the transaction landed.
        block_time: block timestamp in Unix seconds.
        type: transfer behavior — one of `"transfer"`, `"mint"`, `"burn"`, `"wrap"`,
            `"unwrap"`, `"changeOwner"`, `"withdrawWithheldFee"`.
            See the Helius docs for the exact semantics of each value.
        from_user_account: sender wallet (owner) address. `None` for `mint`, `wrap`
            and `withdrawWithheldFee` rows, where the row has no sender side.
        to_user_account: recipient wallet (owner) address. `None` for `burn` and
            certain `unwrap` rows, where the row has no recipient side.
        from_token_account: source SPL token account address. `None` for native SOL
            transfers or rows where a source token account is not meaningful.
        to_token_account: destination SPL token account address. `None` for native SOL
            transfers or rows where a destination token account is not meaningful.
        mint: token mint address for the transfer. In `solMode: "merged"`, WSOL
            transfers are rewritten to the native SOL mint.
        amount: raw transfer amount as a string (token base units). For Token-2022
            transfers with fees, this is the amount credited to the destination.
        decimals: number of decimal places for the mint.
        ui_amount: human-readable amount (already scaled by `decimals`), returned as a string.
        fee_amount: raw Token-2022 withheld fee as a string. `None` when the transfer
            is not a Token-2022 `TransferCheckedWithFee` (i.e. no fees applied).
        fee_ui_amount: human-readable Token-2022 withheld fee, returned as a string.
            `None` when no fee applies.
        confirmation_status: commitment level at the time of the response —
            `"finalized"` or `"confirmed"`.
        transaction_idx: index of the transaction within its block.
        instruction_idx: index of the originating top-level instruction within the transaction.
        inner_instruction_idx: index of the inner instruction (CPI) within its parent
            top-level instruction.
    """
    model_config = ConfigDict(populate_by_name = True)

    signature: str
    slot: int
    block_time: int = Field(alias = "blockTime")
    type: str
    from_user_account: str | None = Field(default = None, alias = "fromUserAccount")
    to_user_account: str | None = Field(default = None, alias = "toUserAccount")
    from_token_account: str | None = Field(default = None, alias = "fromTokenAccount")
    to_token_account: str | None = Field(default = None, alias = "toTokenAccount")
    mint: str
    amount: str
    decimals: int
    ui_amount: str = Field(alias = "uiAmount")
    fee_amount: str | None = Field(default = None, alias = "feeAmount")
    fee_ui_amount: str | None = Field(default = None, alias = "feeUiAmount")
    confirmation_status: str = Field(alias = "confirmationStatus")
    transaction_idx: int = Field(alias = "transactionIdx")
    instruction_idx: int = Field(alias = "instructionIdx")
    inner_instruction_idx: int = Field(alias = "innerInstructionIdx")


class TransferList(BaseModel):
    """
    Paginated list of parsed transfer rows returned inside the
    `getTransfersByAddress` JSON-RPC result.

    Attributes:
        data: list of transfer rows for the current page, ordered as requested by
            `sort_order`.
        pagination_token: cursor to retrieve the next page, or `None` when no
            further pages remain.
    """
    model_config = ConfigDict(populate_by_name = True)

    data: list[Transfer]
    pagination_token: str | None = Field(default = None, alias = "paginationToken")


# ─── getTransfersByAddress response ───────────────────────────────────────────

class PostGetTransfersByAddressResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getTransfersByAddress` RPC method."""
    jsonrpc: str
    id: str | int
    result: TransferList
