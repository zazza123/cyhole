from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient
from ...solscan.v1.schema import (
    GetAccountTokensResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeAccountsResponse,
    GetAccountSplTransfersResponse,
    GetAccountSolTransfersResponse,
    GetAccountExportTransactionsResponse,
    GetAccountExportRewardsResponse,
    GetAccountDetailResponse
)

if TYPE_CHECKING:
    from ...solscan.v1.interaction import Solscan

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    def get_account_tokens(self, account: str) -> GetAccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_tokens`][cyhole.solscan.interaction.v1.Solscan._get_account_tokens].
        """
        return self._interaction._get_account_tokens(True, account)

    def get_account_transactions(self, account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.interaction.v1.Solscan._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, before_hash, limit)

    def get_account_stake_accounts(self, account: str) -> GetAccountStakeAccountsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake_accounts`][cyhole.solscan.interaction.v1.Solscan._get_account_stake_accounts].
        """
        return self._interaction._get_account_stake_accounts(True, account)

    def get_account_spl_transfers(
        self,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSplTransfersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account SplTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-splTransfers)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_spl_transfers`][cyhole.solscan.interaction.v1.Solscan._get_account_spl_transfers].
        """
        return self._interaction._get_account_spl_transfers(True, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    def get_account_sol_transfers(
        self,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSolTransfersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account SolTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-solTransfers)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_sol_transfers`][cyhole.solscan.interaction.v1.Solscan._get_account_sol_transfers].
        """
        return self._interaction._get_account_sol_transfers(True, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    def get_account_export_transactions(self, account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_transactions`][cyhole.solscan.interaction.v1.Solscan._get_account_export_transactions].
        """
        return self._interaction._get_account_export_transactions(True, account, export_type, dt_from, dt_to)

    def get_account_export_rewards(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Rewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_rewards`][cyhole.solscan.interaction.v1.Solscan._get_account_export_rewards].
        """
        return self._interaction._get_account_export_rewards(True, account, dt_from, dt_to)

    def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.interaction.v1.Solscan._get_account_detail].
        """
        return self._interaction._get_account_detail(True, account)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def get_account_tokens(self, account: str) -> GetAccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_tokens`][cyhole.solscan.interaction.v1.Solscan._get_account_tokens].
        """
        return await self._interaction._get_account_tokens(False, account)

    async def get_account_transactions(self, account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.interaction.v1.Solscan._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, before_hash, limit)

    async def get_account_stake_accounts(self, account: str) -> GetAccountStakeAccountsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake_accounts`][cyhole.solscan.interaction.v1.Solscan._get_account_stake_accounts].
        """
        return await self._interaction._get_account_stake_accounts(False, account)

    async def get_account_spl_transfers(
        self,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSplTransfersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account SplTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-splTransfers)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_spl_transfers`][cyhole.solscan.interaction.v1.Solscan._get_account_spl_transfers].
        """
        return await self._interaction._get_account_spl_transfers(False, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    async def get_account_sol_transfers(
        self,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSolTransfersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account SolTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-solTransfers)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_sol_transfers`][cyhole.solscan.interaction.v1.Solscan._get_account_sol_transfers].
        """
        return await self._interaction._get_account_sol_transfers(False, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    async def get_account_export_transactions(self, account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_transactions`][cyhole.solscan.interaction.v1.Solscan._get_account_export_transactions].
        """
        return await self._interaction._get_account_export_transactions(False, account, export_type, dt_from, dt_to)

    async def get_account_export_rewards(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Rewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_rewards`][cyhole.solscan.interaction.v1.Solscan._get_account_export_rewards].
        """
        return await self._interaction._get_account_export_rewards(False, account, dt_from, dt_to)

    async def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.interaction.v1.Solscan._get_account_detail].
        """
        return await self._interaction._get_account_detail(False, account)