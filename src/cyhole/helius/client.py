from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
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
)

if TYPE_CHECKING:
    from ..helius.interaction import Helius


class HeliusClient(APIClient):
    """Client for synchronous API calls for `Helius` interaction."""

    def __init__(self, interaction: Helius, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Helius = self._interaction

    def post_get_asset(self, asset_id: str, options: PostGetAssetOptions | None = None) -> PostGetAssetResponse:
        """
        Call the Helius POST **[getAsset](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset`][cyhole.helius.interaction.Helius._post_get_asset].
        """
        return self._interaction._post_get_asset(True, asset_id, options)

    def post_get_asset_batch(self, ids: list[str]) -> PostGetAssetBatchResponse:
        """
        Call the Helius POST **[getAssetBatch](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_batch`][cyhole.helius.interaction.Helius._post_get_asset_batch].
        """
        return self._interaction._post_get_asset_batch(True, ids)

    def post_get_asset_proof(self, asset_id: str) -> PostGetAssetProofResponse:
        """
        Call the Helius POST **[getAssetProof](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_proof`][cyhole.helius.interaction.Helius._post_get_asset_proof].
        """
        return self._interaction._post_get_asset_proof(True, asset_id)

    def post_get_asset_proof_batch(self, ids: list[str]) -> PostGetAssetProofBatchResponse:
        """
        Call the Helius POST **[getAssetProofBatch](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_proof_batch`][cyhole.helius.interaction.Helius._post_get_asset_proof_batch].
        """
        return self._interaction._post_get_asset_proof_batch(True, ids)

    def post_get_assets_by_owner(self, body: PostGetAssetsByOwnerBody) -> PostGetAssetsByOwnerResponse:
        """
        Call the Helius POST **[getAssetsByOwner](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_owner`][cyhole.helius.interaction.Helius._post_get_assets_by_owner].
        """
        return self._interaction._post_get_assets_by_owner(True, body)

    def post_get_assets_by_group(self, body: PostGetAssetsByGroupBody) -> PostGetAssetsByGroupResponse:
        """
        Call the Helius POST **[getAssetsByGroup](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_group`][cyhole.helius.interaction.Helius._post_get_assets_by_group].
        """
        return self._interaction._post_get_assets_by_group(True, body)

    def post_get_assets_by_creator(self, body: PostGetAssetsByCreatorBody) -> PostGetAssetsByCreatorResponse:
        """
        Call the Helius POST **[getAssetsByCreator](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_creator`][cyhole.helius.interaction.Helius._post_get_assets_by_creator].
        """
        return self._interaction._post_get_assets_by_creator(True, body)

    def post_get_assets_by_authority(self, body: PostGetAssetsByAuthorityBody) -> PostGetAssetsByAuthorityResponse:
        """
        Call the Helius POST **[getAssetsByAuthority](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_authority`][cyhole.helius.interaction.Helius._post_get_assets_by_authority].
        """
        return self._interaction._post_get_assets_by_authority(True, body)

    def post_search_assets(self, body: PostSearchAssetsBody) -> PostSearchAssetsResponse:
        """
        Call the Helius POST **[searchAssets](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_search_assets`][cyhole.helius.interaction.Helius._post_search_assets].
        """
        return self._interaction._post_search_assets(True, body)

    def post_get_signatures_for_asset(self, asset_id: str, page: int | None = None, limit: int | None = None) -> PostGetSignaturesForAssetResponse:
        """
        Call the Helius POST **[getSignaturesForAsset](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_signatures_for_asset`][cyhole.helius.interaction.Helius._post_get_signatures_for_asset].
        """
        return self._interaction._post_get_signatures_for_asset(True, asset_id, page, limit)

    def post_get_nft_editions(self, mint: str, page: int | None = None, limit: int | None = None) -> PostGetNftEditionsResponse:
        """
        Call the Helius POST **[getNftEditions](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_nft_editions`][cyhole.helius.interaction.Helius._post_get_nft_editions].
        """
        return self._interaction._post_get_nft_editions(True, mint, page, limit)

    def post_get_token_accounts(self, body: PostGetTokenAccountsBody) -> PostGetTokenAccountsResponse:
        """
        Call the Helius POST **[getTokenAccounts](https://www.helius.dev/docs/das-api)** DAS API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_token_accounts`][cyhole.helius.interaction.Helius._post_get_token_accounts].
        """
        return self._interaction._post_get_token_accounts(True, body)

    def post_get_transfers_by_address(self, address: str, body: PostGetTransfersByAddressBody | None = None) -> PostGetTransfersByAddressResponse:
        """
        Call the Helius POST **[getTransfersByAddress](https://www.helius.dev/docs/rpc/gettransfersbyaddress)** RPC API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_transfers_by_address`][cyhole.helius.interaction.Helius._post_get_transfers_by_address].
        """
        return self._interaction._post_get_transfers_by_address(True, address, body)

    def post_get_transactions_for_address(self, address: str, body: PostGetTransactionsForAddressBody | None = None) -> PostGetTransactionsForAddressResponse:
        """
        Call the Helius POST **[getTransactionsForAddress](https://www.helius.dev/docs/rpc/gettransactionsforaddress)** RPC API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._post_get_transactions_for_address`][cyhole.helius.interaction.Helius._post_get_transactions_for_address].
        """
        return self._interaction._post_get_transactions_for_address(True, address, body)

    def get_transactions_by_address(self, address: str, query: GetTransactionsByAddressQuery | None = None) -> GetTransactionsByAddressResponse:
        """
        Call the Helius GET **[getTransactionsByAddress](https://www.helius.dev/docs/api-reference/enhanced-transactions/gettransactionsbyaddress)** Enhanced Transactions API endpoint for synchronous logic.
        All the API endpoint details are available on [`Helius._get_transactions_by_address`][cyhole.helius.interaction.Helius._get_transactions_by_address].
        """
        return self._interaction._get_transactions_by_address(True, address, query)


class HeliusAsyncClient(AsyncAPIClient):
    """Client for asynchronous API calls for `Helius` interaction."""

    def __init__(self, interaction: Helius, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Helius = self._interaction

    async def post_get_asset(self, asset_id: str, options: PostGetAssetOptions | None = None) -> PostGetAssetResponse:
        """
        Call the Helius POST **[getAsset](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset`][cyhole.helius.interaction.Helius._post_get_asset].
        """
        return await self._interaction._post_get_asset(False, asset_id, options)

    async def post_get_asset_batch(self, ids: list[str]) -> PostGetAssetBatchResponse:
        """
        Call the Helius POST **[getAssetBatch](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_batch`][cyhole.helius.interaction.Helius._post_get_asset_batch].
        """
        return await self._interaction._post_get_asset_batch(False, ids)

    async def post_get_asset_proof(self, asset_id: str) -> PostGetAssetProofResponse:
        """
        Call the Helius POST **[getAssetProof](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_proof`][cyhole.helius.interaction.Helius._post_get_asset_proof].
        """
        return await self._interaction._post_get_asset_proof(False, asset_id)

    async def post_get_asset_proof_batch(self, ids: list[str]) -> PostGetAssetProofBatchResponse:
        """
        Call the Helius POST **[getAssetProofBatch](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_asset_proof_batch`][cyhole.helius.interaction.Helius._post_get_asset_proof_batch].
        """
        return await self._interaction._post_get_asset_proof_batch(False, ids)

    async def post_get_assets_by_owner(self, body: PostGetAssetsByOwnerBody) -> PostGetAssetsByOwnerResponse:
        """
        Call the Helius POST **[getAssetsByOwner](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_owner`][cyhole.helius.interaction.Helius._post_get_assets_by_owner].
        """
        return await self._interaction._post_get_assets_by_owner(False, body)

    async def post_get_assets_by_group(self, body: PostGetAssetsByGroupBody) -> PostGetAssetsByGroupResponse:
        """
        Call the Helius POST **[getAssetsByGroup](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_group`][cyhole.helius.interaction.Helius._post_get_assets_by_group].
        """
        return await self._interaction._post_get_assets_by_group(False, body)

    async def post_get_assets_by_creator(self, body: PostGetAssetsByCreatorBody) -> PostGetAssetsByCreatorResponse:
        """
        Call the Helius POST **[getAssetsByCreator](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_creator`][cyhole.helius.interaction.Helius._post_get_assets_by_creator].
        """
        return await self._interaction._post_get_assets_by_creator(False, body)

    async def post_get_assets_by_authority(self, body: PostGetAssetsByAuthorityBody) -> PostGetAssetsByAuthorityResponse:
        """
        Call the Helius POST **[getAssetsByAuthority](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_assets_by_authority`][cyhole.helius.interaction.Helius._post_get_assets_by_authority].
        """
        return await self._interaction._post_get_assets_by_authority(False, body)

    async def post_search_assets(self, body: PostSearchAssetsBody) -> PostSearchAssetsResponse:
        """
        Call the Helius POST **[searchAssets](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_search_assets`][cyhole.helius.interaction.Helius._post_search_assets].
        """
        return await self._interaction._post_search_assets(False, body)

    async def post_get_signatures_for_asset(self, asset_id: str, page: int | None = None, limit: int | None = None) -> PostGetSignaturesForAssetResponse:
        """
        Call the Helius POST **[getSignaturesForAsset](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_signatures_for_asset`][cyhole.helius.interaction.Helius._post_get_signatures_for_asset].
        """
        return await self._interaction._post_get_signatures_for_asset(False, asset_id, page, limit)

    async def post_get_nft_editions(self, mint: str, page: int | None = None, limit: int | None = None) -> PostGetNftEditionsResponse:
        """
        Call the Helius POST **[getNftEditions](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_nft_editions`][cyhole.helius.interaction.Helius._post_get_nft_editions].
        """
        return await self._interaction._post_get_nft_editions(False, mint, page, limit)

    async def post_get_token_accounts(self, body: PostGetTokenAccountsBody) -> PostGetTokenAccountsResponse:
        """
        Call the Helius POST **[getTokenAccounts](https://www.helius.dev/docs/das-api)** DAS API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_token_accounts`][cyhole.helius.interaction.Helius._post_get_token_accounts].
        """
        return await self._interaction._post_get_token_accounts(False, body)

    async def post_get_transfers_by_address(self, address: str, body: PostGetTransfersByAddressBody | None = None) -> PostGetTransfersByAddressResponse:
        """
        Call the Helius POST **[getTransfersByAddress](https://www.helius.dev/docs/rpc/gettransfersbyaddress)** RPC API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_transfers_by_address`][cyhole.helius.interaction.Helius._post_get_transfers_by_address].
        """
        return await self._interaction._post_get_transfers_by_address(False, address, body)

    async def post_get_transactions_for_address(self, address: str, body: PostGetTransactionsForAddressBody | None = None) -> PostGetTransactionsForAddressResponse:
        """
        Call the Helius POST **[getTransactionsForAddress](https://www.helius.dev/docs/rpc/gettransactionsforaddress)** RPC API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._post_get_transactions_for_address`][cyhole.helius.interaction.Helius._post_get_transactions_for_address].
        """
        return await self._interaction._post_get_transactions_for_address(False, address, body)

    async def get_transactions_by_address(self, address: str, query: GetTransactionsByAddressQuery | None = None) -> GetTransactionsByAddressResponse:
        """
        Call the Helius GET **[getTransactionsByAddress](https://www.helius.dev/docs/api-reference/enhanced-transactions/gettransactionsbyaddress)** Enhanced Transactions API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Helius._get_transactions_by_address`][cyhole.helius.interaction.Helius._get_transactions_by_address].
        """
        return await self._interaction._get_transactions_by_address(False, address, query)
