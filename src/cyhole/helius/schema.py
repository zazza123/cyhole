from pydantic import BaseModel, ConfigDict, Field, RootModel


# ─── Shared request sub-schemas ───────────────────────────────────────────────

class HeliusSortConfig(BaseModel):
    """
    Sort configuration used in DAS asset collection request bodies.

    Attributes:
        sort_by: field to sort by (see [`HeliusSortBy`][cyhole.helius.param.HeliusSortBy]).
        sort_direction: sort order (see [`HeliusSortDirection`][cyhole.helius.param.HeliusSortDirection]).
    """
    model_config = ConfigDict(populate_by_name = True)

    sort_by: str = Field(alias = "sortBy")
    sort_direction: str = Field(alias = "sortDirection")


class HeliusDisplayOptions(BaseModel):
    """
    Display options that control which extra fields are returned in DAS collection responses.

    All fields default to `None` (API default: `False`).
    """
    model_config = ConfigDict(populate_by_name = True)

    show_fungible: bool | None = Field(default = None, alias = "showFungible")
    show_native_balance: bool | None = Field(default = None, alias = "showNativeBalance")
    show_collection_metadata: bool | None = Field(default = None, alias = "showCollectionMetadata")
    show_unverified_collections: bool | None = Field(default = None, alias = "showUnverifiedCollections")
    show_grand_total: bool | None = Field(default = None, alias = "showGrandTotal")
    show_inscription: bool | None = Field(default = None, alias = "showInscription")
    show_zero_balance: bool | None = Field(default = None, alias = "showZeroBalance")


# ─── Asset sub-schemas ─────────────────────────────────────────────────────────

class AssetFile(BaseModel):
    """A file attachment in an asset's content (image, animation, etc.)."""
    uri: str | None = None
    cdn_uri: str | None = None
    mime: str | None = None


class AssetAttribute(BaseModel):
    """A single trait attribute for an NFT asset."""
    value: str | None = None
    trait_type: str | None = None


class AssetMetadata(BaseModel):
    """On-chain metadata fields for a digital asset."""
    attributes: list[AssetAttribute] | None = None
    description: str | None = None
    name: str
    symbol: str


class AssetLinks(BaseModel):
    """External links associated with a digital asset."""
    image: str | None = None
    external_url: str | None = None
    animation_url: str | None = None


class AssetContent(BaseModel):
    """Content fields of a digital asset, including metadata and attached files."""
    schema_uri: str | None = Field(default = None, alias = "$schema")
    json_uri: str | None = None
    files: list[AssetFile] | None = None
    metadata: AssetMetadata
    links: AssetLinks | None = None


class AssetAuthority(BaseModel):
    """Update authority record for a digital asset."""
    address: str
    scopes: list[str]


class AssetCompression(BaseModel):
    """Compression state and Merkle tree details for a compressed NFT (cNFT)."""
    eligible: bool
    compressed: bool
    data_hash: str | None = None
    creator_hash: str | None = None
    asset_hash: str | None = None
    tree: str | None = None
    seq: int | None = None
    leaf_id: int | None = None


class AssetCollectionMetadata(BaseModel):
    """Metadata for the collection an asset belongs to."""
    name: str | None = None
    symbol: str | None = None
    image: str | None = None
    description: str | None = None
    external_url: str | None = None


class AssetGrouping(BaseModel):
    """Grouping membership (e.g. collection) for a digital asset."""
    group_key: str
    group_value: str | None = None
    verified: bool | None = None
    collection_metadata: AssetCollectionMetadata | None = None


class AssetRoyalty(BaseModel):
    """Royalty configuration for a digital asset."""
    royalty_model: str
    target: str | None = None
    percent: float
    basis_points: int
    primary_sale_happened: bool
    locked: bool


class AssetCreator(BaseModel):
    """A creator entry in an asset's creator array."""
    address: str
    share: int
    verified: bool


class AssetOwnership(BaseModel):
    """Ownership details of a digital asset."""
    frozen: bool
    delegated: bool
    delegate: str | None = None
    ownership_model: str
    owner: str


