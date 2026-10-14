"""Schemas for the Enhanced Transactions endpoints (getTransactionsByAddress, getTransactions)."""

from pydantic import BaseModel, ConfigDict, Field, RootModel


# ─── getTransactionsByAddress schemas ──────────────────────────────────────────

class GetTransactionsByAddressQuery(BaseModel):
    """
    Query parameters for the `getTransactionsByAddress` Enhanced Transactions REST endpoint.

    All fields are optional. Omitted fields apply no constraint on that dimension.
    Use [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment],
    [`HeliusTokenAccountFilter`][cyhole.helius.param.HeliusTokenAccountFilter], and
    [`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder] for the corresponding `.value` strings.

    Attributes:
        before_signature: paginate backwards — return only transactions that occurred
            before this transaction signature. `None` means no upper signature bound.
        after_signature: paginate forwards — return only transactions that occurred
            after this transaction signature. `None` means no lower signature bound.
        commitment: block finality level (`"finalized"` or `"confirmed"`).
            API default: `"finalized"`. `None` uses the API default.
        token_accounts: include transactions for token accounts owned by the queried
            address (`"none"`, `"balanceChanged"`, or `"all"`). API default: `"none"`.
            `None` uses the API default.
        sort_order: result ordering (`"desc"` or `"asc"`). API default: `"desc"` (newest first).
            `None` uses the API default.
        gt_slot: return only transactions in a slot strictly greater than this value.
            `None` means no lower slot bound.
        gte_slot: return only transactions in a slot greater than or equal to this value.
            `None` means no lower slot bound.
        lt_slot: return only transactions in a slot strictly less than this value.
            `None` means no upper slot bound.
        lte_slot: return only transactions in a slot less than or equal to this value.
            `None` means no upper slot bound.
        gt_time: return only transactions with a block time strictly greater than this
            Unix timestamp (seconds). `None` means no lower time bound.
        gte_time: return only transactions with a block time greater than or equal to
            this Unix timestamp (seconds). `None` means no lower time bound.
        lt_time: return only transactions with a block time strictly less than this
            Unix timestamp (seconds). `None` means no upper time bound.
        lte_time: return only transactions with a block time less than or equal to
            this Unix timestamp (seconds). `None` means no upper time bound.
        source: filter by transaction source (e.g. `"MAGIC_EDEN"`, `"JUPITER"`, `"ORCA"`).
            `None` means no source filter.
        type: filter by transaction type (e.g. `"SWAP"`, `"NFT_SALE"`, `"TRANSFER"`).
            `None` means no type filter.
        limit: maximum number of transactions to return (range `1`–`100`).
            `None` uses the API default.
    """
    model_config = ConfigDict(populate_by_name = True)

    before_signature: str | None = Field(default = None, alias = "before-signature")
    after_signature: str | None = Field(default = None, alias = "after-signature")
    commitment: str | None = None
    token_accounts: str | None = Field(default = None, alias = "token-accounts")
    sort_order: str | None = Field(default = None, alias = "sort-order")
    gt_slot: int | None = Field(default = None, alias = "gt-slot")
    gte_slot: int | None = Field(default = None, alias = "gte-slot")
    lt_slot: int | None = Field(default = None, alias = "lt-slot")
    lte_slot: int | None = Field(default = None, alias = "lte-slot")
    gt_time: int | None = Field(default = None, alias = "gt-time")
    gte_time: int | None = Field(default = None, alias = "gte-time")
    lt_time: int | None = Field(default = None, alias = "lt-time")
    lte_time: int | None = Field(default = None, alias = "lte-time")
    source: str | None = None
    type: str | None = None
    limit: int | None = None


class EnhancedTransactionNativeTransfer(BaseModel):
    """
    A native SOL transfer within an enhanced transaction.

    Attributes:
        from_user_account: sender wallet address. `None` when there is no sender side
            (e.g. validator rewards).
        to_user_account: recipient wallet address. `None` when there is no recipient side.
        amount: transferred amount in lamports (1 SOL = 1,000,000,000 lamports).
    """
    model_config = ConfigDict(populate_by_name = True)

    from_user_account: str | None = Field(default = None, alias = "fromUserAccount")
    to_user_account: str | None = Field(default = None, alias = "toUserAccount")
    amount: int


