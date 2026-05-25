from typing import Any, Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..helius.client import HeliusClient, HeliusAsyncClient
from ..helius.param import HeliusNetwork
from ..helius.schema import (
    PostGetAssetOptions,
    PostGetAssetsByOwnerBody,
    PostGetAssetsByGroupBody,
    PostGetAssetsByCreatorBody,
    PostGetAssetsByAuthorityBody,
    PostSearchAssetsBody,
    PostGetTokenAccountsBody,
    PostGetTransfersByAddressBody,
    PostGetTransactionsForAddressBody,
    GetTransactionsByAddressQuery,
    PostGetAssetResponse,
    PostGetAssetBatchResponse,
    PostGetAssetProofResponse,
    PostGetAssetProofBatchResponse,
    PostGetAssetsByOwnerResponse,
    PostGetAssetsByGroupResponse,
    PostGetAssetsByCreatorResponse,
    PostGetAssetsByAuthorityResponse,
    PostSearchAssetsResponse,
    PostGetSignaturesForAssetResponse,
    PostGetNftEditionsResponse,
    PostGetTokenAccountsResponse,
    PostGetTransfersByAddressResponse,
    PostGetTransactionsForAddressResponse,
    GetTransactionsByAddressResponse,
    PostGetTransactionsResponse,
)


