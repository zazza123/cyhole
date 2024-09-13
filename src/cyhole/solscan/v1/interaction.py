import os
from datetime import datetime
from requests import HTTPError
from typing import Coroutine, Literal, overload

from ...core.param import RequestType
from ...core.interaction import Interaction
from ...core.exception import MissingAPIKeyError
from ...solscan.v1.exception import SolscanException
from ...solscan.v1.client import SolscanClient, SolscanAsyncClient
from ...solscan.v1.param import SolscanExportType, SolscanSort, SolscanOrder
from ...solscan.v1.schema import (
    SolscanHTTPError,
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
        url = self.base_url + "account/tokens"
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
        url = self.base_url + "account/transactions"
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
        url = self.base_url + "account/stakeAccounts"
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
        url = self.base_url + "account/splTransfers"
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
        url = self.base_url + "account/solTransfers"
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
        url = self.base_url + "account/exportTransactions"
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
        url = self.base_url + "account/exportRewards"
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

    @overload
    def _get_token_holders(
        self,
        sync: Literal[True],
        token: str,
        limit: int = 10,
        offset: int | None = None,
        amount_from: int | None = None,
        amount_to: int | None = None
    ) -> GetTokenHoldersResponse: ...

    @overload
    def _get_token_holders(
        self,
        sync: Literal[False],
        token: str,
        limit: int = 10,
        offset: int | None = None,
        amount_from: int | None = None,
        amount_to: int | None = None
    ) -> Coroutine[None, None, GetTokenHoldersResponse]: ...

    def _get_token_holders(
        self,
        sync: bool,
        token: str,
        limit: int = 10,
        offset: int | None = None,
        amount_from: int | None = None,
        amount_to: int | None = None
    ) -> GetTokenHoldersResponse | Coroutine[None, None, GetTokenHoldersResponse]:
        """
            This function refers to the GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-holders)** of **V1** API endpoint, 
            and it is used to get token holders of a token.

            Parameters:
                token: The token address.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.
                amount_from: The minimum amount of the token.
                amount_to: The maximum amount of the token

            Returns:
                List of token holders of the token.
        """
        # set params
        url = self.base_url + "token/holders"
        api_params = {
            "tokenAddress": token,
            "limit": limit,
            "offset": offset,
            "fromAmount": amount_from,
            "toAmount": amount_to
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
            This function refers to the GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-meta)** of **V1** API endpoint, 
            and it is used to get meta of a token.

            Parameters:
                token: The token address.

            Returns:
                Meta of the token.
        """
        # set params
        url = self.base_url + "token/meta"
        api_params = {
            "tokenAddress": token
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
    def _get_token_transfer(
        self,
        sync: Literal[True],
        token: str,
        account: str | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenTransferResponse: ...

    @overload
    def _get_token_transfer(
        self,
        sync: Literal[False],
        token: str,
        account: str | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> Coroutine[None, None, GetTokenTransferResponse]: ...

    def _get_token_transfer(
        self,
        sync: bool,
        token: str,
        account: str | None = None,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenTransferResponse | Coroutine[None, None, GetTokenTransferResponse]:
        """
            This function refers to the GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-transfer)** of **V1** API endpoint, 
            and it is used to get token transfers of a token.

            Parameters:
                token: The token address.
                account: The account address to filter for.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                List of token transfers of the token.
        """
        # set params
        url = self.base_url + "token/transfer"
        api_params = {
            "tokenAddress": token,
            "address": account,
            "limit": limit,
            "offset": offset
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenTransferResponse,
            params = api_params
        )

    @overload
    def _get_token_list(
        self,
        sync: Literal[True],
        sort_by: str = SolscanSort.MARKET_CAP.value,
        order_by: str = SolscanOrder.DESCENDING.value,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenListResponse: ...

    @overload
    def _get_token_list(
        self,
        sync: Literal[False],
        sort_by: str = SolscanSort.MARKET_CAP.value,
        order_by: str = SolscanOrder.DESCENDING.value,
        limit: int = 10,
        offset: int | None = None
    ) -> Coroutine[None, None, GetTokenListResponse]: ...

    def _get_token_list(
        self,
        sync: bool,
        sort_by: str = SolscanSort.MARKET_CAP.value,
        order_by: str = SolscanOrder.DESCENDING.value,
        limit: int = 10,
        offset: int | None = None
    ) -> GetTokenListResponse | Coroutine[None, None, GetTokenListResponse]:
        """
            This function refers to the GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/token-list)** of **V1** API endpoint, 
            and it is used to get list of tokens according to Solscan, with additional token's information.

            Parameters:
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                List of tokens.
        """
        # set params
        url = self.base_url + "token/list"
        api_params = {
            "sortBy": sort_by,
            "direction": order_by,
            "limit": limit,
            "offset": offset
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
    def _get_market_token_detail(self, sync: Literal[True], token: str, limit: int = 10, offset: int | None = None) -> GetMarketTokenDetailResponse: ...

    @overload
    def _get_market_token_detail(self, sync: Literal[False], token: str, limit: int = 10, offset: int | None = None) -> Coroutine[None, None, GetMarketTokenDetailResponse]: ...

    def _get_market_token_detail(self, sync: bool, token: str, limit: int = 10, offset: int | None = None) -> GetMarketTokenDetailResponse | Coroutine[None, None, GetMarketTokenDetailResponse]:
        """
            This function refers to the GET **[Market Token Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/market-token-detail)** of **V1** API endpoint, 
            and it is used to get market details of a token.

            Parameters:
                token: The token address.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                Market details of the token.
        """
        # set params
        url = self.base_url + f"market/token/{token}"
        api_params = {
            "limit": limit,
            "offset": offset
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetMarketTokenDetailResponse,
            params = api_params
        )

    @overload
    def _get_transaction_last(self, sync: Literal[True], limit: int = 10) -> GetTransactionLastResponse: ...

    @overload
    def _get_transaction_last(self, sync: Literal[False], limit: int = 10) -> Coroutine[None, None, GetTransactionLastResponse]: ...

    def _get_transaction_last(self, sync: bool, limit: int = 10) -> GetTransactionLastResponse | Coroutine[None, None, GetTransactionLastResponse]:
        """
            This function refers to the GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-last)** of **V1** API endpoint, 
            and it is used to get last transactions.

            Parameters:
                limit: The number of transactions to get; maximum is 20.

            Returns:
                Last transactions.
        """
        # set params
        url = self.base_url + "transaction/last"
        api_params = {
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetTransactionLastResponse(data = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetTransactionLastResponse(data = content_raw.json())
            return async_request()

    @overload
    def _get_transaction_detail(self, sync: Literal[True], transaction_id: str) -> GetTransactionDetailResponse: ...

    @overload
    def _get_transaction_detail(self, sync: Literal[False], transaction_id: str) -> Coroutine[None, None, GetTransactionDetailResponse]: ...

    def _get_transaction_detail(self, sync: bool, transaction_id: str) -> GetTransactionDetailResponse | Coroutine[None, None, GetTransactionDetailResponse]:
        """
            This function refers to the GET **[Transaction Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/transaction-detail)** of **V1** API endpoint, 
            and it is used to get detail of a transaction.

            Parameters:
                transaction_id: The transaction hash.

            Returns:
                Detail of the transaction.
        """
        # set params
        url = self.base_url + f"transaction/{transaction_id}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTransactionDetailResponse
        )

    @overload
    def _get_block_last(self, sync: Literal[True], limit: int = 10) -> GetBlockLastResponse: ...

    @overload
    def _get_block_last(self, sync: Literal[False], limit: int = 10) -> Coroutine[None, None, GetBlockLastResponse]: ...

    def _get_block_last(self, sync: bool, limit: int = 10) -> GetBlockLastResponse | Coroutine[None, None, GetBlockLastResponse]:
        """
            This function refers to the GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-last)** of **V1** API endpoint, 
            and it is used to get last block.

            Parameters:
                limit: The number of blocks to get; maximum is 20.

            Returns:
                Last block.
        """
        # set params
        url = self.base_url + "block/last"
        api_params = {
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetBlockLastResponse(data = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetBlockLastResponse(data = content_raw.json())
            return async_request()

    @overload
    def _get_block_detail(self, sync: Literal[True], block_id: int) -> GetBlockDetailResponse: ...

    @overload
    def _get_block_detail(self, sync: Literal[False], block_id: int) -> Coroutine[None, None, GetBlockDetailResponse]: ...

    def _get_block_detail(self, sync: bool, block_id: int) -> GetBlockDetailResponse | Coroutine[None, None, GetBlockDetailResponse]:
        """
            This function refers to the GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-detail)** of **V1** API endpoint, 
            and it is used to get detail of a block.

            Parameters:
                block_id: The block number.

            Returns:
                Detail of the block.
        """
        # set params
        url = self.base_url + f"block/{block_id}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlockDetailResponse
        )

    @overload
    def _get_block_transactions(
        self,
        sync: Literal[True],
        block_id: int,
        limit: int = 10,
        offset: int | None = None
    ) -> GetBlockTransactionsResponse: ...

    @overload
    def _get_block_transactions(
        self,
        sync: Literal[False],
        block_id: int,
        limit: int = 10,
        offset: int | None = None
    ) -> Coroutine[None, None, GetBlockTransactionsResponse]: ...

    def _get_block_transactions(
        self,
        sync: bool,
        block_id: int,
        limit: int = 10,
        offset: int | None = None
    ) -> GetBlockTransactionsResponse | Coroutine[None, None, GetBlockTransactionsResponse]:
        """
            This function refers to the GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/block-transactions)** of **V1** API endpoint, 
            and it is used to get transactions of a block.

            Parameters:
                block_id: The block number.
                limit: The number of transactions to get; maximum is 50.
                offset: The offset of the transactions.

            Returns:
                List of transactions of the block.
        """
        # set params
        url = self.base_url + "block/transactions"
        api_params = {
            "block": block_id,
            "limit": limit,
            "offset": offset
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetBlockTransactionsResponse(transactions = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetBlockTransactionsResponse(transactions = content_raw.json())
            return async_request()

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
            return SolscanException(f"Code: {error.status}, Message: {error.error.message}")
        except Exception:
            return SolscanException(exception.response.content.decode())