class AssetSupply(BaseModel):
    """Print supply details for a master/edition NFT."""
    print_max_supply: int | None = None
    print_current_supply: int | None = None
    edition_nonce: int | None = None
    edition_number: int | None = None
    master_edition_mint: str | None = None


class AssetPriceInfo(BaseModel):
    """Price information for a fungible token."""
    price_per_token: float | None = None
    total_price: float | None = None
    currency: str | None = None


class AssetTokenInfo(BaseModel):
    """Token-specific information returned for fungible assets."""
    symbol: str | None = None
    balance: int | None = None
    supply: int | None = None
    decimals: int | None = None
    token_program: str | None = None
    associated_token_address: str | None = None
    price_info: AssetPriceInfo | None = None
    mint_authority: str | None = None
    freeze_authority: str | None = None


class AssetInscription(BaseModel):
    """Inscription data attached to a digital asset."""
    order: int | None = None
    size: int | None = None
    content_type: str | None = None
    encoding: str | None = None
    validation_hash: str | None = None
    inscription_data_account: str | None = None
    authority: str | None = None


class AssetNativeBalance(BaseModel):
    """SOL native balance for the asset owner, returned when `showNativeBalance` is enabled."""
    lamports: int
    price_per_sol: float | None = None
    total_price: float | None = None


class Asset(BaseModel):
    """Full digital asset record returned by the Helius DAS API."""
    interface: str
    id: str
    content: AssetContent | None = None
    authorities: list[AssetAuthority] | None = None
    compression: AssetCompression | None = None
    grouping: list[AssetGrouping] | None = None
    royalty: AssetRoyalty | None = None
    creators: list[AssetCreator] | None = None
    ownership: AssetOwnership
    supply: AssetSupply | None = None
    mutable: bool | None = None
    burnt: bool | None = None
    token_info: AssetTokenInfo | None = None
    inscription: AssetInscription | None = None
    spl20: dict | None = None
    last_indexed_slot: int | None = None


class AssetList(BaseModel):
    """Paginated list of digital assets returned by DAS collection endpoints."""
    total: int
    limit: int
    page: int | None = None
    cursor: str | None = None
    items: list[Asset]
    native_balance: AssetNativeBalance | None = Field(default = None, alias = "nativeBalance")
    grand_total: int | None = Field(default = None, alias = "grandTotal")


# ─── Proof schemas ─────────────────────────────────────────────────────────────

class AssetProof(BaseModel):
    """Merkle proof for a compressed NFT, required for on-chain operations."""
    root: str
    proof: list[str]
    node_index: int
    leaf: str
    tree_id: str


# ─── Signature schemas ─────────────────────────────────────────────────────────

class AssetSignatureList(BaseModel):
    """
    Paginated list of transaction signatures for a digital asset.

    Each item in `items` is a two-element list: `[signature, transaction_type]`.
    """
    total: int
    limit: int
    page: int
    items: list[list[str]]


# ─── Token account schemas ─────────────────────────────────────────────────────

class TokenAccount(BaseModel):
    """A single SPL token account record."""
    address: str
    mint: str
    owner: str
    amount: int
    delegated_amount: int
    frozen: bool


class TokenAccountList(BaseModel):
    """Paginated list of SPL token accounts."""
    total: int
    limit: int
    page: int
    token_accounts: list[TokenAccount]


# ─── NFT edition schemas ────────────────────────────────────────────────────────

class NftEditionItem(BaseModel):
    """A single print edition of a master NFT."""
    mint: str
    edition_address: str
    edition: int


class NftEditionList(BaseModel):
    """Paginated list of print editions for a master NFT."""
    total: int
    limit: int
    page: int
    master_edition_address: str
    supply: int
    max_supply: int | None = None
    editions: list[NftEditionItem]


# ─── Request body schemas ───────────────────────────────────────────────────────

