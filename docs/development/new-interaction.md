# New `Interaction`

This section is dedicated to all the people who wants to create a new `Interaction`. Since these objects are the building blocks of the library, it is important to define a set of rules to follow to standardise their creation.

First, it is highly suggested to read the introduction on what an [`Interaction`](../interactions/index.md) is, and to have a look on the [Core](core/index.md) section.

Second, fork the repository and create a dedicated branch with the corresponding pattern name: `{name}-new-interaction`, where `{name}` should be replaced with the name of the new interaction.

## Folders Organisation

This section is dedicated to explain the folders' organisation inside the library (including tests and documentation).

- **Library**: inside `src/cyhole` it is necessary to create a new folder called `{name}` that will have all the required files to manage the new interaction.
- **Tests**: inside `tests/resources` it is necessary to create a new folder called `{name}` that will store the JSON files with the responses of the API endpoints used by the mocker during the tests executions.
- **Documentation**: inside `docs/interactions` it is necessary to create a new folder called `{name}` that will provide all the Markdown files necessary for the documentations.

The structure will look similar to this:

``` hl_lines="4-5 10-11 16-17"
.
├─ docs/
│  ├─ interactions/
│  │  ├─ {name}/
│  │  │  └─ ...
│  │  └─ ...
│  └─ ...
├─ src/
│  ├─ cyhole/
│  │  ├─ {name}/
│  │  │  └─ ...
│  │  └─ ...
│  └─ ...
├─ tests/
│  │  └─ resources/
│  │     ├─ {name}/
│  │     │  └─ ...
│  │     └─ ...
│  ├─ ...
└─ ...
```

## Core

This section is dedicated to explain the rules to follow during the creation of a new `Interaction`.

!!! abstract "Assumptions"

    - The actual code **must** be available inside the folder `src/cyhole/{name}`.
    - Inside the code's folder there **must** be the following files:
        - `__init__.py`: the actual entry point in the library.
        - `client.py`: API client classes.
        - `exception.py`: dedicated exceptions.
        - `interaction.py`: interaction class.
        - `param.py`: possible parameters required by the endopints.
        - `schema.py`: response and body schemas to use in the endpoints.

We now proceed to further analyse every required file.

### `__init__.py`

This file should recall **only** the new `Interaction` class from the `interaction.py` file.

``` py title="__init__.py"
from ..{name}.interaction import {Name}

__all__ = [
    "{Name}"
]
```

### `interaction.py`

This is the most important file because the new `Interaction`'s class is defined here.

The box below provides all the assumptions to follow during the creation of a new `Interaction`.

