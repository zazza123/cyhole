"""Schemas for the Parsed Events endpoints (transactions, transaction-history)."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel


# ─── Parsed Events schemas ─────────────────────────────────────────────────────

class PostParsedEventsRange(BaseModel):
    """
    Open or closed numeric interval used to bound a Parsed Events history query,
    either by slot or by block time.

    Set at most one lower bound (`gt` or `gte`) and at most one upper bound
    (`lt` or `lte`). Omitted bounds apply no constraint on that side.

    Attributes:
        gt: strictly greater than this value. `None` means no exclusive lower bound.
        gte: greater than or equal to this value. `None` means no inclusive lower bound.
        lt: strictly less than this value. `None` means no exclusive upper bound.
        lte: less than or equal to this value. `None` means no inclusive upper bound.
    """
    gt: int | None = None
    gte: int | None = None
    lt: int | None = None
    lte: int | None = None


class PostParsedEventsTransactionHistoryBody(BaseModel):
    """
    Request body for the Parsed Events **transaction-history** endpoint.

    Only `address` is required. Use
    [`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder] and
    [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment] for the corresponding `.value` strings.

    Attributes:
        address: base58-encoded Solana address whose history is fetched (wallet, program,
            mint, pool or token account).
        limit: maximum number of transactions to return, in the range `1`-`100`.
            `None` uses the API default (`100`).
        before_signature: return only transactions older than this signature.
            `None` means no upper signature bound. Prefer `pagination_token` to page.
        after_signature: return only transactions newer than this signature.
            `None` means no lower signature bound.
        pagination_token: cursor taken from the `pagination_token` of the previous response,
            used to fetch the next page. `None` fetches the first page.
        sort_order: result ordering — `"desc"` (newest first, API default) or `"asc"`.
            `None` uses the API default.
        commitment: block finality level — `"confirmed"` (API default) or `"finalized"`.
            `"processed"` is not supported. `None` uses the API default.
        include_raw_transaction: when `True`, every result also carries the original Solana
            transaction payload in `raw_transaction`. `None` uses the API default (`False`).
        slot: restrict the history to a slot interval. `None` means no slot bound.
        time: restrict the history to a block-time interval, in Unix seconds.
            `None` means no time bound.
    """
    model_config = ConfigDict(populate_by_name = True)

    address: str
    limit: int | None = None
    before_signature: str | None = Field(default = None, alias = "beforeSignature")
    after_signature: str | None = Field(default = None, alias = "afterSignature")
    pagination_token: str | None = Field(default = None, alias = "paginationToken")
    sort_order: str | None = Field(default = None, alias = "sortOrder")
    commitment: str | None = None
    include_raw_transaction: bool | None = Field(default = None, alias = "includeRawTransaction")
    slot: PostParsedEventsRange | None = None
    time: PostParsedEventsRange | None = None


class ParsedEventsNativeTransfer(BaseModel):
    """
    A native SOL movement detected in a parsed transaction.

    Covers System Program `transfer` and `create_account` instructions, plus the
    lamports returned to the destination when an SPL token account is closed.

    Attributes:
        from_user_account: account sending the lamports. `None` when there is no sender side.
        to_user_account: account receiving the lamports. `None` when there is no recipient side.
        amount: amount moved, in lamports (1 SOL = 1,000,000,000 lamports).
    """
    model_config = ConfigDict(populate_by_name = True)

    from_user_account: str | None = Field(default = None, alias = "fromUserAccount")
    to_user_account: str | None = Field(default = None, alias = "toUserAccount")
    amount: int


class ParsedEventsTokenTransfer(BaseModel):
    """
    An SPL Token or Token-2022 movement detected in a parsed transaction.

    Covers transfers, burns and mints (`transfer`, `transfer_checked`,
    `transfer_checked_with_fee`, `burn`, `burn_checked`, `mint_to`, `mint_to_checked`).
    Zero-amount transfers are omitted by the API.

    Unlike the legacy Enhanced Transactions API, the amount is **not** UI-scaled:
    divide `raw_token_amount` by `10 ** decimals` to obtain the human-readable quantity.

    Attributes:
        from_user_account: owner or authority of the source side. `None` when unknown or
            when there is no source (mint rows).
        to_user_account: owner of the destination side. `None` when unknown or when there
            is no destination (burn rows).
        from_token_account: source token account. `None` for mint rows.
        to_token_account: destination token account. `None` for burn rows.
        raw_token_amount: amount moved as a raw integer, in the mint's smallest unit.
        decimals: number of decimals of the mint, used to interpret `raw_token_amount`.
        token_standard: token standard when known (e.g. `"Fungible"`, `"UnknownStandard"`).
        mint: token mint address.
    """
    model_config = ConfigDict(populate_by_name = True)

    from_user_account: str | None = Field(default = None, alias = "fromUserAccount")
    to_user_account: str | None = Field(default = None, alias = "toUserAccount")
    from_token_account: str | None = Field(default = None, alias = "fromTokenAccount")
    to_token_account: str | None = Field(default = None, alias = "toTokenAccount")
    raw_token_amount: int = Field(alias = "rawTokenAmount")
    decimals: int
    token_standard: str | None = Field(default = None, alias = "tokenStandard")
    mint: str


class ParsedEventsSummary(BaseModel):
    """
    Human-readable classification of a transaction, or of one of its instructions.

    The same shape is used at transaction level and at instruction level.

    Attributes:
        type: summary type, e.g. `"swap"` or `"transfer"`. See
            [`HeliusParsedEventsSummaryType`][cyhole.helius.param.HeliusParsedEventsSummaryType]
            for the known values; the set is open, so unknown strings are valid.
        description: English sentence describing what happened.
        parsed_data: structured data behind the summary, whose keys depend on `type` and on the
            protocol. For a `swap` it carries `protocol`, `kind`, `in_amount`,
            `actual_out_amount`, `input_mint`, `output_mint` and `inner_swaps` (amounts are
            raw integers encoded as strings). `None` for the types that carry no structured
            data, such as a plain `transfer`.
    """
    model_config = ConfigDict(populate_by_name = True)

    type: str
    description: str | None = None
    parsed_data: dict[str, Any] | None = Field(default = None, alias = "parsedData")


class ParsedEventsDecodedAccount(BaseModel):
    """
    An account of a decoded instruction, labelled with its name in the program IDL.

    Attributes:
        name: account name as declared in the program IDL, in snake_case (e.g. `"pool"`).
        pubkey: base58-encoded account address.
        is_signer: whether the account signed the transaction.
        is_writable: whether the instruction may write to the account.
    """
    model_config = ConfigDict(populate_by_name = True)

    name: str
    pubkey: str
    is_signer: bool = Field(alias = "isSigner")
    is_writable: bool = Field(alias = "isWritable")


class ParsedEventsDecodedInstruction(BaseModel):
    """
    Arguments and accounts of an instruction decoded against its program IDL.

    Attributes:
        args: decoded arguments keyed by their snake_case IDL name. 64-bit integers are
            usually encoded as strings. `None` when the arguments could not be decoded.
        accounts: decoded accounts in instruction order, each labelled with its IDL name.
            `None` when the accounts could not be labelled — the positional list is always
            available in the instruction's `raw_accounts`.
    """
    args: dict[str, Any] | None = None
    accounts: list[ParsedEventsDecodedAccount] | None = None


class ParsedEventsInstruction(BaseModel):
    """
    A single instruction of a parsed transaction.

    The API returns top-level and inner (CPI) instructions in **one flat list**, in
    execution order. An inner instruction is recognised by a non-`None`
    `inner_instruction_index`; its parent is the top-level instruction sharing the same
    `instruction_index`.

    Attributes:
        instruction_index: index of the top-level instruction this entry belongs to.
        inner_instruction_index: position within the parent's inner instructions.
            `None` for a top-level instruction.
        stack_height: call-stack depth (`1` for top-level). `None` when not available.
        program_id: address of the program that executed the instruction.
        program_name: program name known to the parser (e.g. `"pump_amm"`, `"token"`).
            `None` when the program is not in the parser's catalogue.
        instruction_name: decoded instruction name (e.g. `"create_pool"`, `"initialize_mint_2"`).
            `None` when the instruction could not be decoded.
        raw_accounts: account addresses passed to the instruction, in positional order.
        raw_data: raw instruction data, base58-encoded.
        summary: instruction-level summary. `None` when the parser has none for this instruction.
        decoded: decoded arguments and named accounts. `None` when decoding did not succeed.
    """
    model_config = ConfigDict(populate_by_name = True)

    instruction_index: int = Field(alias = "instructionIndex")
    inner_instruction_index: int | None = Field(default = None, alias = "innerInstructionIndex")
    stack_height: int | None = Field(default = None, alias = "stackHeight")
    program_id: str = Field(alias = "programId")
    program_name: str | None = Field(default = None, alias = "programName")
    instruction_name: str | None = Field(default = None, alias = "instructionName")
    raw_accounts: list[str] = Field(default_factory = list, alias = "rawAccounts")
    raw_data: str | None = Field(default = None, alias = "rawData")
    summary: ParsedEventsSummary | None = None
    decoded: ParsedEventsDecodedInstruction | None = None


class ParsedEventsDecodedError(BaseModel):
    """
    A custom program error decoded from a failed transaction.

    Attributes:
        instruction_index: index of the top-level instruction that failed.
        program_id: address of the program that raised the error.
        program_name: name of that program. `None` when not known to the parser.
        code: numeric custom error code.
        name: error name as declared by the program.
        msg: error message declared by the program. `None` when the program declares none.
    """
    model_config = ConfigDict(populate_by_name = True)

    instruction_index: int = Field(alias = "instructionIndex")
    program_id: str = Field(alias = "programId")
    program_name: str | None = Field(default = None, alias = "programName")
    code: int
    name: str
    msg: str | None = None


class ParsedEventsTransaction(BaseModel):
    """
    A transaction parsed by the Helius Parsed Events API.

    It is the successor of [`EnhancedTransaction`][cyhole.helius.schema.EnhancedTransaction].
    The transfer arrays keep the same meaning; the classification moves from `type` / `source`
    to `summary`, there is no per-account balance delta, and instructions come as a flat,
    decoded list instead of a nested one.

    Attributes:
        slot: slot of the block containing the transaction.
        block_time: block production time as a Unix timestamp (seconds). `None` when not available.
        fee: transaction fee, in lamports.
        fee_payer: address that paid the fee (the first account key). `None` when not available.
        transaction_status: on-chain execution outcome, `"OK"` or `"ERROR"`. Not to be confused
            with the parsing outcome of the enclosing result.
        error: raw execution error as returned by the chain. `None` for successful transactions.
        decoded_error: custom program error decoded from `error`. `None` for successful
            transactions and when the error could not be decoded.
        native_transfers: native SOL movements detected in the transaction. Empty when none.
        token_transfers: SPL Token and Token-2022 movements detected in the transaction.
            Empty when none.
        summary: best transaction-level summary. `None` when the parser could not classify
            the transaction (the equivalent of the legacy type `"UNKNOWN"`).
        instructions: every top-level and inner instruction, in execution order.
    """
    model_config = ConfigDict(populate_by_name = True)

    slot: int
    block_time: int | None = Field(default = None, alias = "blockTime")
    fee: int
    fee_payer: str | None = Field(default = None, alias = "feePayer")
    transaction_status: str = Field(alias = "transactionStatus")
    error: Any | None = None
    decoded_error: ParsedEventsDecodedError | None = Field(default = None, alias = "decodedError")
    native_transfers: list[ParsedEventsNativeTransfer] = Field(default_factory = list, alias = "nativeTransfers")
    token_transfers: list[ParsedEventsTokenTransfer] = Field(default_factory = list, alias = "tokenTransfers")
    summary: ParsedEventsSummary | None = None
    instructions: list[ParsedEventsInstruction] = Field(default_factory = list)


class ParsedEventsParserError(BaseModel):
    """
    Reason why a single item of a Parsed Events response could not be parsed.

    Attributes:
        code: machine-readable error code (e.g. `"invalid_signature"`, `"transaction_not_found"`).
        message: human-readable explanation.
    """
    code: str
    message: str | None = None


class ParsedEventsTransactionResult(BaseModel):
    """
    One item of a Parsed Events response: a signature together with either its parsed
    transaction or the reason it could not be parsed.

    A failure is reported per item and never fails the whole request, so always check
    `parser_status` before reading `parsed`.

    Attributes:
        signature: base58-encoded transaction signature this result refers to.
        parser_status: parsing outcome — see
            [`HeliusParserStatus`][cyhole.helius.param.HeliusParserStatus].
        parsed: the parsed transaction. `None` when `parser_status` is `"ERROR"`.
        parser_error: why the item was not parsed. `None` when `parser_status` is `"OK"`.
        raw_transaction: original Solana transaction payload. `None` unless the request
            set `include_raw_transaction`.
    """
    model_config = ConfigDict(populate_by_name = True)

    signature: str
    parser_status: str = Field(alias = "parserStatus")
    parsed: ParsedEventsTransaction | None = None
    parser_error: ParsedEventsParserError | None = Field(default = None, alias = "parserError")
    raw_transaction: dict[str, Any] | None = Field(default = None, alias = "rawTransaction")


class PostParsedEventsTransactionsResponse(RootModel[list[ParsedEventsTransactionResult]]):
    """
    Response for the Parsed Events **transactions** endpoint.

    Wraps a list of [`ParsedEventsTransactionResult`][cyhole.helius.schema.ParsedEventsTransactionResult]
    objects, one per signature submitted, in input order (duplicates included).
    Access the results via `.root`.
    """


class PostParsedEventsTransactionHistoryResponse(BaseModel):
    """
    Response for the Parsed Events **transaction-history** endpoint.

    Attributes:
        data: one result per transaction of the queried address, ordered as requested by
            `sort_order` (newest first by default).
        pagination_token: cursor to pass as `pagination_token` in the next request body to
            fetch the following page. `None` when the end of the available history was reached.
    """
    model_config = ConfigDict(populate_by_name = True)

    data: list[ParsedEventsTransactionResult] = Field(default_factory = list)
    pagination_token: str | None = Field(default = None, alias = "paginationToken")
