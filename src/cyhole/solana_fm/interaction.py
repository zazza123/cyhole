import os
from datetime import datetime
from typing import Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..solana_fm.client import SolanaFMClient, SolanaFMAsyncClient
from ..solana_fm.param import SolanaFMBlocksPaginationType
from ..solana_fm.schema import (
    GetAccountTransactionsParam,
    GetAccountTransactionsResponse,
    GetAccountTransfersParam,
    GetAccountTransfersResponse,
    GetAccountTransfersCsvExportParam,
    GetAccountTransfersCsvExportResponse,
    GetAccountTransactionsFeesResponse,
    GetBlocksResponse,
    GetBlockResponse,
    PostMultipleBlocksResponse,
    GetSolanaDailyTransactionFeesResponse,
    GetTaggedTokensListResponse,
    GetTokenInfoV0Response,
    PostTokenMultipleInfoV0Response,
    GetTokenInfoV1Response,
    PostTokenMultipleInfoV1Response,
    PostUserTokenAccountsResponse,
    GetMintTokenAccountsResponse,
    GetOnChainTokenDataResponse,
    GetTokenSupplyResponse,
    GetTransferTransactionsResponse,
    PostMultipleTransferTransactionsResponse,
    GetAllTransferActionsResponse
)


class SolanaFM(Interaction):
    """
        Class used to connect [SolanaFM](https://solana.fm/) API, popular site to interact and explore Solana blockchain.
        To have access SolanaFM API is **not** required an API key, but it is recommended to have one to increase the rate limit. 

        Check [https://docs.solana.fm/](https://docs.solana.fm/) for all the details on the available endpoints.

        !!! info
            If the API key is not provided during the object creation, then it is tried to be 
            retrieved also from ENV variable **SOLANA_FM_API_KEY**.

        Parameters:
            api_key: specify the API key to use for the connection.

        **Example**
        ```python
        import asyncio
        from cyhole.solana_fm import SolanaFM

        account = "ACCOUNT_ID"
        solana_fm = SolanaFM()

        # Get account transactions
        # synchronous
        response = solana_fm.client.get_account_transactions(account)
        print("Transactions Extracted:", len(response.result.data))

        # asynchronous
        async def main() -> None:
            async with solana_fm.async_client as client:
                response = await client.get_account_transactions(account)
                print("Transactions Extracted:", len(response.result.data))

        asyncio.run(main())
        ```
    """
    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key
        if api_key is None:
            self.api_key = os.environ.get("SOLANA_FM_API_KEY")

        # headers setup
        headers = None
        if self.api_key is not None:
            headers = {
                "ApiKey": self.api_key
            }
        super().__init__(headers)

        # clients
        self.client = SolanaFMClient(self, headers = headers)
        self.async_client = SolanaFMAsyncClient(self, headers = headers)

        # API urls
        self.base_v0_url = "https://api.solana.fm/v0/"
        self.base_v1_url = "https://api.solana.fm/v1/"

        # private attributes
        self._name = "SolanaFM"
        self._description = "Interact with SolanaFM API"
        return

    def __str__(self) -> str:
        return self._name

    @overload
    def _get_account_transactions(self, sync: Literal[True], account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse: ...

    @overload
    def _get_account_transactions(self, sync: Literal[False], account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> Coroutine[None, None, GetAccountTransactionsResponse]: ...

    def _get_account_transactions(self, sync: bool, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse | Coroutine[None, None, GetAccountTransactionsResponse]:
        """
            This function refers to the GET **[Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** API endpoint, 
            and it is used to get the list of transactions for a given account according to input parameters.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of transactions.
        """
        # set params
        url = self.base_v0_url + f"accounts/{account}/transactions"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountTransactionsResponse,
            params = api_params
        )

    @overload
    def _get_account_transactions_fees(self, sync: Literal[True], account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse: ...

    @overload
    def _get_account_transactions_fees(self, sync: Literal[False], account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> Coroutine[None, None, GetAccountTransactionsFeesResponse]: ...

    def _get_account_transactions_fees(self, sync: bool, account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse | Coroutine[None, None, GetAccountTransactionsFeesResponse]:
        """
            This function refers to the GET **[Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** API endpoint,
            and it is used to get the list of transactions fees for a given account according to input parameters.

            Parameters:
                account: The account address.
                dt_from: The start date to filter transactions.
                dt_to: The end date to filter transactions.

            Returns:
                List of transactions fees.
        """
        # set params
        url = self.base_v0_url + f"accounts/{account}/fees"

        api_params = {}
        if dt_from is not None:
            api_params["from"] = dt_from.strftime("%Y-%m-%d")
        if dt_to is not None:
            api_params["to"] = dt_to.strftime("%Y-%m-%d")

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTransactionsFeesResponse(data = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTransactionsFeesResponse(data = content_raw.json())
            return async_request()

    @overload
    def _get_account_transfers(self, sync: Literal[True], account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse: ...

    @overload
    def _get_account_transfers(self, sync: Literal[False], account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> Coroutine[None, None, GetAccountTransfersResponse]: ...

    def _get_account_transfers(self, sync: bool, account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse | Coroutine[None, None, GetAccountTransfersResponse]:
        """
            This function refers to the GET **[Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** API endpoint, 
            and it is used to get the list of transfers for a given account according to input parameters.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of transfers.
        """
        # set params
        url = self.base_v0_url + f"accounts/{account}/transfers"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetAccountTransfersResponse,
            params = api_params
        )

    @overload
    def _get_account_transfers_csv_export(self, sync: Literal[True], account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse: ...

    @overload
    def _get_account_transfers_csv_export(self, sync: Literal[False], account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> Coroutine[None, None, GetAccountTransfersCsvExportResponse]: ...

    def _get_account_transfers_csv_export(self, sync: bool, account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse | Coroutine[None, None, GetAccountTransfersCsvExportResponse]:
        """
            This function refers to the GET **[Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** API endpoint,
            and it is used to get the list of transfers for a given account according to input parameters in CSV format.

            Parameters:
                account: The account address.
                params: The parameters to be used in the request.
                    More details in the object definition.

            Returns:
                List of transfers in CSV format.
        """
        # set params
        url = self.base_v0_url + f"accounts/{account}/transfers/csv"
        api_params = params.model_dump(
            by_alias = True,
            exclude_defaults = True
        )

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTransfersCsvExportResponse(csv = content_raw.text)
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTransfersCsvExportResponse(csv = content_raw.text)
            return async_request()

    @overload
    def _get_blocks(
            self,
            sync: Literal[True],
            from_block: int | None = None,
            page_size: int = 50,
            page_type: str = SolanaFMBlocksPaginationType.BLOCK_NUMBER.value,
            ascending: bool | None = None
        ) -> GetBlocksResponse: ...

    @overload
    def _get_blocks(
            self,
            sync: Literal[False],
            from_block: int | None = None,
            page_size: int = 50,
            page_type: str = SolanaFMBlocksPaginationType.BLOCK_NUMBER.value,
            ascending: bool | None = None
        ) -> Coroutine[None, None, GetBlocksResponse]: ...

    def _get_blocks(
        self,
        sync: bool,
        from_block: int | None = None,
        page_size: int = 50,
        page_type: str = SolanaFMBlocksPaginationType.BLOCK_NUMBER.value,
        ascending: bool | None = None
    ) -> GetBlocksResponse | Coroutine[None, None, GetBlocksResponse]:
        """
            This function refers to the GET **[Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** API endpoint,
            and it is used to get the list of blocks according to input parameters.

            Parameters:
                from_block: The block number to start from.
                    If not provided, the latest block is returned.
                page_size: The number of blocks to return.
                page_type: The type of page to return.
                    The supported types are available on [`SolanaFMBlocksPaginationType`][cyhole.solana_fm.param.SolanaFMBlocksPaginationType].
                ascending: The order of the blocks.

            Returns:
                List of blocks.
        """
        # check param consistency
        SolanaFMBlocksPaginationType.check(page_type)

        # set params
        url = self.base_v0_url + "blocks"

        api_params = {
            "from": from_block,
            "pageSize": page_size,
            "paginationType": page_type,
            "reverse": ascending
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlocksResponse,
            params = api_params
        )

    @overload
    def _get_block(self, sync: Literal[True], block_number: int) -> GetBlockResponse: ...

    @overload
    def _get_block(self, sync: Literal[False], block_number: int) -> Coroutine[None, None, GetBlockResponse]: ...

    def _get_block(self, sync: bool, block_number: int) -> GetBlockResponse | Coroutine[None, None, GetBlockResponse]:
        """
            This function refers to the GET **[Block](https://docs.solana.fm/reference/get_block)** API endpoint,
            and it is used to get the block details for a given block Number.

            Parameters:
                block_number: The block number.

            Returns:
                Block details.
        """
        # set params
        url = self.base_v0_url + f"blocks/{block_number}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetBlockResponse
        )

    @overload
    def _post_multiple_blocks(self, sync: Literal[True], block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse: ...

    @overload
    def _post_multiple_blocks(self, sync: Literal[False], block_numbers: list[int], producer_details: bool = True) -> Coroutine[None, None, PostMultipleBlocksResponse]: ...

    def _post_multiple_blocks(self, sync: bool, block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse | Coroutine[None, None, PostMultipleBlocksResponse]:
        """
            This function refers to the POST **[Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** API endpoint,
            and it is used to get multiple blocks information from the SolanaFM API.

            Parameters:
                block_numbers: The list of block numbers to get.

            Returns:
                Block details.
        """
        # set params
        url = self.base_v0_url + "blocks"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        json = {
            "hydration": { "accountHash": producer_details },
            "blockNumbers": block_numbers,
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.POST.value,
            url = url,
            response_model = PostMultipleBlocksResponse,
            headers = headers,
            json = json
        )

    @overload
    def _get_solana_daily_transaction_fees(self, sync: Literal[True], dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse: ...

    @overload
    def _get_solana_daily_transaction_fees(self, sync: Literal[False], dt: datetime = datetime.now()) -> Coroutine[None, None, GetSolanaDailyTransactionFeesResponse]: ...

    def _get_solana_daily_transaction_fees(self, sync: bool, dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse | Coroutine[None, None, GetSolanaDailyTransactionFeesResponse]:
        """
            This function refers to the GET **[Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** API endpoint,
            and it is used to get the daily transaction fees for a given date on the whole Solana chain.

            Observe that if the date is not provided, the current date is used and the result could change over time 
            as the day is not finished yet.

            Parameters:
                dt: The date to get the transaction fees.
                    By default, the current date is used.

            Returns:
                Daily transaction fees.
        """
        # set params
        url = self.base_v0_url + "stats/tx-fees"

        api_params = {
            "date": dt.strftime("%d-%m-%Y")
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetSolanaDailyTransactionFeesResponse,
            params = api_params
        )

    @overload
    def _get_tagged_tokens_list(self, sync: Literal[True]) -> GetTaggedTokensListResponse: ...

    @overload
    def _get_tagged_tokens_list(self, sync: Literal[False]) -> Coroutine[None, None, GetTaggedTokensListResponse]: ...

    def _get_tagged_tokens_list(self, sync: bool) -> GetTaggedTokensListResponse | Coroutine[None, None, GetTaggedTokensListResponse]:
        """
            This function refers to the GET **[Tagged Tokens List](https://docs.solana.fm/reference/get_tokens_by_pagination)** API endpoint,
            and it is used to get the list of tagged tokens identified by the SolanaFM team (**not tokens indexed on-chain**).

            Returns:
                List of tagged tokens.
        """
        # set params
        url = self.base_v0_url + "tokens"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTaggedTokensListResponse
        )

    @overload
    def _get_token_info_v0(self, sync: Literal[True], address: str) -> GetTokenInfoV0Response: ...

    @overload
    def _get_token_info_v0(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenInfoV0Response]: ...

    def _get_token_info_v0(self, sync: bool, address: str) -> GetTokenInfoV0Response | Coroutine[None, None, GetTokenInfoV0Response]:
        """
            This function refers to the GET **[Token Info V0](https://docs.solana.fm/reference/get_token_by_account_hash)** API endpoint,
            and it is used to get the token information for a given token address.

            !!! info
                This endpoint refers to the **V0** version of the API.

            Parameters:
                address: The token address.

            Returns:
                Token information.
        """
        # set params
        url = self.base_v0_url + f"tokens/{address}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenInfoV0Response
        )

    @overload
    def _post_token_multiple_info_v0(self, sync: Literal[True], addresses: list[str]) -> PostTokenMultipleInfoV0Response: ...

    @overload
    def _post_token_multiple_info_v0(self, sync: Literal[False], addresses: list[str]) -> Coroutine[None, None, PostTokenMultipleInfoV0Response]: ...

    def _post_token_multiple_info_v0(self, sync: bool, addresses: list[str]) -> PostTokenMultipleInfoV0Response | Coroutine[None, None, PostTokenMultipleInfoV0Response]:
        """
            This function refers to the POST **[Token Multiple Info V0](https://docs.solana.fm/reference/get_tokens_by_account_hashes)** API endpoint,
            and it is used to get the token information for multiple token addresses.

            !!! info
                This endpoint refers to the **V0** version of the API.

            Parameters:
                addresses: The list of token addresses.

            Returns:
                Token information.
        """
        # set params
        url = self.base_v0_url + "tokens"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        json = {
            "hydration": { "accountHash": True },
            "tokenHashes": addresses
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.POST.value,
            url = url,
            response_model = PostTokenMultipleInfoV0Response,
            headers = headers,
            json = json
        )

    @overload
    def _get_token_info_v1(self, sync: Literal[True], address: str) -> GetTokenInfoV1Response: ...

    @overload
    def _get_token_info_v1(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenInfoV1Response]: ...

    def _get_token_info_v1(self, sync: bool, address: str) -> GetTokenInfoV1Response | Coroutine[None, None, GetTokenInfoV1Response]:
        """
            This function refers to the GET **[Token Info V1](https://docs.solana.fm/reference/get_one_token)** API endpoint,
            and it is used to get the token information for a given token address.

            !!! info
                This endpoint refers to the **V1** version of the API.

            Parameters:
                address: The token address.

            Returns:
                Token information.
        """
        # set params
        url = self.base_v1_url + f"tokens/{address}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenInfoV1Response
        )

    @overload
    def _post_token_multiple_info_v1(self, sync: Literal[True], addresses: list[str]) -> PostTokenMultipleInfoV1Response: ...

    @overload
    def _post_token_multiple_info_v1(self, sync: Literal[False], addresses: list[str]) -> Coroutine[None, None, PostTokenMultipleInfoV1Response]: ...

    def _post_token_multiple_info_v1(self, sync: bool, addresses: list[str]) -> PostTokenMultipleInfoV1Response | Coroutine[None, None, PostTokenMultipleInfoV1Response]:
        """
            This function refers to the POST **[Token Multiple Info V1](https://docs.solana.fm/reference/retrieve_multiple_tokens)** API endpoint,
            and it is used to get the token information for multiple token addresses.

            !!! info
                This endpoint refers to the **V1** version of the API.

            Parameters:
                addresses: The list of token addresses.

            Returns:
                Token information.
        """
        # set params
        url = self.base_v1_url + "tokens"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        json = {
            "tokens": addresses
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.POST.value, url, headers = headers, json = json)
            return PostTokenMultipleInfoV1Response(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.POST.value, url, headers = headers, json = json)
                return PostTokenMultipleInfoV1Response(tokens = content_raw.json())
            return async_request()

    @overload
    def _post_user_token_accounts(self, sync: Literal[True], address: str, include_sol_balance: bool = False, tokens: list[str] | None = None) -> PostUserTokenAccountsResponse: ...

    @overload
    def _post_user_token_accounts(self, sync: Literal[False], address: str, include_sol_balance: bool = False, tokens: list[str] | None = None) -> Coroutine[None, None, PostUserTokenAccountsResponse]: ...

    def _post_user_token_accounts(self, sync: bool, address: str, include_sol_balance: bool = False, tokens: list[str] | None = None) -> PostUserTokenAccountsResponse | Coroutine[None, None, PostUserTokenAccountsResponse]:
        """
            This function refers to the POST **[User Token Accounts](https://docs.solana.fm/reference/get_user_token_accounts)** API endpoint,
            and it is used to get the token accounts for a given user address.

            Parameters:
                address: The user address.
                include_sol_balance: Flag to include the Sol balance of the account.
                tokens: The list of token addresses to filter the accounts.

            Returns:
                Token accounts.
        """
        # set params
        url = self.base_v1_url + f"tokens/{address}/token-accounts"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        json = {
            "includeSolBalance": include_sol_balance,
            "tokenHashes": tokens
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.POST.value,
            url = url,
            response_model = PostUserTokenAccountsResponse,
            headers = headers,
            json = json
        )

    @overload
    def _get_mint_token_accounts(self, sync: Literal[True], address: str, page: int | None = None, page_size: int | None = None) -> GetMintTokenAccountsResponse: ...

    @overload
    def _get_mint_token_accounts(self, sync: Literal[False], address: str, page: int | None = None, page_size: int | None = None) -> Coroutine[None, None, GetMintTokenAccountsResponse]: ...

    def _get_mint_token_accounts(self, sync: bool, address: str, page: int | None = None, page_size: int | None = None) -> GetMintTokenAccountsResponse | Coroutine[None, None, GetMintTokenAccountsResponse]:
        """
            This function refers to the GET **[Mint Token Accounts](https://docs.solana.fm/reference/get_token_accounts_for_token_mint)** API endpoint,
            and it is used to get the token accounts owned by a given token mint address.

            Parameters:
                address: The token address.
                page: The page number.
                page_size: The number of accounts to return per page.

            Returns:
                Token accounts.
        """
        # set params
        url = self.base_v1_url + f"tokens/{address}/holders"

        api_params = {
            "page": page,
            "pageSize": page_size
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetMintTokenAccountsResponse,
            params = api_params
        )

    @overload
    def _get_on_chain_token_data(self, sync: Literal[True], address: str) -> GetOnChainTokenDataResponse: ...

    @overload
    def _get_on_chain_token_data(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetOnChainTokenDataResponse]: ...

    def _get_on_chain_token_data(self, sync: bool, address: str) -> GetOnChainTokenDataResponse | Coroutine[None, None, GetOnChainTokenDataResponse]:
        """
            This function refers to the GET **[On-Chain Token Data](https://docs.solana.fm/reference/get_tfi_token_data)** API endpoint,
            and it is used to get the token data for a given token address stored on-chain.

            Parameters:
                address: The token address.

            Returns:
                Token data.
        """
        # set params
        url = self.base_v1_url + f"tokens/{address}/info"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetOnChainTokenDataResponse
        )

    @overload
    def _get_token_supply(self, sync: Literal[True], address: str) -> GetTokenSupplyResponse: ...

    @overload
    def _get_token_supply(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenSupplyResponse]: ...

    def _get_token_supply(self, sync: bool, address: str) -> GetTokenSupplyResponse | Coroutine[None, None, GetTokenSupplyResponse]:
        """
            This function refers to the GET **[Token Supply](https://docs.solana.fm/reference/get_token_circulating_supply)** API endpoint,
            and it is used to get the token circulating supply for a given token address.

            Parameters:
                address: The token address.

            Returns:
                Token supply.
        """
        # set params
        url = self.base_v1_url + f"tokens/{address}/supply"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTokenSupplyResponse
        )

    @overload
    def _get_transfer_transactions(self, sync: Literal[True], transaction: str) -> GetTransferTransactionsResponse: ...

    @overload
    def _get_transfer_transactions(self, sync: Literal[False], transaction: str) -> Coroutine[None, None, GetTransferTransactionsResponse]: ...

    def _get_transfer_transactions(self, sync: bool, transaction: str) -> GetTransferTransactionsResponse | Coroutine[None, None, GetTransferTransactionsResponse]:
        """
            This function refers to the GET **[Transfer Transactions](https://docs.solana.fm/reference/get_transfers)** API endpoint,
            and it is used to get the list of transfer transactions for a given account according to input parameters.

            Parameters:
                transaction: The transaction hash.

            Returns:
                List of transfer transactions.
        """
        # set params
        url = self.base_v0_url + f"transfers/{transaction}"

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.GET.value,
            url = url,
            response_model = GetTransferTransactionsResponse
        )

    @overload
    def _post_multiple_transfer_transactions(self, sync: Literal[True], transactions: list[str]) -> PostMultipleTransferTransactionsResponse: ...

    @overload
    def _post_multiple_transfer_transactions(self, sync: Literal[False], transactions: list[str]) -> Coroutine[None, None, PostMultipleTransferTransactionsResponse]: ...

    def _post_multiple_transfer_transactions(self, sync: bool, transactions: list[str]) -> PostMultipleTransferTransactionsResponse | Coroutine[None, None, PostMultipleTransferTransactionsResponse]:
        """
            This function refers to the POST **[Multiple Transfer Transactions](https://docs.solana.fm/reference/post_transfers)** API endpoint,
            and it is used to get multiple transfer transactions information from the SolanaFM API.

            Parameters:
                transactions: The list of transaction hashes to get.

            Returns:
                Transfer transactions details.
        """
        # set params
        url = self.base_v0_url + "transfers"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        json = {
            "transactionHashes": transactions
        }

        # execute request
        return  self.api_return_model(
            sync = sync,
            type = RequestType.POST.value,
            url = url,
            response_model = PostMultipleTransferTransactionsResponse,
            headers = headers,
            json = json
        )

    @overload
    def _get_all_transfer_actions(self, sync: Literal[True]) -> GetAllTransferActionsResponse: ...

    @overload
    def _get_all_transfer_actions(self, sync: Literal[False]) -> Coroutine[None, None, GetAllTransferActionsResponse]: ...

    def _get_all_transfer_actions(self, sync: bool) -> GetAllTransferActionsResponse | Coroutine[None, None, GetAllTransferActionsResponse]:
        """
            This function refers to the GET **[All Transfer Actions](https://docs.solana.fm/reference/get_actions)** API endpoint,
            and it is used to get the list of all transfer actions on SolanaFM.

            Returns:
                List of all transfer actions.
        """
        # set params
        url = self.base_v1_url + "actions"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetAllTransferActionsResponse(actions = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetAllTransferActionsResponse(actions = content_raw.json())
            return async_request()