class EnhancedTransactionTokenTransfer(BaseModel):
    """
    An SPL token transfer within an enhanced transaction.

    Attributes:
        from_user_account: sender wallet (owner) address. `None` for mint rows where
            there is no sender.
        to_user_account: recipient wallet (owner) address. `None` for burn rows where
            there is no recipient.
        from_token_account: source SPL token account address. `None` for native SOL
            transfers or rows where a source account is not meaningful.
        to_token_account: destination SPL token account address. `None` for native SOL
            transfers or rows where a destination account is not meaningful.
        token_amount: transferred amount as a UI-scaled float (already divided by
            the mint's decimal places).
        mint: token mint address.
    """
    model_config = ConfigDict(populate_by_name = True)

    from_user_account: str | None = Field(default = None, alias = "fromUserAccount")
    to_user_account: str | None = Field(default = None, alias = "toUserAccount")
    from_token_account: str | None = Field(default = None, alias = "fromTokenAccount")
    to_token_account: str | None = Field(default = None, alias = "toTokenAccount")
    token_amount: float = Field(alias = "tokenAmount")
    mint: str


class EnhancedTransactionRawTokenAmount(BaseModel):
    """
    Raw token amount with its decimal precision, used inside account-data balance changes.

    Attributes:
        token_amount: token balance in base units (before dividing by `10^decimals`),
            serialised as a string to preserve full precision for large integers.
        decimals: number of decimal places for the mint.
    """
    model_config = ConfigDict(populate_by_name = True)

    token_amount: str = Field(alias = "tokenAmount")
    decimals: int


class EnhancedTransactionTokenBalanceChange(BaseModel):
    """
    A token balance change record within account data, showing how a token account's
    balance shifted as a result of the transaction.

    Attributes:
        user_account: wallet (owner) address of the token account.
        token_account: SPL token account address whose balance changed.
        mint: token mint address.
        raw_token_amount: balance change expressed in base units, with decimal
            precision encoded separately.
    """
    model_config = ConfigDict(populate_by_name = True)

    user_account: str = Field(alias = "userAccount")
    token_account: str = Field(alias = "tokenAccount")
    mint: str
    raw_token_amount: EnhancedTransactionRawTokenAmount = Field(alias = "rawTokenAmount")


class EnhancedTransactionAccountData(BaseModel):
    """
    Account-level balance-change data for one account involved in an enhanced transaction.

    Attributes:
        account: the account's public key.
        native_balance_change: net lamport change for this account. Negative means
            the account paid lamports (e.g. paid the fee or transferred SOL);
            positive means it received lamports.
        token_balance_changes: list of per-token-account balance deltas for this
            account. Empty list when no SPL token balances changed for this account.
            `None` when the field is absent from the API response.
    """
    model_config = ConfigDict(populate_by_name = True)

    account: str
    native_balance_change: int = Field(alias = "nativeBalanceChange")
    token_balance_changes: list[EnhancedTransactionTokenBalanceChange] | None = Field(
        default = None, alias = "tokenBalanceChanges"
    )


class EnhancedTransactionError(BaseModel):
    """
    Error details for a failed transaction.

    Attributes:
        error: human-readable error message describing why the transaction failed.
    """
    error: str


class EnhancedTransactionInnerInstruction(BaseModel):
    """
    A Cross-Program Invocation (CPI) inner instruction nested inside a top-level instruction.

    Attributes:
        accounts: ordered list of account public keys referenced by this instruction.
        data: base58-encoded instruction data payload.
        program_id: public key of the program that owns this instruction.
    """
    model_config = ConfigDict(populate_by_name = True)

    accounts: list[str]
    data: str
    program_id: str = Field(alias = "programId")


