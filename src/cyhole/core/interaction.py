from typing import Any, TypeVar, Type, Coroutine
from pydantic import BaseModel

from ..core.client import APIClient, AsyncAPIClient

ResponseModel = TypeVar('ResponseModel', bound = BaseModel)

class Interaction:
    """
        This class is the building block for a new integration of an external API in `cyhole` library, 
        and every new external API **must** be identified by a class that inherits from this class.

        Inside an `Interaction` there are two attributes identifying the clients responsable to 
        perform the API calls:

        - `client`: object used for **synchronous** logic.
        - `async_client`: object used for **asynchronous** logic.

        During the creation of the object is possible to specify some global configurations.

        Parameters:
            headers: headers used globally in all API requests.
    """
    def __init__(self, headers: Any | None = None) -> None:
        self.headers = headers

        # clients
        self.client = APIClient(self, headers = self.headers)
        self.async_client = AsyncAPIClient(self, headers = self.headers)

        return

    def api_return_model(self, sync: bool, type: str, url: str, response_model: Type[ResponseModel], *args: tuple, **kwargs: Any) -> ResponseModel | Coroutine[None, None, ResponseModel]:
        """
            This function is used to execute a request to the API by forwarding the call to the 
            corresponding client (synchronous or asynchronous) according to the `sync` parameter.

            This function is used to avoid code duplication in the methods of the `Interaction` classes, 
            and it assumes that the response of the API request is a JSON object that can be parsed into 
            a `pydantic.BaseModel` model.

            Parameters:
                sync: boolean to define if the request is synchronous or asynchronous.
                type: request's type ([`RequestType`][cyhole.core.param.RequestType]).
                url: the URL of the API endpoint.
                response_model: the `pydantic.BaseModel` model used to parse the response.
                args: the positional arguments to be passed to the API request.
                kwargs: the named arguments to be passed to the API request.

            Returns:
                The response of the API request. If the request is synchronous, the response is a 
                `pydantic.BaseModel` model. If the request is asynchronous, the response is a coroutine 
                that will return a `pydantic.BaseModel` model.
        """
        if sync:
            content_raw = self.client.api(type, url, *args, **kwargs)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(type, url, *args, **kwargs)
                return response_model(**content_raw.json())
            return async_request()