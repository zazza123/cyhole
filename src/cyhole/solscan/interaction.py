import os
from typing import Any, Coroutine, Literal, Type, overload, cast

from ..core.param import RequestType
from ..core.interaction import Interaction, ResponseModel
from ..solscan.client import SolscanClient, SolscanAsyncClient
from ..solscan.schema import (
    GetV1AccountTokensResponse
)

class Solscan(Interaction):
    """
        Class used to connect [Solscan](https://solscan.io) API, one of them most popular Solana chain explorer. 
        To have access Solscan Pro API (v1 or v2) is required to have a valid API key.

        Check [API Documentation](https://pro-api.solscan.io/pro-api-docs/v2.0) for all the details on the available endpoints.

        Solscan API is currently divided into two versions:

        - **v1** - the first and classic version of the Pro API.
        - **v2** - a new and improved version of the Pro API, with more endpoints and features.
            This version is under development and may have some changes.

        Each client (`sync` and `async`) has two attributes `v1` and `v2` that represent the API 
        versions; in this way, you can access the endpoints of each version separately. 

        !!! info
            Both versions require different API keys for access. If the API keys are not 
            provided during the object creation, then they are automatically retrieved from 
            environment variables `SOLSCAN_API_V1_KEY` and `SOLSCAN_API_V2_KEY` respectively.

        Parameters:
            api_key_v1: specifies the API key for Solscan Pro API v1.
            api_key_v2: specifies the API key for Solscan Pro API v2.

        **Example**
    """

    def __init__(self, api_key_v1: str | None = None, api_key_v2: str | None = None) -> None:

        # set APIs
        self.api_key_v1 = api_key_v1 if api_key_v1 is not None else os.environ.get("SOLSCAN_API_V1_KEY")
        self.api_key_v2 = api_key_v2 if api_key_v2 is not None else os.environ.get("SOLSCAN_API_V2_KEY")

        super().__init__()

        # clients
        self.client = SolscanClient(self)
        self.async_client = SolscanAsyncClient(self)

        # API urls
        self.pro_v1_url = "https://pro-api.solscan.io/v1.0/"
        self.pro_v2_url = "https://pro-api.solscan.io/v2.0/"

        # private attributes
        self._name = "Solscan"
        self._description = "Interact with Solscan API"
        self._api_versions = ["v1", "v2"]
        return

    def __str__(self) -> str:
        return self._name

    def api_return_model(
        self, 
        sync: bool,
        type: str,
        url: str,
        response_model: Type[ResponseModel],
        *args: tuple,
        **kwargs: Any
    ) -> ResponseModel | Coroutine[None, None, ResponseModel]:

        # check API version
        if "api_version" not in kwargs:
            raise ValueError("The 'api_version' parameter is required to specify the API version.")

        api_version = cast(str, kwargs["api_version"])
        if api_version not in self._api_versions:
            raise ValueError(f"The API version '{api_version}' not admitted. Admitted versions: {self._api_versions}")

        # remove api_version from kwargs
        kwargs.pop("api_version")

        # set clients
        client = self.client
        async_client = self.async_client

        match api_version:
            case "v1":
                client = self.client.v1
                async_client = self.async_client.v1
            case "v2":
                client = self.client.v2
                async_client = self.async_client.v2

        # execute request
        if sync:
            content_raw = client.api(type, url, *args, **kwargs)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                content_raw = await async_client.api(type, url, *args, **kwargs)
                return response_model(**content_raw.json())
            return async_request()

    # **************************
    # * V1 API                 *
    # **************************
    @overload
    def _get_v1_account_tokens(self, sync: Literal[True], account: str) -> GetV1AccountTokensResponse: ...

    @overload
    def _get_v1_account_tokens(self, sync: Literal[False], account: str) -> Coroutine[None, None, GetV1AccountTokensResponse]: ...

    def _get_v1_account_tokens(self, sync: bool, account: str) -> GetV1AccountTokensResponse | Coroutine[None, None, GetV1AccountTokensResponse]:
        """
            This function refers to the GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint, 
            and it is used to get tokens balances of an account.

            Parameters:
                account: The account address.

            Returns:
                List of tokens balances of the account.
        """
        # set params
        url = self.pro_v1_url + f"account/tokens"
        api_params = {
            "account": account
        }

        # execute request
        if sync:
            content_raw = self.client.v1.api(RequestType.GET.value, url, params = api_params)
            return GetV1AccountTokensResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.v1.api(RequestType.GET.value, url, params = api_params)
                return GetV1AccountTokensResponse(tokens = content_raw.json())
            return async_request()

    # **************************
    # * V2 API                 *
    # **************************