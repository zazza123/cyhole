import os
from datetime import datetime
from typing import Coroutine, Literal, overload

from ...core.param import RequestType
from ...core.interaction import Interaction
from ...core.exception import MissingAPIKeyError
from ...solscan.v2.client import SolscanClient, SolscanAsyncClient
from ...solscan.v2.param import (
    SolscanReturnLimitType,
    SolscanPageSizeType,
    SolscanAccountType
)
from ...solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse,
    GetAccountTokenNFTAccountResponse,
    GetAccountDefiActivitiesParam,
    GetAccountDefiActivitiesResponse,
    GetAccountBalanceChangeActivitiesParam,
    GetAccountBalanceChangeActivitiesResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeResponse,
    GetAccountDetailResponse,
    GetAccountRewardsExportResponse,
    GetTokenTransferParam,
    GetTokenTransferResponse,
)

class Solscan(Interaction):
    """
        Class used to connect only [Solscan](https://solscan.io) **V2** API, one of them most popular Solana chain explorer. 
        To have access Solscan Pro API is required to have a valid API key.

        Check [API Documentation](https://pro-api.solscan.io/pro-api-docs/v2.0) for all the details on the available endpoints.

        Solscan API is currently divided into two versions:

        - **v1** - the first and classic version of the Pro API.
        - **v2** - a new and improved version of the Pro API, with more endpoints and features.
            *This version is under development and may have some changes*.

        !!! info
            This `Interaction` is dedicated to the Solscan Pro API v2.0.
            Use `cyhole.solscan.SolscanV1` or `cyhole.solscan.v1.Solscan` for the Solscan Pro API v1.0.
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from environment variable `SOLSCAN_API_V2_KEY`.

        Parameters:
            api_key: specifies the API key for Solscan Pro API v2.

        **Example**
    """

    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("SOLSCAN_API_V2_KEY")
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
        self.base_url = "https://pro-api.solscan.io/v2.0/"

        # private attributes
        self._name = "Solscan V2 API"
        self._description = "Interact with Solscan API V2"
        return

    def __str__(self) -> str:
        return self._name

    @overload
    def _get_account_transfers(self, sync: Literal[True], account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse: ...

    @overload
    def _get_account_transfers(self, sync: Literal[False], account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> Coroutine[None, None, GetAccountTransferResponse]: ...

    def _get_account_transfers(self, sync: bool, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse | Coroutine[None, None, GetAccountTransferResponse]:
        """
            This function refers to the GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** of **V2** API endpoint, 
            and it is used to get transfers of an account.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of transfers of the account.
        """
        # set params
        url = self.base_url + "account/transfer"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )
        api_params["address"] = account

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountTransferResponse,
            params = api_params
        )

    @overload
    def _get_account_token_nft_account(
        self,
        sync: Literal[True],
        account: str,
        account_type: str,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value,
        hide_zero: bool = True
    ) -> GetAccountTokenNFTAccountResponse: ...

    @overload
    def _get_account_token_nft_account(
        self,
        sync: Literal[False],
        account: str,
        account_type: str,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value,
        hide_zero: bool = True
    ) -> Coroutine[None, None, GetAccountTokenNFTAccountResponse]: ...

    def _get_account_token_nft_account(
        self,
        sync: bool,
        account: str,
        account_type: str,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value,
        hide_zero: bool = True
    ) -> GetAccountTokenNFTAccountResponse | Coroutine[None, None, GetAccountTokenNFTAccountResponse]:
        """
            This function refers to the GET **[Account Token/NFT Account](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-token-nft-account)** of **V2** API endpoint, 
            and it is used to get the NFT/Tokens' accounts of an account.

            Parameters:
                account: The account address.
                account_type: The account type (NFT/Token).
                    The supported types are available on [`SolscanAccountType`][cyhole.solscan.v2.param.SolscanAccountType].
                page: The page number.
                page_size: The number of accounts per page.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].
                hide_zero: Hide zero balances accounts.

            Returns:
                List of NFT/Tokens accountS.
        """
        # check param consistency
        SolscanAccountType.check(account_type)
        SolscanPageSizeType.check(page_size)

        # set params
        url = self.base_url + "account/token-accounts"
        api_params = {
            "address": account,
            "type": account_type,
            "page": page,
            "page_size": page_size,
            "hide_zero": "true" if hide_zero else "false"
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountTokenNFTAccountResponse,
            params = api_params
        )

    @overload
    def _get_account_defi_activities(self, sync: Literal[True], account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse: ...

    @overload
    def _get_account_defi_activities(self, sync: Literal[False], account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> Coroutine[None, None, GetAccountDefiActivitiesResponse]: ...

    def _get_account_defi_activities(self, sync: bool, account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse | Coroutine[None, None, GetAccountDefiActivitiesResponse]:
        """
            This function refers to the GET **[Account DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** of **V2** API endpoint, 
            and it is used to get the DeFi activities of an account.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.

            Returns:
                List of DeFi activities.
        """
        # set params
        url = self.base_url + "account/defi/activities"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )
        api_params["address"] = account

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountDefiActivitiesResponse,
            params = api_params
        )

    @overload
    def _get_account_balance_change_activities(self, sync: Literal[True], account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse: ...

    @overload
    def _get_account_balance_change_activities(self, sync: Literal[False], account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> Coroutine[None, None, GetAccountBalanceChangeActivitiesResponse]: ...

    def _get_account_balance_change_activities(self, sync: bool, account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse | Coroutine[None, None, GetAccountBalanceChangeActivitiesResponse]:
        """
            This function refers to the GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** of **V2** API endpoint, 
            and it is used to get the balance change activities of an account.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.

            Returns:
                List of balance change activities.
        """
        # set params
        url = self.base_url + "account/balance_change"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )
        api_params["address"] = account

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountBalanceChangeActivitiesResponse,
            params = api_params
        )

    @overload
    def _get_account_transactions(self, sync: Literal[True], account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse: ...

    @overload
    def _get_account_transactions(self, sync: Literal[False], account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> Coroutine[None, None, GetAccountTransactionsResponse]: ...

    def _get_account_transactions(self, sync: bool, account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse | Coroutine[None, None, GetAccountTransactionsResponse]:
        """
            This function refers to the GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** of **V2** API endpoint, 
            and it is used to get the latest transactions of an account.

            Parameters:
                account: The account address.
                before_transaction: The signature of the latest transaction of previous page.
                limit: The number of transactions to be returned.
                    The supported types are available on [`SolscanReturnLimitType`][cyhole.solscan.v2.param.SolscanReturnLimitType].

            Returns:
                List of transactions of the account.
        """
        # check param consistency
        SolscanReturnLimitType.check(limit)

        # set params
        url = self.base_url + "account/transactions"
        api_params = {
            "address": account,
            "before": before_transaction,
            "limit": limit
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountTransactionsResponse,
            params = api_params
        )

    @overload
    def _get_account_stake(self, sync: Literal[True], account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse: ...

    @overload
    def _get_account_stake(self, sync: Literal[False], account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> Coroutine[None, None, GetAccountStakeResponse]: ...

    def _get_account_stake(self, sync: bool, account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse | Coroutine[None, None, GetAccountStakeResponse]:
        """
            This function refers to the GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** of **V2** API endpoint, 
            and it is used to get the staking activities of an account.

            Parameters:
                account: The account address.
                page: The page number.
                limit: The number of staking activities to be returned.
                    The supported types are available on [`SolscanReturnLimitType`][cyhole.solscan.v2.param.SolscanReturnLimitType].

            Returns:
                List of staking activities of the account.
        """
        # check param consistency
        SolscanReturnLimitType.check(limit)

        # set params
        url = self.base_url + "account/stake"
        api_params = {
            "address": account,
            "page": page,
            "page_size": limit
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountStakeResponse,
            params = api_params
        )

    @overload
    def _get_account_detail(self, sync: Literal[True], account: str) -> GetAccountDetailResponse: ...

    @overload
    def _get_account_detail(self, sync: Literal[False], account: str) -> Coroutine[None, None, GetAccountDetailResponse]: ...

    def _get_account_detail(self, sync: bool, account: str) -> GetAccountDetailResponse | Coroutine[None, None, GetAccountDetailResponse]:
        """
            This function refers to the GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** of **V2** API endpoint, 
            and it is used to get the detail of an account.

            Parameters:
                account: The account address.

            Returns:
                Detail of the account.
        """
        # set params
        url = self.base_url + "account/detail"
        api_params = {
            "address": account
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountDetailResponse,
            params = api_params
        )

    @overload
    def _get_account_rewards_export(self, sync: Literal[True], account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse: ...

    @overload
    def _get_account_rewards_export(self, sync: Literal[False], account: str, dt_from: datetime, dt_to: datetime) -> Coroutine[None, None, GetAccountRewardsExportResponse]: ...

    def _get_account_rewards_export(self, sync: bool, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse | Coroutine[None, None, GetAccountRewardsExportResponse]:
        """
            This function refers to the GET **[Account Rewards Export](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** of **V2** API endpoint, 
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
        url = self.base_url + f"account/reward/export"
        api_params = {
            "address": account,
            "time_from": int(dt_from.timestamp()),
            "time_to": int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountRewardsExportResponse(csv = content_raw.text)
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountRewardsExportResponse(csv = content_raw.text)
            return async_request()

    @overload
    def _get_token_transfer(self, sync: Literal[True], token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse: ...

    @overload
    def _get_token_transfer(self, sync: Literal[False], token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> Coroutine[None, None, GetTokenTransferResponse]: ...

    def _get_token_transfer(self, sync: bool, token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse | Coroutine[None, None, GetTokenTransferResponse]:
        """
            This function refers to the GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** of **V2** API endpoint, 
            and it is used to get transfers of a token.

            Parameters:
                token: The token address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of transfers of the token.
        """
        # set params
        url = self.base_url + "token/transfer"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )
        api_params["address"] = token

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenTransferResponse,
            params = api_params
        )