class Helius(Interaction):
    """
    Class used to connect [Helius](https://www.helius.dev) API.

    Helius provides enhanced Solana RPC infrastructure including the
    **Digital Asset Standard (DAS) API** — a unified interface for querying
    on-chain NFTs, compressed NFTs (cNFTs), fungible tokens, and inscriptions.

    All DAS endpoints require an API key obtained from the
    [Helius Dashboard](https://dashboard.helius.dev). The key is appended
    as a URL query parameter on every request.

    **Example — sync**

    ```python
    from cyhole.helius import Helius

    helius = Helius(api_key="your-api-key")
    response = helius.client.post_get_asset("4ZkS7zADmEFnkLPMHqJfPvHDN8oqfPjqDFGEQHiqPbEz")
    print(response.result.id)
    ```

    **Example — async**

    ```python
    import asyncio
    from cyhole.helius import Helius

    helius = Helius(api_key="your-api-key")

    async def main():
        async with helius.async_client as client:
            response = await client.post_get_asset("4ZkS7zADmEFnkLPMHqJfPvHDN8oqfPjqDFGEQHiqPbEz")
        print(response.result.ownership.owner)

    asyncio.run(main())
    ```
    """

    def __init__(
        self,
        api_key: str,
        network: HeliusNetwork = HeliusNetwork.MAINNET,
        headers: Any | None = None,
    ) -> None:
        super().__init__(headers)
        self._api_key = api_key
        self.url_api = f"https://{network.value}.helius-rpc.com/?api-key={api_key}"
        self.url_api_enhanced = f"https://api-{network.value}.helius-rpc.com"
        self.client = HeliusClient(self)
        self.async_client = HeliusAsyncClient(self)

    # ─── getAsset ─────────────────────────────────────────────────────────────

    @overload
    def _post_get_asset(self, sync: Literal[True], asset_id: str, options: PostGetAssetOptions | None = None) -> PostGetAssetResponse: ...
    @overload
    def _post_get_asset(self, sync: Literal[False], asset_id: str, options: PostGetAssetOptions | None = None) -> Coroutine[None, None, PostGetAssetResponse]: ...
    def _post_get_asset(self, sync: bool, asset_id: str, options: PostGetAssetOptions | None = None) -> PostGetAssetResponse | Coroutine[None, None, PostGetAssetResponse]:
        """
        This function refers to the **getAsset** DAS API endpoint.

        Retrieves the full on-chain record for a single digital asset (NFT, cNFT,
        or fungible token) identified by its mint address. The response includes
        ownership, royalty, compression state, content metadata, and optional
        fungible or inscription data depending on the `options` provided.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            asset_id: the mint address of the asset to retrieve.
            options: optional display flags — use [`PostGetAssetOptions`][cyhole.helius.schema.PostGetAssetOptions]
                to enable `showFungible`, `showInscription`, `showCollectionMetadata`, or
                `showUnverifiedCollections`.

        Returns:
            PostGetAssetResponse: full asset record wrapped in a JSON-RPC 2.0 envelope.
                Access the asset data via `response.result`.
        """
        params: dict = {"id": asset_id}
        if options:
            params["options"] = options.model_dump(by_alias = True, exclude_none = True)
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getAsset", "params": params}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetResponse, json = body)

    # ─── getAssetBatch ────────────────────────────────────────────────────────

    @overload
    def _post_get_asset_batch(self, sync: Literal[True], ids: list[str]) -> PostGetAssetBatchResponse: ...
    @overload
    def _post_get_asset_batch(self, sync: Literal[False], ids: list[str]) -> Coroutine[None, None, PostGetAssetBatchResponse]: ...
    def _post_get_asset_batch(self, sync: bool, ids: list[str]) -> PostGetAssetBatchResponse | Coroutine[None, None, PostGetAssetBatchResponse]:
        """
        This function refers to the **getAssetBatch** DAS API endpoint.

        Retrieves up to 1,000 digital assets in a single request. Useful for
        bulk enrichment of mint address lists (e.g. wallet portfolio snapshots).
        Items in the result list follow the same schema as a single `getAsset` call.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            ids: list of mint addresses to retrieve (max 1,000 items).

        Returns:
            PostGetAssetBatchResponse: list of asset records wrapped in a JSON-RPC 2.0 envelope.
                Access the list via `response.result`.
        """
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getAssetBatch", "params": {"ids": ids}}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetBatchResponse, json = body)

    # ─── getAssetProof ────────────────────────────────────────────────────────

    @overload
    def _post_get_asset_proof(self, sync: Literal[True], asset_id: str) -> PostGetAssetProofResponse: ...
    @overload
    def _post_get_asset_proof(self, sync: Literal[False], asset_id: str) -> Coroutine[None, None, PostGetAssetProofResponse]: ...
    def _post_get_asset_proof(self, sync: bool, asset_id: str) -> PostGetAssetProofResponse | Coroutine[None, None, PostGetAssetProofResponse]:
        """
        This function refers to the **getAssetProof** DAS API endpoint.

        Returns the Merkle proof required to execute on-chain operations (transfer,
        burn, delegate) on a **compressed NFT** (cNFT). The proof must be passed to
        the Bubblegum program alongside the instruction. Only applicable to cNFTs;
        regular NFTs do not require a proof.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            asset_id: the mint address of the compressed NFT.

        Returns:
            PostGetAssetProofResponse: Merkle proof data wrapped in a JSON-RPC 2.0 envelope.
                Access the proof via `response.result`.
        """
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getAssetProof", "params": {"id": asset_id}}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetProofResponse, json = body)

    # ─── getAssetProofBatch ───────────────────────────────────────────────────

    @overload
    def _post_get_asset_proof_batch(self, sync: Literal[True], ids: list[str]) -> PostGetAssetProofBatchResponse: ...
    @overload
    def _post_get_asset_proof_batch(self, sync: Literal[False], ids: list[str]) -> Coroutine[None, None, PostGetAssetProofBatchResponse]: ...
    def _post_get_asset_proof_batch(self, sync: bool, ids: list[str]) -> PostGetAssetProofBatchResponse | Coroutine[None, None, PostGetAssetProofBatchResponse]:
        """
        This function refers to the **getAssetProofBatch** DAS API endpoint.

        Fetches Merkle proofs for multiple compressed NFTs in a single round-trip.
        The response is a mapping of asset mint address → proof object, making it
        straightforward to look up the proof for each cNFT in a batch transfer.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            ids: list of compressed NFT mint addresses.

        Returns:
            PostGetAssetProofBatchResponse: dict of proofs keyed by asset ID,
                wrapped in a JSON-RPC 2.0 envelope. Access via `response.result["<mint>"]`.
        """
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getAssetProofBatch", "params": {"ids": ids}}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetProofBatchResponse, json = body)

    # ─── getAssetsByOwner ─────────────────────────────────────────────────────

    @overload
    def _post_get_assets_by_owner(self, sync: Literal[True], body: PostGetAssetsByOwnerBody) -> PostGetAssetsByOwnerResponse: ...
    @overload
    def _post_get_assets_by_owner(self, sync: Literal[False], body: PostGetAssetsByOwnerBody) -> Coroutine[None, None, PostGetAssetsByOwnerResponse]: ...
    def _post_get_assets_by_owner(self, sync: bool, body: PostGetAssetsByOwnerBody) -> PostGetAssetsByOwnerResponse | Coroutine[None, None, PostGetAssetsByOwnerResponse]:
        """
        This function refers to the **getAssetsByOwner** DAS API endpoint.

        Returns all digital assets (NFTs, cNFTs, fungible tokens) held by a given wallet.
        Supports pagination, sorting, and display options such as native SOL balance and
        fungible token data. Useful for building wallet portfolio views.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: request body — see [`PostGetAssetsByOwnerBody`][cyhole.helius.schema.PostGetAssetsByOwnerBody].
                At minimum, set `owner_address`. Use `display_options` to include
                fungible balances or native SOL balance.

        Returns:
            PostGetAssetsByOwnerResponse: paginated asset list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.items`. Total count is in `response.result.total`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "getAssetsByOwner",
            "params": body.model_dump(by_alias = True, exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetsByOwnerResponse, json = rpc_body)

    # ─── getAssetsByGroup ─────────────────────────────────────────────────────

    @overload
    def _post_get_assets_by_group(self, sync: Literal[True], body: PostGetAssetsByGroupBody) -> PostGetAssetsByGroupResponse: ...
    @overload
    def _post_get_assets_by_group(self, sync: Literal[False], body: PostGetAssetsByGroupBody) -> Coroutine[None, None, PostGetAssetsByGroupResponse]: ...
    def _post_get_assets_by_group(self, sync: bool, body: PostGetAssetsByGroupBody) -> PostGetAssetsByGroupResponse | Coroutine[None, None, PostGetAssetsByGroupResponse]:
        """
        This function refers to the **getAssetsByGroup** DAS API endpoint.

        Returns all assets that belong to a specific collection (or other grouping key).
        The most common usage is to supply `group_key = "collection"` and
        `group_value = "<collection_mint_address>"` to enumerate every NFT in a collection.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: request body — see [`PostGetAssetsByGroupBody`][cyhole.helius.schema.PostGetAssetsByGroupBody].
                Must supply `group_key` and `group_value`.

        Returns:
            PostGetAssetsByGroupResponse: paginated asset list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.items`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "getAssetsByGroup",
            "params": body.model_dump(by_alias = True, exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetsByGroupResponse, json = rpc_body)

    # ─── getAssetsByCreator ───────────────────────────────────────────────────

    @overload
    def _post_get_assets_by_creator(self, sync: Literal[True], body: PostGetAssetsByCreatorBody) -> PostGetAssetsByCreatorResponse: ...
    @overload
    def _post_get_assets_by_creator(self, sync: Literal[False], body: PostGetAssetsByCreatorBody) -> Coroutine[None, None, PostGetAssetsByCreatorResponse]: ...
    def _post_get_assets_by_creator(self, sync: bool, body: PostGetAssetsByCreatorBody) -> PostGetAssetsByCreatorResponse | Coroutine[None, None, PostGetAssetsByCreatorResponse]:
        """
        This function refers to the **getAssetsByCreator** DAS API endpoint.

        Returns all digital assets created by a given wallet address. Optionally
        filter to only verified creator entries using `only_verified = True`, which
        excludes assets where the creator has not signed the metadata.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: request body — see [`PostGetAssetsByCreatorBody`][cyhole.helius.schema.PostGetAssetsByCreatorBody].
                Must supply `creator_address`.

        Returns:
            PostGetAssetsByCreatorResponse: paginated asset list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.items`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "getAssetsByCreator",
            "params": body.model_dump(by_alias = True, exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetsByCreatorResponse, json = rpc_body)

    # ─── getAssetsByAuthority ─────────────────────────────────────────────────

    @overload
    def _post_get_assets_by_authority(self, sync: Literal[True], body: PostGetAssetsByAuthorityBody) -> PostGetAssetsByAuthorityResponse: ...
    @overload
    def _post_get_assets_by_authority(self, sync: Literal[False], body: PostGetAssetsByAuthorityBody) -> Coroutine[None, None, PostGetAssetsByAuthorityResponse]: ...
    def _post_get_assets_by_authority(self, sync: bool, body: PostGetAssetsByAuthorityBody) -> PostGetAssetsByAuthorityResponse | Coroutine[None, None, PostGetAssetsByAuthorityResponse]:
        """
        This function refers to the **getAssetsByAuthority** DAS API endpoint.

        Returns all assets whose **update authority** matches the given address.
        Update authority controls the ability to modify on-chain metadata, so this
        endpoint is useful for discovering all assets managed by a specific program
        or wallet (e.g. all NFTs minted under a particular candy machine).

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: request body — see [`PostGetAssetsByAuthorityBody`][cyhole.helius.schema.PostGetAssetsByAuthorityBody].
                Must supply `authority_address`.

        Returns:
            PostGetAssetsByAuthorityResponse: paginated asset list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.items`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "getAssetsByAuthority",
            "params": body.model_dump(by_alias = True, exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetAssetsByAuthorityResponse, json = rpc_body)

    # ─── searchAssets ─────────────────────────────────────────────────────────

    @overload
    def _post_search_assets(self, sync: Literal[True], body: PostSearchAssetsBody) -> PostSearchAssetsResponse: ...
    @overload
    def _post_search_assets(self, sync: Literal[False], body: PostSearchAssetsBody) -> Coroutine[None, None, PostSearchAssetsResponse]: ...
    def _post_search_assets(self, sync: bool, body: PostSearchAssetsBody) -> PostSearchAssetsResponse | Coroutine[None, None, PostSearchAssetsResponse]:
        """
        This function refers to the **searchAssets** DAS API endpoint.

        Performs a flexible, multi-criteria search across all digital assets indexed
        by Helius. Filters can be combined freely: narrow by owner, creator, collection,
        token type, compression state, or burn status. All fields in the request body
        are optional — omitting a field means no constraint is applied for that dimension.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: search body — see [`PostSearchAssetsBody`][cyhole.helius.schema.PostSearchAssetsBody].
                All fields are optional; combine as needed.

        Returns:
            PostSearchAssetsResponse: paginated asset list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.items`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "searchAssets",
            "params": body.model_dump(by_alias = True, exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostSearchAssetsResponse, json = rpc_body)

    # ─── getSignaturesForAsset ────────────────────────────────────────────────

    @overload
    def _post_get_signatures_for_asset(self, sync: Literal[True], asset_id: str, page: int | None = None, limit: int | None = None) -> PostGetSignaturesForAssetResponse: ...
    @overload
    def _post_get_signatures_for_asset(self, sync: Literal[False], asset_id: str, page: int | None = None, limit: int | None = None) -> Coroutine[None, None, PostGetSignaturesForAssetResponse]: ...
    def _post_get_signatures_for_asset(self, sync: bool, asset_id: str, page: int | None = None, limit: int | None = None) -> PostGetSignaturesForAssetResponse | Coroutine[None, None, PostGetSignaturesForAssetResponse]:
        """
        This function refers to the **getSignaturesForAsset** DAS API endpoint.

        Returns the transaction history for a digital asset, including both regular
        NFTs and compressed NFTs (cNFTs). Each item in the result is a two-element
        list of `[signature, transaction_type]` (e.g. `["5abc...", "Transfer"]`).
        Useful for auditing provenance or tracking the ownership history of an asset.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            asset_id: the mint address of the asset.
            page: page number for pagination (default 1).
            limit: number of signatures per page, max 1,000 (default 1,000).

        Returns:
            PostGetSignaturesForAssetResponse: paginated signature list wrapped in a
                JSON-RPC 2.0 envelope. Access via `response.result.items`.
        """
        params: dict = {"id": asset_id}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getSignaturesForAsset", "params": params}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetSignaturesForAssetResponse, json = body)

    # ─── getNftEditions ───────────────────────────────────────────────────────

    @overload
    def _post_get_nft_editions(self, sync: Literal[True], mint: str, page: int | None = None, limit: int | None = None) -> PostGetNftEditionsResponse: ...
    @overload
    def _post_get_nft_editions(self, sync: Literal[False], mint: str, page: int | None = None, limit: int | None = None) -> Coroutine[None, None, PostGetNftEditionsResponse]: ...
    def _post_get_nft_editions(self, sync: bool, mint: str, page: int | None = None, limit: int | None = None) -> PostGetNftEditionsResponse | Coroutine[None, None, PostGetNftEditionsResponse]:
        """
        This function refers to the **getNftEditions** DAS API endpoint.

        Returns all **print editions** derived from a given **master edition** NFT.
        Each item contains the edition mint address, edition address (PDA), and
        sequential edition number. The response also includes the master edition
        address, current supply, and optional max supply.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            mint: the master edition mint address.
            page: page number for pagination (default 1).
            limit: number of editions per page, max 1,000 (default 1,000).

        Returns:
            PostGetNftEditionsResponse: paginated edition list wrapped in a JSON-RPC 2.0 envelope.
                Access via `response.result.editions`. Supply info is in `response.result.supply`.
        """
        params: dict = {"mint": mint}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getNftEditions", "params": params}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetNftEditionsResponse, json = body)

    # ─── getTokenAccounts ─────────────────────────────────────────────────────

    @overload
    def _post_get_token_accounts(self, sync: Literal[True], body: PostGetTokenAccountsBody) -> PostGetTokenAccountsResponse: ...
    @overload
    def _post_get_token_accounts(self, sync: Literal[False], body: PostGetTokenAccountsBody) -> Coroutine[None, None, PostGetTokenAccountsResponse]: ...
    def _post_get_token_accounts(self, sync: bool, body: PostGetTokenAccountsBody) -> PostGetTokenAccountsResponse | Coroutine[None, None, PostGetTokenAccountsResponse]:
        """
        This function refers to the **getTokenAccounts** DAS API endpoint.

        Returns SPL token accounts filtered by mint address, owner wallet, or both.
        Each account record includes the token balance (`amount`), whether the account
        is frozen, and any delegated amount. Provide at least one of `mint` or `owner`
        to narrow the result set.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            body: query body — see [`PostGetTokenAccountsBody`][cyhole.helius.schema.PostGetTokenAccountsBody].
                Provide `mint`, `owner`, or both.

        Returns:
            PostGetTokenAccountsResponse: paginated token account list wrapped in a
                JSON-RPC 2.0 envelope. Access via `response.result.token_accounts`.
        """
        rpc_body = {
            "jsonrpc": "2.0",
            "id": "cyhole",
            "method": "getTokenAccounts",
            "params": body.model_dump(exclude_none = True),
        }
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetTokenAccountsResponse, json = rpc_body)

    # ─── getTransfersByAddress ────────────────────────────────────────────────

    @overload
    def _post_get_transfers_by_address(self, sync: Literal[True], address: str, body: PostGetTransfersByAddressBody | None = None) -> PostGetTransfersByAddressResponse: ...
    @overload
    def _post_get_transfers_by_address(self, sync: Literal[False], address: str, body: PostGetTransfersByAddressBody | None = None) -> Coroutine[None, None, PostGetTransfersByAddressResponse]: ...
    def _post_get_transfers_by_address(self, sync: bool, address: str, body: PostGetTransfersByAddressBody | None = None) -> PostGetTransfersByAddressResponse | Coroutine[None, None, PostGetTransfersByAddressResponse]:
        """
        This function refers to the **getTransfersByAddress** Helius RPC endpoint.

        Returns parsed, human-readable token and native SOL transfer records for a
        wallet owner address, suitable for ledgers, payment tracking, and balance
        reconciliation. Results can be narrowed by counterparty, direction, mint,
        amount/time/slot ranges and paginated via `pagination_token`.

        The endpoint is a Helius-exclusive feature (not part of standard Solana RPC),
        requires a Developer plan or higher, costs 10 credits per request, and
        returns at most the most recent 1 year of transfer history. Failed
        transactions and hidden SOL balance-change movements are not included.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            address: base58-encoded wallet **owner** address to query. Must be the
                owner wallet, not an associated token account (ATA).
            body: optional configuration object — see
                [`PostGetTransfersByAddressBody`][cyhole.helius.schema.PostGetTransfersByAddressBody].
                All fields are optional. Use it to filter by counterparty, direction
                ([`HeliusTransferDirection`][cyhole.helius.param.HeliusTransferDirection]),
                mint, SOL/WSOL mode ([`HeliusSolMode`][cyhole.helius.param.HeliusSolMode]),
                numeric ranges, commitment ([`HeliusCommitment`][cyhole.helius.param.HeliusCommitment]),
                ordering ([`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder]),
                and pagination (`limit`, `pagination_token`).

        Returns:
            PostGetTransfersByAddressResponse: paginated transfer rows wrapped in a
                JSON-RPC 2.0 envelope. Access the rows via `response.result.data`
                and the next-page cursor via `response.result.pagination_token`
                (`None` when there are no more pages).
        """
        params: list = [address]
        if body is not None:
            params.append(body.model_dump(by_alias = True, exclude_none = True))
        rpc_body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getTransfersByAddress", "params": params}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetTransfersByAddressResponse, json = rpc_body)

    # ─── getTransactionsForAddress ────────────────────────────────────────────

    @overload
    def _post_get_transactions_for_address(self, sync: Literal[True], address: str, body: PostGetTransactionsForAddressBody | None = None) -> PostGetTransactionsForAddressResponse: ...
    @overload
    def _post_get_transactions_for_address(self, sync: Literal[False], address: str, body: PostGetTransactionsForAddressBody | None = None) -> Coroutine[None, None, PostGetTransactionsForAddressResponse]: ...
    def _post_get_transactions_for_address(self, sync: bool, address: str, body: PostGetTransactionsForAddressBody | None = None) -> PostGetTransactionsForAddressResponse | Coroutine[None, None, PostGetTransactionsForAddressResponse]:
        """
        This function refers to the **getTransactionsForAddress** Helius RPC endpoint.

        Returns the transaction history for any Solana account with advanced
        filtering (time, slot, signature, success/failure status, token-account
        inclusion), bidirectional sorting (`asc` / `desc`), and cursor-based
        pagination. Unlike `getSignaturesForAddress`, this endpoint can optionally
        return the **full transaction payload** in a single call and can include
        activity on token accounts owned by the queried wallet via
        `filters.token_accounts`.

        The endpoint is a Helius-exclusive feature (not part of standard Solana RPC),
        requires a Developer plan or higher, costs 50 credits per request and
        returns up to 100 full transactions or 1,000 signatures per page. The
        `token_accounts` filter does not see transactions prior to December 2022;
        devnet retention is limited to 2 weeks while mainnet retention is unlimited.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            address: base58-encoded account address to query (wallet, program, mint,
                pool, or token account).
            body: optional configuration object — see
                [`PostGetTransactionsForAddressBody`][cyhole.helius.schema.PostGetTransactionsForAddressBody].
                All fields are optional. Use it to choose detail level
                ([`HeliusTransactionDetails`][cyhole.helius.param.HeliusTransactionDetails]),
                sort order ([`HeliusSortOrder`][cyhole.helius.param.HeliusSortOrder]),
                commitment ([`HeliusCommitment`][cyhole.helius.param.HeliusCommitment]),
                encoding ([`HeliusEncoding`][cyhole.helius.param.HeliusEncoding]),
                and filters such as status
                ([`HeliusTransactionStatus`][cyhole.helius.param.HeliusTransactionStatus])
                and token-account inclusion
                ([`HeliusTokenAccountFilter`][cyhole.helius.param.HeliusTokenAccountFilter]).

        Returns:
            PostGetTransactionsForAddressResponse: paginated transaction list wrapped
                in a JSON-RPC 2.0 envelope. Access the rows via `response.result.data`
                and the next-page cursor via `response.result.pagination_token`
                (`None` when there are no more pages). Each
                [`TransactionForAddressItem`][cyhole.helius.schema.TransactionForAddressItem]
                exposes signature-mode or full-mode fields depending on the
                `transaction_details` parameter.
        """
        params: list = [address]
        if body is not None:
            params.append(body.model_dump(by_alias = True, exclude_none = True))
        rpc_body = {"jsonrpc": "2.0", "id": "cyhole", "method": "getTransactionsForAddress", "params": params}
        return self.api_return_model(sync, RequestType.POST.value, self.url_api, PostGetTransactionsForAddressResponse, json = rpc_body)

    # ─── getTransactionsByAddress ─────────────────────────────────────────────

    @overload
    def _get_transactions_by_address(self, sync: Literal[True], address: str, query: GetTransactionsByAddressQuery | None = None) -> GetTransactionsByAddressResponse: ...
    @overload
    def _get_transactions_by_address(self, sync: Literal[False], address: str, query: GetTransactionsByAddressQuery | None = None) -> Coroutine[None, None, GetTransactionsByAddressResponse]: ...
    def _get_transactions_by_address(self, sync: bool, address: str, query: GetTransactionsByAddressQuery | None = None) -> GetTransactionsByAddressResponse | Coroutine[None, None, GetTransactionsByAddressResponse]:
        """
        This function refers to the **getTransactionsByAddress** Enhanced Transactions API endpoint.

        Returns a list of fully decoded, human-readable enhanced transactions for a given
        Solana address. Unlike the JSON-RPC `getTransactionsForAddress`, this REST endpoint
        provides pre-parsed `description`, `type`, `source`, native/token transfer arrays,
        account-data balance deltas, instruction-level detail, and structured event objects
        for swaps, NFT operations, and compressed-NFT actions — all in a single call
        without additional parsing.

        Results are ordered newest-first by default and capped at 100 per page.
        Paginate backwards with `before_signature` or forwards with `after_signature`.
        Filter by time, slot, transaction type, or source program using the `query` object.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            address: base58-encoded Solana account address to query (wallet, program,
                mint, or token account).
            query: optional query-parameter object — see
                [`GetTransactionsByAddressQuery`][cyhole.helius.schema.GetTransactionsByAddressQuery].
                All fields are optional. Omit entirely to fetch the most recent
                transactions with API defaults.

        Returns:
            GetTransactionsByAddressResponse: list of enhanced transactions accessible
                via `.root`. Each [`EnhancedTransaction`][cyhole.helius.schema.EnhancedTransaction]
                exposes a human-readable `description`, `type`, `source`, transfer arrays,
                account-data deltas, instructions, and event details.

        Raises:
            HeliusException: if the API returns an error status.
        """
        url = f"{self.url_api_enhanced}/v0/addresses/{address}/transactions"
        params: dict = {"api-key": self._api_key}
        if query is not None:
            params.update(query.model_dump(by_alias = True, exclude_none = True))
        return self.api_return_model(sync, RequestType.GET.value, url, GetTransactionsByAddressResponse, params = params)

    # ─── getTransactions ──────────────────────────────────────────────────────

    @overload
    def _post_get_transactions(self, sync: Literal[True], signatures: list[str], commitment: str | None = None) -> PostGetTransactionsResponse: ...
    @overload
    def _post_get_transactions(self, sync: Literal[False], signatures: list[str], commitment: str | None = None) -> Coroutine[None, None, PostGetTransactionsResponse]: ...
    def _post_get_transactions(self, sync: bool, signatures: list[str], commitment: str | None = None) -> PostGetTransactionsResponse | Coroutine[None, None, PostGetTransactionsResponse]:
        """
        This function refers to the **getTransactions** Enhanced Transactions API endpoint.

        Parses up to 100 raw Solana transaction signatures into fully decoded,
        human-readable enhanced transactions in a single call. Each returned item
        exposes a parsed `description`, classified `type` and `source`, native and
        token transfer arrays, per-account balance deltas, top-level instructions
        with their CPI inner instructions, and structured event objects for swaps,
        NFT operations, and compressed-NFT actions — saving the caller from having
        to decode the raw transaction blob manually. Use this endpoint when you
        already know the signatures of interest (e.g. from a webhook, an indexer,
        or a previous `getTransactionsByAddress` call) and want enriched data for
        each one.

        Parameters:
            sync: if `True` run synchronously, else return a coroutine.
            signatures: list of base58-encoded transaction signatures to decode.
                Capped at 100 items per request by the API.
            commitment: optional block-finality level — `"finalized"` (API default)
                or `"confirmed"`. `"processed"` is not supported. Pass `None` to
                use the API default. See
                [`HeliusCommitment`][cyhole.helius.param.HeliusCommitment]
                for the corresponding `.value` strings.

        Returns:
            PostGetTransactionsResponse: list of enhanced transactions accessible
                via `.root`, preserving the order of `signatures`. Each
                [`EnhancedTransaction`][cyhole.helius.schema.EnhancedTransaction]
                exposes a human-readable `description`, `type`, `source`, transfer
                arrays, account-data deltas, instructions, and event details.

        Raises:
            HeliusException: if the API returns an error status.
        """
        url = f"{self.url_api_enhanced}/v0/transactions"
        params: dict = {"api-key": self._api_key}
        if commitment is not None:
            params["commitment"] = commitment
        body = {"transactions": signatures}
        return self.api_return_model(sync, RequestType.POST.value, url, PostGetTransactionsResponse, params = params, json = body)