class PostGetAssetOptions(BaseModel):
    """
    Optional display flags for the `getAsset` DAS endpoint.

    All fields default to `None` (API default: `False`).
    """
    model_config = ConfigDict(populate_by_name = True)

    show_unverified_collections: bool | None = Field(default = None, alias = "showUnverifiedCollections")
    show_collection_metadata: bool | None = Field(default = None, alias = "showCollectionMetadata")
    show_fungible: bool | None = Field(default = None, alias = "showFungible")
    show_inscription: bool | None = Field(default = None, alias = "showInscription")


class PostGetAssetsByOwnerBody(BaseModel):
    """
    Request body for the `getAssetsByOwner` DAS endpoint.

    Attributes:
        owner_address: wallet address of the asset owner.
        page: page number for pagination (default 1).
        limit: results per page, max 1,000 (default 1,000).
        display_options: optional flags controlling extra fields in the response.
        sort_by: optional sort configuration.
    """
    model_config = ConfigDict(populate_by_name = True)

    owner_address: str = Field(alias = "ownerAddress")
    page: int | None = None
    limit: int | None = None
    display_options: HeliusDisplayOptions | None = Field(default = None, alias = "displayOptions")
    sort_by: HeliusSortConfig | None = Field(default = None, alias = "sortBy")


class PostGetAssetsByGroupBody(BaseModel):
    """
    Request body for the `getAssetsByGroup` DAS endpoint.

    Attributes:
        group_key: grouping key, typically `"collection"`.
        group_value: collection mint address.
        page: page number for pagination (default 1).
        limit: results per page, max 1,000 (default 1,000).
        display_options: optional flags controlling extra fields in the response.
        sort_by: optional sort configuration.
    """
    model_config = ConfigDict(populate_by_name = True)

    group_key: str = Field(alias = "groupKey")
    group_value: str = Field(alias = "groupValue")
    page: int | None = None
    limit: int | None = None
    display_options: HeliusDisplayOptions | None = Field(default = None, alias = "displayOptions")
    sort_by: HeliusSortConfig | None = Field(default = None, alias = "sortBy")


class PostGetAssetsByCreatorBody(BaseModel):
    """
    Request body for the `getAssetsByCreator` DAS endpoint.

    Attributes:
        creator_address: wallet address of the creator.
        only_verified: if True, return only assets where the creator is verified (default False).
        page: page number for pagination (default 1).
        limit: results per page, max 1,000 (default 1,000).
        display_options: optional flags controlling extra fields in the response.
        sort_by: optional sort configuration.
    """
    model_config = ConfigDict(populate_by_name = True)

    creator_address: str = Field(alias = "creatorAddress")
    only_verified: bool | None = Field(default = None, alias = "onlyVerified")
    page: int | None = None
    limit: int | None = None
    display_options: HeliusDisplayOptions | None = Field(default = None, alias = "displayOptions")
    sort_by: HeliusSortConfig | None = Field(default = None, alias = "sortBy")


class PostGetAssetsByAuthorityBody(BaseModel):
    """
    Request body for the `getAssetsByAuthority` DAS endpoint.

    Attributes:
        authority_address: update authority address.
        page: page number for pagination (default 1).
        limit: results per page, max 1,000 (default 1,000).
        display_options: optional flags controlling extra fields in the response.
        sort_by: optional sort configuration.
    """
    model_config = ConfigDict(populate_by_name = True)

    authority_address: str = Field(alias = "authorityAddress")
    page: int | None = None
    limit: int | None = None
    display_options: HeliusDisplayOptions | None = Field(default = None, alias = "displayOptions")
    sort_by: HeliusSortConfig | None = Field(default = None, alias = "sortBy")


