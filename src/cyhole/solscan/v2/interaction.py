import os
from datetime import datetime
from requests import HTTPError
from typing import Coroutine, Literal, overload

from ...core.param import RequestType
from ...core.interaction import Interaction
from ...core.exception import MissingAPIKeyError
from ...solscan.v2.client import SolscanClient, SolscanAsyncClient
from ...solscan.v2.exception import SolscanInvalidTimeRange, SolscanInvalidAmountRange, SolscanException
from ...solscan.v2.param import (
    SolscanTransactionFilterType,
    SolscanReturnLimitType,
    SolscanNFTItemSortType,
    SolscanNFTPageSizeType,
    SolscanPageSizeType,
    SolscanAccountType,
    SolscanOrderType,
    SolscanSortType
)
from ...solscan.v2.schema import (
    SolscanHTTPError,
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
    GetTokenDefiActivitiesParam,
    GetTokenDefiActivitiesResponse,
    GetTokenMarketsResponse,
    GetTokenListResponse,
    GetTokenTrendingResponse,
    GetTokenPriceResponse,
    GetTokenHoldersResponse,
    GetTokenMetaResponse,
    GetNFTNewsResponse,
    GetNFTActivitiesParam,
    GetNFTActivitiesResponse,
    GetNFTCollectionListsParam,
    GetNFTCollectionListsResponse,
    GetNFTCollectionItemsResponse,
    GetTransactionLastResponse,
    GetTransactionActionsResponse,
    GetBlockLastResponse,
    GetBlockTransactionsResponse,
    GetBlockDetailResponse
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
        url = self.base_url + "account/reward/export"
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

    @overload
    def _get_token_defi_activities(self, sync: Literal[True], token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse: ...

    @overload
    def _get_token_defi_activities(self, sync: Literal[False], token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> Coroutine[None, None, GetTokenDefiActivitiesResponse]: ...

    def _get_token_defi_activities(self, sync: bool, token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse | Coroutine[None, None, GetTokenDefiActivitiesResponse]:
        """
            This function refers to the GET **[Token DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** of **V2** API endpoint, 
            and it is used to get the DeFi activities of a token.

            Parameters:
                token: The token address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of DeFi activities of the token.
        """
        # set params
        url = self.base_url + "token/defi/activities"
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
            response_model = GetTokenDefiActivitiesResponse,
            params = api_params
        )

    @overload
    def _get_token_markets(
        self,
        sync: Literal[True],
        tokens: str | list[str],
        program_address: str | list[str] | None  = None,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenMarketsResponse: ...

    @overload
    def _get_token_markets(
        self,
        sync: Literal[False],
        tokens: str | list[str],
        program_address: str | list[str] | None  = None,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> Coroutine[None, None, GetTokenMarketsResponse]: ...

    def _get_token_markets(
        self,
        sync: bool,
        tokens: str | list[str],
        program_address: str | list[str] | None  = None,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenMarketsResponse | Coroutine[None, None, GetTokenMarketsResponse]:
        """
            This function refers to the GET **[Token Markets](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-markets)** of **V2** API endpoint, 
            and it is used to get the markets data of a set of tokens.

            Parameters:
                tokens: The token address or list of token addresses.
                program_address: The program address or list of program addresses.
                page: The page number.
                page_size: The number of markets per page.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].

            Returns:
                List of markets of the token.
        """
        # check param consistency
        SolscanPageSizeType.check(page_size)

        # set params
        url = self.base_url + "token/markets"
        api_params = {
            "token[]": tokens,
            "program[]": program_address,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenMarketsResponse,
            params = api_params
        )

    @overload
    def _get_token_list(
        self,
        sync: Literal[True],
        sort_by: str = SolscanSortType.MARKET_CAP.value,
        order_by: str = SolscanOrderType.DESCENDING.value,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenListResponse: ...

    @overload
    def _get_token_list(
        self,
        sync: Literal[False],
        sort_by: str = SolscanSortType.MARKET_CAP.value,
        order_by: str = SolscanOrderType.DESCENDING.value,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> Coroutine[None, None, GetTokenListResponse]: ...

    def _get_token_list(
        self,
        sync: bool,
        sort_by: str = SolscanSortType.MARKET_CAP.value,
        order_by: str = SolscanOrderType.DESCENDING.value,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenListResponse | Coroutine[None, None, GetTokenListResponse]:
        """
            This function refers to the GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-list)** of **V2** API endpoint, 
            and it is used to get the list of tokens.

            Parameters:
                sort_by: The sorting method.
                    The supported types are available on [`SolscanSortType`][cyhole.solscan.v2.param.SolscanSortType].
                order_by: The ordering to get the response.
                    The supported types are available on [`SolscanOrderType`][cyhole.solscan.v2.param.SolscanOrderType].
                page: The page number.
                page_size: The number of tokens per page.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].

            Returns:
                List of tokens.
        """
        # check param consistency
        SolscanSortType.check(sort_by)
        SolscanOrderType.check(order_by)
        SolscanPageSizeType.check(page_size)

        # set params
        url = self.base_url + "token/list"
        api_params = {
            "sort_by": sort_by,
            "sort_order": order_by,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenListResponse,
            params = api_params
        )

    @overload
    def _get_token_trending(self, sync: Literal[True], limit: int = 10) -> GetTokenTrendingResponse: ...

    @overload
    def _get_token_trending(self, sync: Literal[False], limit: int = 10) -> Coroutine[None, None, GetTokenTrendingResponse]: ...

    def _get_token_trending(self, sync: bool, limit: int = 10) -> GetTokenTrendingResponse | Coroutine[None, None, GetTokenTrendingResponse]:
        """
            This function refers to the GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** of **V2** API endpoint, 
            and it is used to get the trending tokens on Solscan.

            Parameters:
                limit: The number of trending tokens to be returned.

            Returns:
                List of trending tokens.
        """

        # set params
        url = self.base_url + "token/trending"
        api_params = {
            "limit": limit
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenTrendingResponse,
            params = api_params
        )

    @overload
    def _get_token_price(self, sync: Literal[True], token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse: ...

    @overload
    def _get_token_price(self, sync: Literal[False], token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> Coroutine[None, None, GetTokenPriceResponse]: ...

    def _get_token_price(self, sync: bool, token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse | Coroutine[None, None, GetTokenPriceResponse]:
        """
            This function refers to the GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** of **V2** API endpoint, 
            and it is used to get the price of a token.

            Parameters:
                token: The token address.
                time_range: The time range.
                    It can be a single datetime object or a tuple of two datetime objects.

            Returns:
                Price of the token.
        """
        # check consistency and convert to string
        time_range_str: list[str]
        if isinstance(time_range, tuple):
            # check consistency
            if time_range[0] > time_range[1]:
                raise SolscanInvalidTimeRange("the start time is greater than the end time.")
            # convert to string
            time_range_str = [time_range[0].strftime("%Y%m%d"), time_range[1].strftime("%Y%m%d")]
        else:
            time_range_str = [time_range.strftime("%Y%m%d")]

        # set params
        url = self.base_url + "token/price"
        api_params = {
            "address": token,
            "time[]": time_range_str
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenPriceResponse,
            params = api_params
        )

    @overload
    def _get_token_holders(self, sync: Literal[True], token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse: ...

    @overload
    def _get_token_holders(self, sync: Literal[False], token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> Coroutine[None, None, GetTokenHoldersResponse]: ...

    def _get_token_holders(self, sync: bool, token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse | Coroutine[None, None, GetTokenHoldersResponse]:
        """
            This function refers to the GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** of **V2** API endpoint, 
            and it is used to get the holders of a token.

            Parameters:
                token: The token address.
                amount_range: The amount range.
                    It can be a tuple of two integers (from, to).
                page: The page number.
                page_size: The number of holders per page.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].

            Returns:
                List of holders of the token.
        """
        from_amount = None
        to_amount = None

        # check param consistency
        SolscanPageSizeType.check(page_size)

        if amount_range:
            if amount_range[0] > amount_range[1]:
                raise SolscanInvalidAmountRange("The start amount is greater than the end amount.")

            from_amount = str(amount_range[0])
            to_amount = str(amount_range[1])

        # set params
        url = self.base_url + "token/holders"
        api_params = {
            "address": token,
            "from_amount": from_amount,
            "to_amount": to_amount,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenHoldersResponse,
            params = api_params
        )

    @overload
    def _get_token_meta(self, sync: Literal[True], token: str) -> GetTokenMetaResponse: ...

    @overload
    def _get_token_meta(self, sync: Literal[False], token: str) -> Coroutine[None, None, GetTokenMetaResponse]: ...

    def _get_token_meta(self, sync: bool, token: str) -> GetTokenMetaResponse | Coroutine[None, None, GetTokenMetaResponse]:
        """
            This function refers to the GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** of **V2** API endpoint, 
            and it is used to get the metadata of a token.

            Parameters:
                token: The token address.

            Returns:
                Metadata of the token.
        """
        # set params
        url = self.base_url + "token/meta"
        api_params = {
            "address": token
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenMetaResponse,
            params = api_params
        )

    @overload
    def _get_nft_news(self, sync: Literal[True], filter: str = "created_time", page: int = 1, page_size: int = SolscanNFTPageSizeType.SIZE_12.value) -> GetNFTNewsResponse: ...

    @overload
    def _get_nft_news(self, sync: Literal[False], filter: str = "created_time", page: int = 1, page_size: int = SolscanNFTPageSizeType.SIZE_12.value) -> Coroutine[None, None, GetNFTNewsResponse]: ...

    def _get_nft_news(self, sync: bool, filter: str = "created_time", page: int = 1, page_size: int = SolscanNFTPageSizeType.SIZE_12.value) -> GetNFTNewsResponse | Coroutine[None, None, GetNFTNewsResponse]:
        """
            This function refers to the GET **[NFT News](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-news)** of **V2** API endpoint, 
            and it is used to get the latest NFT news.

            Parameters:
                filter: The filter to be used.
                page: The page number.
                page_size: The number of NFT per page.
                    The supported types are available on [`SolscanNFTPageSizeType`][cyhole.solscan.v2.param.SolscanNFTPageSizeType].

            Returns:
                List of NFT news.
        """
        # check param consistency
        SolscanNFTPageSizeType.check(page_size)

        # set params
        url = self.base_url + "nft/news"
        api_params = {
            "filter": filter,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetNFTNewsResponse,
            params = api_params
        )

    @overload
    def _get_nft_activities(self, sync: Literal[True], params: GetNFTActivitiesParam = GetNFTActivitiesParam()) -> GetNFTActivitiesResponse: ...

    @overload
    def _get_nft_activities(self, sync: Literal[False], params: GetNFTActivitiesParam = GetNFTActivitiesParam()) -> Coroutine[None, None, GetNFTActivitiesResponse]: ...

    def _get_nft_activities(self, sync: bool, params: GetNFTActivitiesParam = GetNFTActivitiesParam()) -> GetNFTActivitiesResponse | Coroutine[None, None, GetNFTActivitiesResponse]:
        """
            This function refers to the GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** of **V2** API endpoint, 
            and it is used to get the NFT activities.

            Parameters:
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of NFT activities.
        """
        # set params
        url = self.base_url + "nft/activities"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetNFTActivitiesResponse,
            params = api_params
        )

    @overload
    def _get_nft_collection_lists(self, sync: Literal[True], params: GetNFTCollectionListsParam = GetNFTCollectionListsParam()) -> GetNFTCollectionListsResponse: ...

    @overload
    def _get_nft_collection_lists(self, sync: Literal[False], params: GetNFTCollectionListsParam = GetNFTCollectionListsParam()) -> Coroutine[None, None, GetNFTCollectionListsResponse]: ...

    def _get_nft_collection_lists(self, sync: bool, params: GetNFTCollectionListsParam = GetNFTCollectionListsParam()) -> GetNFTCollectionListsResponse | Coroutine[None, None, GetNFTCollectionListsResponse]:
        """
            This function refers to the GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** of **V2** API endpoint, 
            and it is used to get the list of NFT collections.

            Parameters:
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of NFT collections.
        """
        # set params
        url = self.base_url + "nft/collection/lists"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetNFTCollectionListsResponse,
            params = api_params
        )

    @overload
    def _get_nft_collection_items(
        self,
        sync: Literal[True],
        collection: str,
        sort_by: str = SolscanNFTItemSortType.LAST_TRADE.value,
        page: int = 1,
        page_size: int = SolscanNFTPageSizeType.SIZE_12.value
    ) -> GetNFTCollectionItemsResponse: ...

    @overload
    def _get_nft_collection_items(
        self,
        sync: Literal[False],
        collection: str,
        sort_by: str = SolscanNFTItemSortType.LAST_TRADE.value,
        page: int = 1,
        page_size: int = SolscanNFTPageSizeType.SIZE_12.value
    ) -> Coroutine[None, None, GetNFTCollectionItemsResponse]: ...

    def _get_nft_collection_items(
        self,
        sync: bool,
        collection: str,
        sort_by: str = SolscanNFTItemSortType.LAST_TRADE.value,
        page: int = 1,
        page_size: int = SolscanNFTPageSizeType.SIZE_12.value
    ) -> GetNFTCollectionItemsResponse | Coroutine[None, None, GetNFTCollectionItemsResponse]:
        """
            This function refers to the GET **[NFT Collection Items](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-items)** of **V2** API endpoint, 
            and it is used to get the items of a NFT collection.

            Parameters:
                collection: The collection address.
                sort_by: The sorting method.
                    The supported types are available on [`SolscanNFTItemSortType`][cyhole.solscan.v2.param.SolscanNFTItemSortType].
                page: The page number.
                page_size: The number of items per page.
                    The supported types are available on [`SolscanNFTPageSizeType`][cyhole.solscan.v2.param.SolscanNFTPageSizeType].

            Returns:
                List of NFT items of the collection.
        """
        # check param consistency
        SolscanNFTPageSizeType.check(page_size)
        SolscanNFTItemSortType.check(sort_by)

        # set params
        url = self.base_url + "nft/collection/items"
        api_params = {
            "collection": collection,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetNFTCollectionItemsResponse,
            params = api_params
        )

    @overload
    def _get_transaction_last(self, sync: Literal[True], limit: int = SolscanReturnLimitType.LIMIT_10.value, filter: str = SolscanTransactionFilterType.EXCEPT_VOTE.value) -> GetTransactionLastResponse: ...

    @overload
    def _get_transaction_last(self, sync: Literal[False], limit: int = SolscanReturnLimitType.LIMIT_10.value, filter: str = SolscanTransactionFilterType.EXCEPT_VOTE.value) -> Coroutine[None, None, GetTransactionLastResponse]: ...

    def _get_transaction_last(self, sync: bool, limit: int = SolscanReturnLimitType.LIMIT_10.value, filter: str = SolscanTransactionFilterType.EXCEPT_VOTE.value) -> GetTransactionLastResponse | Coroutine[None, None, GetTransactionLastResponse]:
        """
            This function refers to the GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-last)** of **V2** API endpoint, 
            and it is used to get the latest transactions.

            Parameters:
                limit: The number of transactions to be returned.
                    The supported types are available on [`SolscanReturnLimitType`][cyhole.solscan.v2.param.SolscanReturnLimitType].
                filter: The filter to be used.
                    The supported types are available on [`SolscanTransactionFilterType`][cyhole.solscan.v2.param.SolscanTransactionFilterType].

            Returns:
                List of latest transactions.
        """
        # check param consistency
        SolscanReturnLimitType.check(limit)
        SolscanTransactionFilterType.check(filter)

        # set params
        url = self.base_url + "transaction/last"
        api_params = {
            "limit": limit,
            "filter": filter
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTransactionLastResponse,
            params = api_params
        )

    @overload
    def _get_transaction_actions(self, sync: Literal[True], transaction: str) -> GetTransactionActionsResponse: ...

    @overload
    def _get_transaction_actions(self, sync: Literal[False], transaction: str) -> Coroutine[None, None, GetTransactionActionsResponse]: ...

    def _get_transaction_actions(self, sync: bool, transaction: str) -> GetTransactionActionsResponse | Coroutine[None, None, GetTransactionActionsResponse]:
        """
            This function refers to the GET **[Transaction Actions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-actions)** of **V2** API endpoint, 
            and it is used to get the actions of a transaction.

            Parameters:
                transaction: The transaction signature.

            Returns:
                List of actions of the transaction.
        """
        # set params
        url = self.base_url + "transaction/actions"
        api_params = {
            "tx": transaction
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTransactionActionsResponse,
            params = api_params
        )

    @overload
    def _get_block_last(self, sync: Literal[True], page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockLastResponse: ...

    @overload
    def _get_block_last(self, sync: Literal[False], page_size: int = SolscanPageSizeType.SIZE_10.value) -> Coroutine[None, None, GetBlockLastResponse]: ...

    def _get_block_last(self, sync: bool, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockLastResponse | Coroutine[None, None, GetBlockLastResponse]:
        """
            This function refers to the GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-last)** of **V2** API endpoint, 
            and it is used to get the latest blocks.

            Parameters:
                page_size: The number of blocks to be returned.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].

            Returns:
                List of latest blocks.
        """
        # check param consistency
        SolscanPageSizeType.check(page_size)

        # set params
        url = self.base_url + "block/last"
        api_params = {
            "limit": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlockLastResponse,
            params = api_params
        )

    @overload
    def _get_block_transactions(self, sync: Literal[True], block: int, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockTransactionsResponse: ...

    @overload
    def _get_block_transactions(self, sync: Literal[False], block: int, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> Coroutine[None, None, GetBlockTransactionsResponse]: ...

    def _get_block_transactions(self, sync: bool, block: int, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockTransactionsResponse | Coroutine[None, None, GetBlockTransactionsResponse]:
        """
            This function refers to the GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-transactions)** of **V2** API endpoint, 
            and it is used to get the transactions of a block.

            Parameters:
                block: The block number.
                page: The page number.
                page_size: The number of transactions per page.
                    The supported types are available on [`SolscanPageSizeType`][cyhole.solscan.v2.param.SolscanPageSizeType].

            Returns:
                List of transactions of the block.
        """
        # check param consistency
        SolscanPageSizeType.check(page_size)

        # set params
        url = self.base_url + "block/transactions"
        api_params = {
            "block": block,
            "page": page,
            "page_size": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlockTransactionsResponse,
            params = api_params
        )

    @overload
    def _get_block_detail(self, sync: Literal[True], block: int) -> GetBlockDetailResponse: ...

    @overload
    def _get_block_detail(self, sync: Literal[False], block: int) -> Coroutine[None, None, GetBlockDetailResponse]: ...

    def _get_block_detail(self, sync: bool, block: int) -> GetBlockDetailResponse | Coroutine[None, None, GetBlockDetailResponse]:
        """
            This function refers to the GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-detail)** of **V2** API endpoint, 
            and it is used to get the detail of a block.

            Parameters:
                block: The block number.

            Returns:
                Detail of the block.
        """
        # set params
        url = self.base_url + "block/detail"
        api_params = {
            "block": block
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlockDetailResponse,
            params = api_params
        )

    def _raise(self, exception: HTTPError) -> SolscanException:
        """
            Internal function used to raise the manage 
            the exceptions raised by the API.

            Parameters:
                exception: the HTTP error returned from Solscan API.

            Raises:
                SolscanException: general exception raised when an unknown error is found.
        """
        try:
            error = SolscanHTTPError(**exception.response.json())
            return SolscanException(f"Code: {error.errors.code}, Message: {error.errors.message}")
        except Exception:
            return SolscanException(exception.response.content.decode())