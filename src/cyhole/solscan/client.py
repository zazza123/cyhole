from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast

from ..core.client import APIClient, AsyncAPIClient

if TYPE_CHECKING:
    from ..solscan.interaction import Solscan

class SolscanV1Client(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

class SolscanV2Client(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

        # set API versions clients
        self.v1 = SolscanV1Client(self._interaction, headers = {"token": self._interaction.api_key_v1})
        self.v2 = SolscanV2Client(self._interaction, headers = {"token": self._interaction.api_key_v2})

class SolscanV1AsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

class SolscanV2AsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast(Solscan, self._interaction)

        # set API versions clients
        self.v1 = SolscanV1AsyncClient(self._interaction, headers = {"token": self._interaction.api_key_v1})
        self.v2 = SolscanV2AsyncClient(self._interaction, headers = {"token": self._interaction.api_key_v2})