from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient

if TYPE_CHECKING:
    from ...solscan.v2.interaction import Solscan

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)