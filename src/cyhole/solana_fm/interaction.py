import os
from typing import Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..solana_fm.client import SolanaFMClient, SolanaFMAsyncClient
from ..solana_fm.schema import (
    GetAccountTransactionsParam,
    GetAccountTransactionsResponse,
    GetAccountTransfersParam,
    GetAccountTransfersResponse,
    GetAccountTransfersCsvExportParam,
    GetAccountTransfersCsvExportResponse
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
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTransactionsResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTransactionsResponse(**content_raw.json())
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
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = api_params)
            return GetAccountTransfersResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = api_params)
                return GetAccountTransfersResponse(**content_raw.json())
            return async_request()

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