class PostSearchAssetsBody(BaseModel):
    """
    Request body for the `searchAssets` DAS endpoint.

    All fields are optional — combine filters as needed.

    Attributes:
        page: page number for pagination (default 1).
        limit: results per page, max 1,000 (default 1,000).
        owner_address: filter by owner wallet address.
        creator_address: filter by creator wallet address.
        creator_verified: if True, only return assets from verified creators.
        grouping: collection filter as a two-element list `["collection", "<mint_address>"]`.
        burnt: if True, include burnt assets.
        compressed: filter by compression status.
        token_type: filter by token type (see [`HeliusTokenType`][cyhole.helius.param.HeliusTokenType]).
        sort_by: optional sort configuration.
    """
    model_config = ConfigDict(populate_by_name = True)

    page: int | None = None
    limit: int | None = None
    owner_address: str | None = Field(default = None, alias = "ownerAddress")
    creator_address: str | None = Field(default = None, alias = "creatorAddress")
    creator_verified: bool | None = Field(default = None, alias = "creatorVerified")
    grouping: list[str] | None = None
    burnt: bool | None = None
    compressed: bool | None = None
    token_type: str | None = Field(default = None, alias = "tokenType")
    sort_by: HeliusSortConfig | None = Field(default = None, alias = "sortBy")


class PostGetTokenAccountsBody(BaseModel):
    """
    Request body for the `getTokenAccounts` DAS endpoint.

    Provide at least one of `mint` or `owner` to narrow the results.

    Attributes:
        mint: SPL token mint address to filter by.
        owner: wallet address of the token account owner.
        page: page number for pagination (default 1).
        limit: results per page (default 100).
    """
    mint: str | None = None
    owner: str | None = None
    page: int | None = None
    limit: int | None = None


# ─── getTransfersByAddress schemas ─────────────────────────────────────────────

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


# ─── Response schemas (JSON-RPC 2.0 wrapper) ────────────────────────────────────

class PostGetAssetResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAsset` DAS method."""
    jsonrpc: str
    id: str | int
    result: Asset


class PostGetAssetBatchResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetBatch` DAS method."""
    jsonrpc: str
    id: str | int
    result: list[Asset]


class PostGetAssetProofResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetProof` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetProof


class PostGetAssetProofBatchResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetProofBatch` DAS method."""
    jsonrpc: str
    id: str | int
    result: dict[str, AssetProof]


class PostGetAssetsByOwnerResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetsByOwner` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetList


class PostGetAssetsByGroupResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetsByGroup` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetList


class PostGetAssetsByCreatorResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetsByCreator` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetList


class PostGetAssetsByAuthorityResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getAssetsByAuthority` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetList


class PostSearchAssetsResponse(BaseModel):
    """JSON-RPC 2.0 response for the `searchAssets` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetList


class PostGetSignaturesForAssetResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getSignaturesForAsset` DAS method."""
    jsonrpc: str
    id: str | int
    result: AssetSignatureList


class PostGetNftEditionsResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getNftEditions` DAS method."""
    jsonrpc: str
    id: str | int
    result: NftEditionList


class PostGetTokenAccountsResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getTokenAccounts` DAS method."""
    jsonrpc: str
    id: str | int
    result: TokenAccountList


class PostGetTransfersByAddressResponse(BaseModel):
    """JSON-RPC 2.0 response for the `getTransfersByAddress` RPC method."""
    jsonrpc: str
    id: str | int
    result: TransferList


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
            the complete transaction payload in a single call (`limit` must be `<= 100`).
        sort_order: result ordering. Accepts the values of
            [`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder] (`"desc"`, `"asc"`).
            API default: `"desc"` (newest first).
        limit: maximum number of transactions returned. Up to `1000` in `"signatures"`
            mode and up to `100` in `"full"` mode. API default: `1000`.
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
            a cNFT operation.
        distribute_compression_rewards: compression reward distribution event data.
            Returned as a raw dict; `None` when absent.
        set_authority: set-authority event data. Returned as a raw dict; `None` when absent.
    """
    model_config = ConfigDict(populate_by_name = True)

    nft: EnhancedTransactionNFTEvent | None = None
    swap: EnhancedTransactionSwapEvent | None = None
    compressed: EnhancedTransactionCompressedNFTEvent | None = None
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
