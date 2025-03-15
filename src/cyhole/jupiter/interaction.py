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
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    GetTokenInfoResponse,
    GetTokenMarketMintsResponse,
    GetTokenTaggedResponse,
    GetTokenNewResponse,
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
from ..jupiter.param import JupiterTokenTagType

class Jupiter(Interaction):
    """
        Class used to connect [Jupiter](https://jup.ag) API, one of them most popular Solana DEX. 
        To have access Jupiter API is **not** required an API key.

        Check [https://station.jup.ag/docs/api](https://station.jup.ag/docs/api) for all the details on the available endpoints.

        **Example**

        ```python
        import asyncio
        from cyhole.jupiter import Jupiter
        from cyhole.core.token.solana import JUP

        jupiter = Jupiter()

        # Get current price of JUP on Solana
        # synchronous
        response = jupiter.client.get_price([JUP.address])
        print("Current JUP/USDC:", response.data[JUP.address].price)

        # asynchronous
        async def main() -> None:
            async with jupiter.async_client as client:
                response = await client.get_price([JUP.address])
                print("Current JUP/USDC:", response.data[JUP.address].price)

        asyncio.run(main())
        ```
    """

    def __init__(self, headers: Any | None = None) -> None:
        super().__init__(headers)

        # clients
        self.client = JupiterClient(self)
        self.async_client = JupiterAsyncClient(self)

        # API urls
        self.url_api_price = "https://api.jup.ag/price/v2"
        self.url_api_quote = "https://api.jup.ag/swap/v1/"
        self.url_api_token = "https://api.jup.ag/tokens/v1/"
        self.url_api_limit = "https://jup.ag/api/limit/v1/"
        return

    @overload
    def _get_price(self, sync: Literal[True], address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse: ...

    @overload
    def _get_price(self, sync: Literal[False], address: list[str], extra_info: bool = False, vs_address: str | None = None) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(self, sync: bool, address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the GET **[Price](https://station.jup.ag/docs/utility/price-api)** API endpoint, 
            and it is used to get the current price of a list of tokens on Solana chain with respect to another token
            taken from [Jupiter Swap](https://jup.ag).

            The API returns the unit buy price for the tokens; by default, the price is provided according to 
            the value of `USDC` token. It is also possible to provide another comparison token in the request.

            !!! info
                Observe that when the token address or comparison token address are not found, 
                the response provided will have a `data` object with the token address as key and
                the value will be `None`.

            Parameters:
                address: list of tokens addresses to get the price.
                    For example, `So11111111111111111111111111111111111111112`.
                extra_info: flag to include extra information in the response
                    that could be useful fot analysis (e.g., last swap, current quote price).
                    More important, if activated, then `vs_address` is ignored.
                vs_address: comparison token address.
                    Default Value: `None` (`USDC`)

            Returns:
                tokens' prices.
        """

        # extra_info consistency
        if extra_info:
            vs_address = None

        # set params
        params = {
            "ids": ",".join(address),
            "vsToken": vs_address,
            "showExtraInfo": "true" if extra_info else "false"
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
            This function refers to the GET **[Quote](https://station.jup.ag/docs/api/quote)** API endpoint, 
            and it is used to get a quote for swapping a specific amount of tokens.  
            The function can be combined with the `post_swap` enpdpoint to implement a payment mechanism.

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
    def _get_quote_program_id_label(self, sync: Literal[True]) -> GetQuoteProgramIdLabelResponse: ...

    @overload
    def _get_quote_program_id_label(self, sync: Literal[False]) -> Coroutine[None, None, GetQuoteProgramIdLabelResponse]: ...

    def _get_quote_program_id_label(self, sync: bool) -> GetQuoteProgramIdLabelResponse | Coroutine[None, None, GetQuoteProgramIdLabelResponse]:
        """
            This function refers to the GET **[Quote Program ID to Label](https://api.jup.ag/swap/v1/program-id-to-label)** API endpoint, 
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
            This function refers to the POST **[Swap](https://station.jup.ag/api-v6/post-swap)** API endpoint, 
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
    def _get_token_info(self, sync: Literal[True], address: str) -> GetTokenInfoResponse: ...

    @overload
    def _get_token_info(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenInfoResponse]: ...

    def _get_token_info(self, sync: bool, address: str) -> GetTokenInfoResponse | Coroutine[None, None, GetTokenInfoResponse]:
        """
            This function refers to the GET **[Token](https://station.jup.ag/docs/api/token-information)** API endpoint,
            with a specific focus on retrieving the information of a token given its address.

            Parameters:
                address: address of the token to check.
                    For example, `So11111111111111111111111111111111111111112`.

            Returns:
                Information of the token.
        """
        # set url
        url = self.url_api_token + address

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetTokenInfoResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetTokenInfoResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_market_mints(self, sync: Literal[True], address: str) -> GetTokenMarketMintsResponse: ...

    @overload
    def _get_token_market_mints(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenMarketMintsResponse]: ...

    def _get_token_market_mints(self, sync: bool, address: str) -> GetTokenMarketMintsResponse | Coroutine[None, None, GetTokenMarketMintsResponse]:
        """
            This function refers to the GET **[Token Market Mints](https://station.jup.ag/docs/api/mints-in-market)** API endpoint,
            and can be used to retrieve the list of token addresses that belong to a market/pool address.

            Parameters:
                address: address of the market/pool to check.

            Returns:
                List of token addresses.
        """
        # set url
        url = self.url_api_token + f"market/{address}/mints"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetTokenMarketMintsResponse(mints = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetTokenMarketMintsResponse(mints = content_raw.json())
            return async_request()

    @overload
    def _get_token_tagged(self, sync: Literal[True], tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse: ...

    @overload
    def _get_token_tagged(self, sync: Literal[False], tag: str | JupiterTokenTagType) -> Coroutine[None, None, GetTokenTaggedResponse]: ...

    def _get_token_tagged(self, sync: bool, tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse | Coroutine[None, None, GetTokenTaggedResponse]:
        """
            This function refers to the GET **[Tagged Token](https://station.jup.ag/docs/api/tagged)** API endpoint, 
            and it is used to retrieved the list of tokens eligible for trading, managed by Jupiter.  
            Choose the tokens list according to `tag` field.

            Parameters:
                tag: Jupiter manages the tradable tokens through a set of tags in order to guarantee its 
                    core values and provide a secure service. The supported tages are available on [`JupiterTokenTagType`][cyhole.jupiter.param.JupiterTokenTagType].

            Returns:
                List of Jupiter's tokens list.
        """
        # check param consistency
        tag_str = tag if isinstance(tag, str) else tag.value
        JupiterTokenTagType.check(tag_str)

        # set params
        url = self.url_api_token + "tagged/" + tag_str

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetTokenTaggedResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetTokenTaggedResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_token_new(self, sync: Literal[True], limit: int = 10, offset: int | None = None) -> GetTokenNewResponse: ...

    @overload
    def _get_token_new(self, sync: Literal[False], limit: int = 10, offset: int | None = None) -> Coroutine[None, None, GetTokenNewResponse]: ...

    def _get_token_new(self, sync: bool, limit: int = 10, offset: int | None = None) -> GetTokenNewResponse | Coroutine[None, None, GetTokenNewResponse]:
        """
            This function refers to the GET **[New Token](https://station.jup.ag/docs/api/new)** API endpoint, 
            and it is used to retrieved the list of new tokens managed by Jupiter.

            Parameters:
                limit: number of tokens to retrieve.
                offset: number of tokens to skip.

            Returns:
                List of Jupiter's tokens list.
        """
        # set params
        url = self.url_api_token + "new"
        params = {
            "limit": limit,
            "offset": offset
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenNewResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenNewResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _post_limit_order_create(self, sync: Literal[True], body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse: ...

    @overload
    def _post_limit_order_create(self, sync: Literal[False], body: PostLimitOrderCreateBody) -> Coroutine[None, None, PostLimitOrderCreateResponse]: ...

    def _post_limit_order_create(self, sync: bool, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse | Coroutine[None, None, PostLimitOrderCreateResponse]:
        """
            This function refers to the POST **[Limit Order - Create](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint, 
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
            This function refers to the POST **[Limit Order - Cancel](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint, 
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
            This function refers to the GET **[Limit Order - Open](https://station.jup.ag/docs/limit-order/limit-order-api)** 
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
            This function refers to the GET **[Limit Order - History](https://station.jup.ag/docs/limit-order/limit-order-api)** 
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
            This function refers to the GET **[Limit Order - Trade History](https://station.jup.ag/docs/limit-order/limit-order-api)** 
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