import os
from requests.exceptions import HTTPError
from typing import Any, Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..solscan.client import SolscanClient, SolscanAsyncClient

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
        return