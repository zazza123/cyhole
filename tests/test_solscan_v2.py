import pytest
from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.solscan.v2 import Solscan
from cyhole.solscan.v2.param import (
    SolscanActivityTransferType,
    SolscanActivityDefiType,
    SolscanAccountType,
    SolscanFlowType
)
from cyhole.solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse,
    GetAccountTokenNFTAccountResponse,
    GetAccountDefiActivitiesParam,
    GetAccountDefiActivitiesResponse,
    GetAccountBalanceChangeActivitiesParam,
    GetAccountBalanceChangeActivitiesResponse,
    GetAccountTransactionsResponse
)

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.solscan.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

SOLSCAN_DONATION_ADDRESS = "D27DgiipBR5dRdij2L6NQ27xwyiLK5Q2DsEM5ML5EuLK"

class TestSolscanV2:
    """
        Class grouping all unit tests.
    """
    solscan = Solscan(api_key = config.solscan.api_v2_key)
    mocker = MockerManager(mock_path)

    def test_get_account_transfers_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transfers" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_transfers.json
        """
        # load mock response
        mock_file_name = "get_v2_account_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransferResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetAccountTransferParam(
            activity_type = SolscanActivityTransferType.SPL_TRANSFER.value,
            flow_direction = SolscanFlowType.INCOMING.value,
            time_range = (datetime(2024, 8, 1), datetime(2024, 8, 31)),
            amount_range = (1, 100_000_000)
        )
        response = self.solscan.client.get_account_transfers(SOLSCAN_DONATION_ADDRESS, param)

        # actual test
        assert isinstance(response, GetAccountTransferResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transfers_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transfers" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_transfers.json
        """
        # load mock response
        mock_file_name = "get_v2_account_transfers"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransferResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_transfers(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountTransferResponse)

    def test_get_account_token_nft_account_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Token/NFT Account" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_token_nft_account.json
        """
        # load mock response
        mock_file_name = "get_v2_account_token_nft_account"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTokenNFTAccountResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_token_nft_account(SOLSCAN_DONATION_ADDRESS, SolscanAccountType.TOKEN.value)

        # actual test
        assert isinstance(response, GetAccountTokenNFTAccountResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_token_nft_account_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Token/NFT Account" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_token_nft_account.json
        """
        # load mock response
        mock_file_name = "get_v2_account_token_nft_account"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTokenNFTAccountResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_token_nft_account(SOLSCAN_DONATION_ADDRESS, SolscanAccountType.TOKEN.value)

        # actual test
        assert isinstance(response, GetAccountTokenNFTAccountResponse)

    def test_get_account_defi_activities_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account DeFi Activities" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_defi_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_account_defi_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountDefiActivitiesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetAccountDefiActivitiesParam(
            activity_type = [
                SolscanActivityDefiType.SPL_TOKEN_UNSTAKE.value,
                SolscanActivityDefiType.AGG_TOKEN_SWAP.value
            ],
            time_range = (datetime(2024, 6, 1), datetime(2024, 8, 31))
        )
        response = self.solscan.client.get_account_defi_activities(SOLSCAN_DONATION_ADDRESS, param)

        # actual test
        assert isinstance(response, GetAccountDefiActivitiesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_defi_activities_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account DeFi Activities" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_defi_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_account_defi_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountDefiActivitiesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_defi_activities(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountDefiActivitiesResponse)

    def test_get_account_balance_change_activities_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Balance Change Activities" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_balance_change_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_account_balance_change_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountBalanceChangeActivitiesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetAccountBalanceChangeActivitiesParam(
            time_range = (datetime(2024, 8, 20), datetime(2024, 8, 31)),
            flow_direction = SolscanFlowType.INCOMING.value,
            amount_range = (1, 1_000_000_000),
            remove_spam = True
        )
        response = self.solscan.client.get_account_balance_change_activities(SOLSCAN_DONATION_ADDRESS, param)

        # actual test
        assert isinstance(response, GetAccountBalanceChangeActivitiesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_balance_change_activities_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Balance Change Activities" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_balance_change_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_account_balance_change_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountBalanceChangeActivitiesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_balance_change_activities(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountBalanceChangeActivitiesResponse)

    def test_get_account_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transactions" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_transactions.json
        """
        # load mock response
        mock_file_name = "get_v2_account_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_transactions(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Transactions" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_transactions.json
        """
        # load mock response
        mock_file_name = "get_v2_account_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_transactions(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountTransactionsResponse)