import pytest
from pathlib import Path
from datetime import datetime

from pytest_mock import MockerFixture

from cyhole.solana_fm import SolanaFM
from cyhole.solana_fm.schema import (
    GetAccountTransactionsParam,
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
    PostTokenMultipleInfoV0Response,
    GetTokenInfoV1Response,
    PostTokenMultipleInfoV1Response,
    PostUserTokenAccountsResponse,
    GetMintTokenAccountsResponse,
    GetOnChainTokenDataResponse,
    GetTokenSupplyResponse,
    GetTransferTransactionsResponse,
    PostMultipleTransferTransactionsResponse,
    GetAllTransferActionsResponse
)
from cyhole.core.token.solana import JUP, USDC, WSOL

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

        # set params
        params = GetAccountTransactionsParam(
            inflow = True,
            outflow = False
        )
        raw_params = params.model_dump(by_alias = True, exclude_defaults = True)
        assert raw_params["inflow"] == "true"
        assert raw_params["outflow"] == "false"

        # execute request
        response = self.solana_fm.client.get_account_transactions(JUP.address, params = params)

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
            response = await client.get_account_transactions(JUP.address)

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
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_account_transactions_fees(JUP.address, dt_from = datetime(2024, 8, 15), dt_to = datetime(2024, 8, 20))

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
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transactions_fees(JUP.address, dt_from = datetime(2024, 8, 15), dt_to = datetime(2024, 8, 20))

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
        response = self.solana_fm.client.get_token_info_v0(USDC.address)

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
            response = await client.get_token_info_v0(USDC.address)

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
        response = self.solana_fm.client.post_token_multiple_info_v0([USDC.address, WSOL.address])

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
            response = await client.post_token_multiple_info_v0([USDC.address, WSOL.address])

        # actual test
        assert isinstance(response, PostTokenMultipleInfoV0Response)

    def test_get_token_info_v1_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Info V1" for synchronous logic.

            Mock Response File: get_token_info_v1.json
        """

        # load mock response
        mock_file_name = "get_token_info_v1"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoV1Response)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_token_info_v1(JUP.address)

        # actual test
        assert isinstance(response, GetTokenInfoV1Response)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_info_v1_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Info V1" for asynchronous logic.

            Mock Response File: get_token_info_v1.json
        """

        # load mock response
        mock_file_name = "get_token_info_v1"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoV1Response)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_token_info_v1(JUP.address)

        # actual test
        assert isinstance(response, GetTokenInfoV1Response)

    def test_post_token_multiple_info_v1_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Token Multiple Info V1" for synchronous logic.

            Mock Response File: post_token_multiple_info_v1.json
        """

        # load mock response
        mock_file_name = "post_token_multiple_info_v1"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenMultipleInfoV1Response)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.post_token_multiple_info_v1([JUP.address, USDC.address])

        # actual test
        assert isinstance(response, PostTokenMultipleInfoV1Response)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_token_multiple_info_v1_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Token Multiple Info V1" for asynchronous logic.

            Mock Response File: post_token_multiple_info_v1.json
        """

        # load mock response
        mock_file_name = "post_token_multiple_info_v1"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenMultipleInfoV1Response)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.post_token_multiple_info_v1([JUP.address, USDC.address])

        # actual test
        assert isinstance(response, PostTokenMultipleInfoV1Response)

    def test_post_user_token_accounts_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post User Token Accounts" for synchronous logic.

            Mock Response File: post_user_token_accounts.json
        """

        # load mock response
        mock_file_name = "post_user_token_accounts"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostUserTokenAccountsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.post_user_token_accounts(JUP.address)

        # actual test
        assert isinstance(response, PostUserTokenAccountsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_user_token_accounts_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post User Token Accounts" for asynchronous logic.

            Mock Response File: post_user_token_accounts.json
        """

        # load mock response
        mock_file_name = "post_user_token_accounts"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostUserTokenAccountsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.post_user_token_accounts(JUP.address)

        # actual test
        assert isinstance(response, PostUserTokenAccountsResponse)

    def test_get_mint_token_accounts_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Mint Token Accounts" for synchronous logic.

            Mock Response File: get_mint_token_accounts.json
        """

        # load mock response
        mock_file_name = "get_mint_token_accounts"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMintTokenAccountsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_mint_token_accounts(JUP.address, page_size = 2)

        # actual test
        assert isinstance(response, GetMintTokenAccountsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_mint_token_accounts_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Mint Token Accounts" for asynchronous logic.

            Mock Response File: get_mint_token_accounts.json
        """

        # load mock response
        mock_file_name = "get_mint_token_accounts"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMintTokenAccountsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_mint_token_accounts(JUP.address, page_size = 2)

        # actual test
        assert isinstance(response, GetMintTokenAccountsResponse)

    def test_get_on_chain_token_data_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get On Chain Token Data" for synchronous logic.

            Mock Response File: get_on_chain_token_data.json
        """

        # load mock response
        mock_file_name = "get_on_chain_token_data"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOnChainTokenDataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        CWIF = "7atgF8KQo4wJrD5ATGX7t1V2zVvykPJbFfNeVf1icFv1"
        response = self.solana_fm.client.get_on_chain_token_data(CWIF)

        # actual test
        assert isinstance(response, GetOnChainTokenDataResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_on_chain_token_data_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get On Chain Token Data" for asynchronous logic.

            Mock Response File: get_on_chain_token_data.json
        """

        # load mock response
        mock_file_name = "get_on_chain_token_data"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOnChainTokenDataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        CWIF = "7atgF8KQo4wJrD5ATGX7t1V2zVvykPJbFfNeVf1icFv1"
        async with self.solana_fm.async_client as client:
            response = await client.get_on_chain_token_data(CWIF)

        # actual test
        assert isinstance(response, GetOnChainTokenDataResponse)

    def test_get_token_supply_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Supply" for synchronous logic.

            Mock Response File: get_token_supply.json
        """

        # load mock response
        mock_file_name = "get_token_supply"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSupplyResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_token_supply(JUP.address)

        # actual test
        assert isinstance(response, GetTokenSupplyResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_supply_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Token Supply" for asynchronous logic.

            Mock Response File: get_token_supply.json
        """

        # load mock response
        mock_file_name = "get_token_supply"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSupplyResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_token_supply(JUP.address)

        # actual test
        assert isinstance(response, GetTokenSupplyResponse)

    def test_get_transfer_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Transfer Transactions" for synchronous logic.

            Mock Response File: get_transfer_transactions.json
        """

        # load mock response
        mock_file_name = "get_transfer_transactions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransferTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        transaction = "FUCoNwzCfPugjBwR4Q2uzDMZJdA3E5GAqDB1HGgfi3cTPyqBk11HniqQCGSCin3oBGQLFwcQ3fEHdsEJbgaZZ5p"
        response = self.solana_fm.client.get_transfer_transactions(transaction)

        # actual test
        assert isinstance(response, GetTransferTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transfer_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Transfer Transactions" for asynchronous logic.

            Mock Response File: get_transfer_transactions.json
        """

        # load mock response
        mock_file_name = "get_transfer_transactions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransferTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        transaction = "FUCoNwzCfPugjBwR4Q2uzDMZJdA3E5GAqDB1HGgfi3cTPyqBk11HniqQCGSCin3oBGQLFwcQ3fEHdsEJbgaZZ5p"
        async with self.solana_fm.async_client as client:
            response = await client.get_transfer_transactions(transaction)

        # actual test
        assert isinstance(response, GetTransferTransactionsResponse)

    def test_post_multiple_transfer_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Transfer Transactions" for synchronous logic.

            Mock Response File: post_multiple_transfer_transactions.json
        """

        # load mock response
        mock_file_name = "post_multiple_transfer_transactions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleTransferTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        transactions = [
            "4wGMriaRA55F1opEhJW2is34aDQdJHE13vJCbqP6WzrnzFwThnvZYvRZ2AKc2Meh5JToETz3eCCeuavepz6iTPZx",
            "FUCoNwzCfPugjBwR4Q2uzDMZJdA3E5GAqDB1HGgfi3cTPyqBk11HniqQCGSCin3oBGQLFwcQ3fEHdsEJbgaZZ5p"
        ]
        response = self.solana_fm.client.post_multiple_transfer_transactions(transactions)

        # actual test
        assert isinstance(response, PostMultipleTransferTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_multiple_transfer_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Post Multiple Transfer Transactions" for asynchronous logic.

            Mock Response File: post_multiple_transfer_transactions.json
        """

        # load mock response
        mock_file_name = "post_multiple_transfer_transactions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostMultipleTransferTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        transactions = [
            "4wGMriaRA55F1opEhJW2is34aDQdJHE13vJCbqP6WzrnzFwThnvZYvRZ2AKc2Meh5JToETz3eCCeuavepz6iTPZx",
            "FUCoNwzCfPugjBwR4Q2uzDMZJdA3E5GAqDB1HGgfi3cTPyqBk11HniqQCGSCin3oBGQLFwcQ3fEHdsEJbgaZZ5p"
        ]
        async with self.solana_fm.async_client as client:
            response = await client.post_multiple_transfer_transactions(transactions)

        # actual test
        assert isinstance(response, PostMultipleTransferTransactionsResponse)

    def test_get_all_transfer_actions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get All Transfer Actions" for synchronous logic.

            Mock Response File: get_all_transfer_actions.json
        """

        # load mock response
        mock_file_name = "get_all_transfer_actions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAllTransferActionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["actions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solana_fm.client.get_all_transfer_actions()

        # actual test
        assert isinstance(response, GetAllTransferActionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solana_fm.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_all_transfer_actions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get All Transfer Actions" for asynchronous logic.

            Mock Response File: get_all_transfer_actions.json
        """

        # load mock response
        mock_file_name = "get_all_transfer_actions"
        if config.mock_response or config.solana_fm.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAllTransferActionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["actions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solana_fm.async_client as client:
            response = await client.get_all_transfer_actions()

        # actual test
        assert isinstance(response, GetAllTransferActionsResponse)