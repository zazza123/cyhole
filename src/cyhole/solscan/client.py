from __future__ import annotations
from typing import TYPE_CHECKING, Any, cast

from ..core.client import APIClient, AsyncAPIClient
from ..solscan.schema import (
    GetV1AccountTokensResponse
)

if TYPE_CHECKING:
    from ..solscan.interaction import Solscan

# **************************
# * V1 API                 *
# **************************

class SolscanV1Client(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    def get_v1_account_tokens(self, account: str) -> GetV1AccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_v1_account_tokens`][cyhole.solscan.interaction.Solscan._get_v1_account_tokens].
        """
        return self._interaction._get_v1_account_tokens(True, account)

class SolscanV1AsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def get_v1_account_tokens(self, account: str) -> GetV1AccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_v1_account_tokens`][cyhole.solscan.interaction.Solscan._get_v1_account_tokens].
        """
        return await self._interaction._get_v1_account_tokens(False, account)

# **************************
# * V2 API                 *
# **************************

class SolscanV2Client(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

class SolscanV2AsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

# **************************
# * Clients                *
# **************************

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

        # set API versions clients
        self.v1 = SolscanV1Client(self._interaction, headers = {"token": self._interaction.api_key_v1})
        self.v2 = SolscanV2Client(self._interaction, headers = {"token": self._interaction.api_key_v2})

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

        # set API versions clients
        self.v1 = SolscanV1AsyncClient(self._interaction, headers = {"token": self._interaction.api_key_v1})
        self.v2 = SolscanV2AsyncClient(self._interaction, headers = {"token": self._interaction.api_key_v2})