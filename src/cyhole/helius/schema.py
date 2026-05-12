from pydantic import BaseModel, ConfigDict, Field


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
