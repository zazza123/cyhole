import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from pycrypt.birdeye import Birdeye
from pycrypt.birdeye.param import BirdeyeAddressType, BirdeyeTimeFrame
from pycrypt.birdeye.schema import (
    GetTokenListResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetHistoryResponse
)
from pycrypt.core.exception import MissingAPIKeyError

# load test config
from tests.config import load_config
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)


def test_missing_api_key() -> None:
    """
        Unit Test to correcty identify a missing/wrong API Key
    """
    with pytest.raises(MissingAPIKeyError):
        client = Birdeye()

def test_get_token_list(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Token - List".

        If the test configuration enables mock requests, then the test loads the response 
        from 'get_token_list.json' file from the 'resources' folder.

        Note: file 'get_token_list.json' is created every time a test is executed using 
        mock response option disabled.
    """
    client = Birdeye(api_key = config.birdeye.api_key)

    # load mock response
    mock_file = "get_token_list.json"
    mock_path_file = mock_path / mock_file
    if config.birdeye.mock_response:

        if not mock_path_file.exists():
            raise Exception("mock file for 'Token - List' does not exist.")
        
        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = GetTokenListResponse(**data)
        
        mocker.patch.object(client, "get_token_list", return_value = mock_response)
        
    # execute request
    response = client.get_token_list(limit = 1)

    # actual test
    assert isinstance(response, GetTokenListResponse)

    # store request (only not mock)
    if not config.birdeye.mock_response:
        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))

def test_get_price(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Price".

        If the test configuration enables mock requests, then the test loads the response 
        from 'get_price.json' file from the 'resources' folder.

        Note: file 'get_price.json' is created every time a test is executed using 
        mock response option disabled.
    """
    client = Birdeye(api_key = config.birdeye.api_key)

    # load mock response
    mock_file = "get_price.json"
    mock_path_file = mock_path / mock_file
    if config.birdeye.mock_response:

        if not mock_path_file.exists():
            raise Exception("mock file for 'Price' does not exist.")
        
        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = GetPriceResponse(**data)
        
        mocker.patch.object(client, "get_price", return_value = mock_response)
        
    # execute request
    response = client.get_price(address = "So11111111111111111111111111111111111111112")

    # actual test
    assert isinstance(response, GetPriceResponse)

    # store request (only not mock)
    if not config.birdeye.mock_response:
        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))

def test_get_price_multiple(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Price - Multiple".

        If the test configuration enables mock requests, then the test loads the response 
        from 'get_price_multiple.json' file from the 'resources' folder.

        Note: file 'get_price_multiple.json' is created every time a test is executed using 
        mock response option disabled.
    """
    client = Birdeye(api_key = config.birdeye.api_key)

    # load mock response
    mock_file = "get_price_multiple.json"
    mock_path_file = mock_path / mock_file
    if config.birdeye.mock_response:

        if not mock_path_file.exists():
            raise Exception("mock file for 'Price - Multiple' does not exist.")
        
        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = GetPriceMultipleResponse(**data)
        
        mocker.patch.object(client, "get_price_multiple", return_value = mock_response)
        
    # execute request
    tokens_ca = ["So11111111111111111111111111111111111111112", "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"]
    response = client.get_price_multiple(list_address = tokens_ca)

    # actual test
    assert isinstance(response, GetPriceMultipleResponse)

    # store request (only not mock)
    if not config.birdeye.mock_response:
        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))

def test_get_price_historical(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Price - Historical".

        If the test configuration enables mock requests, then the test loads the response 
        from 'get_price_historical.json' file from the 'resources' folder.

        Note: file 'get_price_historical.json' is created every time a test is executed using 
        mock response option disabled.
    """
    client = Birdeye(api_key = config.birdeye.api_key)

    # load mock response
    mock_file = "get_price_historical.json"
    mock_path_file = mock_path / mock_file
    if config.birdeye.mock_response:

        if not mock_path_file.exists():
            raise Exception("mock file for 'Price - Historical' does not exist.")
        
        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = GetPriceHistoricalResponse(**data)
        
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
        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))

def test_get_history(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "History".

        If the test configuration enables mock requests, then the test loads the response 
        from 'get_history.json' file from the 'resources' folder.

        Note: file 'get_history.json' is created every time a test is executed using 
        mock response option disabled.
    """
    client = Birdeye(api_key = config.birdeye.api_key)

    # load mock response
    mock_file = "get_history.json"
    mock_path_file = mock_path / mock_file
    if config.birdeye.mock_response:

        if not mock_path_file.exists():
            raise Exception("mock file for 'History' does not exist.")
        
        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = GetHistoryResponse(**data)
        
        mocker.patch.object(client, "get_history", return_value = mock_response)
        
    # execute request
    response = client.get_history()

    # actual test
    assert isinstance(response, GetHistoryResponse)

    # store request (only not mock)
    if not config.birdeye.mock_response:
        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))