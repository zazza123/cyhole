import pytest
from pathlib import Path
from datetime import datetime

from pytest_mock import MockerFixture

from cyhole.solscan import Solscan
from cyhole.solscan.schema import (
    GetV1AccountTokensResponse,
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
    solscan = Solscan(api_key_v1 = config.solscan.api_v1_key)
    mocker = MockerManager(mock_path)

    def test_get_v1_account_tokens_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Tokens" on V1 API for synchronous logic.

            Mock Response File: get_v1_account_tokens.json
        """

        # load mock response
        mock_file_name = "get_v1_account_tokens"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV1AccountTokensResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.solscan.client.v1.get_account_tokens(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetV1AccountTokensResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.solscan.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v1_account_tokens_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Account Tokens" on V1 API for asynchronous logic.

            Mock Response File: get_v1_account_tokens.json
        """

        # load mock response
        mock_file_name = "get_v1_account_tokens"
        if config.mock_response or config.solscan.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV1AccountTokensResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.solscan.async_client.v1 as client:
            response = await client.get_account_tokens(SOLSCAN_DONATION_ADDRESS)

        # actual test
        assert isinstance(response, GetV1AccountTokensResponse)