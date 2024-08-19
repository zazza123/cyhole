from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..solana_fm.schema import (
    GetAccountTransactionsParam,
    GetAccountTransactionsResponse
)

if TYPE_CHECKING:
    from ..solana_fm.interaction import SolanaFM

class SolanaFMClient(APIClient):
    """
        Client used for synchronous API calls for `SolanaFM` interaction.
    """

    def __init__(self, interaction: SolanaFM, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: SolanaFM = self._interaction

    def get_account_transactions(self, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, params)

class SolanaFMAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `SolanaFM` interaction.
    """

    def __init__(self, interaction: SolanaFM, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: SolanaFM = self._interaction

    async def get_account_transactions(self, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, params)