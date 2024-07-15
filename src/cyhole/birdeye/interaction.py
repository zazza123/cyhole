import os
import requests
from typing import Any
from datetime import datetime

from ..core.api import APICaller
from ..core.param import RequestType
from ..core.interaction import Interaction
from ..core.exception import MissingAPIKeyError, AuthorizationAPIKeyError
from ..birdeye.client import BirdeyeClient, BirdeyeAsyncClient
from ..birdeye.exception import BirdeyeTimeRangeError, BirdeyeAuthorisationError
from ..birdeye.param import (
    BirdeyeChain,
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTimeFrame,
    BirdeyeTradeType,
    BirdeyeAddressType
)
from ..birdeye.schema import (
    GetTokenListResponse,
    GetTokenSecurityResponse,
    GetTokenCreationInfoResponse,
    GetTokenOverviewResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetHistoryResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse
)

class Birdeye(Interaction):
    """
        Class used to connect [https://birdeye.so](https://birdeye.so) API.
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check [https://docs.birdeye.so](https://docs.birdeye.so) for all the details on the available endpoints.

        !!! info
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from ENV variable **BIRDEYE_API_KEY**.

        Parameters:
            api_key: specify the API key to use for the connection.

        **Example**

        ```python
        from cyhole.birdeye import Birdeye

        # get current token list on Solana
        birdeye = Birdeye()
        token_list = Birdeye().get_token_list()
        ```

        Raises:
            MissingAPIKeyError: if no API Key was available during the object creation.
    """
    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("BIRDEYE_API_KEY")
        if self.api_key is None:
            raise MissingAPIKeyError("no API key is provided during object's creation.")

        # header setup
        header = {
            "X-API-KEY": self.api_key
        }
        super().__init__(header)

        # clients
        self.client = BirdeyeClient(self)
        self.async_client = BirdeyeAsyncClient(self)

        # API urls
        self.url_api_public = "https://public-api.birdeye.so/defi/"
        self.url_api_private = "https://public-api.birdeye.so/defi/"
        self.url_api_private_wallet = "https://public-api.birdeye.so/v1/wallet"
        return