class EnhancedTransactionInstruction(BaseModel):
    """
    A top-level instruction in an enhanced transaction.

    Attributes:
        accounts: ordered list of account public keys referenced by this instruction.
        data: base58-encoded instruction data payload.
        program_id: public key of the program that owns this instruction.
        inner_instructions: list of CPI inner instructions invoked by this instruction.
            Empty list when no CPIs were made. `None` when the field is absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    accounts: list[str]
    data: str
    program_id: str = Field(alias = "programId")
    inner_instructions: list[EnhancedTransactionInnerInstruction] | None = Field(
        default = None, alias = "innerInstructions"
    )


class EnhancedTransactionNFTEventNFT(BaseModel):
    """
    A single NFT item referenced in an NFT event.

    Attributes:
        mint: mint address of the NFT.
        token_standard: token standard of the NFT (e.g. `"NonFungible"`, `"FungibleAsset"`,
            `"Fungible"`, `"NonFungibleEdition"`).
    """
    model_config = ConfigDict(populate_by_name = True)

    mint: str
    token_standard: str = Field(alias = "tokenStandard")


class EnhancedTransactionNFTEvent(BaseModel):
    """
    Decoded NFT event data for an enhanced transaction (sale, listing, mint, bid, etc.).

    Attributes:
        description: human-readable description of the NFT event. `None` when absent.
        type: NFT event type (e.g. `"NFT_SALE"`, `"NFT_LISTING"`, `"NFT_MINT"`).
            `None` when absent.
        source: marketplace or program that generated the event (e.g. `"MAGIC_EDEN"`,
            `"TENSOR"`). `None` when absent.
        amount: transaction amount in lamports. `None` when absent.
        fee: transaction fee in lamports. `None` when absent.
        fee_payer: wallet address that paid the transaction fee. `None` when absent.
        signature: transaction signature. `None` when absent.
        slot: slot containing the transaction. `None` when absent.
        timestamp: block time as a Unix timestamp (seconds). `None` when absent.
        sale_type: sale mechanism (`"AUCTION"`, `"INSTANT_SALE"`, `"OFFER"`,
            `"GLOBAL_OFFER"`, `"MINT"`, `"UNKNOWN"`). `None` when absent.
        buyer: wallet address of the buyer. `None` when absent or not a sale.
        seller: wallet address of the seller. `None` when absent or not a sale.
        staker: wallet address of the staker. `None` when absent.
        nfts: list of NFT items involved in the event. `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    description: str | None = None
    type: str | None = None
    source: str | None = None
    amount: int | None = None
    fee: int | None = None
    fee_payer: str | None = Field(default = None, alias = "feePayer")
    signature: str | None = None
    slot: int | None = None
    timestamp: int | None = None
    sale_type: str | None = Field(default = None, alias = "saleType")
    buyer: str | None = None
    seller: str | None = None
    staker: str | None = None
    nfts: list[EnhancedTransactionNFTEventNFT] | None = None


class EnhancedTransactionNativeBalanceChange(BaseModel):
    """
    A native SOL balance change entry within a swap event.

    Attributes:
        account: public key of the account whose SOL balance changed.
        amount: SOL amount as a string in lamports (serialised as string to avoid
            integer overflow for large values).
    """
    account: str
    amount: str


class EnhancedTransactionSwapProgramInfo(BaseModel):
    """
    Program metadata for an inner swap hop, identifying the DEX program used.

    Attributes:
        source: human-readable source name (e.g. `"ORCA"`, `"RAYDIUM"`). `None` when absent.
        account: program account public key. `None` when absent.
        program_name: name of the program (e.g. `"Orca Whirlpool"`). `None` when absent.
        instruction_name: name of the instruction invoked (e.g. `"swap"`). `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    source: str | None = None
    account: str | None = None
    program_name: str | None = Field(default = None, alias = "programName")
    instruction_name: str | None = Field(default = None, alias = "instructionName")


