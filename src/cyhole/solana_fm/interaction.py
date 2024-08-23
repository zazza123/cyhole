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
    GetSolanaDailyTransactionFeesResponse
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
            This function refers to the **[Get Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** API endpoint, 
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
            This function refers to the **[Get Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** API endpoint,
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
            This function refers to the **[Get Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** API endpoint, 
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
            This function refers to the **[Get Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** API endpoint,
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
            This function refers to the **[Get Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** API endpoint,
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
            This function refers to the **[Get Block](https://docs.solana.fm/reference/get_block)** API endpoint,
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
            This function refers to the **[Post Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** API endpoint,
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
            This function refers to the **[Get Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** API endpoint,
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