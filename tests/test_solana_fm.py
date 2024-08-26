import pytest
from pathlib import Path
from datetime import datetime

from pytest_mock import MockerFixture

from cyhole.solana_fm import SolanaFM
from cyhole.solana_fm.schema import (
    GetAccountTransactionsResponse,
    GetAccountTransfersParam,
    GetAccountTransfersResponse,
    GetAccountTransfersCsvExportParam,
    GetAccountTransfersCsvExportResponse,
    GetAccountTransactionsFeesResponse,
    GetBlocksResponse,
    GetBlockResponse,
    PostMultipleBlocksResponse,
    GetSolanaDailyTransactionFeesResponse,
    GetTaggedTokensListResponse,
    GetTokenInfoV0Response,
    PostTokenMultipleInfoV0Response
)
from cyhole.core.address.solana import JUP, USDC, SOL

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.solana_fm.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestSolanaFM:
    """
        Class grouping all unit tests.
    """
    solana_fm = SolanaFM()
    mocker = MockerManager(mock_path)

    def test_get_account_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transactions" for synchronous logic.

            Mock Response File: get_account_transactions.json
        """

        # load mock response
        mock_file_name = "get_account_transactions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.solana_fm.client.get_account_transactions(JUP)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transactions" for asynchronous logic.

            Mock Response File: get_account_transactions.json
        """

        # load mock response
        mock_file_name = "get_account_transactions"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transactions(JUP)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)

    def test_get_account_transactions_fees_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transactions Fees" for synchronous logic.

            Mock Response File: get_account_transactions_fees.json
        """

        # load mock response
        mock_file_name = "get_account_transactions_fees"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsFeesResponse)

            # response content to be adjusted
            content = str(mock_response.json()["data"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_account_transactions_fees(JUP, dt_from = datetime(2024, 8, 15), dt_to = datetime(2024, 8, 20))

        # actual test
        assert isinstance(response, GetAccountTransactionsFeesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transactions_fees_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transactions Fees" for asynchronous logic.

            Mock Response File: get_account_transactions_fees.json
        """

        # load mock response
        mock_file_name = "get_account_transactions_fees"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsFeesResponse)

            # response content to be adjusted
            content = str(mock_response.json()["data"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transactions_fees(JUP, dt_from = datetime(2024, 8, 15), dt_to = datetime(2024, 8, 20))

        # actual test
        assert isinstance(response, GetAccountTransactionsFeesResponse)

    def test_get_account_transfers_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers" for synchronous logic.

            Mock Response File: get_account_transfers.json
        """

        # load mock response
        mock_file_name = "get_account_transfers"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransfersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        response = self.solana_fm.client.get_account_transfers(account, params)

        # actual test
        assert isinstance(response, GetAccountTransfersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transfers_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers" for asynchronous logic.

            Mock Response File: get_account_transfers.json
        """

        # load mock response
        mock_file_name = "get_account_transfers"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransfersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transfers(account, params)

        # actual test
        assert isinstance(response, GetAccountTransfersResponse)

    def test_get_account_transfers_csv_export_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers CSV Export" for synchronous logic.

            Mock Response File: get_account_transfers_csv_export.json
        """

        # load mock response
        mock_file_name = "get_account_transfers_csv_export"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransfersCsvExportResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersCsvExportParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        response = self.solana_fm.client.get_account_transfers_csv_export(account, params)

        # actual test
        assert isinstance(response, GetAccountTransfersCsvExportResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transfers_csv_export_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers CSV Export" for asynchronous logic.

            Mock Response File: get_account_transfers_csv_export.json
        """

        # load mock response
        mock_file_name = "get_account_transfers_csv_export"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransfersCsvExportResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersCsvExportParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transfers_csv_export(account, params)

        # actual test
        assert isinstance(response, GetAccountTransfersCsvExportResponse)

    def test_get_blocks_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Blocks" for synchronous logic.

            Mock Response File: get_blocks.json
        """

        # load mock response
        mock_file_name = "get_blocks"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlocksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_blocks(page_size = 1)

        # actual test
        assert isinstance(response, GetBlocksResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_blocks_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Blocks" for asynchronous logic.

            Mock Response File: get_blocks.json
        """

        # load mock response
        mock_file_name = "get_blocks"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlocksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_blocks(page_size = 1)

        # actual test
        assert isinstance(response, GetBlocksResponse)

    def test_get_block_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Block" for synchronous logic.

            Mock Response File: get_block.json
        """

        # load mock response
        mock_file_name = "get_block"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_block(19941305)

        # actual test
        assert isinstance(response, GetBlockResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Block" for asynchronous logic.

            Mock Response File: get_block.json
        """

        # load mock response
        mock_file_name = "get_block"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_block(19941305)

        # actual test
        assert isinstance(response, GetBlockResponse)

    def test_post_multiple_blocks_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Blocks" for synchronous logic.

            Mock Response File: post_multiple_blocks.json
        """

        # load mock response
        mock_file_name = "post_multiple_blocks"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleBlocksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.post_multiple_blocks([180000000])

        # actual test
        assert isinstance(response, PostMultipleBlocksResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_multiple_blocks_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Blocks" for asynchronous logic.

            Mock Response File: post_multiple_blocks.json
        """

        # load mock response
        mock_file_name = "post_multiple_blocks"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleBlocksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.post_multiple_blocks([180000000])

        # actual test
        assert isinstance(response, PostMultipleBlocksResponse)

    def test_post_multiple_blocks_no_producer_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Blocks" for synchronous logic by setting
            producer's details to false.

            Mock Response File: post_multiple_blocks_no_producer.json
        """

        # load mock response
        mock_file_name = "post_multiple_blocks_no_producer"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleBlocksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.post_multiple_blocks([200000000], producer_details = False)

        # actual test
        assert isinstance(response, PostMultipleBlocksResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_multiple_blocks_no_producer_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Blocks" for asynchronous logic by setting
            producer's details to false.

            Mock Response File: post_multiple_blocks_no_producer.json
        """

        # load mock response
        mock_file_name = "post_multiple_blocks_no_producer"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleBlocksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.post_multiple_blocks([200000000], producer_details = False)

        # actual test
        assert isinstance(response, PostMultipleBlocksResponse)

    def test_get_solana_daily_transaction_fees_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Solana Daily Transaction Fees" for synchronous logic.

            Mock Response File: get_solana_daily_transaction_fees.json
        """

        # load mock response
        mock_file_name = "get_solana_daily_transaction_fees"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSolanaDailyTransactionFeesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_solana_daily_transaction_fees()

        # actual test
        assert isinstance(response, GetSolanaDailyTransactionFeesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_solana_daily_transaction_fees_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Solana Daily Transaction Fees" for asynchronous logic.

            Mock Response File: get_solana_daily_transaction_fees.json
        """

        # load mock response
        mock_file_name = "get_solana_daily_transaction_fees"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSolanaDailyTransactionFeesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_solana_daily_transaction_fees()

        # actual test
        assert isinstance(response, GetSolanaDailyTransactionFeesResponse)

    def test_get_tagged_tokens_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Tagged Tokens List" for synchronous logic.

            Mock Response File: get_tagged_tokens_list.json
        """

        # load mock response
        mock_file_name = "get_tagged_tokens_list"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTaggedTokensListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_tagged_tokens_list()

        # actual test
        assert isinstance(response, GetTaggedTokensListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_tagged_tokens_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Tagged Tokens List" for asynchronous logic.

            Mock Response File: get_tagged_tokens_list.json
        """

        # load mock response
        mock_file_name = "get_tagged_tokens_list"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTaggedTokensListResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_tagged_tokens_list()

        # actual test
        assert isinstance(response, GetTaggedTokensListResponse)

    def test_get_token_info_v0_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Info V0" for synchronous logic.

            Mock Response File: get_token_info_v0.json
        """

        # load mock response
        mock_file_name = "get_token_info_v0"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoV0Response)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_token_info_v0(USDC)

        # actual test
        assert isinstance(response, GetTokenInfoV0Response)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_info_v0_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Info V0" for asynchronous logic.

            Mock Response File: get_token_info_v0.json
        """

        # load mock response
        mock_file_name = "get_token_info_v0"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoV0Response)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_token_info_v0(USDC)

        # actual test
        assert isinstance(response, GetTokenInfoV0Response)

    def test_post_token_multiple_info_v0_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Token Multiple Info V0" for synchronous logic.

            Mock Response File: post_token_multiple_info_v0.json
        """

        # load mock response
        mock_file_name = "post_token_multiple_info_v0"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenMultipleInfoV0Response)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.post_token_multiple_info_v0([USDC, SOL])

        # actual test
        assert isinstance(response, PostTokenMultipleInfoV0Response)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_token_multiple_info_v0_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Token Multiple Info V0" for asynchronous logic.

            Mock Response File: post_token_multiple_info_v0.json
        """

        # load mock response
        mock_file_name = "post_token_multiple_info_v0"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenMultipleInfoV0Response)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.post_token_multiple_info_v0([USDC, SOL])

        # actual test
        assert isinstance(response, PostTokenMultipleInfoV0Response)