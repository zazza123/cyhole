import pytest
from pathlib import Path
from datetime import datetime

from pytest_mock import MockerFixture

from cyhole.solana_fm import SolanaFM
from cyhole.solana_fm.schema import (
    GetAccountTransactionsResponse,
    GetAccountTransfersParam,
    GetAccountTransfersResponse,
    GetAccountTransfersCsvExportParam
)
from cyhole.core.address.solana import JUP

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

    def test_get_account_transfers_csv_export_sync(self) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers CSV Export" for synchronous logic.
        """
        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersCsvExportParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        response = self.solana_fm.client.get_account_transfers_csv_export(account, params)

        # actual test
        assert isinstance(response, str)

    @pytest.mark.asyncio
    async def test_get_account_transfers_csv_export_async(self) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            "Get Account Transfers CSV Export" for asynchronous logic.
        """
        # execute request
        account = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
        params = GetAccountTransfersCsvExportParam(
            utc_from_unix_time = int(datetime.now().timestamp()) - 5, # 5 seconds ago
            utc_to_unix_time = int(datetime.now().timestamp())
        )
        async with self.solana_fm.async_client as client:
            response = await client.get_account_transfers_csv_export(account, params)

        # actual test
        assert isinstance(response, str)