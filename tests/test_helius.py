import json
import pytest
from pathlib import Path
from pydantic import ValidationError
from requests import Response
from pytest_mock import MockerFixture

from cyhole.helius import Helius
from cyhole.helius.exception import HeliusAccountCountError, HeliusException, HeliusRPCError
from cyhole.helius.param import HeliusAccountEncoding, HeliusCommitment, HeliusEncoding, HeliusParsedEventsSummaryType, HeliusParserStatus, HeliusSortOrder
from cyhole.helius.schema import (
    PostGetAssetsByOwnerBody,
    PostGetAssetsByGroupBody,
    PostGetAssetsByCreatorBody,
    PostGetAssetsByAuthorityBody,
    PostSearchAssetsBody,
    PostGetTokenAccountsBody,
    PostGetTransfersByAddressBody,
    PostGetTransactionsForAddressBody,
    PostGetSignaturesForAddressBody,
    PostGetTransactionBody,
    PostGetAccountInfoBody,
    AccountDataSlice,
    GetTransactionsByAddressQuery,
    PostParsedEventsRange,
    PostParsedEventsTransactionHistoryBody,
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
    PostGetSignaturesForAddressResponse,
    PostGetTransactionResponse,
    PostGetAccountInfoResponse,
    PostGetMultipleAccountsResponse,
    GetTransactionsByAddressResponse,
    PostGetTransactionsResponse,
    PostParsedEventsTransactionsResponse,
    PostParsedEventsTransactionHistoryResponse,
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
TEST_TRANSACTION_SIGNATURE = "5j7s6fJ2HMoqMhiMWBgFMDWHkKnMJpBzPvKxjMwWqkibMr5PAtPQWViHJEgjSGj3CeAnj8Vp7rR9Z5Z8Z5Z8Z5"
# Parsed Events: a plain SOL transfer, a Pump.fun AMM swap, and a string that is not a
# valid signature (the Enhanced Transactions placeholder above), in this order.
TEST_PARSED_EVENTS_TRANSFER_SIGNATURE = "3UbfkqQtk9v3dht5YmK3n5j3F2WDPG3mToZX4nwNd327dHGgm7vXuyUzyf7VnQjSwcU8xZF5X2r3DprkxRCBprWx"
TEST_PARSED_EVENTS_SWAP_SIGNATURE = "3F4vmiSZcPtafg5QhPkuBF6XRzbxQkYcn2Td8hRZL8gXMKjDwvA6p1CS7aAZrUsNX2UrK5C7RpJTrPGYcm6QgyE9"
TEST_PARSED_EVENTS_SIGNATURES = [
    TEST_PARSED_EVENTS_TRANSFER_SIGNATURE,
    TEST_PARSED_EVENTS_SWAP_SIGNATURE,
    TEST_TRANSACTION_SIGNATURE,
]
TEST_PARSED_EVENTS_ADDRESS = "8zxkmeqHrpmqyzCSGxLNWZ4W7ZgjwHuo4HV11ALceNAg"
# Standard Solana RPC (getSignaturesForAddress / getTransaction): the fee payer of the
# mainnet transaction captured in the mocks, that transaction, and two older signatures
# of the same address used as `before` / `until` bounds.
TEST_SIGNATURES_ADDRESS = "CHryNxUfvY8yTWDdCjspz24zmkgYoKbi5MQGL42H4yme"
TEST_RPC_TRANSACTION_SIGNATURE = "4AtQkCrszud6jZ3PpL7hVGd6DRaXvNWGHqYsiFBbeZxTv614yaef7xZTSoALEZ7jJDopseMuitMifDC7UnBZ5YJp"
TEST_SIGNATURES_BEFORE = "2pago8JTbTpaJj9PWkj66sUsbNXdmmHyxAiUFwfnHi24PZNESJL8YgSvjPExxrs2Mfn1vbdyLT56byghYpSetyXw"
TEST_SIGNATURES_UNTIL = "343wGRyiZtzX4tsSXKCe1BUZ1WtxBPDD7ifyjrCSp4a7hJdfpiB2bEM6TL7nRoXS7xawfjEi4XbGJGpePL5qYV5T"
# Standard Solana RPC (getAccountInfo / getMultipleAccounts): the WSOL vault of a Meteora
# DAMM v2 pool, that pool, and a never-funded address, as captured in the mocks.
TEST_ACCOUNT_ADDRESS = "7V9ARybm8rqtcvRKBECNFM7KcQG2MjpMNM6fQRDpHHwU"
TEST_POOL_ADDRESS = "7meYct58Wx9ojhwG8UqyR5jwDF1xctniuTgGSvvaiKD5"
TEST_ACCOUNT_MISSING = "5vDymKjPUAG2aswC6SGMuhKJ8bHyVTFJ5LHm96SGhXtv"
# A plain system wallet (no data), read without an encoding.
TEST_ACCOUNT_WALLET = "6iuhuVyE7PMTLraNud7FH64byeNgdxJm1NfJNVPd1dyS"
WSOL_MINT = "So11111111111111111111111111111111111111112"


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

    # ─── getSignaturesForAddress ──────────────────────────────────────────────

    def test_post_get_signatures_for_address_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getSignaturesForAddress" — synchronous logic.

        Mock Response File: postGetSignaturesForAddress_default.json
        """
        mock_file_name = "postGetSignaturesForAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetSignaturesForAddressResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_signatures_for_address(TEST_SIGNATURES_ADDRESS)
        assert isinstance(response, PostGetSignaturesForAddressResponse)
        assert len(response.result) > 0
        slots = [item.slot for item in response.result]
        assert slots == sorted(slots, reverse = True)

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_signatures_for_address_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getSignaturesForAddress" — asynchronous logic.

        Mock Response File: postGetSignaturesForAddress_default.json
        """
        mock_file_name = "postGetSignaturesForAddress_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetSignaturesForAddressResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetSignaturesForAddressBody(limit = 5)
        async with self.helius.async_client as client:
            response = await client.post_get_signatures_for_address(TEST_SIGNATURES_ADDRESS, body)
        assert isinstance(response, PostGetSignaturesForAddressResponse)
        assert 0 < len(response.result) <= 5

    def test_post_get_signatures_for_address_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getSignaturesForAddress" — request sent to the API.

        Checks the URL and the JSON-RPC body, with and without the optional config object,
        and that the config is sent with the API's camelCase names.

        Mock Response File: postGetSignaturesForAddress_default.json
        """
        mock_response = self.mocker.load_mock_response("postGetSignaturesForAddress_default", PostGetSignaturesForAddressResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.helius.client.post_get_signatures_for_address(TEST_SIGNATURES_ADDRESS)
        args, kwargs = api.call_args
        assert args[0] == "POST"
        assert args[1] == self.helius.url_api
        assert kwargs["json"] == {"jsonrpc": "2.0", "id": "cyhole", "method": "getSignaturesForAddress", "params": [TEST_SIGNATURES_ADDRESS]}

        body = PostGetSignaturesForAddressBody(
            limit = 100,
            before = TEST_SIGNATURES_BEFORE,
            until = TEST_SIGNATURES_UNTIL,
            commitment = HeliusCommitment.CONFIRMED.value,
            min_context_slot = 456000000,
        )
        self.helius.client.post_get_signatures_for_address(TEST_SIGNATURES_ADDRESS, body)
        _, kwargs = api.call_args
        assert kwargs["json"]["params"] == [
            TEST_SIGNATURES_ADDRESS,
            {
                "limit": 100,
                "before": TEST_SIGNATURES_BEFORE,
                "until": TEST_SIGNATURES_UNTIL,
                "commitment": "confirmed",
                "minContextSlot": 456000000,
            },
        ]

    def test_post_get_signatures_for_address_body_limit(self) -> None:
        """
        Unit Test for endpoint "getSignaturesForAddress" — `limit` bounds of the body.

        The API accepts between 1 and 1,000 signatures per call.
        """
        with pytest.raises(ValidationError):
            PostGetSignaturesForAddressBody(limit = 0)
        with pytest.raises(ValidationError):
            PostGetSignaturesForAddressBody(limit = 1001)
        assert PostGetSignaturesForAddressBody(limit = 1000).limit == 1000

    # ─── getTransaction ───────────────────────────────────────────────────────

    def test_post_get_transaction_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — synchronous logic.

        Mock Response File: postGetTransaction_default.json
        """
        mock_file_name = "postGetTransaction_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetTransactionBody(encoding = HeliusEncoding.JSON.value, max_supported_transaction_version = 0)
        response = self.helius.client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE, body)
        assert isinstance(response, PostGetTransactionResponse)
        assert response.result is not None
        assert response.result.transaction["signatures"][0] == TEST_RPC_TRANSACTION_SIGNATURE
        assert response.result.meta is not None
        assert len(response.result.meta.pre_balances) == len(response.result.meta.post_balances)

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_transaction_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — asynchronous logic.

        Mock Response File: postGetTransaction_default.json
        """
        mock_file_name = "postGetTransaction_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetTransactionBody(encoding = HeliusEncoding.JSON.value, max_supported_transaction_version = 0)
        async with self.helius.async_client as client:
            response = await client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE, body)
        assert isinstance(response, PostGetTransactionResponse)
        assert response.result is not None
        assert response.result.meta is not None
        assert response.result.meta.fee > 0

    def test_post_get_transaction_not_found(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — signature not found.

        The API answers with `result: null`, which must be read as `None`. The mock file is
        served as is: `MockerManager.load_mock_response` drops `None` fields, and `result` is
        required so that a JSON-RPC error answer cannot pass for "not found".

        Mock Response File: postGetTransaction_not_found.json
        """
        mock_response = Response()
        mock_response._content = (mock_path / "postGetTransaction_not_found.json").read_bytes()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"
        mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_transaction(TEST_TRANSACTION_SIGNATURE)
        assert isinstance(response, PostGetTransactionResponse)
        assert response.result is None

    def _rpc_error_mock(self, code: int = -32015, message: str = "Transaction version (0) is not supported", data: object = None) -> Response:
        """
        A JSON-RPC error answer: HTTP 200 and an `error` object in place of `result`.
        """
        error: dict = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        mock_response = Response()
        mock_response._content = json.dumps({"jsonrpc": "2.0", "id": "cyhole", "error": error}).encode()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"
        return mock_response

    def test_post_get_transaction_rpc_error(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — a JSON-RPC error answer raises
        `HeliusRPCError` with its code, message and data, not a `ValidationError`.
        """
        mocker.patch("cyhole.core.client.APIClient.api", return_value = self._rpc_error_mock(data = {"slot": 1}))

        with pytest.raises(HeliusRPCError) as error:
            self.helius.client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE)
        assert isinstance(error.value, HeliusException)
        assert error.value.code == -32015
        assert error.value.message == "Transaction version (0) is not supported"
        assert error.value.data == {"slot": 1}
        assert "-32015" in str(error.value)

    @pytest.mark.asyncio
    async def test_post_get_transaction_rpc_error_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — asynchronous logic raises
        `HeliusRPCError` on a JSON-RPC error answer.
        """
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = self._rpc_error_mock())

        with pytest.raises(HeliusRPCError) as error:
            async with self.helius.async_client as client:
                await client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE)
        assert error.value.code == -32015
        assert error.value.message == "Transaction version (0) is not supported"
        assert error.value.data is None

    def test_post_get_account_info_rpc_error(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — the JSON-RPC error check is shared by
        the standard RPC methods.
        """
        mocker.patch("cyhole.core.client.APIClient.api", return_value = self._rpc_error_mock(code = -32602, message = "Invalid param"))

        with pytest.raises(HeliusRPCError) as error:
            self.helius.client.post_get_account_info(TEST_ACCOUNT_ADDRESS)
        assert error.value.code == -32602
        assert error.value.message == "Invalid param"

    @pytest.mark.asyncio
    async def test_post_get_account_info_rpc_error_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — asynchronous logic raises
        `HeliusRPCError` on a JSON-RPC error answer.
        """
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = self._rpc_error_mock(code = -32602, message = "Invalid param"))

        with pytest.raises(HeliusRPCError):
            async with self.helius.async_client as client:
                await client.post_get_account_info(TEST_ACCOUNT_ADDRESS)

    def test_post_get_transaction_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransaction" — request sent to the API.

        Checks the URL and the JSON-RPC body, with and without the optional config object,
        and that the config is sent with the API's camelCase names.

        Mock Response File: postGetTransaction_default.json
        """
        mock_response = self.mocker.load_mock_response("postGetTransaction_default", PostGetTransactionResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.helius.client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE)
        args, kwargs = api.call_args
        assert args[0] == "POST"
        assert args[1] == self.helius.url_api
        assert kwargs["json"] == {"jsonrpc": "2.0", "id": "cyhole", "method": "getTransaction", "params": [TEST_RPC_TRANSACTION_SIGNATURE]}

        body = PostGetTransactionBody(
            encoding = HeliusEncoding.JSON_PARSED.value,
            commitment = HeliusCommitment.CONFIRMED.value,
            max_supported_transaction_version = 0,
        )
        self.helius.client.post_get_transaction(TEST_RPC_TRANSACTION_SIGNATURE, body)
        _, kwargs = api.call_args
        assert kwargs["json"]["params"] == [
            TEST_RPC_TRANSACTION_SIGNATURE,
            {"encoding": "jsonParsed", "commitment": "confirmed", "maxSupportedTransactionVersion": 0},
        ]

    # ─── getAccountInfo ───────────────────────────────────────────────────────

    def test_post_get_account_info_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — synchronous logic, base64 encoding.

        Mock Response File: postGetAccountInfo_default.json
        """
        mock_file_name = "postGetAccountInfo_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAccountInfoResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostGetAccountInfoBody(encoding = HeliusAccountEncoding.BASE64.value)
        response = self.helius.client.post_get_account_info(TEST_ACCOUNT_ADDRESS, body)
        assert isinstance(response, PostGetAccountInfoResponse)
        assert response.result.value is not None
        assert response.result.value.data[1] == "base64"
        assert response.result.context.slot > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_account_info_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — asynchronous logic, jsonParsed encoding.

        Mock Response File: postGetAccountInfo_json_parsed.json
        """
        mock_file_name = "postGetAccountInfo_json_parsed"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetAccountInfoResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostGetAccountInfoBody(encoding = HeliusAccountEncoding.JSON_PARSED.value)
        async with self.helius.async_client as client:
            response = await client.post_get_account_info(TEST_ACCOUNT_ADDRESS, body)
        assert isinstance(response, PostGetAccountInfoResponse)
        assert response.result.value is not None
        assert isinstance(response.result.value.data, dict)
        assert response.result.value.data["parsed"]["info"]["mint"] == WSOL_MINT

    def test_post_get_account_info_not_found_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — account not found.

        The API answers with `value: null`, which must be read as `None`. The mock file is
        served as is: `MockerManager.load_mock_response` drops `None` fields.

        Mock Response File: postGetAccountInfo_not_found.json
        """
        mock_response = Response()
        mock_response._content = (mock_path / "postGetAccountInfo_not_found.json").read_bytes()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"
        mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_account_info(TEST_ACCOUNT_MISSING)
        assert isinstance(response, PostGetAccountInfoResponse)
        assert response.result.value is None

    def test_post_get_account_info_body_serialises(self) -> None:
        """
        Unit Test for the "getAccountInfo" config object: camelCase names and the data slice.
        """
        body = PostGetAccountInfoBody(encoding = "base64", data_slice = AccountDataSlice(offset = 64, length = 8))
        assert body.model_dump(by_alias = True, exclude_none = True) == {
            "encoding": "base64", "dataSlice": {"offset": 64, "length": 8}}

    def test_post_get_account_info_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — request sent to the API.

        Mock Response File: postGetAccountInfo_default.json
        """
        mock_response = self.mocker.load_mock_response("postGetAccountInfo_default", PostGetAccountInfoResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.helius.client.post_get_account_info(TEST_ACCOUNT_ADDRESS)
        args, kwargs = api.call_args
        assert args[0] == "POST"
        assert args[1] == self.helius.url_api
        assert kwargs["json"] == {"jsonrpc": "2.0", "id": "cyhole", "method": "getAccountInfo", "params": [TEST_ACCOUNT_ADDRESS]}

        body = PostGetAccountInfoBody(encoding = HeliusAccountEncoding.BASE64.value, commitment = HeliusCommitment.CONFIRMED.value)
        self.helius.client.post_get_account_info(TEST_ACCOUNT_ADDRESS, body)
        _, kwargs = api.call_args
        assert kwargs["json"]["params"] == [TEST_ACCOUNT_ADDRESS, {"encoding": "base64", "commitment": "confirmed"}]

    def _raw_mock(self, file_name: str) -> Response:
        """A mock file served as is, bypassing `MockerManager`, which drops `None` fields."""
        mock_response = Response()
        mock_response._content = (mock_path / f"{file_name}.json").read_bytes()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"
        return mock_response

    def test_post_get_account_info_without_encoding(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — no encoding in the request.

        The API default is base58, returned as a plain string, not as a `[data, encoding]`
        pair.

        Mock Response File: postGetAccountInfo_no_encoding.json
        """
        mocker.patch("cyhole.core.client.APIClient.api", return_value = self._raw_mock("postGetAccountInfo_no_encoding"))

        response = self.helius.client.post_get_account_info(TEST_ACCOUNT_WALLET)
        assert response.result.value is not None
        assert response.result.value.data == ""

    def test_post_get_account_info_error_answer(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getAccountInfo" — JSON-RPC error answer.

        Without an encoding the API answers an account larger than 128 bytes with an
        error and no `result`: it must raise `HeliusRPCError`, not read as a missing account.

        Mock Response File: postGetAccountInfo_error.json
        """
        mocker.patch("cyhole.core.client.APIClient.api", return_value = self._raw_mock("postGetAccountInfo_error"))

        with pytest.raises(HeliusRPCError):
            self.helius.client.post_get_account_info(TEST_POOL_ADDRESS)

    # ─── getMultipleAccounts ──────────────────────────────────────────────────

    def _multiple_accounts_mock(self) -> Response:
        """
        The `getMultipleAccounts` mock served as is: its third account is `null`, and
        `MockerManager.load_mock_response` would drop it.
        """
        mock_response = Response()
        mock_response._content = (mock_path / "postGetMultipleAccounts_default.json").read_bytes()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"
        return mock_response

    def test_post_get_multiple_accounts_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — synchronous logic.

        A pool, its WSOL vault and a missing account: the missing one is `None`, in place.

        Mock Response File: postGetMultipleAccounts_default.json
        """
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = self._multiple_accounts_mock())

        body = PostGetAccountInfoBody(encoding = HeliusAccountEncoding.BASE64.value)
        response = self.helius.client.post_get_account_info([TEST_POOL_ADDRESS, TEST_ACCOUNT_ADDRESS, TEST_ACCOUNT_MISSING], body)
        assert isinstance(response, PostGetMultipleAccountsResponse)
        assert len(response.result.value) == 3
        assert response.result.value[0] is not None and response.result.value[1] is not None
        assert response.result.value[2] is None
        _, kwargs = api.call_args
        assert kwargs["json"] == {
            "jsonrpc": "2.0", "id": "cyhole", "method": "getMultipleAccounts",
            "params": [[TEST_POOL_ADDRESS, TEST_ACCOUNT_ADDRESS, TEST_ACCOUNT_MISSING], {"encoding": "base64"}],
        }

    @pytest.mark.asyncio
    async def test_post_get_multiple_accounts_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — asynchronous logic.

        Mock Response File: postGetMultipleAccounts_default.json
        """
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = self._multiple_accounts_mock())

        body = PostGetAccountInfoBody(encoding = HeliusAccountEncoding.BASE64.value)
        async with self.helius.async_client as client:
            response = await client.post_get_account_info([TEST_POOL_ADDRESS, TEST_ACCOUNT_ADDRESS, TEST_ACCOUNT_MISSING], body)
        assert isinstance(response, PostGetMultipleAccountsResponse)
        assert [account is None for account in response.result.value] == [False, False, True]

    @pytest.mark.parametrize("addresses", [[], [TEST_ACCOUNT_ADDRESS] * 101])
    def test_post_get_account_info_rejects_bad_address_count(self, mocker: MockerFixture, addresses: list[str]) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — an empty list or more than 100
        addresses is refused before any request.
        """
        api = mocker.patch("cyhole.core.client.APIClient.api")
        with pytest.raises(HeliusAccountCountError):
            self.helius.client.post_get_account_info(addresses)
        api.assert_not_called()

    @pytest.mark.asyncio
    async def test_post_get_account_info_rejects_bad_address_count_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — asynchronous logic refuses more
        than 100 addresses before any request.
        """
        api = mocker.patch("cyhole.core.client.AsyncAPIClient.api")
        with pytest.raises(HeliusAccountCountError):
            async with self.helius.async_client as client:
                await client.post_get_account_info([TEST_ACCOUNT_ADDRESS] * 101)
        api.assert_not_called()

    def test_post_get_account_info_accepts_one_hundred_addresses(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — 100 addresses, the most one call reads,
        are sent in one request.
        """
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = self._multiple_accounts_mock())
        self.helius.client.post_get_account_info([TEST_ACCOUNT_ADDRESS] * 100)
        _, kwargs = api.call_args
        assert kwargs["json"]["method"] == "getMultipleAccounts"
        assert len(kwargs["json"]["params"][0]) == 100

    def test_post_get_account_info_rejects_other_collections(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getMultipleAccounts" — only a list keeps the answer in the
        request's order, so a set is refused before any request.
        """
        api = mocker.patch("cyhole.core.client.APIClient.api")
        with pytest.raises(TypeError):
            self.helius.client.post_get_account_info({TEST_POOL_ADDRESS, TEST_ACCOUNT_ADDRESS})  # type: ignore[call-overload]
        api.assert_not_called()

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

    # ─── getTransactions ──────────────────────────────────────────────────────

    def test_post_get_transactions_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactions" — synchronous logic.

        Mock Response File: postGetTransactions_default.json
        """
        mock_file_name = "postGetTransactions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_get_transactions([TEST_TRANSACTION_SIGNATURE])
        assert isinstance(response, PostGetTransactionsResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_get_transactions_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "getTransactions" — asynchronous logic.

        Mock Response File: postGetTransactions_default.json
        """
        mock_file_name = "postGetTransactions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostGetTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_get_transactions([TEST_TRANSACTION_SIGNATURE])
        assert isinstance(response, PostGetTransactionsResponse)
        assert len(response.root) > 0

    # ─── parsedEventsTransactions ─────────────────────────────────────────────

    def test_post_parsed_events_transactions_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactions" — synchronous logic.

        Mock Response File: postParsedEventsTransactions_default.json
        """
        mock_file_name = "postParsedEventsTransactions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostParsedEventsTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.helius.client.post_parsed_events_transactions(
            TEST_PARSED_EVENTS_SIGNATURES,
            commitment = HeliusCommitment.FINALIZED.value,
        )
        assert isinstance(response, PostParsedEventsTransactionsResponse)

        # one result per signature, in input order
        assert [result.signature for result in response.root] == TEST_PARSED_EVENTS_SIGNATURES
        transfer, swap, invalid = response.root

        # a plain transfer: parsed, with its SOL movement and a transfer summary
        assert transfer.parser_status == HeliusParserStatus.OK.value
        assert transfer.parser_error is None
        assert transfer.parsed is not None
        assert transfer.parsed.transaction_status == "OK"
        assert transfer.parsed.fee_payer is not None
        assert len(transfer.parsed.native_transfers) > 0
        assert transfer.parsed.native_transfers[0].amount > 0
        assert transfer.parsed.summary is not None
        assert transfer.parsed.summary.type == HeliusParsedEventsSummaryType.TRANSFER.value

        # a swap: structured data behind the summary, raw token amounts, and a flat
        # instruction list holding both top-level and inner instructions
        assert swap.parsed is not None
        assert swap.parsed.summary is not None
        assert swap.parsed.summary.type == HeliusParsedEventsSummaryType.SWAP.value
        assert swap.parsed.summary.parsed_data is not None
        assert {"protocol", "in_amount", "actual_out_amount", "input_mint", "output_mint"} <= set(swap.parsed.summary.parsed_data)
        assert len(swap.parsed.token_transfers) > 0
        assert all(isinstance(token_transfer.raw_token_amount, int) for token_transfer in swap.parsed.token_transfers)
        assert any(instruction.inner_instruction_index is None for instruction in swap.parsed.instructions)
        assert any(instruction.inner_instruction_index is not None for instruction in swap.parsed.instructions)
        assert any(instruction.instruction_name is not None for instruction in swap.parsed.instructions)
        assert any(instruction.decoded is not None and instruction.decoded.accounts for instruction in swap.parsed.instructions)

        # an item that cannot be parsed does not fail the request
        assert invalid.parser_status == HeliusParserStatus.ERROR.value
        assert invalid.parsed is None
        assert invalid.parser_error is not None
        assert invalid.parser_error.code != ""

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_parsed_events_transactions_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactions" — asynchronous logic.

        Mock Response File: postParsedEventsTransactions_default.json
        """
        mock_file_name = "postParsedEventsTransactions_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostParsedEventsTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.helius.async_client as client:
            response = await client.post_parsed_events_transactions(TEST_PARSED_EVENTS_SIGNATURES)
        assert isinstance(response, PostParsedEventsTransactionsResponse)
        assert [result.signature for result in response.root] == TEST_PARSED_EVENTS_SIGNATURES
        assert response.root[0].parsed is not None
        assert response.root[-1].parser_status == HeliusParserStatus.ERROR.value

    def test_post_parsed_events_transactions_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactions" — request sent to the API.

        Checks the URL, the API key and the JSON body, with and without the optional inputs.

        Mock Response File: postParsedEventsTransactions_default.json
        """
        mock_response = self.mocker.load_mock_response("postParsedEventsTransactions_default", PostParsedEventsTransactionsResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.helius.client.post_parsed_events_transactions(TEST_PARSED_EVENTS_SIGNATURES)
        args, kwargs = api.call_args
        assert args[0] == "POST"
        assert args[1] == "https://mainnet.helius-rpc.com/v1/parsed-events/transactions"
        assert set(kwargs["params"]) == {"api-key"}
        assert kwargs["json"] == {"transactions": TEST_PARSED_EVENTS_SIGNATURES}

        self.helius.client.post_parsed_events_transactions(
            TEST_PARSED_EVENTS_SIGNATURES,
            commitment = HeliusCommitment.FINALIZED.value,
            include_raw_transaction = True,
        )
        _, kwargs = api.call_args
        assert kwargs["json"] == {
            "transactions": TEST_PARSED_EVENTS_SIGNATURES,
            "commitment": "finalized",
            "includeRawTransaction": True,
        }

    # ─── parsedEventsTransactionHistory ───────────────────────────────────────

    def test_post_parsed_events_transaction_history_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactionHistory" — synchronous logic.

        Mock Response File: postParsedEventsTransactionHistory_default.json
        """
        mock_file_name = "postParsedEventsTransactionHistory_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostParsedEventsTransactionHistoryResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostParsedEventsTransactionHistoryBody(
            address = TEST_PARSED_EVENTS_ADDRESS,
            limit = 3,
            sort_order = HeliusSortOrder.ASC.value,
            commitment = HeliusCommitment.FINALIZED.value,
        )
        response = self.helius.client.post_parsed_events_transaction_history(body)
        assert isinstance(response, PostParsedEventsTransactionHistoryResponse)
        assert 0 < len(response.data) <= 3
        assert response.pagination_token is not None

        for result in response.data:
            assert result.parser_status == HeliusParserStatus.OK.value
            assert result.parsed is not None
            assert result.parsed.slot > 0
            assert result.parsed.block_time is not None

        # oldest first, as requested
        block_times = [result.parsed.block_time for result in response.data if result.parsed is not None]
        assert block_times == sorted(block_times)

        if config.mock_file_overwrite and not config.helius.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_parsed_events_transaction_history_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactionHistory" — asynchronous logic.

        Mock Response File: postParsedEventsTransactionHistory_default.json
        """
        mock_file_name = "postParsedEventsTransactionHistory_default"
        if config.mock_response or config.helius.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostParsedEventsTransactionHistoryResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostParsedEventsTransactionHistoryBody(address = TEST_PARSED_EVENTS_ADDRESS, limit = 3, sort_order = HeliusSortOrder.ASC.value)
        async with self.helius.async_client as client:
            response = await client.post_parsed_events_transaction_history(body)
        assert isinstance(response, PostParsedEventsTransactionHistoryResponse)
        assert len(response.data) > 0
        assert response.data[0].parsed is not None

    def test_post_parsed_events_transaction_history_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "parsedEventsTransactionHistory" — request sent to the API.

        Checks the URL, the API key and that the body is sent with the API's camelCase
        names, leaving out every field that was not set.

        Mock Response File: postParsedEventsTransactionHistory_default.json
        """
        mock_response = self.mocker.load_mock_response("postParsedEventsTransactionHistory_default", PostParsedEventsTransactionHistoryResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.helius.client.post_parsed_events_transaction_history(PostParsedEventsTransactionHistoryBody(address = TEST_PARSED_EVENTS_ADDRESS))
        args, kwargs = api.call_args
        assert args[0] == "POST"
        assert args[1] == "https://mainnet.helius-rpc.com/v1/parsed-events/transaction-history"
        assert set(kwargs["params"]) == {"api-key"}
        assert kwargs["json"] == {"address": TEST_PARSED_EVENTS_ADDRESS}

        body = PostParsedEventsTransactionHistoryBody(
            address = TEST_PARSED_EVENTS_ADDRESS,
            limit = 50,
            before_signature = TEST_PARSED_EVENTS_SWAP_SIGNATURE,
            after_signature = TEST_PARSED_EVENTS_TRANSFER_SIGNATURE,
            pagination_token = "402752376:841",
            sort_order = HeliusSortOrder.DESC.value,
            commitment = HeliusCommitment.CONFIRMED.value,
            include_raw_transaction = False,
            slot = PostParsedEventsRange(gte = 402752376),
            time = PostParsedEventsRange(gt = 1_700_000_000, lte = 1_800_000_000),
        )
        self.helius.client.post_parsed_events_transaction_history(body)
        _, kwargs = api.call_args
        assert kwargs["json"] == {
            "address": TEST_PARSED_EVENTS_ADDRESS,
            "limit": 50,
            "beforeSignature": TEST_PARSED_EVENTS_SWAP_SIGNATURE,
            "afterSignature": TEST_PARSED_EVENTS_TRANSFER_SIGNATURE,
            "paginationToken": "402752376:841",
            "sortOrder": "desc",
            "commitment": "confirmed",
            "includeRawTransaction": False,
            "slot": {"gte": 402752376},
            "time": {"gt": 1_700_000_000, "lte": 1_800_000_000},
        }