class EnhancedTransactionInnerSwap(BaseModel):
    """
    A single hop within a multi-hop swap, showing per-program token movements.

    Attributes:
        token_inputs: SPL tokens entering this hop. `None` when absent.
        token_outputs: SPL tokens leaving this hop. `None` when absent.
        token_fees: SPL token fees paid for this hop. `None` when absent.
        native_fees: native SOL fees paid for this hop. `None` when absent.
        program_info: metadata about the DEX program that executed this hop.
            `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    token_inputs: list[EnhancedTransactionTokenTransfer] | None = Field(
        default = None, alias = "tokenInputs"
    )
    token_outputs: list[EnhancedTransactionTokenTransfer] | None = Field(
        default = None, alias = "tokenOutputs"
    )
    token_fees: list[EnhancedTransactionTokenTransfer] | None = Field(
        default = None, alias = "tokenFees"
    )
    native_fees: list[EnhancedTransactionNativeTransfer] | None = Field(
        default = None, alias = "nativeFees"
    )
    program_info: EnhancedTransactionSwapProgramInfo | None = Field(
        default = None, alias = "programInfo"
    )


class EnhancedTransactionSwapEvent(BaseModel):
    """
    Decoded swap event data for an enhanced transaction, showing token flows across hops.

    Attributes:
        native_input: net native SOL entering the swap (before fees). `None` when SOL
            is not the input token.
        native_output: net native SOL leaving the swap (after fees). `None` when SOL
            is not the output token.
        token_inputs: SPL tokens entering the overall swap. `None` when absent.
        token_outputs: SPL tokens leaving the overall swap. `None` when absent.
        token_fees: SPL token fees paid for the overall swap. `None` when absent.
        native_fees: native SOL fees paid for the overall swap. `None` when absent.
        inner_swaps: ordered list of individual DEX hops that make up the route.
            `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    native_input: EnhancedTransactionNativeBalanceChange | None = Field(
        default = None, alias = "nativeInput"
    )
    native_output: EnhancedTransactionNativeBalanceChange | None = Field(
        default = None, alias = "nativeOutput"
    )
    token_inputs: list[EnhancedTransactionTokenBalanceChange] | None = Field(
        default = None, alias = "tokenInputs"
    )
    token_outputs: list[EnhancedTransactionTokenBalanceChange] | None = Field(
        default = None, alias = "tokenOutputs"
    )
    token_fees: list[EnhancedTransactionTokenBalanceChange] | None = Field(
        default = None, alias = "tokenFees"
    )
    native_fees: list[EnhancedTransactionNativeBalanceChange] | None = Field(
        default = None, alias = "nativeFees"
    )
    inner_swaps: list[EnhancedTransactionInnerSwap] | None = Field(
        default = None, alias = "innerSwaps"
    )


class EnhancedTransactionCompressedNFTEvent(BaseModel):
    """
    Decoded compressed NFT (cNFT) event data for an enhanced transaction.

    Attributes:
        type: compressed NFT event type (e.g. `"COMPRESSED_NFT_MINT"`,
            `"COMPRESSED_NFT_TRANSFER"`). `None` when absent.
        tree_id: Merkle tree account address containing the cNFT. `None` when absent.
        asset_id: asset ID (canonical on-chain identifier) of the cNFT. `None` when absent.
        leaf_index: zero-based position of the cNFT leaf in the Merkle tree.
            `None` when absent.
        instruction_index: index of the top-level instruction that triggered the event.
            `None` when absent.
        inner_instruction_index: index of the inner instruction (CPI) within its parent
            top-level instruction. `None` when absent.
        new_leaf_owner: wallet address of the new owner after the event. `None` when absent.
        old_leaf_owner: wallet address of the previous owner before the event. `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    type: str | None = None
    tree_id: str | None = Field(default = None, alias = "treeId")
    asset_id: str | None = Field(default = None, alias = "assetId")
    leaf_index: int | None = Field(default = None, alias = "leafIndex")
    instruction_index: int | None = Field(default = None, alias = "instructionIndex")
    inner_instruction_index: int | None = Field(default = None, alias = "innerInstructionIndex")
    new_leaf_owner: str | None = Field(default = None, alias = "newLeafOwner")
    old_leaf_owner: str | None = Field(default = None, alias = "oldLeafOwner")


