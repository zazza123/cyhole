import os
from typing import Coroutine, Literal, overload

from ...core.param import RequestType
from ...core.interaction import Interaction
from ...core.exception import MissingAPIKeyError
from ...solscan.v2.client import SolscanClient, SolscanAsyncClient
from ...solscan.v2.param import (
    SolscanPageSizeType,
    SolscanAccountType
)
from ...solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse,
    GetAccountTokenNFTAccountResponse
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