from __future__ import annotations
from datetime import datetime
from requests import Response, HTTPError
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient
from ...solscan.v1.param import SolscanSort, SolscanOrder
from ...solscan.v1.schema import (
    GetAccountTokensResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeAccountsResponse,
    GetAccountSplTransfersResponse,
    GetAccountSolTransfersResponse,
    GetAccountExportTransactionsResponse,
    GetAccountExportRewardsResponse,
    GetAccountDetailResponse,
    GetTokenHoldersResponse,
    GetTokenMetaResponse,
    GetTokenTransferResponse,
    GetTokenListResponse,
    GetMarketTokenDetailResponse,
    GetTransactionLastResponse,
    GetTransactionDetailResponse,
    GetBlockLastResponse,
    GetBlockDetailResponse,
    GetBlockTransactionsResponse
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

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> Response:
        # overide function to manage client specific exceptions
        try:
            return super().api(type, url, *args, **kwargs)
        except HTTPError as e:
            raise self._interaction._raise(e)

    def get_account_tokens(self, account: str) -> GetAccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_tokens`][cyhole.solscan.v1.interaction.Solscan._get_account_tokens].
        """
        return self._interaction._get_account_tokens(True, account)

    def get_account_transactions(self, account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.v1.interaction.Solscan._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, before_hash, limit)

    def get_account_stake_accounts(self, account: str) -> GetAccountStakeAccountsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake_accounts`][cyhole.solscan.v1.interaction.Solscan._get_account_stake_accounts].
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
            All the API endopint details are available on [`Solscan._get_account_spl_transfers`][cyhole.solscan.v1.interaction.Solscan._get_account_spl_transfers].
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
            All the API endopint details are available on [`Solscan._get_account_sol_transfers`][cyhole.solscan.v1.interaction.Solscan._get_account_sol_transfers].
        """
        return self._interaction._get_account_sol_transfers(True, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    def get_account_export_transactions(self, account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_transactions`][cyhole.solscan.v1.interaction.Solscan._get_account_export_transactions].
        """
        return self._interaction._get_account_export_transactions(True, account, export_type, dt_from, dt_to)

    def get_account_export_rewards(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Rewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_rewards`][cyhole.solscan.v1.interaction.Solscan._get_account_export_rewards].
        """
        return self._interaction._get_account_export_rewards(True, account, dt_from, dt_to)

    def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.v1.interaction.Solscan._get_account_detail].
        """
        return self._interaction._get_account_detail(True, account)

    def get_token_holders(
        self,
        token: str,
        limit: int = 10,
        offset: int | None = None,
        amount_from: int | None = None,
        amount_to: int | None = None
    ) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-holders)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.v1.interaction.Solscan._get_token_holders].
        """
        return self._interaction._get_token_holders(True, token, limit, offset, amount_from, amount_to)

    def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-meta)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.v1.interaction.Solscan._get_token_meta].
        """
        return self._interaction._get_token_meta(True, token)

    def get_token_transfer(self, token: str, account: str | None = None, limit: int = 10, offset: int | None = None) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.v1.interaction.Solscan._get_token_transfer].
        """
        return self._interaction._get_token_transfer(True, token, account, limit, offset)

    def get_token_list(
        self,
        sort_by: str = SolscanSort.MARKET_CAP.value,
        order_by: str = SolscanOrder.DESCENDING.value,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenListResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.v1.interaction.Solscan._get_token_list].
        """
        return self._interaction._get_token_list(True, sort_by, order_by, limit, offset)

    def get_market_token_detail(self, token: str, limit: int = 10, offset: int | None = None) -> GetMarketTokenDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_market_token_detail`][cyhole.solscan.v1.interaction.Solscan._get_market_token_detail].
        """
        return self._interaction._get_market_token_detail(True, token, limit, offset)

    def get_transaction_last(self, limit: int = 10) -> GetTransactionLastResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-last)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_last`][cyhole.solscan.v1.interaction.Solscan._get_transaction_last].
        """
        return self._interaction._get_transaction_last(True, limit)

    def get_transaction_detail(self, transaction_id: str) -> GetTransactionDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Transaction Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_detail`][cyhole.solscan.v1.interaction.Solscan._get_transaction_detail].
        """
        return self._interaction._get_transaction_detail(True, transaction_id)

    def get_block_last(self, limit: int = 10) -> GetBlockLastResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-last)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_last`][cyhole.solscan.v1.interaction.Solscan._get_block_last].
        """
        return self._interaction._get_block_last(True, limit)

    def get_block_detail(self, block_id: int) -> GetBlockDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_detail`][cyhole.solscan.v1.interaction.Solscan._get_block_detail].
        """
        return self._interaction._get_block_detail(True, block_id)

    def get_block_transactions(self, block_id: int, limit: int = 10, offset: int | None = None) -> GetBlockTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_transactions`][cyhole.solscan.v1.interaction.Solscan._get_block_transactions].
        """
        return self._interaction._get_block_transactions(True, block_id, limit, offset)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V1** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> Response:
        # overide function to manage client specific exceptions
        try:
            return await super().api(type, url, *args, **kwargs)
        except HTTPError as e:
            raise self._interaction._raise(e)

    async def get_account_tokens(self, account: str) -> GetAccountTokensResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_tokens`][cyhole.solscan.v1.interaction.Solscan._get_account_tokens].
        """
        return await self._interaction._get_account_tokens(False, account)

    async def get_account_transactions(self, account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.v1.interaction.Solscan._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, before_hash, limit)

    async def get_account_stake_accounts(self, account: str) -> GetAccountStakeAccountsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake_accounts`][cyhole.solscan.v1.interaction.Solscan._get_account_stake_accounts].
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
            All the API endopint details are available on [`Solscan._get_account_spl_transfers`][cyhole.solscan.v1.interaction.Solscan._get_account_spl_transfers].
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
            All the API endopint details are available on [`Solscan._get_account_sol_transfers`][cyhole.solscan.v1.interaction.Solscan._get_account_sol_transfers].
        """
        return await self._interaction._get_account_sol_transfers(False, account, utc_from_unix_time, utc_to_unix_time, limit, offset)

    async def get_account_export_transactions(self, account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_transactions`][cyhole.solscan.v1.interaction.Solscan._get_account_export_transactions].
        """
        return await self._interaction._get_account_export_transactions(False, account, export_type, dt_from, dt_to)

    async def get_account_export_rewards(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Export Rewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_export_rewards`][cyhole.solscan.v1.interaction.Solscan._get_account_export_rewards].
        """
        return await self._interaction._get_account_export_rewards(False, account, dt_from, dt_to)

    async def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.v1.interaction.Solscan._get_account_detail].
        """
        return await self._interaction._get_account_detail(False, account)

    async def get_token_holders(
        self,
        token: str,
        limit: int = 10,
        offset: int | None = None,
        amount_from: int | None = None,
        amount_to: int | None = None
    ) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-holders)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.v1.interaction.Solscan._get_token_holders].
        """
        return await self._interaction._get_token_holders(False, token, limit, offset, amount_from, amount_to)

    async def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-meta)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.v1.interaction.Solscan._get_token_meta].
        """
        return await self._interaction._get_token_meta(False, token)

    async def get_token_transfer(self, token: str, account: str | None = None, limit: int = 10, offset: int | None = None) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.v1.interaction.Solscan._get_token_transfer].
        """
        return await self._interaction._get_token_transfer(False, token, account, limit, offset)

    async def get_token_list(
        self,
        sort_by: str = SolscanSort.MARKET_CAP.value,
        order_by: str = SolscanOrder.DESCENDING.value,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenListResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.v1.interaction.Solscan._get_token_list].
        """
        return await self._interaction._get_token_list(False, sort_by, order_by, limit, offset)

    async def get_market_token_detail(self, token: str, limit: int = 10, offset: int | None = None) -> GetMarketTokenDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_market_token_detail`][cyhole.solscan.v1.interaction.Solscan._get_market_token_detail].
        """
        return await self._interaction._get_market_token_detail(False, token, limit, offset)

    async def get_transaction_last(self, limit: int = 10) -> GetTransactionLastResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-last)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_last`][cyhole.solscan.v1.interaction.Solscan._get_transaction_last].
        """
        return await self._interaction._get_transaction_last(False, limit)

    async def get_transaction_detail(self, transaction_id: str) -> GetTransactionDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Transaction Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_detail`][cyhole.solscan.v1.interaction.Solscan._get_transaction_detail].
        """
        return await self._interaction._get_transaction_detail(False, transaction_id)

    async def get_block_last(self, limit: int = 10) -> GetBlockLastResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-last)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_last`][cyhole.solscan.v1.interaction.Solscan._get_block_last].
        """
        return await self._interaction._get_block_last(False, limit)

    async def get_block_detail(self, block_id: int) -> GetBlockDetailResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_detail`][cyhole.solscan.v1.interaction.Solscan._get_block_detail].
        """
        return await self._interaction._get_block_detail(False, block_id)

    async def get_block_transactions(self, block_id: int, limit: int = 10, offset: int | None = None) -> GetBlockTransactionsResponse:
        """
            Call the Solscan's **V1** API endpoint GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_transactions`][cyhole.solscan.v1.interaction.Solscan._get_block_transactions].
        """
        return await self._interaction._get_block_transactions(False, block_id, limit, offset)