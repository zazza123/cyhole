from __future__ import annotations
import requests
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..core.exception import AuthorizationAPIKeyError
from ..birdeye.exception import BirdeyeAuthorisationError

if TYPE_CHECKING:
    from ..birdeye.interaction import Birdeye

class BirdeyeClient(APIClient):
    """
        Client used for synchronous API calls for `Birdeye` interaction.
    """

    def __init__(self, interaction: Birdeye, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Birdeye = self._interaction

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        # overide function to manage client specific exceptions
        try:
            return super().api(type, url, *args, **kwargs)
        except AuthorizationAPIKeyError:
            raise BirdeyeAuthorisationError

class BirdeyeAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Birdeye` interaction.
    """

    def __init__(self, interaction: Birdeye, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Birdeye = self._interaction

    async def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        # overide function to manage client specific exceptions
        try:
            return await super().api(type, url, *args, **kwargs)
        except AuthorizationAPIKeyError:
            raise BirdeyeAuthorisationError