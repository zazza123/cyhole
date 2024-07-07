import requests
from typing import Any

from ..core.param import RequestType
from ..core.exception import RequestTypeNotSupported, AuthorizationAPIKeyError

class APICaller:
    """
        Class used to manage all the REST calls to an external API by using `requests` module. 
        Use this class as middlelayer to manage all the requests to an external API. 
        By default, all new connectors should inherit from this class.

        During the creation of the object is possible to specify some global configurations.

        Parameters:
            header: header used globally in all API requests.
    """
    def __init__(self, header: Any | None = None) -> None:
        self.header = header
        return

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        """
            Function in charge to execute a request to an API endpoint.

            Parameters:
                type: request's type ([`RequestType`][cyhole.core.param.RequestType]).
                url: API endpoint.
                args: additional input parameters to provided.
                kwargs: additional input parameters to provided.

            Returns:
                The response object from `request`library.

            Raises:
                RequestTypeNotSupported: if the request type is not a valid value of [`RequestType`][cyhole.core.param.RequestType].
                AuthorizationAPIKeyError: if the response return a 401 code.
        """
        # check for headers
        headers = self.header
        if "headers" in kwargs:
            headers = kwargs["headers"]
            kwargs.pop("headers")

        # execute request
        match type:
            case RequestType.GET.value:
                response = requests.get(url, headers = headers, *args, **kwargs)
            case RequestType.POST.value:
                response = requests.post(url, headers = headers, *args, **kwargs)
            case _:
                raise RequestTypeNotSupported(f"Request '{type}' not supported.")

        # check response
        match response.status_code:
            case 401:
                raise AuthorizationAPIKeyError("Check API Key")
            case _:
                response.raise_for_status()
                return response