from __future__ import annotations

import abc
import requests
from typing import Any, Coroutine, TYPE_CHECKING

import aiohttp
import requests.structures

from ..core.param import RequestType
from ..core.exception import (
    RequestTypeNotSupported, 
    AuthorizationAPIKeyError, 
    AsyncClientAPISessionNotAvailable
)

if TYPE_CHECKING:
    from ..core.interaction import Interaction

class APIClientInterface(metaclass = abc.ABCMeta):
    """
        The following abstract class defines a general Client API. 
        A client is used in order to connect and interact with an external API.

        The key method of an API client is the `api` function that is used 
        to execute the actual requests.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'api') and callable(subclass.api)
            or NotImplemented
        )

    @abc.abstractmethod
    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response  | Coroutine[None, None, requests.Response]:
        """
            Function in charge to execute a request to an API endpoint.

            Parameters:
                type: request's type ([`RequestType`][cyhole.core.param.RequestType]).
                url: API endpoint.
                args: additional input parameters to provided.
                kwargs: additional input parameters to provided.

            Returns:
                The response object structured as `request` library. Observe that the return type could be a `Coroutine` in case of implementation  of an `async` client.

            Raises:
                RequestTypeNotSupported: if the request type is not a valid value of [`RequestType`][cyhole.core.param.RequestType].
                AuthorizationAPIKeyError: if the response return a 401 code.
        """
        raise NotImplementedError

class APIClient(APIClientInterface):
    """
        This client is designed to manage all the REST calls to an external API by using `requests` module.

        !!! info
            As a conseguence of using `requests` module, this client can be used to perform 
            the API requests in **synchronous** logic and achieve the parallelism by using threads.

        Use this class as middlelayer to manage all the requests to an external API. 
        By default, all new `Interaction` should have the synchronous client that inherits from this class.

        During the creation of the object is possible to specify some global configurations.

        Parameters:
            headers: headers used globally in all API requests.
    """
    def __init__(self, interaction: Interaction, headers: Any | None = None) -> None:
        self._interaction = interaction
        self.headers = headers
        return

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:

        # check for headers
        if self.headers:
            kwargs["headers"] = self.headers

        # execute request
        match type:
            case RequestType.GET.value:
                response = requests.get(url, *args, **kwargs)
            case RequestType.POST.value:
                response = requests.post(url, *args, **kwargs)
            case _:
                raise RequestTypeNotSupported(f"Request '{type}' not supported.")

        # check response
        match response.status_code:
            case 401:
                raise AuthorizationAPIKeyError("Check API Key")
            case _:
                response.raise_for_status()
                return response

class AsyncAPIClient(APIClientInterface):
    """
        This client is designed to manage all the REST calls to an external API by using `aiohttp` module.

        !!! info
            As a conseguence of using `aiohttp` module, this client can be used to perform 
            the API requests in **asynchronous** logic of `async` paradigm.

        Use this class as middlelayer to manage all the requests to an external API. 
        By default, all new `Interaction` should have the asynchronous client that inherits from this class.

        During the creation of the object is possible to specify some global configurations.

        Parameters:
            headers: headers used globally in all API requests.
    """
    def __init__(self, interaction: Interaction, headers: Any | None = None) -> None:
        self._session: aiohttp.ClientSession | None = None
        self._interaction = interaction
        self.headers = headers
        return

    async def __aenter__(self):
        """Open a new session."""
        self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        """Exits from the session."""
        await self.close()
        return

    def is_connected(self) -> bool:
        """Check if the session is available."""
        if self._session is None:
            return False
        return not self._session.closed

    def connect(self) -> None:
        """Init a new session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return

    async def close(self) -> None:
        """Close current available session."""

        if self._session is None:
            raise AsyncClientAPISessionNotAvailable("No session currently available.")

        # close and reset
        await self._session.close()
        self._session = None
        return

    async def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:

        # check session availability
        if self._session is None:
            raise AsyncClientAPISessionNotAvailable("No session currently available.")

        # check for headers
        if self.headers:
            kwargs["headers"] = self.headers

        # clean params
        if "params" in kwargs:
            kwargs["params"] = self._clean_params(kwargs["params"].copy())

        # execute request
        match type:
            case RequestType.GET.value:
                async with self._session.get(url, *args, **kwargs) as resp:
                    response = await self._to_requests_response(resp)
            case RequestType.POST.value:
                async with self._session.post(url, *args, **kwargs) as resp:
                    response = await self._to_requests_response(resp)
            case _:
                raise RequestTypeNotSupported(f"Request '{type}' not supported.")

        # check response
        match response.status_code:
            case 401:
                raise AuthorizationAPIKeyError("Check API Key")
            case _:
                response.raise_for_status()
                return response

    async def _to_requests_response(self, response: aiohttp.ClientResponse) -> requests.Response:
        """
            This internal function is used to convert a response obtained 
            from `aiohttp` to the one from `requests` library.

            Parameters:
                response: response from `aiohttp`.

            Return:
                response from `requests`.
        """
        _response = requests.Response()
        _response.url = str(response.url)
        _response.headers = requests.structures.CaseInsensitiveDict(response.headers)
        _response.status_code = response.status
        _response.reason = response.reason if response.reason else "Not Found"
        _response.encoding = response.get_encoding()
        _response._content = await response.read()

        return _response

    def _clean_params(self, params: dict[str, Any]) -> dict[str, Any]:
        """
            The `aiohttp` requires to remove the keys with `None` value. 
            This function takes as input the original `params` and returns a new 
            object removed from `None`keys.

            arameters:
                params: original params.

            Return:
                new params removed from the keys with `None`valiues.
        """
        return {key: value for key, value in params.items() if value is not None}