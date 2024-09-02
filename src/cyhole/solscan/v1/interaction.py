import os
from datetime import datetime
from typing import Coroutine, Literal, overload

from ...core.param import RequestType
from ...core.interaction import Interaction
from ...core.exception import MissingAPIKeyError
from ...solscan.v1.param import SolscanExportType
from ...solscan.v1.client import SolscanClient, SolscanAsyncClient
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

class Solscan(Interaction):
    """
        Class used to connect only [Solscan](https://solscan.io) **V1** API, one of them most popular Solana chain explorer. 
        To have access Solscan Pro API is required to have a valid API key.

        Check [API Documentation](https://pro-api.solscan.io/pro-api-docs/v2.0) for all the details on the available endpoints.

        Solscan API is currently divided into two versions:

        - **v1** - the first and classic version of the Pro API.
        - **v2** - a new and improved version of the Pro API, with more endpoints and features.
            *This version is under development and may have some changes*.

        !!! info
            This `Interaction` is dedicated to the Solscan Pro API v1.0.
            Use `cyhole.solscan.SolscanV2` or `cyhole.solscan.v2.Solscan` for the Solscan Pro API v2.0.
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from environment variable `SOLSCAN_API_V1_KEY`.

        Parameters:
            api_key: specifies the API key for Solscan Pro API v1.

        **Example**
    """

    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("SOLSCAN_API_V1_KEY")
        if self.api_key is None:
            raise MissingAPIKeyError("no API key is provided during object's creation.")

        # headers setup
        headers = {
            "token": self.api_key
        }
        super().__init__(headers)
        self.headers: dict[str, str]

        # clients
        self.client = SolscanClient(self, headers = self.headers)
        self.async_client = SolscanAsyncClient(self, headers = self.headers)

        # API urls
        self.base_url = "https://pro-api.solscan.io/v1.0/"

        # private attributes
        self._name = "Solscan V1 API"
        self._description = "Interact with Solscan API V1"
        return

    def __str__(self) -> str:
        return self._name

    @overload
    def _get_account_tokens(self, sync: Literal[True], account: str) -> GetAccountTokensResponse: ...

    @overload
    def _get_account_tokens(self, sync: Literal[False], account: str) -> Coroutine[None, None, GetAccountTokensResponse]: ...

    def _get_account_tokens(self, sync: bool, account: str) -> GetAccountTokensResponse | Coroutine[None, None, GetAccountTokensResponse]:
        """
            This function refers to the GET **[Account Tokens](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-tokens)** of **V1** API endpoint, 
            and it is used to get tokens balances of an account.

            Parameters:
                account: The account address.

            Returns:
                List of tokens balances of the account.
        """
        # set params
        url = self.base_url + f"account/tokens"
        api_params = {
            "account": account
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTokensResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTokensResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_account_transactions(self, sync: Literal[True], account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse: ...

    @overload
    def _get_account_transactions(self, sync: Literal[False], account: str, before_hash: str | None = None, limit: int | None = None) -> Coroutine[None, None, GetAccountTransactionsResponse]: ...

    def _get_account_transactions(self, sync: bool, account: str, before_hash: str | None = None, limit: int | None = None) -> GetAccountTransactionsResponse | Coroutine[None, None, GetAccountTransactionsResponse]:
        """
            This function refers to the GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-transactions)** of **V1** API endpoint, 
            and it is used to get transactions of an account.

            Parameters:
                account: The account address.
                before_hash: The transaction hash to get transactions before it.
                limit: The number of transactions to get; maximum is 50.

            Returns:
                List of transactions of the account.
        """
        # set params
        url = self.base_url + f"account/transactions"
        api_params = {
            "account": account,
            "beforeHash": before_hash,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTransactionsResponse(transactions = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTransactionsResponse(transactions = content_raw.json())
            return async_request()

    @overload
    def _get_account_stake_accounts(self, sync: Literal[True], account: str) -> GetAccountStakeAccountsResponse: ...

    @overload
    def _get_account_stake_accounts(self, sync: Literal[False], account: str) -> Coroutine[None, None, GetAccountStakeAccountsResponse]: ...

    def _get_account_stake_accounts(self, sync: bool, account: str) -> GetAccountStakeAccountsResponse | Coroutine[None, None, GetAccountStakeAccountsResponse]:
        """
            This function refers to the GET **[Account StakeAccounts](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-stakeAccounts)** of **V1** API endpoint, 
            and it is used to get stake accounts of an account.

            Parameters:
                account: The account address.

            Returns:
                List of stake accounts of the account.
        """
        # set params
        url = self.base_url + f"account/stakeAccounts"
        api_params = {
            "account": account
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountStakeAccountsResponse(stake_accounts = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountStakeAccountsResponse(stake_accounts = content_raw.json())
            return async_request()

    @overload
    def _get_account_spl_transfers(
        self,
        sync: Literal[True],
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSplTransfersResponse: ...

    @overload
    def _get_account_spl_transfers(
        self,
        sync: Literal[False],
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> Coroutine[None, None, GetAccountSplTransfersResponse]: ...

    def _get_account_spl_transfers(
        self,
        sync: bool,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSplTransfersResponse | Coroutine[None, None, GetAccountSplTransfersResponse]:
        """
            This function refers to the GET **[Account SplTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-splTransfers)** of **V1** API endpoint, 
            and it is used to get spl transfers of an account.

            Parameters:
                account: The account address.
                utc_from_unix_time: The start time in unix time.
                utc_to_unix_time: The end time in unix time.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                List of spl transfers of the account.
        """
        # set params
        url = self.base_url + f"account/splTransfers"
        api_params = {
            "account": account,
            "fromTime": utc_from_unix_time,
            "toTime": utc_to_unix_time,
            "limit": limit,
            "offset": offset
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountSplTransfersResponse,
            params = api_params
        )

    @overload
    def _get_account_sol_transfers(
        self,
        sync: Literal[True],
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSolTransfersResponse: ...

    @overload
    def _get_account_sol_transfers(
        self,
        sync: Literal[False],
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> Coroutine[None, None, GetAccountSolTransfersResponse]: ...

    def _get_account_sol_transfers(
        self,
        sync: bool,
        account: str,
        utc_from_unix_time: int | None = None,
        utc_to_unix_time: int | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetAccountSolTransfersResponse | Coroutine[None, None, GetAccountSolTransfersResponse]:
        """
            This function refers to the GET **[Account SolTransfers](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-solTransfers)** of **V1** API endpoint, 
            and it is used to get sol transfers of an account.

            Parameters:
                account: The account address.
                utc_from_unix_time: The start time in unix time.
                utc_to_unix_time: The end time in unix time.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                List of sol transfers of the account.
        """
        # set params
        url = self.base_url + f"account/solTransfers"
        api_params = {
            "account": account,
            "fromTime": utc_from_unix_time,
            "toTime": utc_to_unix_time,
            "limit": limit,
            "offset": offset
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountSolTransfersResponse,
            params = api_params
        )

    @overload
    def _get_account_export_transactions(self, sync: Literal[True], account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse: ...

    @overload
    def _get_account_export_transactions(self, sync: Literal[False], account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> Coroutine[None, None, GetAccountExportTransactionsResponse]: ...

    def _get_account_export_transactions(self, sync: bool, account: str, export_type: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportTransactionsResponse | Coroutine[None, None, GetAccountExportTransactionsResponse]:
        """
            This function refers to the GET **[Account Export Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportTransactions)** of **V1** API endpoint, 
            and it is used to get export transactions of an account in CSV format.

            !!! info
                The limit of the export transactions is 5000. 
                Moreover, it is possible to execute the export transactions **only** for 1 time for every minute.

            Parameters:
                account: The account address.
                export_type: The export type.
                    The supported types are available on [`SolscanExportType`][cyhole.solscan.v1.param.SolscanExportType].
                dt_from: The start time.
                dt_to: The end time.

            Returns:
                List of export transactions of the account.
        """
        # check param consistency
        SolscanExportType.check(export_type)

        # set params
        url = self.base_url + f"account/exportTransactions"
        api_params = {
            "account": account,
            "type": export_type,
            "fromTime": int(dt_from.timestamp()),
            "toTime": int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountExportTransactionsResponse(csv = content_raw.text)
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountExportTransactionsResponse(csv = content_raw.text)
            return async_request()

    @overload
    def _get_account_export_rewards(self, sync: Literal[True], account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse: ...

    @overload
    def _get_account_export_rewards(self, sync: Literal[False], account: str, dt_from: datetime, dt_to: datetime) -> Coroutine[None, None, GetAccountExportRewardsResponse]: ...

    def _get_account_export_rewards(self, sync: bool, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountExportRewardsResponse | Coroutine[None, None, GetAccountExportRewardsResponse]:
        """
            This function refers to the GET **[Account Export Rewards](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-exportRewards)** of **V1** API endpoint, 
            and it is used to get export rewards of an account in CSV format.

            !!! info
                The limit of the export rewards is 5000 for request. 
                Moreover, it is possible to execute the request **only** 1 time for every minute.

            Parameters:
                account: The account address.
                dt_from: The start time.
                dt_to: The end time.

            Returns:
                List of export rewards of the account.
        """

        # set params
        url = self.base_url + f"account/exportRewards"
        api_params = {
            "account": account,
            "fromTime": int(dt_from.timestamp()),
            "toTime": int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountExportRewardsResponse(csv = content_raw.text)
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountExportRewardsResponse(csv = content_raw.text)
            return async_request()

    @overload
    def _get_account_detail(self, sync: Literal[True], account: str) -> GetAccountDetailResponse: ...

    @overload
    def _get_account_detail(self, sync: Literal[False], account: str) -> Coroutine[None, None, GetAccountDetailResponse]: ...

    def _get_account_detail(self, sync: bool, account: str) -> GetAccountDetailResponse | Coroutine[None, None, GetAccountDetailResponse]:
        """
            This function refers to the GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/account-detail)** of **V1** API endpoint, 
            and it is used to get details of an account.

            Parameters:
                account: The account address.

            Returns:
                Details of the account.
        """
        # set params
        url = self.base_url + f"account/{account}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountDetailResponse
        )