class EnhancedTransactionEvents(BaseModel):
    """
    Parsed event data for an enhanced transaction, categorised by event type.

    Only the event type(s) relevant to the transaction are populated; all others
    are `None`.

    Attributes:
        nft: NFT event details (sale, listing, mint, etc.). `None` when the transaction
            is not an NFT event.
        swap: DEX swap event details. `None` when the transaction is not a swap.
        compressed: Compressed NFT event details. `None` when the transaction is not
            a cNFT operation. Returned as a list because a single transaction can
            affect multiple cNFTs.
        distribute_compression_rewards: compression reward distribution event data.
            Returned as a raw dict; `None` when absent.
        set_authority: set-authority event data. Returned as a raw dict; `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    nft: EnhancedTransactionNFTEvent | None = None
    swap: EnhancedTransactionSwapEvent | None = None
    compressed: list[EnhancedTransactionCompressedNFTEvent] | None = None
    distribute_compression_rewards: dict | None = Field(
        default = None, alias = "distributeCompressionRewards"
    )
    set_authority: list[dict] | dict | None = Field(default = None, alias = "setAuthority")


class EnhancedTransaction(BaseModel):
    """
    A fully decoded, human-readable transaction returned by the Helius Enhanced
    Transactions API (`getTransactionsByAddress`).

    Helius enriches the raw Solana transaction data with human-readable descriptions,
    typed transfer records, and structured event payloads for common on-chain actions
    (swaps, NFT sales, compressed NFT operations).

    Attributes:
        description: human-readable English summary of the transaction. `None` when
            Helius cannot interpret the transaction.
        type: transaction type classification (e.g. `"SWAP"`, `"NFT_SALE"`,
            `"TRANSFER"`, `"UNKNOWN"`). `None` when absent.
        source: the program or protocol that generated the transaction
            (e.g. `"MAGIC_EDEN"`, `"JUPITER"`, `"SYSTEM_PROGRAM"`). `None` when absent.
        fee: transaction fee in lamports paid by the fee payer.
        fee_payer: wallet address that paid the transaction fee.
        signature: base58-encoded transaction signature.
        slot: slot number of the block containing this transaction.
        timestamp: block production time as a Unix timestamp (seconds).
        native_transfers: list of native SOL movements within the transaction.
            `None` when absent or no native transfers occurred.
        token_transfers: list of SPL token movements within the transaction.
            `None` when absent or no token transfers occurred.
        account_data: per-account balance deltas (native SOL and tokens) for every
            account touched by the transaction. `None` when absent.
        transaction_error: error details if the transaction failed; `None` for
            successful transactions.
        instructions: top-level instructions executed in the transaction, each with
            its CPI inner instructions. `None` when absent.
        events: structured event data parsed by Helius (NFT, swap, compressed NFT).
            `None` when no recognised event was detected.
    """
    model_config = ConfigDict(populate_by_name = True)

    description: str | None = None
    type: str | None = None
    source: str | None = None
    fee: int
    fee_payer: str = Field(alias = "feePayer")
    signature: str
    slot: int
    timestamp: int
    native_transfers: list[EnhancedTransactionNativeTransfer] | None = Field(
        default = None, alias = "nativeTransfers"
    )
    token_transfers: list[EnhancedTransactionTokenTransfer] | None = Field(
        default = None, alias = "tokenTransfers"
    )
    account_data: list[EnhancedTransactionAccountData] | None = Field(
        default = None, alias = "accountData"
    )
    transaction_error: EnhancedTransactionError | None = Field(
        default = None, alias = "transactionError"
    )
    instructions: list[EnhancedTransactionInstruction] | None = None
    events: EnhancedTransactionEvents | None = None


class GetTransactionsByAddressResponse(RootModel[list[EnhancedTransaction]]):
    """
    Response for the `getTransactionsByAddress` Enhanced Transactions REST endpoint.

    Wraps a list of [`EnhancedTransaction`][cyhole.helius.schema.EnhancedTransaction] objects.
    Access the transactions via `.root`.
    """


class PostGetTransactionsResponse(RootModel[list[EnhancedTransaction]]):
    """
    Response for the `getTransactions` Enhanced Transactions REST endpoint.

    Wraps a list of [`EnhancedTransaction`][cyhole.helius.schema.EnhancedTransaction]
    objects, one per signature submitted in the request body, preserving input order.
    Access the transactions via `.root`.
    """