!!! abstract "Assumptions"

    - The `Interaction` class **must** inherits from [`cyhole.core.interaction.Interaction`](core/interaction.md#cyhole.core.interaction.Interaction) class.
    - The name of the interaction should refers univocally to the external API site; e.g. it is usually the site name.
    - The attributes `client` and `async_client` are initiated inside the `__init__` method and defined in `client.py` file.
    - Every endpoint is identified by **one private** method with the following assumptions:

        - The name should recall univocally the endpoint and the type of the request. The naming convention is `_{request_type}_{endpoint_name}`, where `{request_type}` reflects the request's type (get, post, ...) and `{endpoint_name}` recalls the name of the original endpoint.
        - The **first** parameter is called `sync` of type `bool` and is used to define the synchronous/asynchronous behavior of the method.
        - The output/input schema of an endpoint is defined by a `pydantic.BaseModel` inside the `schema.py` file.
        - The naming convention of an output/input schema should recall univocally the corresponding endpoint. The naming convention is `{request_type}{endpoint_name}Response/Body`, where `{request_type}` and `{endpoint_name}` recalls the name of the original endpoint, and they are concatenated using the camel case syntax.
        - To manage the `sync` and `async` behavior, the output of the method must be of type `{output_schema_response} | Coroutine[None, None, {output_schema_response}]`, where `{output_schema_response}` is the output schema.
        - Above the method definition is required to include two `@overload` definitions to specify the output type according to the value of `sync` parameter:

            - `True`: the output should be `{output_schema_response}`.
            - `False`: the output should be `Coroutine[None, None, {output_schema_response}]`.

### `client.py`

In this file are defined the Clients used by the `Interaction` to perform the actual calls to the external API endpoints.

!!! abstract "Assumptions"

    - An `Interaction` requires two Clients:

        - The Client in charge to perform the **synchronous** logic must inherits from [`cyhole.core.client.APIClient`](core/client.md#cyhole.core.client.APIClient), and its name should follow the naming convention `{name}Client`, where `{name}` is the name of the new interaction.
        - The Client in charge to perform the **asynchronous** logic must inherits from [`cyhole.core.client.AsyncAPIClient`](core/client.md#cyhole.core.client.AsyncAPIClient), and its name should follow the naming convention `{name}AsyncClient`, where `{name}` is the name of the new interaction.

    - As described in the previous section, every endpoint is identified inside the `Interaction` class by a private function. Since the clients are responsable for the *actual* interaction with the external API, it is required to implement on **both** clients, a **public** version of the method; one for `sync` logic and one for `async`. The method's name should be the same for both clients, and it must be equals the private method's name without the `_` prefix. Hence, we should obtain the following situation:
        - `_get_example` method defined in the `Interaction` class with the actual endpoint's logic.
        - `get_example` method defined inside the **synchronous** client and recalling the `_get_example` method with `sync` equals `True`.
        - `async get_example` method defined inside the **asynchronous** client and recalling the `_get_example` method with `sync` equals `False`.

### `schema.py`

Inside this file are defined all the classes used to standardise the input/output schemas required by all the implemented enpoints.

!!! abstract "Assumptions"

    - Every schema **must** inherits from `pydantic.BaseModel` class.
    - Every schema and sub-schema name **must** recall the corresponding endpoint. The naming convention to use is `{endpoint_method_name}{type}`, where the `{endpoint_method_name}` is the name of the endpoint function using the camel-case syntax, and `{type}` depends on the situation:
        - `Response`: if the schema refers to the actual response of the endpoint.
        - `Body`: if the schema refers to the input body required by a POST endpoint.
        - Other names can be used for intermediate schemas.

### `param.py`

It could happen that the external endpoints require parameters (`params`) coming from specific value lists. To help as much as possible the users and avoid wrong values, this file stores all the `Enum` classes identifing the `params` with value lists.

!!! abstract "Assumptions"

    - Every param **must** inherits from [`cyhole.core.param.CyholeParam`](core/param.md#cyhole.core.param.CyholeParam) class.
    - The naming convention **must** be `{name}{param_name}`, where `{name}` is the name of the new interaction, and `{param_name}` a set of words that identify the param univocally.

### `exception.py`

All the exceptions dedicated to this extension are defined inside this file.

!!! abstract "Assumptions"

    - There should be a general `Exception` extension specific. This exception **must** inherits from [`cyhole.core.exception.CyholeException`](core/exception.md#cyhole.core.exception.CyholeException), and its name should follow the naming convention `{name}Exception`, where `{name}` is the name of the new interaction.
    - All other exceptions **must** inherits from the `{name}Exception` class.

## Tests

The implementation of proper tests is crucial for the maintenance of the library, for this reason this section describes the test's management for a new `Interaction`. It is also suggested to check [Testing](testing.md) chapter for more details on test's management.

!!! abstract "Assumptions"

    - All the tests **must** be available in a file called `test_{name}.py` inside `tests` folder, where `{name}` is the name of the new interaction.
    - Every endpoint **must** have at least one basic test to ensure the response schema consistency.
    - Every test that call an endpoint **must** be available for both *synchronous* (test's name ends with `_sync`) and *asynchronous* (test's name ends with `_async`) logic.
    - The mock responses **must** be available inside the `tests/resources/{name}` folder.
    - Every endpoint **must** have at least one mock response JSON file, and the naming convention is `{endpoint_method_name}_{info}.json`, where the `{endpoint_method_name}` is the name of the endpoint function using the camel-case syntax, and `{info}` provides additional information to the test.
    - The test's configuration (`tests/config.py`) **must** be extended to manage at least `mock_response` and `mock_folder` variables, and the corresponding `tets.default.ini` configuration must be updated as well.
    - Every test involving a call to an endopint and checking the respoonse **must** implement the `mocker` functionlity to ensure the test's execution also in offline mode.

## Documentation

As a final step in the implementation of a new `Interaction`, it is required to create the proper documentation to ensure its usability.

The *default* documentation structure is described below:

``` hl_lines="4-10"
.
├─ docs/
│  ├─ interactions/
│  │  ├─ {name}/
│  │  │  ├─ client.md
│  │  │  ├─ exception.md
│  │  │  ├─ index.md
│  │  │  ├─ interaction.md
│  │  │  ├─ param.md
│  │  │  └─ schema.md
│  │  └─ ...
│  └─ ...
└─ ...
```

where:

- `client.md`: this file is entitled *Client*, and recalls the source code of `client.py` file.
- `exception.md`: this file is entitled *Exceptions*, and recalls the source code of `exception.py` file.
- `index.md`: this file is used to introduce the new `Interaction` by providing a description, some examples and the links to the other sections.
- `interaction.md`: this file is entitled *Interaction*, and recalls the source code of `__init__.py` file.
- `param.md`: this file is entitled *Parameters*, and recalls the source code of `param.py` file.
- `schema.md`: this file is entitled *Schema*, and recalls the source code of `schema.py` file.

!!! abstract "Assumptions"

    - The above structure **must** be always available, and can be integrated with additional chapters and sections if required.
    - To ensure the correct visualisation of the new section, it is also necessary to include them inside the `mkdocs.yml` file in `nav.Interactions` list.

## Example

Since the best way to understand a topic is through examples, in the following part we will provide all the previous sections contextualised in the situation of a hypothetical `Interaction` for a site called *sun.net* with only one API endpoint of type GET `sun.net/prices`.

- The GitHub brench will be called `sun-new-interaction`.
- The main class will be `Sun` inside `cyhole.sun.interaction`.
- The new brench will have the following new folders and files (highlighted):
    ``` hl_lines="5-11 16-22 27-28 31"
    .
    ├─ docs/
    │  ├─ interactions/
    │  │  ├─ ...
    │  │  ├─ sun/
    │  │  │  ├─ client.md
    │  │  │  ├─ exception.md
    │  │  │  ├─ index.md
    │  │  │  ├─ interaction.md
    │  │  │  ├─ param.md
    │  │  │  └─ schema.md
    │  │  └─ index.md
    │  └─ ...
    ├─ src/
    │  ├─ cyhole/
    │  │  ├─ sun/
    │  │  │  ├─ __init__.py
    │  │  │  ├─ client.py
    │  │  │  ├─ exception.py
    │  │  │  ├─ interaction.py
    │  │  │  ├─ param.py
    │  │  │  └─ schema.py
    │  │  └─ __init__.py
    │  └─ requirements.txt
    ├─ tests/
    │  │  └─ resources/
    │  │     ├─ sun/
    │  │     │  └─ get_price.json
    │  │     └─ ...
    │  ├─ ...
    │  └─ test_sun.py
    └─ mkdocs.yml
    ```

In more details, we are going to have the core of the extension defined inside the `sun/interaction.py` with the `Sun` class.

``` py title="interaction.py"
from ..core.param import RequestType
from ..core.interaction import Interaction
from ..sun.client import SunClient, SunAsyncClient
from ..sun.schema import GetPriceResponse

class Sun(Interaction):
"""
    Class used to connect [Sun](https://sun.net) API.
"""

    def __init__(self, headers: Any | None = None) -> None:
        super().__init__(headers)

        # clients
        self.client = SunClient(self)
        self.async_client = SunAsyncClient(self)

        # API urls
        self.url_api = "https://sun.net/"
        return

    @overload
    def _get_price(self, sync: Literal[True]) -> GetPriceResponse: ...

    @overload
    def _get_price(self, sync: Literal[False]) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(self, sync: bool) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the **Price** API endpoint.

            Returns:
                tokens' prices.
        """
        # set params
        url = self.url_api + "prices"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, self.url_api_price)
            return GetPriceResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, self.url_api_price)
                return GetPriceResponse(**content_raw.json())
            return async_request()
```

The class inherits from [`cyhole.core.interaction.Interaction`](core/interaction.md#cyhole.core.interaction.Interaction) and it has attributes `client` and `async_client` that are instances of `sun.client.SunClient` and `sun.client.SunAsyncClient`.

The only endopint is mapped into the private class `_get_price` that contains the actual logic for the extraction and returns a `GetPriceResponse` object in synchronous logic and a `Coroutine` returning a `GetPriceResponse` object in asynchronous case.

The actual API calls are then defined inside the `sun/client.py` file:

``` py title="client.py"
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..sun.schema import GetPriceResponse

if TYPE_CHECKING:
    from ..sun.interaction import Sun

class SunClient(APIClient):
    """
        Client used for synchronous API calls for `Sun` interaction.
    """

    def __init__(self, interaction: Sun, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Sun = self._interaction

    def get_price(self) -> GetPriceResponse:
        """
            Call the Sun's **Price** API endpoint for synchronous logic. 
            All the API endopint details are available on `Sun._get_price`.
        """
        return self._interaction._get_price(True)

class SunAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Sun` interaction.
    """

    def __init__(self, interaction: Sun, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Sun = self._interaction

    async def get_price(self) -> GetPriceResponse:
        """
            Call the Sun's **Price** API endpoint for asynchronous logic. 
            All the API endopint details are available on `Sun._get_price`.
        """
        return await self._interaction._get_price(False)
```

The client classes inherit from [`cyhole.core.client.APIClient`](core/client.md#cyhole.core.client.APIClient) and [`cyhole.core.client.AsyncAPIClient`](core/client.md#cyhole.core.client.AsyncAPIClient).

Finally, the `sun/__init__.py` file will recall **only** the main class:

``` py title="__init__.py"
from ..sun.interaction import Sun

__all__ = [
    "Sun"
]
```

- To ensure consistency of the code, all tests should be implemented; in this scenario the tests are available in `tests/test_sun.py` file. 
The code below is only an example of test implementation according to our initial assumptions.

``` py title="test_sun.py"
import pytest
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.sun import Sun
from cyhole.sun.schema import GetPriceResponse

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.sun.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestSun:
    """
        Class grouping all unit tests.
    """
    sun = Sun()
    mocker = MockerManager(mock_path)

    def test_get_price_token_address_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" for synchronous logic.

            Mock Response File: get_price.json
        """

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.sun.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.sun.client.get_price()

        # actual test
        assert isinstance(response, GetPriceResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.sun.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" for asynchronous logic.

            Mock Response File: get_price.json
        """

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.sun.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.sun.async_client as client:
            response = await client.get_price()

        # actual test
        assert isinstance(response, GetPriceResponse)
```

It is possible to notice that we have created two tests for the end point `get_price`, the first one to test the synchronous logic and another to test the asynchronous one. 
In addition, in order to guarantee replicability of the tests also to other developers who might not have access to the newly implemented API, the file `get_price.json` was introduced inside the new folder `tests/resources/sun` with an example of an endpoint response inside, which could be used in case of mocking calls.

In order to to handle the aspect just described, the default test configuration was therefore also modified so that it could handle the mocking of Sun API calls.

```  ini title="config.default.ini" hl_lines="11-14"
# WARNING
# This is the default test.ini file used to configure the cyhole tests
# Edit and rename it to test.ini in order to use it during the implementation fase.

[global]
# configuration available for all the tests
mock_response = True
mock_folder = tests/resources/mock
mock_file_overwrite = False

[sun]
# configuration for sun integration
mock_response = True
mock_folder = sun
```

- Finally, a new section was introduced in the library documentation in order to explain in all its details the new `Interaction`.