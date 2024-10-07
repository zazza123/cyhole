import pytest
from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.core.token.solana import JUP, WSOL
from cyhole.core.exception import MissingAPIKeyError
from cyhole.solscan.v2 import Solscan
from cyhole.solscan.v2.exception import (
    SolscanInvalidAmountRange,
    SolscanInvalidTimeRange,
    SolscanException
)
from cyhole.solscan.v2.param import (
    SolscanNFTCollectionPageSizeType,
    SolscanActivityTransferType,
    SolscanNFTDaysRangeType,
    SolscanActivityDefiType,
    SolscanActivityNFTType,
    SolscanPageSizeType,
    SolscanNFTSortType,
    SolscanAccountType,
    SolscanOrderType,
    SolscanFlowType
)
from cyhole.solscan.v2.schema import (
    SolscanHTTPError,
    GetAccountTransferParam,
    GetAccountTransferResponse,
    GetAccountTokenNFTAccountResponse,
    GetAccountDefiActivitiesParam,
    GetAccountDefiActivitiesResponse,
    GetAccountBalanceChangeActivitiesParam,
    GetAccountBalanceChangeActivitiesResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeResponse,
    GetAccountDetailResponse,
    GetAccountRewardsExportResponse,
    GetTokenTransferParam,
    GetTokenTransferResponse,
    GetTokenDefiActivitiesParam,
    GetTokenDefiActivitiesResponse,
    GetTokenMarketsResponse,
    GetTokenListResponse,
    GetTokenTrendingResponse,
    GetTokenPriceResponse,
    GetTokenHoldersResponse,
    GetTokenMetaResponse,
    GetNFTNewsResponse,
    GetNFTActivitiesParam,
    GetNFTActivitiesResponse,
    GetNFTCollectionListsParam,
    GetNFTCollectionListsResponse,
    GetNFTCollectionItemsResponse,
    GetTransactionLastResponse,
    GetTransactionActionsResponse,
    GetBlockLastResponse,
    GetBlockTransactionsResponse,
    GetBlockDetailResponse
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

    def test_missing_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key.
        """
        with pytest.raises(MissingAPIKeyError):
            monkeypatch.delenv("SOLSCAN_API_V2_KEY", raising = False)
            Solscan()

    def test_get_error_response_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check an error response schema
             of an endpoint on V2 API in synchronous mode.

            Mock Response File: get_v2_error.json
        """
        # load mock response
        mock_file_name = "get_v2_error"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, SolscanHTTPError)
            mock_response.status_code = 500

            mocker.patch("requests.get", return_value = mock_response)

        # execute request
        with pytest.raises(SolscanException):
            self.solscan.client.get_block_detail(123456789123)

    @pytest.mark.asyncio
    async def test_get_error_response_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check an error response schema
            of an endpoint on V2 API in asynchronous mode.
            
            Mock Response File: get_v2_error.json
        """
        # load mock response
        mock_file_name = "get_v2_error"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, SolscanHTTPError)
            mock_response.status_code = 500

            mocker.patch("cyhole.core.client.AsyncAPIClient._to_requests_response", return_value = mock_response)

        # execute request
        with pytest.raises(SolscanException):
            async with self.solscan.async_client as client:
                await client.get_block_detail(123456789123)

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
            amount_range = (1, 100_000_000),
            page_size = SolscanPageSizeType.SIZE_10.value
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

    def test_get_account_balance_change_activities_invalid_amount_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Account Balance Change Activities" on V2 API 
            when the amount range is invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidAmountRange):
            GetAccountBalanceChangeActivitiesParam(
                amount_range = (100_000_000, 1),
                page_size = SolscanPageSizeType.SIZE_10.value
            )

    def test_get_account_balance_change_activities_invalid_time_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Account Balance Change Activities" on V2 API 
            when the time range is invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidTimeRange):
            GetAccountBalanceChangeActivitiesParam(
                time_range = (datetime(2024, 8, 31), datetime(2024, 8, 1))
            )

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

    def test_get_account_stake_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Stake" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_stake.json
        """
        # load mock response
        mock_file_name = "get_v2_account_stake"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountStakeResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        account = "DyyJ9jNRM6US9DocYKeuwLrG73JkaPr2kHSijBBrKVcR"
        response = self.solscan.client.get_account_stake(account)

        # actual test
        assert isinstance(response, GetAccountStakeResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_stake_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Stake" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_stake.json
        """
        # load mock response
        mock_file_name = "get_v2_account_stake"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountStakeResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            account = "DyyJ9jNRM6US9DocYKeuwLrG73JkaPr2kHSijBBrKVcR"
            response = await client.get_account_stake(account)

        # actual test
        assert isinstance(response, GetAccountStakeResponse)

    def test_get_account_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Detail" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_detail.json
        """
        # load mock response
        mock_file_name = "get_v2_account_detail"
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
            GET "Account Detail" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_detail.json
        """
        # load mock response
        mock_file_name = "get_v2_account_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountDetailResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_detail(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetAccountDetailResponse)

    def test_get_account_rewards_export_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Rewards Export" on V2 API for synchronous logic.

            Mock Response File: get_v2_account_rewards_export.json
        """
        # load mock response
        mock_file_name = "get_v2_account_rewards_export"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountRewardsExportResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_account_rewards_export(
            account = SOLSCAN_DONATION_ADDRESS,
            dt_from = datetime(2024, 1, 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetAccountRewardsExportResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_account_rewards_export_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Rewards Export" on V2 API for asynchronous logic.

            Mock Response File: get_v2_account_rewards_export.json
        """
        # load mock response
        mock_file_name = "get_v2_account_rewards_export"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAccountRewardsExportResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["csv"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_account_rewards_export(
                account = SOLSCAN_DONATION_ADDRESS,
                dt_from = datetime(2024, 1, 1),
                dt_to = datetime.now()
            )

        # actual test
        assert isinstance(response, GetAccountRewardsExportResponse)

    def test_get_token_transfer_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Transfer" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_transfer.json
        """
        # load mock response
        mock_file_name = "get_v2_token_transfer"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTransferResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetTokenTransferParam(
            activity_type = SolscanActivityTransferType.SPL_TRANSFER.value,
            time_range = (datetime(2024, 8, 1), datetime(2024, 8, 31)),
            amount_range = (1, 100_000_000),
            exclude_amount_zero = True
        )
        response = self.solscan.client.get_token_transfer(JUP.address, param)

        # actual test
        assert isinstance(response, GetTokenTransferResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_transfer_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Transfer" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_transfer.json
        """
        # load mock response
        mock_file_name = "get_v2_token_transfer"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTransferResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        param = GetTokenTransferParam(
            activity_type = SolscanActivityTransferType.SPL_TRANSFER.value,
            time_range = (datetime(2024, 8, 1), datetime(2024, 8, 31)),
            amount_range = (1, 100_000_000),
            exclude_amount_zero = True
        )
        async with self.solscan.async_client as client:
            response = await client.get_token_transfer(JUP.address, param)

        # actual test
        assert isinstance(response, GetTokenTransferResponse)

    def test_get_token_transfer_invalid_time_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Token Transfer" on V2 API when the time range is 
            invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidTimeRange):
            GetTokenTransferParam(
                activity_type = [SolscanActivityTransferType.SPL_TRANSFER.value],
                time_range = (datetime(2024, 8, 31), datetime(2024, 8, 1))
            )

    def test_get_token_transfer_invalid_amount_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Token Transfer" on V2 API when the amount range is 
            invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidAmountRange):
            GetTokenTransferParam(
                amount_range = (100_000_000, 1)
            )

    def test_get_token_defi_activities_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token DeFi Activities" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_defi_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_token_defi_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDefiActivitiesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetTokenDefiActivitiesParam(
            activity_type = [
                SolscanActivityDefiType.SPL_TOKEN_UNSTAKE.value,
                SolscanActivityDefiType.AGG_TOKEN_SWAP.value
            ],
            time_range = (datetime(2024, 6, 1), datetime(2024, 8, 31))
        )
        response = self.solscan.client.get_token_defi_activities(JUP.address, param)

        # actual test
        assert isinstance(response, GetTokenDefiActivitiesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_defi_activities_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token DeFi Activities" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_defi_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_token_defi_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDefiActivitiesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_defi_activities(JUP.address)

        # actual test
        assert isinstance(response, GetTokenDefiActivitiesResponse)

    def test_get_token_defi_activities_invalid_time_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Token Defi Activities" on V2 API when the time range is 
            invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidTimeRange):
            GetTokenDefiActivitiesParam(
                activity_type = SolscanActivityDefiType.SPL_TOKEN_UNSTAKE.value,
                time_range = (datetime(2024, 8, 31), datetime(2024, 8, 1)),
                page_size = SolscanPageSizeType.SIZE_10.value
            )

    def test_get_token_markets_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Markets" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_markets.json
        """
        # load mock response
        mock_file_name = "get_v2_token_markets"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMarketsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_markets([JUP.address, WSOL.address])

        # actual test
        assert isinstance(response, GetTokenMarketsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_markets_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Markets" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_markets.json
        """
        # load mock response
        mock_file_name = "get_v2_token_markets"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMarketsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_markets([JUP.address, WSOL.address])

        # actual test
        assert isinstance(response, GetTokenMarketsResponse)

    def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token List" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_list.json
        """
        # load mock response
        mock_file_name = "get_v2_token_list"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_list()

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token List" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_list.json
        """
        # load mock response
        mock_file_name = "get_v2_token_list"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_list()

        # actual test
        assert isinstance(response, GetTokenListResponse)

    def test_get_token_trending_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Trending" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_trending.json
        """
        # load mock response
        mock_file_name = "get_v2_token_trending"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTrendingResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_trending(limit = 2)

        # actual test
        assert isinstance(response, GetTokenTrendingResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_trending_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Trending" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_trending.json
        """
        # load mock response
        mock_file_name = "get_v2_token_trending"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTrendingResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_trending()

        # actual test
        assert isinstance(response, GetTokenTrendingResponse)

    def test_get_token_price_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Price" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_price.json
        """
        # load mock response
        mock_file_name = "get_v2_token_price"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_price(
            token = JUP.address,
            time_range = (datetime(2024, 8, 1), datetime(2024, 8, 10))
        )

        # actual test
        assert isinstance(response, GetTokenPriceResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_price_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Price" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_price.json
        """
        # load mock response
        mock_file_name = "get_v2_token_price"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_price(JUP.address)

        # actual test
        assert isinstance(response, GetTokenPriceResponse)

    def test_get_token_price_invalid_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Token Price" on V2 API when the time range is 
            invalid for synchronous logic.
        """
        # execute request
        with pytest.raises(SolscanInvalidTimeRange):
            self.solscan.client.get_token_price(
                token = JUP.address,
                time_range = (datetime(2024, 8, 10), datetime(2024, 8, 1))
            )

    def test_get_token_holders_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Holders" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_holders.json
        """
        # load mock response
        mock_file_name = "get_v2_token_holders"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_token_holders(JUP.address, amount_range = (1, 1_000_000_000))

        # actual test
        assert isinstance(response, GetTokenHoldersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holders_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Holders" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_holders.json
        """
        # load mock response
        mock_file_name = "get_v2_token_holders"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_holders(JUP.address)

        # actual test
        assert isinstance(response, GetTokenHoldersResponse)

    def test_get_token_holders_invalid_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "Token Holders" on V2 API when the amount range 
            is invalid for synchronous logic.
        """
        # execute request
        with pytest.raises(SolscanInvalidAmountRange):
            self.solscan.client.get_token_holders(
                token = JUP.address,
                amount_range = (1_000_000, 1)
            )

    def test_get_token_meta_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Token Meta" on V2 API for synchronous logic.

            Mock Response File: get_v2_token_meta.json
        """
        # load mock response
        mock_file_name = "get_v2_token_meta"
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
            GET "Token Meta" on V2 API for asynchronous logic.

            Mock Response File: get_v2_token_meta.json
        """
        # load mock response
        mock_file_name = "get_v2_token_meta"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMetaResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_token_meta(JUP.address)

        # actual test
        assert isinstance(response, GetTokenMetaResponse)

    def test_get_nft_news_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT News" on V2 API for synchronous logic.

            Mock Response File: get_v2_nft_news.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_news"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTNewsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_nft_news()

        # actual test
        assert isinstance(response, GetNFTNewsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_nft_news_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT News" on V2 API for asynchronous logic.

            Mock Response File: get_v2_nft_news.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_news"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTNewsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_nft_news()

        # actual test
        assert isinstance(response, GetNFTNewsResponse)

    def test_get_nft_activities_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Activities" on V2 API for synchronous logic.

            Mock Response File: get_v2_nft_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTActivitiesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetNFTActivitiesParam(
            activity_type = SolscanActivityNFTType.SOLD.value,
            time_range = (datetime(2023, 12, 31), datetime(2024, 6, 30)),
            currency_token_address = WSOL.address,
            amount_range = (1, 1_000_000_000)
        )
        response = self.solscan.client.get_nft_activities(param)

        # actual test
        assert isinstance(response, GetNFTActivitiesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_nft_activities_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Activities" on V2 API for asynchronous logic.

            Mock Response File: get_v2_nft_activities.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_activities"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTActivitiesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_nft_activities()

        # actual test
        assert isinstance(response, GetNFTActivitiesResponse)

    def test_get_nft_activities_invalid_amount_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "NFT Activities" on V2 API when the amount range is invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidAmountRange):
            GetNFTActivitiesParam(
                amount_range = (100_000_000, 1),
                page_size = SolscanPageSizeType.SIZE_20.value
            )

    def test_get_nft_activities_invalid_time_range(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response from endpoint 
            GET "NFT Activities" on V2 API when the time range is invalid.
        """
        # execute request
        with pytest.raises(SolscanInvalidTimeRange):
            GetNFTActivitiesParam(
                activity_type = [SolscanActivityNFTType.SOLD.value],
                time_range = (datetime(2024, 8, 31), datetime(2024, 8, 1))
            )

    def test_get_nft_collectin_lists_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Collection Lists" on V2 API for synchronous logic.

            Mock Response File: get_v2_nft_collection_lists.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_collection_lists"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTCollectionListsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        param = GetNFTCollectionListsParam(
            days_range = SolscanNFTDaysRangeType.DAYS_7.value,
            sort_by = SolscanNFTSortType.VOLUMES.value,
            order_by = SolscanOrderType.DESCENDING.value,
            page_size = SolscanNFTCollectionPageSizeType.SIZE_10.value
        )
        response = self.solscan.client.get_nft_collection_lists(param)

        # actual test
        assert isinstance(response, GetNFTCollectionListsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_nft_collectin_lists_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Collection Lists" on V2 API for asynchronous logic.

            Mock Response File: get_v2_nft_collection_lists.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_collection_lists"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTCollectionListsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_nft_collection_lists()

        # actual test
        assert isinstance(response, GetNFTCollectionListsResponse)

    def test_get_nft_collection_items_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Collection Items" on V2 API for synchronous logic.

            Mock Response File: get_v2_nft_collection_items.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_collection_items"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTCollectionItemsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        collection = "fc8dd31116b25e6690d83f6fb102e67ac6a9364dc2b96285d636aed462c4a983"
        response = self.solscan.client.get_nft_collection_items(collection)

        # actual test
        assert isinstance(response, GetNFTCollectionItemsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_nft_collection_items_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "NFT Collection Items" on V2 API for asynchronous logic.

            Mock Response File: get_v2_nft_collection_items.json
        """
        # load mock response
        mock_file_name = "get_v2_nft_collection_items"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNFTCollectionItemsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            collection = "fc8dd31116b25e6690d83f6fb102e67ac6a9364dc2b96285d636aed462c4a983"
            response = await client.get_nft_collection_items(collection)

        # actual test
        assert isinstance(response, GetNFTCollectionItemsResponse)

    def test_get_transaction_last_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Last" on V2 API for synchronous logic.

            Mock Response File: get_v2_transaction_last.json
        """
        # load mock response
        mock_file_name = "get_v2_transaction_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionLastResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_transaction_last()

        # actual test
        assert isinstance(response, GetTransactionLastResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transaction_last_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Last" on V2 API for asynchronous logic.

            Mock Response File: get_v2_transaction_last.json
        """
        # load mock response
        mock_file_name = "get_v2_transaction_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionLastResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_transaction_last()

        # actual test
        assert isinstance(response, GetTransactionLastResponse)

    def test_get_transaction_actions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Actions" on V2 API for synchronous logic.

            Mock Response Files:
                - get_v2_transaction_actions_general.json
                - get_v2_transaction_actions_spl_token_1.json
                - get_v2_transaction_actions_spl_token_2.json
        """

        file_transaction = {
            "general": "5hDQ5qXcrURie1fPicPSrGFUEFZaRZaa4Hda9oouWj6Vk9skMJ8bXeSXAU2qDJWC5K5Ehh8mzUrnbFKNc8VhhWGM",
            "spl_token_1": "59UUQj6iYTxbh2yeVfEuJjtSSfsbx8Z6NWB1dYNV7XCmQMMb1EPDftF7RoiJCCZcomUSioFGExpwxaZafYr5B6mi",
            "spl_token_2": "5v7Ykci6MTGkJMm4T2B3rP1WbW92Q8oxTC1DEchTpKX9ofeQs2CEyBweTVDrFxTJVGBWoJFnyAomWonY7cfMEG63"
        }

        for type, id in file_transaction.items():
            # load mock response
            mock_file_name = f"get_v2_transaction_actions_{type}"
            if config.mock_response or config.solscan.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionActionsResponse)
                mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

            # execute request
            response = self.solscan.client.get_transaction_actions(id)

            # actual test
            assert isinstance(response, GetTransactionActionsResponse)

            # store request (only not mock)
            if config.mock_file_overwrite and not config.solscan.mock_response:
                self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_transaction_actions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Transaction Actions" on V2 API for asynchronous logic.

            Mock Response Files:
                - get_v2_transaction_actions_general.json
                - get_v2_transaction_actions_spl_token_1.json
                - get_v2_transaction_actions_spl_token_2.json
        """

        file_transaction = {
            "general": "5hDQ5qXcrURie1fPicPSrGFUEFZaRZaa4Hda9oouWj6Vk9skMJ8bXeSXAU2qDJWC5K5Ehh8mzUrnbFKNc8VhhWGM",
            "spl_token_1": "59UUQj6iYTxbh2yeVfEuJjtSSfsbx8Z6NWB1dYNV7XCmQMMb1EPDftF7RoiJCCZcomUSioFGExpwxaZafYr5B6mi",
            "spl_token_2": "5v7Ykci6MTGkJMm4T2B3rP1WbW92Q8oxTC1DEchTpKX9ofeQs2CEyBweTVDrFxTJVGBWoJFnyAomWonY7cfMEG63"
        }

        for type, id in file_transaction.items():
            # load mock response
            mock_file_name = f"get_v2_transaction_actions_{type}"
            if config.mock_response or config.solscan.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, GetTransactionActionsResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
            # execute request
            async with self.solscan.async_client as client:
                response = await client.get_transaction_actions(id)

            # actual test
            assert isinstance(response, GetTransactionActionsResponse)

    def test_get_block_last_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Last" on V2 API for synchronous logic.

            Mock Response File: get_v2_block_last.json
        """
        # load mock response
        mock_file_name = "get_v2_block_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockLastResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_last()

        # actual test
        assert isinstance(response, GetBlockLastResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_last_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Last" on V2 API for asynchronous logic.

            Mock Response File: get_v2_block_last.json
        """
        # load mock response
        mock_file_name = "get_v2_block_last"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockLastResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_last()

        # actual test
        assert isinstance(response, GetBlockLastResponse)

    def test_get_block_transactions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Transactions" on V2 API for synchronous logic.

            Mock Response File: get_v2_block_transactions.json
        """
        # load mock response
        mock_file_name = "get_v2_block_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockTransactionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_transactions(267385261)

        # actual test
        assert isinstance(response, GetBlockTransactionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_transactions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Transactions" on V2 API for asynchronous logic.

            Mock Response File: get_v2_block_transactions.json
        """
        # load mock response
        mock_file_name = "get_v2_block_transactions"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockTransactionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_transactions(267385261)

        # actual test
        assert isinstance(response, GetBlockTransactionsResponse)

    def test_get_block_detail_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Detail" on V2 API for synchronous logic.

            Mock Response File: get_v2_block_detail.json
        """
        # load mock response
        mock_file_name = "get_v2_block_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockDetailResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.get_block_detail(267385261)

        # actual test
        assert isinstance(response, GetBlockDetailResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_block_detail_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Block Detail" on V2 API for asynchronous logic.

            Mock Response File: get_v2_block_detail.json
        """
        # load mock response
        mock_file_name = "get_v2_block_detail"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetBlockDetailResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client as client:
            response = await client.get_block_detail(267385261)

        # actual test
        assert isinstance(response, GetBlockDetailResponse)