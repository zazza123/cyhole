import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from cyhole.helius import Helius
from cyhole.helius.schema import (
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
from .config import load_config, MockerManager

config = load_config()

mock_path = Path(config.mock_folder) / config.helius.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

# test constants
TEST_ASSET_ID = "4ZkS7zADmEFnkLPMHqJfPvHDN8oqfPjqDFGEQHiqPbEz"
TEST_OWNER_ADDRESS = "OWNER1111111111111111111111111111111111111111"
TEST_COLLECTION_ADDRESS = "COLL1111111111111111111111111111111111111111"
TEST_CREATOR_ADDRESS = "CREAT1111111111111111111111111111111111111111"
TEST_AUTHORITY_ADDRESS = "AUTH1111111111111111111111111111111111111111"
TEST_MASTER_MINT = "MASTER11111111111111111111111111111111111111"
TEST_TOKEN_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
TEST_TRANSFER_ADDRESS = "86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY"


class TestHelius:
    """Class grouping all unit tests for Helius interaction."""

    helius = Helius(api_key = config.helius.api_key or "test-api-key")
    mocker = MockerManager(mock_path)

    # ─── getAsset ─────────────────────────────────────────────────────────────

    def test_post_get_asset_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAsset" — synchronous logic.

        Mock Response File: postGetAsset_default.json
        """
        mock_file_name = "postGetAsset_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_asset(TEST_ASSET_ID)
        assert isinstance(response, PostGetAssetResponse)
        assert response.result.id == TEST_ASSET_ID

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_asset_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAsset" — asynchronous logic.

        Mock Response File: postGetAsset_default.json
        """
        mock_file_name = "postGetAsset_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_asset(TEST_ASSET_ID)
        assert isinstance(response, PostGetAssetResponse)
        assert response.result.id == TEST_ASSET_ID

    # ─── getAssetBatch ────────────────────────────────────────────────────────

    def test_post_get_asset_batch_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetBatch" — synchronous logic.

        Mock Response File: postGetAssetBatch_default.json
        """
        mock_file_name = "postGetAssetBatch_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetBatchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_asset_batch([TEST_ASSET_ID])
        assert isinstance(response, PostGetAssetBatchResponse)
        assert len(response.result) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_asset_batch_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetBatch" — asynchronous logic.

        Mock Response File: postGetAssetBatch_default.json
        """
        mock_file_name = "postGetAssetBatch_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetBatchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_asset_batch([TEST_ASSET_ID])
        assert isinstance(response, PostGetAssetBatchResponse)
        assert len(response.result) > 0

    # ─── getAssetProof ────────────────────────────────────────────────────────

    def test_post_get_asset_proof_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetProof" — synchronous logic.

        Mock Response File: postGetAssetProof_default.json
        """
        mock_file_name = "postGetAssetProof_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetProofResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_asset_proof(TEST_ASSET_ID)
        assert isinstance(response, PostGetAssetProofResponse)
        assert len(response.result.proof) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_asset_proof_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetProof" — asynchronous logic.

        Mock Response File: postGetAssetProof_default.json
        """
        mock_file_name = "postGetAssetProof_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetProofResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_asset_proof(TEST_ASSET_ID)
        assert isinstance(response, PostGetAssetProofResponse)
        assert len(response.result.proof) > 0

    # ─── getAssetProofBatch ───────────────────────────────────────────────────

    def test_post_get_asset_proof_batch_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetProofBatch" — synchronous logic.

        Mock Response File: postGetAssetProofBatch_default.json
        """
        mock_file_name = "postGetAssetProofBatch_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetProofBatchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_asset_proof_batch([TEST_ASSET_ID])
        assert isinstance(response, PostGetAssetProofBatchResponse)
        assert len(response.result) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_asset_proof_batch_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetProofBatch" — asynchronous logic.

        Mock Response File: postGetAssetProofBatch_default.json
        """
        mock_file_name = "postGetAssetProofBatch_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetProofBatchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_asset_proof_batch([TEST_ASSET_ID])
        assert isinstance(response, PostGetAssetProofBatchResponse)
        assert len(response.result) > 0

    # ─── getAssetsByOwner ─────────────────────────────────────────────────────

    def test_post_get_assets_by_owner_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByOwner" — synchronous logic.

        Mock Response File: postGetAssetsByOwner_default.json
        """
        mock_file_name = "postGetAssetsByOwner_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByOwnerResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetAssetsByOwnerBody(owner_address = TEST_OWNER_ADDRESS)
        response = self.helius.client.post_get_assets_by_owner(body)
        assert isinstance(response, PostGetAssetsByOwnerResponse)
        assert response.result.total > 0
        assert len(response.result.items) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_assets_by_owner_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByOwner" — asynchronous logic.

        Mock Response File: postGetAssetsByOwner_default.json
        """
        mock_file_name = "postGetAssetsByOwner_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByOwnerResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetAssetsByOwnerBody(owner_address = TEST_OWNER_ADDRESS)
        async with self.helius.async_client as client:
            response = await client.post_get_assets_by_owner(body)
        assert isinstance(response, PostGetAssetsByOwnerResponse)
        assert response.result.total > 0

    # ─── getAssetsByGroup ─────────────────────────────────────────────────────

    def test_post_get_assets_by_group_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByGroup" — synchronous logic.

        Mock Response File: postGetAssetsByGroup_default.json
        """
        mock_file_name = "postGetAssetsByGroup_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByGroupResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetAssetsByGroupBody(group_key = "collection", group_value = TEST_COLLECTION_ADDRESS)
        response = self.helius.client.post_get_assets_by_group(body)
        assert isinstance(response, PostGetAssetsByGroupResponse)
        assert response.result.total > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_assets_by_group_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByGroup" — asynchronous logic.

        Mock Response File: postGetAssetsByGroup_default.json
        """
        mock_file_name = "postGetAssetsByGroup_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByGroupResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetAssetsByGroupBody(group_key = "collection", group_value = TEST_COLLECTION_ADDRESS)
        async with self.helius.async_client as client:
            response = await client.post_get_assets_by_group(body)
        assert isinstance(response, PostGetAssetsByGroupResponse)
        assert response.result.total > 0

    # ─── getAssetsByCreator ───────────────────────────────────────────────────

    def test_post_get_assets_by_creator_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByCreator" — synchronous logic.

        Mock Response File: postGetAssetsByCreator_default.json
        """
        mock_file_name = "postGetAssetsByCreator_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByCreatorResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetAssetsByCreatorBody(creator_address = TEST_CREATOR_ADDRESS)
        response = self.helius.client.post_get_assets_by_creator(body)
        assert isinstance(response, PostGetAssetsByCreatorResponse)
        assert response.result.total > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_assets_by_creator_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByCreator" — asynchronous logic.

        Mock Response File: postGetAssetsByCreator_default.json
        """
        mock_file_name = "postGetAssetsByCreator_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByCreatorResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetAssetsByCreatorBody(creator_address = TEST_CREATOR_ADDRESS)
        async with self.helius.async_client as client:
            response = await client.post_get_assets_by_creator(body)
        assert isinstance(response, PostGetAssetsByCreatorResponse)
        assert response.result.total > 0

    # ─── getAssetsByAuthority ─────────────────────────────────────────────────

    def test_post_get_assets_by_authority_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByAuthority" — synchronous logic.

        Mock Response File: postGetAssetsByAuthority_default.json
        """
        mock_file_name = "postGetAssetsByAuthority_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByAuthorityResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetAssetsByAuthorityBody(authority_address = TEST_AUTHORITY_ADDRESS)
        response = self.helius.client.post_get_assets_by_authority(body)
        assert isinstance(response, PostGetAssetsByAuthorityResponse)
        assert response.result.total > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_assets_by_authority_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAssetsByAuthority" — asynchronous logic.

        Mock Response File: postGetAssetsByAuthority_default.json
        """
        mock_file_name = "postGetAssetsByAuthority_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAssetsByAuthorityResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetAssetsByAuthorityBody(authority_address = TEST_AUTHORITY_ADDRESS)
        async with self.helius.async_client as client:
            response = await client.post_get_assets_by_authority(body)
        assert isinstance(response, PostGetAssetsByAuthorityResponse)
        assert response.result.total > 0

    # ─── searchAssets ─────────────────────────────────────────────────────────

    def test_post_search_assets_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "searchAssets" — synchronous logic.

        Mock Response File: postSearchAssets_default.json
        """
        mock_file_name = "postSearchAssets_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSearchAssetsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostSearchAssetsBody(owner_address = TEST_OWNER_ADDRESS)
        response = self.helius.client.post_search_assets(body)
        assert isinstance(response, PostSearchAssetsResponse)
        assert response.result.total > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_search_assets_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "searchAssets" — asynchronous logic.

        Mock Response File: postSearchAssets_default.json
        """
        mock_file_name = "postSearchAssets_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSearchAssetsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostSearchAssetsBody(owner_address = TEST_OWNER_ADDRESS)
        async with self.helius.async_client as client:
            response = await client.post_search_assets(body)
        assert isinstance(response, PostSearchAssetsResponse)
        assert response.result.total > 0

    # ─── getSignaturesForAsset ────────────────────────────────────────────────

    def test_post_get_signatures_for_asset_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getSignaturesForAsset" — synchronous logic.

        Mock Response File: postGetSignaturesForAsset_default.json
        """
        mock_file_name = "postGetSignaturesForAsset_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetSignaturesForAssetResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_signatures_for_asset(TEST_ASSET_ID)
        assert isinstance(response, PostGetSignaturesForAssetResponse)
        assert response.result.total > 0
        assert len(response.result.items) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_signatures_for_asset_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getSignaturesForAsset" — asynchronous logic.

        Mock Response File: postGetSignaturesForAsset_default.json
        """
        mock_file_name = "postGetSignaturesForAsset_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetSignaturesForAssetResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_signatures_for_asset(TEST_ASSET_ID)
        assert isinstance(response, PostGetSignaturesForAssetResponse)
        assert response.result.total > 0

    # ─── getNftEditions ───────────────────────────────────────────────────────

    def test_post_get_nft_editions_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getNftEditions" — synchronous logic.

        Mock Response File: postGetNftEditions_default.json
        """
        mock_file_name = "postGetNftEditions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetNftEditionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_nft_editions(TEST_MASTER_MINT)
        assert isinstance(response, PostGetNftEditionsResponse)
        assert response.result.supply > 0
        assert len(response.result.editions) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_nft_editions_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getNftEditions" — asynchronous logic.

        Mock Response File: postGetNftEditions_default.json
        """
        mock_file_name = "postGetNftEditions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetNftEditionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_nft_editions(TEST_MASTER_MINT)
        assert isinstance(response, PostGetNftEditionsResponse)
        assert response.result.supply > 0

    # ─── getTokenAccounts ─────────────────────────────────────────────────────

    def test_post_get_token_accounts_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTokenAccounts" — synchronous logic.

        Mock Response File: postGetTokenAccounts_default.json
        """
        mock_file_name = "postGetTokenAccounts_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTokenAccountsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetTokenAccountsBody(mint = TEST_TOKEN_MINT)
        response = self.helius.client.post_get_token_accounts(body)
        assert isinstance(response, PostGetTokenAccountsResponse)
        assert response.result.total > 0
        assert len(response.result.token_accounts) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_token_accounts_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTokenAccounts" — asynchronous logic.

        Mock Response File: postGetTokenAccounts_default.json
        """
        mock_file_name = "postGetTokenAccounts_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTokenAccountsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetTokenAccountsBody(mint = TEST_TOKEN_MINT)
        async with self.helius.async_client as client:
            response = await client.post_get_token_accounts(body)
        assert isinstance(response, PostGetTokenAccountsResponse)
        assert response.result.total > 0

    # ─── getTransfersByAddress ────────────────────────────────────────────────

    def test_post_get_transfers_by_address_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransfersByAddress" — synchronous logic.

        Mock Response File: postGetTransfersByAddress_default.json
        """
        mock_file_name = "postGetTransfersByAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransfersByAddressResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_transfers_by_address(TEST_TRANSFER_ADDRESS)
        assert isinstance(response, PostGetTransfersByAddressResponse)
        assert len(response.result.data) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_transfers_by_address_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransfersByAddress" — asynchronous logic.

        Mock Response File: postGetTransfersByAddress_default.json
        """
        mock_file_name = "postGetTransfersByAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransfersByAddressResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetTransfersByAddressBody(limit = 50)
        async with self.helius.async_client as client:
            response = await client.post_get_transfers_by_address(TEST_TRANSFER_ADDRESS, body)
        assert isinstance(response, PostGetTransfersByAddressResponse)
        assert len(response.result.data) > 0

    # ─── getTransactionsForAddress ────────────────────────────────────────────

    def test_post_get_transactions_for_address_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactionsForAddress" — synchronous logic.

        Mock Response File: postGetTransactionsForAddress_default.json
        """
        mock_file_name = "postGetTransactionsForAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionsForAddressResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_transactions_for_address(TEST_TRANSFER_ADDRESS)
        assert isinstance(response, PostGetTransactionsForAddressResponse)
        assert len(response.result.data) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_transactions_for_address_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactionsForAddress" — asynchronous logic.

        Mock Response File: postGetTransactionsForAddress_default.json
        """
        mock_file_name = "postGetTransactionsForAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionsForAddressResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetTransactionsForAddressBody(limit = 50)
        async with self.helius.async_client as client:
            response = await client.post_get_transactions_for_address(TEST_TRANSFER_ADDRESS, body)
        assert isinstance(response, PostGetTransactionsForAddressResponse)
        assert len(response.result.data) > 0

    # ─── getTransactionsByAddress ─────────────────────────────────────────────

    def test_get_transactions_by_address_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactionsByAddress" — synchronous logic.

        Mock Response File: getTransactionsByAddress_default.json
        """
        mock_file_name = "getTransactionsByAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionsByAddressResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.get_transactions_by_address(TEST_TRANSFER_ADDRESS)
        assert isinstance(response, GetTransactionsByAddressResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transactions_by_address_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactionsByAddress" — asynchronous logic.

        Mock Response File: getTransactionsByAddress_default.json
        """
        mock_file_name = "getTransactionsByAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionsByAddressResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        query = GetTransactionsByAddressQuery(limit = 10)
        async with self.helius.async_client as client:
            response = await client.get_transactions_by_address(TEST_TRANSFER_ADDRESS, query)
        assert isinstance(response, GetTransactionsByAddressResponse)
        assert len(response.root) > 0
