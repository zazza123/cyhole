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

        **Example**
    """

    def __init__(self, headers: Any | None = None) -> None:
        super().__init__(headers)

        # clients
        self.client = SolscanClient(self)
        self.async_client = SolscanAsyncClient(self)

        # API urls
        return