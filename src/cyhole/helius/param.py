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
