import pytest
from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.solscan.v1 import Solscan
from cyhole.solscan.v1.param import SolscanExportType
from cyhole.solscan.v1.schema import (
    GetAccountTokensResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeAccountsResponse,
    GetAccountSplTransfersResponse,
    GetAccountSolTransfersResponse,
    GetAccountExportTransactionsResponse
)

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.solscan.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

SOLSCAN_DONATION_ADDRESS = "D27DgiipBR5dRdij2L6NQ27xwyiLK5Q2DsEM5ML5EuLK"

class TestSolscanV1:
    """
        Class grouping all unit tests.
    """
    solscan = Solscan(api_key = config.solscan.api_v1_key)
    mocker = MockerManager(mock_path)

    def test_get_account_tokens_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Tokens" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_tokens.json
        """

        # load mock response
        mock_file_name = "get_v1_account_tokens"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTokensResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_tokens(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountTokensResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_tokens_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Tokens" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_tokens.json
        """

        # load mock response
        mock_file_name = "get_v1_account_tokens"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTokensResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_tokens(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountTokensResponse)

    def test_get_account_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transactions" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_account_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["transactions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_transactions(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transactions" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_account_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["transactions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_transactions(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)

    def test_get_account_stake_accounts_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account StakeAccounts" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_stake_accounts.json
        """

        # load mock response
        mock_file_name = "get_v1_account_stake_accounts"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountStakeAccountsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["stake_accounts"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        account = "DyyJ9jNRM6US9DocYKeuwLrG73JkaPr2kHSijBBrKVcR"
        response = self.solscan.client.get_account_stake_accounts(account)

        # actual test
        assert isinstance(response, GetAccountStakeAccountsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_stake_accounts_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account StakeAccounts" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_stake_accounts.json
        """

        # load mock response
        mock_file_name = "get_v1_account_stake_accounts"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountStakeAccountsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["stake_accounts"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        account = "DyyJ9jNRM6US9DocYKeuwLrG73JkaPr2kHSijBBrKVcR"
        async with self.solscan.async_client as client:
            response = await client.get_account_stake_accounts(account)

        # actual test
        assert isinstance(response, GetAccountStakeAccountsResponse)

    def test_get_account_spl_transfers_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account SplTransfers" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_spl_transfers.json
        """

        # load mock response
        mock_file_name = "get_v1_account_spl_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountSplTransfersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_spl_transfers(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountSplTransfersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_spl_transfers_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account SplTransfers" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_spl_transfers.json
        """
        # load mock response
        mock_file_name = "get_v1_account_spl_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountSplTransfersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_spl_transfers(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountSplTransfersResponse)

    def test_get_account_sol_transfers_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account SolTransfers" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_sol_transfers.json
        """

        # load mock response
        mock_file_name = "get_v1_account_sol_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountSolTransfersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_sol_transfers(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountSolTransfersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_sol_transfers_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account SolTransfers" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_sol_transfers.json
        """

        # load mock response
        mock_file_name = "get_v1_account_sol_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountSolTransfersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_sol_transfers(SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetAccountSolTransfersResponse)

    def test_get_account_export_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Export Transactions" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_export_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_account_export_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountExportTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_export_transactions(
            account = SOLSCAN_DONATION_ADDRESS,
            export_type = SolscanExportType.SOL_TRANSFER.value,
            dt_from = datetime(2024, 8, 12),
            dt_to = datetime(2024, 8, 25)
        )

        # actual test
        assert isinstance(response, GetAccountExportTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_export_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Export Transactions" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_export_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_account_export_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountExportTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_export_transactions(
                account = SOLSCAN_DONATION_ADDRESS,
                export_type = SolscanExportType.SOL_TRANSFER.value,
                dt_from = datetime(2024, 8, 12),
                dt_to = datetime(2024, 8, 25)
            )

        # actual test
        assert isinstance(response, GetAccountExportTransactionsResponse)