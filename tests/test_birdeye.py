import json
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from pycrypt.birdeye import Birdeye
from pycrypt.birdeye.schema import GetTokenListResponse
from pycrypt.core.exception import AuthorizationAPIKeyError

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
    with pytest.raises(AuthorizationAPIKeyError):
        client = Birdeye()
        client.get_token_list()

def test_get_token_list(mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Token - List".

        If the test configuration enables mock requess, then the test loads the reponse 
        from 'get_token_list.json' file from the 'resources' folder.

        File 'get_token_list.json' is created every time a test is executed using 
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