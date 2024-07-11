import pytest

from cyhole.core.client import APIClient, AsyncAPIClient
from cyhole.core.param import CyholeParam, RequestType
from cyhole.core.exception import RequestTypeNotSupported, ParamUnknownError, AsyncClientAPISessionNotAvailable

URL_TEST_GET = "http://httpbin.org/get"
URL_TEST_POST = "http://httpbin.org/post"

# clients
client = APIClient()

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
    client = APIClient(header = headers)
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
    async_client = AsyncAPIClient()

    assert async_client._session is None
    assert async_client.is_connected() == False

@pytest.mark.asyncio
async def test_async_client_connect() -> None:
    """
        Unit Test to check the correct connection of AsyncAPIClient.
    """
    async_client = AsyncAPIClient()
    async_client.connect()

    assert async_client._session is not None
    assert async_client.is_connected() == True

@pytest.mark.asyncio
async def test_async_client_close_connetion() -> None:
    """
        Unit Test to check the correct closing connection of AsyncAPIClient.
    """
    async_client = AsyncAPIClient()
    async_client.connect()
    await async_client.close()

    assert async_client._session is None
    assert async_client.is_connected() == False

@pytest.mark.asyncio
async def test_async_client_close_connetion_error() -> None:
    """
        Unit Test to check error on closing connection 
        if session not available on AsyncAPIClient.
    """
    async_client = AsyncAPIClient()
    with pytest.raises(AsyncClientAPISessionNotAvailable):
        await async_client.close()

@pytest.mark.asyncio
async def test_async_client_context_manager() -> None:
    """
        Unit Test to check the correct usage of context manager of AsyncAPIClient.
    """
    async with AsyncAPIClient() as client:
        assert client._session is not None
        assert client.is_connected() == True

@pytest.mark.asyncio
async def test_async_client_api_request_no_session() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function with Request Type not supported.
    """
    async_client = AsyncAPIClient()
    with pytest.raises(AsyncClientAPISessionNotAvailable):
        await async_client.api(type = RequestType.GET.value, url = URL_TEST_GET)

@pytest.mark.asyncio
async def test_async_client_api_request_type_not_supported() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function with Request Type not supported.
    """
    async with AsyncAPIClient() as client:
        with pytest.raises(RequestTypeNotSupported):
            await client.api(type = "XXX", url = "")

@pytest.mark.asyncio
async def test_async_client_api_get() -> None:
    """
        Unit Test for `AsyncAPIClient.api` function for GET endpoint.
    """
    async with AsyncAPIClient() as client:
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
    async with AsyncAPIClient() as client:
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
    async with AsyncAPIClient(header = headers) as client:
        response = await client.api(
            type = RequestType.POST.value,
            url = URL_TEST_POST,
            json = {"test": "data"})
        assert response.status_code == 200
        assert response.content.decode() is not None

def test_param_unknown() -> None:
    """
        Unit Test for `ParamUnknownError` exception.
    """
    class ParamTest(CyholeParam):
        TEST = "test"

    with pytest.raises(ParamUnknownError):
        ParamTest.check("xxx")