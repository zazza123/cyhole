from requests.exceptions import HTTPError
from typing import Any, Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..jupiter.client import JupiterClient, JupiterAsyncClient
from ..jupiter.schema import (
    JupiterHTTPError,
    GetPriceResponse,
    GetQuoteInput,
    GetQuoteResponse,
    GetQuoteTokensResponse,
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    GetTokenListResponse,
    PostLimitOrderCreateBody,
    PostLimitOrderCreateResponse,
    PostLimitOrderCancelBody,
    PostLimitOrderCancelResponse,
    GetLimitOrderOpenResponse,
    GetLimitOrderHistoryResponse,
    GetLimitOrderTradeHistoryResponse
)
from ..jupiter.exception import (
    JupiterException,
    JupiterNoRouteFoundError,
    JupiterInvalidRequest
)
from ..jupiter.param import JupiterTokenListType

class Jupiter(Interaction):
    """
        Class used to connect [Jupiter](https://jup.ag) API, one of them most popular Solana DEX. 
        To have access Jupiter API is **not** required an API key.

        Check [https://station.jup.ag/docs/api](https://station.jup.ag/docs/api) for all the details on the available endpoints.

        **Example**

        ```python
        import asyncio
        from cyhole.jupiter import Jupiter
        from cyhole.core.address.solana import JUP

        jupiter = Jupiter()

        # Get current price of JUP on Solana
        # synchronous
        response = jupiter.client.get_price([JUP])
        print("Current JUP/USDC:", response.data[JUP].price)

        # asynchronous
        async def main() -> None:
            async with jupiter.async_client as client:
                response = await client.get_price([JUP])
                print("Current JUP/USDC:", response.data[JUP].price)

        asyncio.run(main())
        ```
    """

    def __init__(self, headers: Any | None = None) -> None:
        super().__init__(headers)

        # clients
        self.client = JupiterClient(self)
        self.async_client = JupiterAsyncClient(self)

        # API urls
        self.url_api_price = "https://price.jup.ag/v6/price"
        self.url_api_quote = "https://quote-api.jup.ag/v6/"
        self.url_api_token = "https://token.jup.ag/"
        self.url_api_limit = "https://jup.ag/api/limit/v1/"
        return

    @overload
    def _get_price(self, sync: Literal[True], address: list[str], vs_address: str | None = None) -> GetPriceResponse: ...

    @overload
    def _get_price(self, sync: Literal[False], address: list[str], vs_address: str | None = None) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(self, sync: bool, address: list[str], vs_address: str | None = None) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the **[Price](https://station.jup.ag/docs/apis/price-api)** API endpoint, 
            and it is used to get the current price of a list of tokens on Solana chain with respect to another token. 

            The API returns the unit buy price for the tokens; by default, the price is provided according to 
            the value of `USDC` token. It is also possible to provide another comparison token in the request.

            !!! info
                Observe that when the token address/symbol or comparison token address/symbol are not found, 
                the response provided will have an empty `data` object.

            Parameters:
                address: list of tokens involved in the request.
                    It is possible to provide the Solana tokens' addresses or their symbols. 
                    For example, `SOL` is equivalent to `So11111111111111111111111111111111111111112`.
                vs_address: comparison token address/symbol.
                    Default Value: `None` (`USDC`)

            Returns:
                tokens' prices.
        """
        # set params
        params = {
            "ids": ",".join(address),
            "vsToken": vs_address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, self.url_api_price, params = params)
            return GetPriceResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, self.url_api_price, params = params)
                return GetPriceResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_quote(self, sync: Literal[True], input: GetQuoteInput) -> GetQuoteResponse: ...

    @overload
    def _get_quote(self, sync: Literal[False], input: GetQuoteInput) -> Coroutine[None, None, GetQuoteResponse]: ...

    def _get_quote(self, sync: bool, input: GetQuoteInput) -> GetQuoteResponse | Coroutine[None, None, GetQuoteResponse]:
        """
            This function refers to the **[Get Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint, 
            and it is used to get a quote for swapping a specific amount of tokens.  
            The function can be combined with the `post_swap` to implement a payment mechanism.

            Parameters:
                input: an input schema used to describe the request.
                    More details in the object definition.

            Returns:
                Quote found by Jupiter API.
        """
        # set params
        url = self.url_api_quote + "quote"
        params = input.model_dump(
            by_alias = True, 
            exclude_defaults = True
        )

        # execute request
        if sync:
            try:
                content_raw = self.client.api(RequestType.GET.value, url, params = params)
            except HTTPError as e:
                raise self._raise(e)
            return GetQuoteResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                except HTTPError as e:
                    raise self._raise(e)
                return GetQuoteResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_quote_tokens(self, sync: Literal[True]) -> GetQuoteTokensResponse: ...

    @overload
    def _get_quote_tokens(self, sync: Literal[False]) -> Coroutine[None, None, GetQuoteTokensResponse]: ...

    def _get_quote_tokens(self, sync: bool) -> GetQuoteTokensResponse | Coroutine[None, None, GetQuoteTokensResponse]:
        """
            This function refers to the **[Get Quote Tokens](https://station.jup.ag/api-v6/get-tokens)** API endpoint, 
            and it is used to get the list of the current supported tradable tokens. 

            Returns:
                List of tradable tokens.
        """
        # set params
        url = self.url_api_quote + "tokens"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetQuoteTokensResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetQuoteTokensResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_quote_program_id_label(self, sync: Literal[True]) -> GetQuoteProgramIdLabelResponse: ...

    @overload
    def _get_quote_program_id_label(self, sync: Literal[False]) -> Coroutine[None, None, GetQuoteProgramIdLabelResponse]: ...

    def _get_quote_program_id_label(self, sync: bool) -> GetQuoteProgramIdLabelResponse | Coroutine[None, None, GetQuoteProgramIdLabelResponse]:
        """
            This function refers to the **[Get Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint, 
            and it is used to get the list of supported DEXes to use in quote endpoint. 

            Returns:
                List of DEXs addresses and labels.
        """
        # set params
        url = self.url_api_quote + "program-id-to-label"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetQuoteProgramIdLabelResponse(dexes = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetQuoteProgramIdLabelResponse(dexes = content_raw.json())
            return async_request()

    @overload
    def _post_swap(self, sync: Literal[True], body: PostSwapBody) -> PostSwapResponse: ...

    @overload
    def _post_swap(self, sync: Literal[False], body: PostSwapBody) -> Coroutine[None, None, PostSwapResponse]: ...

    def _post_swap(self, sync: bool, body: PostSwapBody) -> PostSwapResponse | Coroutine[None, None, PostSwapResponse]:
        """
            This function refers to the **[Post Swap](https://station.jup.ag/api-v6/post-swap)** API endpoint, 
            and it is used to recive the transaction to perform the swap initialised from `get_quote` 
            endopoint for the desired pair.  
            The function should be combined with the `get_quote` endpoint.

            Parameters:
                body: the body to sent to Jupiter API that describe the swap.
                    More details in the object definition.

            Returns:
                Transaction found by Jupiter API.
        """
        # set params
        url = self.url_api_quote + "swap"
        headers = {
            "Content-Type": "application/json"
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(
                    type = RequestType.POST.value,
                    url = url,
                    headers = headers,
                    json = body.model_dump(by_alias = True, exclude_defaults = True)
                )
            except HTTPError as e:
                raise self._raise(e)
            return PostSwapResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(
                        type = RequestType.POST.value,
                        url = url,
                        headers = headers,
                        json = body.model_dump(by_alias = True, exclude_defaults = True)
                    )
                except HTTPError as e:
                    raise self._raise(e)
                return PostSwapResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_list(self, sync: Literal[True], type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> GetTokenListResponse: ...

    @overload
    def _get_token_list(self, sync: Literal[False], type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> Coroutine[None, None, GetTokenListResponse]: ...

    def _get_token_list(self, sync: bool, type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> GetTokenListResponse | Coroutine[None, None, GetTokenListResponse]:
        """
            This function refers to the **[Token List](https://station.jup.ag/docs/token-list/token-list-api)** API endpoint, 
            and it is used to retrieved the list of tokens eligible for trading, managed by Jupiter.  
            Choose the tokens list according to `type` field.

            Parameters:
                type: Jupiter manages the tradable tokens through a set of tags in order to guarantee its 
                    core values and provide a secure service. There are two types of lists currently available:  
                    - Strict the most secure list that includes only the tokens with tags `old-registry`, `community`, or `wormhole`.
                    - All all the tokens are included expect the banned ones.
                    The supported types are available on [`JupiterTokenListType`][cyhole.jupiter.param.JupiterTokenListType].
                banned: this flag can be used **only** on `All` type, and it enables the inclusion of banned tokens.

            Returns:
                List of Jupiter's tokens list.
        """
        # check param consistency
        JupiterTokenListType.check(type)

        # set params
        url = self.url_api_token + type
        params = {
            "includeBanned" : banned
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenListResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenListResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _post_limit_order_create(self, sync: Literal[True], body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse: ...

    @overload
    def _post_limit_order_create(self, sync: Literal[False], body: PostLimitOrderCreateBody) -> Coroutine[None, None, PostLimitOrderCreateResponse]: ...

    def _post_limit_order_create(self, sync: bool, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse | Coroutine[None, None, PostLimitOrderCreateResponse]:
        """
            This function refers to the **[Post Limit Order - Create](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint, 
            and it is used to receive the transaction to perform the creation of a Limit Order via Jupiter API.

            Parameters:
                body: the body to sent to Jupiter API that describe the swap.
                    More details in the object definition.

            Returns:
                Transaction created by Jupiter API.
        """

        # set params
        url = self.url_api_limit + "createOrder"
        headers = {
            "Content-Type": "application/json"
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(
                    type = RequestType.POST.value,
                    url = url,
                    headers = headers,
                    json = body.model_dump(by_alias = True, exclude_defaults = True)
                )
            except HTTPError as e:
                raise self._raise(e)
            return PostLimitOrderCreateResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(
                        type = RequestType.POST.value,
                        url = url,
                        headers = headers,
                        json = body.model_dump(by_alias = True, exclude_defaults = True)
                    )
                except HTTPError as e:
                    raise self._raise(e)
                return PostLimitOrderCreateResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_limit_order_cancel(self, sync: Literal[True], body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse: ...

    @overload
    def _post_limit_order_cancel(self, sync: Literal[False], body: PostLimitOrderCancelBody) -> Coroutine[None, None, PostLimitOrderCancelResponse]: ...

    def _post_limit_order_cancel(self, sync: bool, body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse | Coroutine[None, None, PostLimitOrderCancelResponse]:
        """
            This function refers to the **[Post Limit Order - Cancel](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint, 
            and it is used to receive the transaction to perform the cancellation of a Limit Order previously 
            opened via Jupiter API.

            Parameters:
                body: the body to sent to Jupiter API that describe the limit order to cancel.
                    More details in the object definition.

            Returns:
                Transaction created by Jupiter API.
        """

        # set params
        url = self.url_api_limit + "cancelOrders"
        headers = {
            "Content-Type": "application/json"
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(
                    type = RequestType.POST.value,
                    url = url,
                    headers = headers,
                    json = body.model_dump(by_alias = True, exclude_defaults = True)
                )
            except HTTPError as e:
                raise self._raise(e)
            return PostLimitOrderCancelResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(
                        type = RequestType.POST.value,
                        url = url,
                        headers = headers,
                        json = body.model_dump(by_alias = True, exclude_defaults = True)
                    )
                except HTTPError as e:
                    raise self._raise(e)
                return PostLimitOrderCancelResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_limit_order_open(
            self,
            sync: Literal[True],
            wallet: str | None = None,
            input_token: str | None = None,
            output_token: str | None = None
        ) -> GetLimitOrderOpenResponse: ...

    @overload
    def _get_limit_order_open(
            self,
            sync: Literal[False],
            wallet: str | None = None,
            input_token: str | None = None,
            output_token: str | None = None
        ) -> Coroutine[None, None, GetLimitOrderOpenResponse]: ...

    def _get_limit_order_open(
        self,
        sync: bool,
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None
    ) -> GetLimitOrderOpenResponse | Coroutine[None, None, GetLimitOrderOpenResponse]:
        """
            This function refers to the **[Get Limit Order - Open](https://station.jup.ag/docs/limit-order/limit-order-api)** 
            API endpoint, and it is used to receive the current open limit orders related to a wallet, input token 
            or output token via Jupiter API. 

            Observe that all the input parameters are optional; if for example, only the `input_token` is provided, 
            then **all** the limit orders having that input token address are returned (if available).

            Parameters:
                wallet: address of the wallet to check.
                input_token: address of the input token associated to the limit order.
                output_token: address of the output token associated to the limit order.

            Returns:
                Open limit orders created by Jupiter API.
        """
        # set params
        url = self.url_api_limit + "openOrders"
        params = {
            "wallet": wallet,
            "inputMint": input_token,
            "outputMint": output_token
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetLimitOrderOpenResponse(orders = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetLimitOrderOpenResponse(orders = content_raw.json())
            return async_request()

    @overload
    def _get_limit_order_history(
        self,
        sync: Literal[True],
        wallet: str,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderHistoryResponse: ...

    @overload
    def _get_limit_order_history(
        self,
        sync: Literal[False],
        wallet: str,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> Coroutine[None, None, GetLimitOrderHistoryResponse]: ...

    def _get_limit_order_history(
        self,
        sync: bool,
        wallet: str,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderHistoryResponse | Coroutine[None, None, GetLimitOrderHistoryResponse]:
        """
            This function refers to the **[Get Limit Order - History](https://station.jup.ag/docs/limit-order/limit-order-api)** 
            API endpoint, and it is used to retrieve the history of Limit Orders associated to a wallet via Jupiter API. 

            Parameters:
                wallet: address of the wallet to check.
                cursor: specify which 'page' of orders to return.
                skip: specify the number of order to skip (from the top).
                take: specify the number of orders to return.

            Returns:
                History of limit orders associated to the input wallet.
        """
        # set params
        url = self.url_api_limit + "orderHistory"
        params = {
            "wallet": wallet,
            "cursor": cursor,
            "skip": skip,
            "take": take
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetLimitOrderHistoryResponse(orders = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetLimitOrderHistoryResponse(orders = content_raw.json())
            return async_request()

    @overload
    def _get_limit_order_trade_history(
        self,
        sync: Literal[True],
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderTradeHistoryResponse: ...

    @overload
    def _get_limit_order_trade_history(
        self,
        sync: Literal[False],
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> Coroutine[None, None, GetLimitOrderTradeHistoryResponse]: ...

    def _get_limit_order_trade_history(
        self,
        sync: bool,
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderTradeHistoryResponse | Coroutine[None, None, GetLimitOrderTradeHistoryResponse]:
        """
            This function refers to the **[Get Limit Order - Trade History](https://station.jup.ag/docs/limit-order/limit-order-api)** 
            API endpoint, and it is used to retrieve the trades history related to Limit Orders extracted with specific 
            requirements via Jupiter API. 

            Parameters:
                wallet: address of the wallet to check.
                input_token: address of the input token associated to the limit order.
                output_token: address of the output token associated to the limit order.
                cursor: specify which 'page' of orders to return.
                skip: specify the number of order to skip (from the top).
                take: specify the number of orders to return.

            Returns:
                Hostory of limit orders associated to the input wallet.
        """
        # set params
        url = self.url_api_limit + "tradeHistory"
        params = {
            "wallet": wallet,
            "inputMint": input_token,
            "outputMint": output_token,
            "cursor": cursor,
            "skip": skip,
            "take": take
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetLimitOrderTradeHistoryResponse(orders = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetLimitOrderTradeHistoryResponse(orders = content_raw.json())
            return async_request()

    def _raise(self, exception: HTTPError) -> JupiterException:
        """
            Internal function used to raise the correct 
            Jupiter exception according to the error code 
            provided by the API.

            Parameters:
                exception: the HTTP error returned from Jupiter API.

            Raises:
                JupiterNoRouteFoundError: for error code `COULD_NOT_FIND_ANY_ROUTE` 
                    during the creation of a quote.
                JupiterInvalidRequest: for error code `INVALID_REQUEST`.
                JupiterException: general exception raised when an unknown 
                    error code is found or a different error is found.
        """
        try:
            error = JupiterHTTPError(**exception.response.json())
            match error.code:
                case "COULD_NOT_FIND_ANY_ROUTE":
                    return JupiterNoRouteFoundError(error.msg)
                case "INVALID_REQUEST":
                    return JupiterInvalidRequest(error.msg)
                case _:
                    return JupiterException(error.model_dump_json())
        except Exception:
            return JupiterException(exception.response.content.decode())