import pytest
import requests

from cyhole.core.token.solana import SOL
from cyhole.core.interaction import Interaction
from cyhole.core.client import APIClient, AsyncAPIClient, redact
from cyhole.core.param import CyholeParam, RequestType
from cyhole.core.exception import RequestTypeNotSupported, ParamUnknownError, AsyncClientAPISessionNotAvailable

URL_TEST_GET = "http://httpbin.org/get"
URL_TEST_POST = "http://httpbin.org/post"

# variables
interaction = Interaction()
client = APIClient(interaction)

def test_sync_client_api_request_type_not_supported() -> None:
    """
        Unit Test for `APIClient.api` function with Request Type not supported.
    """
    with pytest.raises(RequestTypeNotSupported):
        client.api(type = "XXX", url = "")

def test_sync_client_api_with_header() -> None:
    """
        Unit Test for `APIClient.api` function with `headers`.
    """
    with pytest.raises(RequestTypeNotSupported):
        client.api(type = "XXX", url = "", headers = {"test": "test"})

def test_sync_client_api_get() -> None:
    """
        Unit Test for `APIClient.api` function for GET endpoint.
    """
    response = client.api(type = RequestType.GET.value, url = URL_TEST_GET)
    assert response.status_code == 200
    assert response.content.decode() is not None

def test_sync_client_api_post() -> None:
    """
        Unit Test for `APIClient.api` function for POST endpoint.
    """
    headers = {
        "Content-Type": "application/json"
    }
    interaction = Interaction(headers = headers)
    client = APIClient(interaction)
    response = client.api(
        type = RequestType.POST.value,
        url = URL_TEST_POST,
        json = {"test": "data"}
    )
    assert response.status_code == 200
    assert response.content.decode() is not None

@pytest.mark.asyncio
async def test_async_client_init() -> None:
    """
        Unit Test to check the correct init of AsyncAPIClient.
    """
    async_client = AsyncAPIClient(interaction)

    assert async_client._session is None
    assert not async_client.is_connected()

@pytest.mark.asyncio
async def test_async_client_connect() -> None:
    """
        Unit Test to check the correct connection of AsyncAPIClient.
    """
    async_client = AsyncAPIClient(interaction)
    async_client.connect()

    assert async_client._session is not None
    assert async_client.is_connected()

@pytest.mark.asyncio
async def test_async_client_close_connetion() -> None:
    """
        Unit Test to check the correct closing connection of AsyncAPIClient.
    """
    async_client = AsyncAPIClient(interaction)
    async_client.connect()
    await async_client.close()

    assert async_client._session is None
    assert not async_client.is_connected()

@pytest.mark.asyncio
async def test_async_client_close_connetion_error() -> None:
    """
        Unit Test to check error on closing connection 
        if session not available on AsyncAPIClient.
    """
    async_client = AsyncAPIClient(interaction)
    with pytest.raises(AsyncClientAPISessionNotAvailable):
        await async_client.close()

@pytest.mark.asyncio
async def test_async_client_context_manager() -> None:
    """
        Unit Test to check the correct usage of context manager of AsyncAPIClient.
    """
    async with AsyncAPIClient(interaction) as client:
        assert client._session is not None
        assert client.is_connected()

@pytest.mark.asyncio
async def test_async_client_api_request_no_session() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function with Request Type not supported.
    """
    async_client = AsyncAPIClient(interaction)
    with pytest.raises(AsyncClientAPISessionNotAvailable):
        await async_client.api(type = RequestType.GET.value, url = URL_TEST_GET)

@pytest.mark.asyncio
async def test_async_client_api_request_type_not_supported() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function with Request Type not supported.
    """
    async with AsyncAPIClient(interaction) as client:
        with pytest.raises(RequestTypeNotSupported):
            await client.api(type = "XXX", url = "")

@pytest.mark.asyncio
async def test_async_client_api_get() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function for GET endpoint.
    """
    async with AsyncAPIClient(interaction) as client:
        response = await client.api(type = RequestType.GET.value, url = URL_TEST_GET)
        assert response.status_code == 200
        assert response.content.decode() is not None

@pytest.mark.asyncio
async def test_async_client_api_get_with_params() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function for GET endpoint.
    """
    params = {
        "name": "cyhole",
        "version" : None
    }
    async with AsyncAPIClient(interaction) as client:
        response = await client.api(type = RequestType.GET.value, url = URL_TEST_GET, params = params)
        assert response.status_code == 200
        assert response.content.decode() is not None

