# Testing

This section is dedicated to explain how the testing phase is managed inside `cyhole` library.

By assuming that the reader has downloaded locally the library (see [Latest Library Version](index.md#latest-library-version) for more details). It is required to download also the python testing libraries:

- activate the `python` environment you want to use
- navigate to the `cyhole/tests` folder
- run the command `pip install -r requirements.txt`

This command is required to download `pytest` and its extensions used by `cyhole` for test management.

## Configuration File

The `cyhole` library interacts with many external APIs that sometimes require an API Key in order to extract data. Since the usage of these API Keys could be subjected to costs, a proper configuration for the tests is required.

The configuration is managed by a configuration file called `test.ini`, which is loaded during the execution of the tests. By using this file will be possible to:

- manage externally API Keys
- enable/disable mock responses

Check the default `test.default.ini` file inside the repository for a complete list of the available configurations.

During the tests' execution the configuration is loaded into [`TestConfiguration`](#config.TestConfiguration) class.

## Mock Responses

During the implementation phase, could be not necessary to execute a call to the external API service, especially if the external system requires an API Key with a computational costs. For this reason, it was implementated a method to mock the external API responses and overcome this situation.

The usage of the mocker is defined inside the configuration file in the global/local variables called `mock_response`. 

!!! note
    Global `mock_response` value overwrites the local `mock_response` value.

If the mocker response functionality is enabled, then the tests will try to load a JSON file with the response schema stored from a previous call of the API. The root of the mocker files is defined inside the `mock_folder` global variable, and specificed for each `Interaction` inside the local `mock_folder` variable.

Every time the tests are executed with the mock response functionality disabled, the process automatically stores the response in a JSON file into the proper resources folder. To avoid the overwrite of the JSON file use the global `mock_file_overwrite` variable.

All the functionalities to load and store the mock responses are managed by the [`MockerManager`](#config.MockerManager) class.

### Example

The code below provides a test extracted from `test_birdeye.py` to explain the mocker usage:

```py title="test_birdeye.py"
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cyhole.birdeye import Birdeye
from cyhole.birdeye.schema import GetTokenListResponse

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder

class TestBirdeyePublic:
    """
        Class grouping all unit test associate to **PUBLIC** endpoints.
    """
    birdeye = Birdeye(api_key = config.birdeye.api_key)
    mocker = MockerManager(mock_path)

    def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List" 
            for synchronous logic.

            Mock Response File: get_token_list.json
        """
    
        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.birdeye.client.get_token_list(limit = 1)

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)
```

By analysing the code into different blocks, we first import all the required dependencies:

```py hl_lines="4 6-7"
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cyhole.birdeye import Birdeye
from cyhole.birdeye.schema import GetTokenListResponse

...
```

To hendle the mocker functionalities, we need to import the [`MockerManager`](#config.MockerManager) class from `pytest_mock` library extension of `pytest`. We also import the [`Birdeye`](../interactions/birdeye/interaction.md) class and the [`GetTokenListResponse`](../interactions/birdeye/schema.md#cyhole.birdeye.schema.GetTokenListResponse) schema from the [`cyhole.birdeye`](../interactions/birdeye/index.md) module to use them in the test.

As next step, we load the configuration file by importing the `load_config` function and the [`MockerManager`](#config.MockerManager) class:

```py hl_lines="2 3"
...
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
...
```

For [`cyhole.birdeye`](../interactions/birdeye/index.md) extension, we decided to manage the tests in two different classes: `TestBirdeyePublic` and `TestBirdeyePrivate`. The first one is used to test the public endpoints, while the second one is used to test the private endpoints. In this case, we are testing the public endpoints, so we are using the `TestBirdeyePublic` class.

```py hl_lines="3 7 8"
...

class TestBirdeyePublic:
    """
        Class grouping all unit test associate to **PUBLIC** endpoints.
    """
    birdeye = Birdeye(api_key = config.birdeye.api_key)
    mocker = MockerManager(mock_path)

...
```

The `TestBirdeyePublic` class contains the [`Birdeye`](../interactions/birdeye/interaction.md) object and the [`MockerManager`](#config.MockerManager) that is used to load and store the mock responses. The `mock_path` variable is used to define the path where the mock responses are stored.

As a final step, we define the test method:

```py hl_lines="3 13-15 24-25"
...

def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Token - List" 
        for synchronous logic.

        Mock Response File: get_token_list.json
    """

    # load mock response
    mock_file_name = "get_token_list"
    if config.mock_response or config.birdeye.mock_response_public:
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

    # execute request
    response = self.birdeye.client.get_token_list(limit = 1)

    # actual test
    assert isinstance(response, GetTokenListResponse)

    # store request (only not mock)
    if config.mock_file_overwrite and not config.birdeye.mock_response_public:
        self.mocker.store_mock_model(mock_file_name, response)
```

Observe that the test method is defined with the `mocker` fixture, which is used to patch the [`APIClient.api`](core/client.md#cyhole.core.client.APIClientInterface.api) method. If the mocker response functionality is enabled, the method `load_mock_response` is used to load the mock response from the JSON file. The `patch` method is used to mock the [`APIClient.api`](core/client.md#cyhole.core.client.APIClientInterface.api) method and return the mock response. 

The `get_token_list` method is executed, and the response is stored in the `response` variable. The test checks if the response is an instance of the [`GetTokenListResponse`](../interactions/birdeye/schema.md#cyhole.birdeye.schema.GetTokenListResponse) schema. 

Finally, observe that if the `mock_file_overwrite` variable is enabled and the `mock_response_public` variable is disabled, the method `store_mock_model` is used to store the response in the JSON file.

## `sync` and `async`

The `cyhole` library is designed to work with both synchronous and asynchronous logic. For this reason, every tests in charge to perform a call to an external API service should be implemented in both ways. To hendle `async` tests, the `pytest` library provides the `pytest-asyncio` extension that allows to run `async` tests in a synchronous environment.

The code below provides an example of how to was implemented the test for the [`get_token_list`](../interactions/birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_list) endpoint in both `sync` and `async` logic in [`cyhole.birdeye`](../interactions/birdeye/index.md).

```py hl_lines="1 25-26"
def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Token - List" 
        for synchronous logic.

        Mock Response File: get_token_list.json
    """

    # load mock response
    mock_file_name = "get_token_list"
    if config.mock_response or config.birdeye.mock_response_public:
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

    # execute request
    response = self.birdeye.client.get_token_list(limit = 1)

    # actual test
    assert isinstance(response, GetTokenListResponse)

    # store request (only not mock)
    if config.mock_file_overwrite and not config.birdeye.mock_response_public:
        self.mocker.store_mock_model(mock_file_name, response)

@pytest.mark.asyncio
async def test_get_token_list_async(self, mocker: MockerFixture) -> None:
    """
        Unit Test used to check the response schema of endpoint "Token - List" 
        for asynchronous logic.

        Mock Response File: get_token_list.json
    """

    # load mock response
    mock_file_name = "get_token_list"
    if config.mock_response or config.birdeye.mock_response_public:
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

    # execute request
    async with self.birdeye.async_client as client:
        response = await client.get_token_list(limit = 1)

    # actual test
    assert isinstance(response, GetTokenListResponse)
```

## Annex

### `config.py`

::: config