import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from pycrypt.birdeye import Birdeye
from pycrypt.birdeye.param import BirdeyeAddressType, BirdeyeTimeFrame
from pycrypt.birdeye.schema import (
    GetTokenListResponse,
    GetTokenCreationInfoResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetHistoryResponse
)
from pycrypt.core.exception import MissingAPIKeyError

# load test config
from tests.config import load_config, TestMocker
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestBirdeyePublic:
    """
        Class grouping all unit test associate to PUBLIC endpoints
    """
    mocker = TestMocker(
        mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
    )

    def test_missing_api_key(self) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key
        """
        with pytest.raises(MissingAPIKeyError):
            Birdeye()

    def test_get_token_list(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List".

            Mock Response File: get_token_list.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_list"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch.object(client, "get_token_list", return_value = mock_response)
            
        # execute request
        response = client.get_token_list(limit = 1)

        # actual test
        assert isinstance(response, GetTokenListResponse)   

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)

    def test_get_price(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".

            Mock Response File: get_price.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch.object(client, "get_price", return_value = mock_response)
            
        # execute request
        response = client.get_price(address = "So11111111111111111111111111111111111111112")

        # actual test
        assert isinstance(response, GetPriceResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)

    def test_get_price_multiple(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Multiple".

            Mock Response File: get_price_multiple.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price_multiple"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceMultipleResponse)
            mocker.patch.object(client, "get_price_multiple", return_value = mock_response)
            
        # execute request
        tokens_ca = ["So11111111111111111111111111111111111111112", "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"]
        response = client.get_price_multiple(list_address = tokens_ca)

        # actual test
        assert isinstance(response, GetPriceMultipleResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)

    def test_get_price_historical(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Historical".

            Mock Response File: get_price_historical.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price_historical"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch.object(client, "get_price_historical", return_value = mock_response)
            
        # execute request
        response = client.get_price_historical(
            address = "So11111111111111111111111111111111111111112",
            address_type = BirdeyeAddressType.TOKEN.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetPriceHistoricalResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)

    def test_get_history(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "History".

            Mock Response File: get_history.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_history"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHistoryResponse)
            mocker.patch.object(client, "get_history", return_value = mock_response)
            
        # execute request
        response = client.get_history()

        # actual test
        assert isinstance(response, GetHistoryResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)

class TestBirdeyePrivate:
    """
        Class grouping all unit test associate to PRIVATE endpoints
    """
    mocker = TestMocker(
        mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
    )

    def test_get_token_creation_info(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Creation Token Info".

            Mock Response File: get_token_creation_info.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_creation_info"
        if config.birdeye.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCreationInfoResponse)
            mocker.patch.object(client, "get_token_creation_info", return_value = mock_response)
            
        # execute request
        response = client.get_token_creation_info(address = "So11111111111111111111111111111111111111112")

        # actual test
        assert isinstance(response, GetTokenCreationInfoResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response:
            self.mocker.store_mock_response(mock_file_name, response)