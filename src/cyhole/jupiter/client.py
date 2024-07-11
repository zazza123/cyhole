from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast

from ..core.client import APIClient, AsyncAPIClient
from ..jupiter.schema import GetPriceResponse

if TYPE_CHECKING:
    from ..jupiter.interaction import Jupiter

class JupiterClient(APIClient):
    """
        Client used for synchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's get_price for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return self._interaction._get_price(True, address, vs_address)

class JupiterAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    async def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's get_price for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return await self._interaction._get_price(False, address, vs_address)