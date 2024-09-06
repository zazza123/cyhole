import pytest
from datetime import datetime
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.solscan.v2 import Solscan
from cyhole.solscan.v2.param import (
    SolscanActivityTransferType,
    SolscanFlowType
)
from cyhole.solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse
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