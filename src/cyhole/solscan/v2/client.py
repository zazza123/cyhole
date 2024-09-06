from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient
from ...solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse
)

if TYPE_CHECKING:
    from ...solscan.v2.interaction import Solscan

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.interaction.v2.Solscan._get_account_transfers].
        """
        return self._interaction._get_account_transfers(True, account, params)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.interaction.v2.Solscan._get_account_transfers].
        """
        return await self._interaction._get_account_transfers(False, account, params)