@pytest.mark.asyncio
async def test_async_client_api_post() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function for POST endpoint.
    """
    headers = {
        "Content-Type": "application/json"
    }
    interaction = Interaction(headers = headers)
    async with AsyncAPIClient(interaction) as client:
        response = await client.api(
            type = RequestType.POST.value,
            url = URL_TEST_POST,
            json = {"test": "data"})
        assert response.status_code == 200
        assert response.content.decode() is not None

def test_async_client_clean_params_drops_none_and_coerces_bool() -> None:
    """
        Unit Test for `AsyncAPIClient._clean_params`.

        `aiohttp`'s URL builder rejects raw `bool` query values with
        "Invalid variable type: value should be str, int or float, got True
        of type <class 'bool'>". The cleaner must coerce booleans to the
        lowercase `"true"` / `"false"` strings that REST servers expect, and
        must keep dropping `None`-valued keys.
    """
    interaction = Interaction()
    async_client = AsyncAPIClient(interaction)

    cleaned = async_client._clean_params({
        "drop_me": None,
        "keep_me": "ok",
        "keep_int": 42,
        "keep_float": 1.5,
        "flag_true": True,
        "flag_false": False,
    })

    assert "drop_me" not in cleaned
    assert cleaned["keep_me"] == "ok"
    assert cleaned["keep_int"] == 42
    assert cleaned["keep_float"] == 1.5
    assert cleaned["flag_true"] == "true"
    assert cleaned["flag_false"] == "false"


@pytest.mark.asyncio
async def test_async_client_api_get_with_bool_param() -> None:
    """
        Integration Test: `AsyncAPIClient.api` with a `bool` query param
        no longer raises in `aiohttp`'s URL builder and reaches the server
        as a lowercase string.
    """
    interaction = Interaction()
    params = {
        "name": "cyhole",
        "verbose": True,
    }
    async with AsyncAPIClient(interaction) as client:
        response = await client.api(type = RequestType.GET.value, url = URL_TEST_GET, params = params)
    assert response.status_code == 200
    # httpbin echoes the query string back; the bool came through as "true".
    body = response.json()
    assert body["args"]["verbose"] == "true"
    assert body["args"]["name"] == "cyhole"


def test_param_unknown() -> None:
    """
        Unit Test for `ParamUnknownError` exception.
    """
    class ParamTest(CyholeParam):
        TEST = "test"

    with pytest.raises(ParamUnknownError):
        ParamTest.check("xxx")

def test_token_to_decimals() -> None:
    """
        Unit Test for `CyholeToken.to_decimals` function.
    """
    assert SOL.to_decimals(1_011_000_000) == 1.011
SECRET = "00000000-1111-2222-3333-444444444444"
URL_WITH_KEY = f"https://mainnet.helius-rpc.com/?api-key={SECRET}"

def _error_response(status_code: int = 522) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.reason = "Origin Connection Time-out"
    response.url = URL_WITH_KEY
    return response

def test_redact_masks_key_params() -> None:
    """
        Unit Test for `redact`: the values of key-like query parameters are masked,
        the others are kept.
    """
    text = f"url: https://x.io/v1/e?api-key={SECRET}&limit=10&apikey=a1&token=b2&key=c3&api_key=d4"
    assert redact(text) == "url: https://x.io/v1/e?api-key=***&limit=10&apikey=***&token=***&key=***&api_key=***"

def test_sync_client_api_http_error_hides_the_api_key(mocker) -> None:
    """
        Unit Test for `APIClient.api`: an HTTP error raised for a URL that carries an
        API key must not expose the key, neither in the message nor in the response.
    """
    mocker.patch("cyhole.core.client.requests.post", return_value = _error_response())
    with pytest.raises(requests.HTTPError) as error:
        client.api(type = RequestType.POST.value, url = URL_WITH_KEY, json = {})
    assert SECRET not in str(error.value)
    assert "api-key=***" in str(error.value)
    assert SECRET not in error.value.response.url

def test_sync_client_api_connection_error_hides_the_api_key(mocker) -> None:
    """
        Unit Test for `APIClient.api`: a connection error whose message carries the
        request URL is raised again without the key and without the original chained.
    """
    message = f"HTTPSConnectionPool(host='mainnet.helius-rpc.com', port=443): Max retries exceeded with url: /?api-key={SECRET}"
    mocker.patch("cyhole.core.client.requests.post", side_effect = requests.ConnectionError(message))
    with pytest.raises(requests.ConnectionError) as error:
        client.api(type = RequestType.POST.value, url = URL_WITH_KEY, json = {})
    assert SECRET not in str(error.value)
    assert error.value.__cause__ is None and error.value.__suppress_context__

class _FakeContext:
    async def __aenter__(self) -> "_FakeContext":
        return self
    async def __aexit__(self, *args) -> None:
        return None

class _FakeSession:
    def post(self, *args, **kwargs) -> _FakeContext:
        return _FakeContext()

@pytest.mark.asyncio
async def test_async_client_api_http_error_hides_the_api_key(mocker) -> None:
    """
        Unit Test for `AsyncAPIClient.api`: an HTTP error raised for a URL that carries
        an API key must not expose the key, neither in the message nor in the response.
    """
    async_client = AsyncAPIClient(interaction)
    async_client._session = _FakeSession()
    mocker.patch.object(async_client, "_to_requests_response", return_value = _error_response())
    with pytest.raises(requests.HTTPError) as error:
        await async_client.api(type = RequestType.POST.value, url = URL_WITH_KEY, json = {})
    assert SECRET not in str(error.value)
    assert "api-key=***" in str(error.value)
    assert SECRET not in error.value.response.url
