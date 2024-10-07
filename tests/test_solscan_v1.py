import pytest
from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.core.token.solana import JUP, WSOL
from cyhole.core.exception import MissingAPIKeyError
from cyhole.solscan.v1 import Solscan
from cyhole.solscan.v1.param import SolscanExportType
from cyhole.solscan.v1.exception import SolscanException
from cyhole.solscan.v1.schema import (
    SolscanHTTPError,
    GetAccountTokensResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeAccountsResponse,
    GetAccountSplTransfersResponse,
    GetAccountSolTransfersResponse,
    GetAccountExportTransactionsResponse,
    GetAccountExportRewardsResponse,
    GetAccountDetailResponse,
    GetTokenHoldersResponse,
    GetTokenMetaResponse,
    GetTokenTransferResponse,
    GetTokenListResponse,
    GetMarketTokenDetailResponse,
    GetTransactionLastResponse,
    GetTransactionDetailResponse,
    GetBlockLastResponse,
    GetBlockDetailResponse,
    GetBlockTransactionsResponse
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

    def test_missing_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key.
        """
        with pytest.raises(MissingAPIKeyError):
            monkeypatch.delenv("SOLSCAN_API_V1_KEY", raising = False)
            Solscan()

    def test_get_error_response_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check an error response schema
             of an endpoint on V1 API in synchronous mode.

            Mock Response File: get_v1_error.json
        """
        # load mock response
        mock_file_name = "get_v1_error"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, SolscanHTTPError)
            mock_response.status_code = 400

            mocker.patch("requests.get", return_value = mock_response)

        # execute request
        with pytest.raises(SolscanException):
            self.solscan.client.get_block_detail(123456789123)

    @pytest.mark.asyncio
    async def test_get_error_response_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check an error response schema
            of an endpoint on V1 API in asynchronous mode.
            
            Mock Response File: get_v1_error.json
        """
        # load mock response
        mock_file_name = "get_v1_error"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, SolscanHTTPError)
            mock_response.status_code = 400

            mocker.patch("cyhole.core.client.AsyncAPIClient._to_requests_response", return_value = mock_response)

        # execute request
        with pytest.raises(SolscanException):
            async with self.solscan.async_client as client:
                await client.get_block_detail(123456789123)

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

    def test_get_account_export_rewards_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Export Rewards" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_export_rewards.json
        """

        # load mock response
        mock_file_name = "get_v1_account_export_rewards"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountExportRewardsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_export_rewards(
            account = SOLSCAN_DONATION_ADDRESS,
            dt_from = datetime(2024, 1, 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetAccountExportRewardsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_export_rewards_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Export Rewards" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_export_rewards.json
        """

        # load mock response
        mock_file_name = "get_v1_account_export_rewards"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountExportRewardsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_export_rewards(
                account = SOLSCAN_DONATION_ADDRESS,
                dt_from = datetime(2024, 1, 1),
                dt_to = datetime.now()
            )

        # actual test
        assert isinstance(response, GetAccountExportRewardsResponse)

    def test_get_account_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Detail" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_account_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountDetailResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_detail(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountDetailResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_detail_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Detail" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_account_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountDetailResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_detail(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountDetailResponse)

    def test_get_token_holders_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Holders" on V1 API for synchronous logic.

            Mock Response File: get_v1_token_holders.json
        """

        # load mock response
        mock_file_name = "get_v1_token_holders"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_holders(JUP.address, limit = 2)

        # actual test
        assert isinstance(response, GetTokenHoldersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holders_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Holders" on V1 API for asynchronous logic.

            Mock Response File: get_v1_token_holders.json
        """

        # load mock response
        mock_file_name = "get_v1_token_holders"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_holders(JUP.address, limit = 2)

        # actual test
        assert isinstance(response, GetTokenHoldersResponse)

    def test_get_token_meta_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Meta" on V1 API for synchronous logic.

            Mock Response File: get_v1_token_meta.json
        """

        # load mock response
        mock_file_name = "get_v1_token_meta"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMetaResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_meta(JUP.address)

        # actual test
        assert isinstance(response, GetTokenMetaResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_meta_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Meta" on V1 API for asynchronous logic.

            Mock Response File: get_v1_token_meta.json
        """

        # load mock response
        mock_file_name = "get_v1_token_meta"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMetaResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_meta(JUP.address)

        # actual test
        assert isinstance(response, GetTokenMetaResponse)

    def test_get_token_transfer_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Transfer" on V1 API for synchronous logic.

            Mock Response File: get_v1_token_transfer.json
        """

        # load mock response
        mock_file_name = "get_v1_token_transfer"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTransferResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_transfer(token = WSOL.address, account = SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetTokenTransferResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_transfer_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Transfer" on V1 API for asynchronous logic.

            Mock Response File: get_v1_token_transfer.json
        """

        # load mock response
        mock_file_name = "get_v1_token_transfer"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTransferResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_transfer(token = WSOL.address, account = SOLSCAN_DONATION_ADDRESS, limit = 2)

        # actual test
        assert isinstance(response, GetTokenTransferResponse)

    def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token List" on V1 API for synchronous logic.

            Mock Response File: get_v1_token_list.json
        """

        # load mock response
        mock_file_name = "get_v1_token_list"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_list(limit = 2)

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token List" on V1 API for asynchronous logic.

            Mock Response File: get_v1_token_list.json
        """

        # load mock response
        mock_file_name = "get_v1_token_list"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_list(limit = 2)

        # actual test
        assert isinstance(response, GetTokenListResponse)

    def test_get_market_token_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Market Token Detail" on V1 API for synchronous logic.

            Mock Response File: get_v1_market_token_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_market_token_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMarketTokenDetailResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_market_token_detail(JUP.address, limit = 2)

        # actual test
        assert isinstance(response, GetMarketTokenDetailResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_market_token_detail_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Market Token Detail" on V1 API for asynchronous logic.

            Mock Response File: get_v1_market_token_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_market_token_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMarketTokenDetailResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_market_token_detail(JUP.address, limit = 2)

        # actual test
        assert isinstance(response, GetMarketTokenDetailResponse)

    def test_get_transaction_last_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Last" on V1 API for synchronous logic.

            Mock Response File: get_v1_transaction_last.json
        """

        # load mock response
        mock_file_name = "get_v1_transaction_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionLastResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_transaction_last(limit = 2)

        # actual test
        assert isinstance(response, GetTransactionLastResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transaction_last_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Last" on V1 API for asynchronous logic.

            Mock Response File: get_v1_transaction_last.json
        """

        # load mock response
        mock_file_name = "get_v1_transaction_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionLastResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_transaction_last(limit = 2)

        # actual test
        assert isinstance(response, GetTransactionLastResponse)

    def test_get_transaction_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Detail" on V1 API for synchronous logic.

            Mock Response Files:
                - get_v1_transaction_detail_vote.json
                - get_v1_transaction_detail_general.json
                - get_v1_transaction_detail_spl_token_1.json
                - get_v1_transaction_detail_spl_token_2.json
                - get_v1_transaction_detail_fail_1.json
                - get_v1_transaction_detail_fail_2.json
        """

        file_transaction = {
            "vote": "4TQYuua7nVABnCEj6re7QBb5PTKZDZzKhwi4yEntLYiacoT38HKdAbay5iB54dHbMc9JQ9vJgE1bzjkk1qZGpyuU",
            "general": "5hDQ5qXcrURie1fPicPSrGFUEFZaRZaa4Hda9oouWj6Vk9skMJ8bXeSXAU2qDJWC5K5Ehh8mzUrnbFKNc8VhhWGM",
            "spl_token_1": "59UUQj6iYTxbh2yeVfEuJjtSSfsbx8Z6NWB1dYNV7XCmQMMb1EPDftF7RoiJCCZcomUSioFGExpwxaZafYr5B6mi",
            "spl_token_2": "5v7Ykci6MTGkJMm4T2B3rP1WbW92Q8oxTC1DEchTpKX9ofeQs2CEyBweTVDrFxTJVGBWoJFnyAomWonY7cfMEG63",
            "fail_1": "5q1d8YkQsBVVjhrckydFuAr9QbVYDuRedmQ4brGpBhaFwvwwHYKQB7eX8VczPEGpEsWnWw7idSuVoKsq4putfLeW",
            "fail_2": "66uVLbp2XTtL4va1mFt9ea3Daix9rkVBnZYxsUD7TnqbKYT66jeNossEnch5cPzXrdJGQKpWHMEt9NX9srEwyFM4"
        }

        for type, id in file_transaction.items():
            # load mock response
            mock_file_name = f"get_v1_transaction_detail_{type}"
            if config.mock_response or config.solscan.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionDetailResponse)
                mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

            # execute request
            response = self.solscan.client.get_transaction_detail(id)

            # actual test
            assert isinstance(response, GetTransactionDetailResponse)

            # store request (only not mock)
            if config.mock_file_overwrite and not config.solscan.mock_response:
                self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transaction_detail_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Detail" on V1 API for asynchronous logic.

            Mock Response Files:
                - get_v1_transaction_detail_vote.json
                - get_v1_transaction_detail_general.json
                - get_v1_transaction_detail_spl_token_1.json
                - get_v1_transaction_detail_spl_token_2.json
                - get_v1_transaction_detail_fail_1.json
                - get_v1_transaction_detail_fail_2.json
        """

        file_transaction = {
            "vote": "4TQYuua7nVABnCEj6re7QBb5PTKZDZzKhwi4yEntLYiacoT38HKdAbay5iB54dHbMc9JQ9vJgE1bzjkk1qZGpyuU",
            "general": "5hDQ5qXcrURie1fPicPSrGFUEFZaRZaa4Hda9oouWj6Vk9skMJ8bXeSXAU2qDJWC5K5Ehh8mzUrnbFKNc8VhhWGM",
            "spl_token_1": "59UUQj6iYTxbh2yeVfEuJjtSSfsbx8Z6NWB1dYNV7XCmQMMb1EPDftF7RoiJCCZcomUSioFGExpwxaZafYr5B6mi",
            "spl_token_2": "5v7Ykci6MTGkJMm4T2B3rP1WbW92Q8oxTC1DEchTpKX9ofeQs2CEyBweTVDrFxTJVGBWoJFnyAomWonY7cfMEG63",
            "fail_1": "5q1d8YkQsBVVjhrckydFuAr9QbVYDuRedmQ4brGpBhaFwvwwHYKQB7eX8VczPEGpEsWnWw7idSuVoKsq4putfLeW",
            "fail_2": "66uVLbp2XTtL4va1mFt9ea3Daix9rkVBnZYxsUD7TnqbKYT66jeNossEnch5cPzXrdJGQKpWHMEt9NX9srEwyFM4"
        }

        for type, id in file_transaction.items():
            # load mock response
            mock_file_name = f"get_v1_transaction_detail_{type}"
            if config.mock_response or config.solscan.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionDetailResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
            # execute request
            async with self.solscan.async_client as client:
                response = await client.get_transaction_detail(id)

            # actual test
            assert isinstance(response, GetTransactionDetailResponse)

    def test_get_block_last_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Last" on V1 API for synchronous logic.

            Mock Response File: get_v1_block_last.json
        """

        # load mock response
        mock_file_name = "get_v1_block_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockLastResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_last(limit = 2)

        # actual test
        assert isinstance(response, GetBlockLastResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_last_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Last" on V1 API for asynchronous logic.

            Mock Response File: get_v1_block_last.json
        """

        # load mock response
        mock_file_name = "get_v1_block_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockLastResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["data"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_last(limit = 2)

        # actual test
        assert isinstance(response, GetBlockLastResponse)

    def test_get_block_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Detail" on V1 API for synchronous logic.

            Mock Response File: get_v1_block_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_block_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockDetailResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_detail(288107093)

        # actual test
        assert isinstance(response, GetBlockDetailResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_detail_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Detail" on V1 API for asynchronous logic.

            Mock Response File: get_v1_block_detail.json
        """

        # load mock response
        mock_file_name = "get_v1_block_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockDetailResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_detail(288107093)

        # actual test
        assert isinstance(response, GetBlockDetailResponse)

    def test_get_block_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Transactions" on V1 API for synchronous logic.

            Mock Response File: get_v1_block_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_block_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["transactions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_transactions(288107093, limit = 2)

        # actual test
        assert isinstance(response, GetBlockTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Transactions" on V1 API for asynchronous logic.

            Mock Response File: get_v1_block_transactions.json
        """

        # load mock response
        mock_file_name = "get_v1_block_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockTransactionsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["transactions"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_transactions(288107093, limit = 2)

        # actual test
        assert isinstance(response, GetBlockTransactionsResponse)