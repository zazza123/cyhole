from requests.exceptions import HTTPError
from typing import Any, Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..jupiter.client import JupiterClient, JupiterAsyncClient
from ..jupiter.schema import (
    JupiterHTTPError,
    # Price API
    GetPriceResponse,
    # Swap API
    GetQuoteParams,
    GetQuoteResponse,
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    PostSwapInstructionsResponse,
    # Token API
    GetTokenInfoResponse,
    GetTokenMarketMintsResponse,
    GetTokenTaggedResponse,
    GetTokenNewResponse,
    # Limit Order API
    PostLimitOrderCreateBody,
    PostLimitOrderCreateResponse,
    PostLimitOrderCancelBody,
    PostLimitOrderCancelResponse,
    GetLimitOrderOpenResponse,
    GetLimitOrderHistoryResponse,
    # Ultra API
    GetUltraOrderResponse,
    GetUltraBalancesResponse,
    PostUltraExecuteOrderResponse,
    # Trigger API
    PostTriggerCreateOrderBody,
    PostTriggerCreateOrderResponse,
    PostTriggerExecuteResponse,
    PostTriggerCancelOrderResponse,
)
from ..jupiter.exception import (
    JupiterException,
    JupiterNoRouteFoundError,
    JupiterComputeAmountThresholdError,
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
        self.url_api_swap  = "https://api.jup.ag/swap/v1/"
        self.url_api_token = "https://api.jup.ag/tokens/v1/"
        self.url_api_limit = "https://api.jup.ag/limit/v2/"
        self.url_api_ultra = "https://api.jup.ag/ultra/v1/"
        self.url_api_trigger = "https://api.jup.ag/trigger/v1/"
        return

    @overload
    def _get_price(self, sync: Literal[True], address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse: ...

    @overload
    def _get_price(self, sync: Literal[False], address: list[str], extra_info: bool = False, vs_address: str | None = None) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(self, sync: bool, address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the GET **[Price](https://station.jup.ag/docs/api/price-api/price)** API endpoint, 
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
    def _get_quote(self, sync: Literal[True], input: GetQuoteParams) -> GetQuoteResponse: ...

    @overload
    def _get_quote(self, sync: Literal[False], input: GetQuoteParams) -> Coroutine[None, None, GetQuoteResponse]: ...

    def _get_quote(self, sync: bool, input: GetQuoteParams) -> GetQuoteResponse | Coroutine[None, None, GetQuoteResponse]:
        """
            This function refers to the GET **[Quote](https://station.jup.ag/docs/api/swap-api/quote)** API endpoint, 
            and it is used to get a quote for swapping a specific amount of tokens.  
            The function can be combined with the `post_swap` enpdpoint to implement a payment mechanism.

            Parameters:
                input: an input schema used to describe the request.
                    More details in the object definition.

            Returns:
                Quote found by Jupiter API.
        """
        # set params
        url = self.url_api_swap + "quote"
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
            This function refers to the GET **[Quote Program ID to Label](https://station.jup.ag/docs/api/swap-api/program-id-to-label)** API endpoint, 
            and it is used to get the list of supported DEXes to use in quote endpoint. 

            Returns:
                List of DEXs addresses and labels.
        """
        # set params
        url = self.url_api_swap + "program-id-to-label"

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
    def _post_swap(self, sync: Literal[True], body: PostSwapBody, with_instructions: Literal[False]) -> PostSwapResponse: ...

    @overload
    def _post_swap(self, sync: Literal[True], body: PostSwapBody, with_instructions: Literal[True]) -> PostSwapInstructionsResponse: ...

    @overload
    def _post_swap(self, sync: Literal[False], body: PostSwapBody, with_instructions: Literal[False]) -> Coroutine[None, None, PostSwapResponse]: ...

    @overload
    def _post_swap(self, sync: Literal[False], body: PostSwapBody, with_instructions: Literal[True]) -> Coroutine[None, None, PostSwapInstructionsResponse]: ...

    def _post_swap(self, sync: bool, body: PostSwapBody, with_instructions: bool = False) -> PostSwapResponse | PostSwapInstructionsResponse | Coroutine[None, None, PostSwapResponse | PostSwapInstructionsResponse]:
        """
            This function refers to the POST **[Swap](https://station.jup.ag/docs/api/swap-api/swap)** API endpoint, 
            and it is used to recive the transaction to perform the swap initialised from Jupiter client 
            `get_quote` endpoint for the desired pair; for this reason the function should be combined 
            with the `get_quote` endpoint.

            Jupiter API provides also the possibility to retrieve only the instructions to perform the swap 
            without the transaction. This is useful to check the instructions before performing the swap, 
            and in case of need, to modify the instructions before sending the transaction. This behaviour 
            can be activated by setting the `with_instructions` flag to `True`. Observe that in this case, 
            the response will be different from the standard swap response. In Jupiter's API documentation,
            this endpoint is referred to the POST **[Swap Instructions](https://station.jup.ag/docs/api/swap-api/swap-instructions)**.

            Parameters:
                body: the body to sent to Jupiter API that describe the swap.
                    More details in the object definition.
                with_instructions: flag to receive only the instructions to perform the swap.

            Returns:
                Transaction found by Jupiter API in case `with_instructions` is `False`, 
                otherwise instructions to perform the swap.
        """
        # set params
        url = self.url_api_swap + "swap"
        response_model_class = PostSwapResponse
        headers = {
            "Content-Type": "application/json"
        }

        # check instructions
        if with_instructions:
            url += "-instructions"
            response_model_class = PostSwapInstructionsResponse

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
            return response_model_class(**content_raw.json())
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
                return response_model_class(**content_raw.json())
            return async_request()

    @overload
    def _get_token_info(self, sync: Literal[True], address: str) -> GetTokenInfoResponse: ...

    @overload
    def _get_token_info(self, sync: Literal[False], address: str) -> Coroutine[None, None, GetTokenInfoResponse]: ...

    def _get_token_info(self, sync: bool, address: str) -> GetTokenInfoResponse | Coroutine[None, None, GetTokenInfoResponse]:
        """
            This function refers to the GET **[Token](https://station.jup.ag/docs/api/token-api/token-information)** API endpoint,
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
            This function refers to the GET **[Token Market Mints](https://station.jup.ag/docs/api/token-api/mints-in-market)** API endpoint,
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
            This function refers to the GET **[Tagged Token](https://station.jup.ag/docs/api/token-api/tagged)** API endpoint, 
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
            This function refers to the GET **[New Token](https://station.jup.ag/docs/api/token-api/new)** API endpoint, 
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
            This function refers to the POST **[Limit Order - Create](https://station.jup.ag/docs/swap-api/limit-order-api#create-limit-order-transaction)** API endpoint, 
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
                    json = body.model_dump(by_alias = True, exclude_defaults = True, exclude_none = True)
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
                        json = body.model_dump(by_alias = True, exclude_defaults = True, exclude_none = True)
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
            This function refers to the POST **[Limit Order - Cancel](https://station.jup.ag/docs/swap-api/limit-order-api#cancel-limit-order-transaction)** 
            API endpoint, and it is used to receive the transaction to perform the cancellation of a Limit Order previously opened via Jupiter API.

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
    def _get_limit_order_open(self, sync: Literal[True], wallet: str, input_token: str | None = None, output_token: str | None = None) -> GetLimitOrderOpenResponse: ...

    @overload
    def _get_limit_order_open(self, sync: Literal[False], wallet: str, input_token: str | None = None, output_token: str | None = None) -> Coroutine[None, None, GetLimitOrderOpenResponse]: ...

    def _get_limit_order_open(self, sync: bool, wallet: str, input_token: str | None = None, output_token: str | None = None) -> GetLimitOrderOpenResponse | Coroutine[None, None, GetLimitOrderOpenResponse]:
        """
            This function refers to the GET **[Limit Order - Open](https://station.jup.ag/docs/swap-api/limit-order-api#view-open-orders)** 
            API endpoint, and it is used to receive the current open limit orders related to a wallet, input token 
            or output token via Jupiter API. 

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
    def _get_limit_order_history(self, sync: Literal[True], wallet: str, page: int = 1) -> GetLimitOrderHistoryResponse: ...

    @overload
    def _get_limit_order_history(self, sync: Literal[False], wallet: str, page: int = 1) -> Coroutine[None, None, GetLimitOrderHistoryResponse]: ...

    def _get_limit_order_history(self, sync: bool, wallet: str, page: int = 1) -> GetLimitOrderHistoryResponse | Coroutine[None, None, GetLimitOrderHistoryResponse]:
        """
            This function refers to the GET **[Limit Order - History](https://station.jup.ag/docs/swap-api/limit-order-api#view-order-history)** 
            API endpoint, and it is used to retrieve the history of Limit Orders associated to a wallet via Jupiter API. 

            Parameters:
                wallet: address of the wallet to check.
                page: specify which 'page' of orders to return.

            Returns:
                History of limit orders associated to the input wallet.
        """
        # set params
        url = self.url_api_limit + "orderHistory"
        params = {
            "wallet": wallet,
            "page": page
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetLimitOrderHistoryResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetLimitOrderHistoryResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ultra_order(self, sync: Literal[True], input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse: ...

    @overload
    def _get_ultra_order(self, sync: Literal[False], input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> Coroutine[None, None, GetUltraOrderResponse]: ...

    def _get_ultra_order(self, sync: bool, input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse | Coroutine[None, None, GetUltraOrderResponse]:
        """
            This function refers to the GET **[Ultra - Get Order](https://station.jup.ag/docs/ultra-api/get-order)** API endpoint, 
            and it is used to create a swap order using the Jupiter Ultra API. This API was designed to facilitate 
            the creation of a swap order without the need to use the `get_quote` endpoint. In fact, the Ultra API 
            was created over the Swap API to provide a more direct way to create a swap order. This endpoint 
            can be then combined with the `post_ultra_execute_order` endpoint to perform the swap.

            Parameters:
                input_token: address of the input token.
                output_token: address of the output token.
                input_amount: amount of input token to swap.
                    The amount to swap **must** be factored in the token decimals. 
                    For example, if the token has 6 decimals, then `1.0` = `1_000_000`.
                taker_wallet_key: address of the taker wallet. 
                    If the `taker_wallet_key` is not provided, then the response will have `transaction_id` equals `None`.

            Returns:
                Order information provided by Jupiter API.
        """
        # set params
        url = self.url_api_ultra + "order"
        params = {
            "inputMint": input_token,
            "outputMint": output_token,
            "amount": input_amount,
            "taker": taker_wallet_key
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(RequestType.GET.value, url, params = params)
            except HTTPError as e:
                raise self._raise(e)
            return GetUltraOrderResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                except HTTPError as e:
                    raise self._raise(e)
                return GetUltraOrderResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_ultra_execute_order(self, sync: Literal[True], signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse: ...

    @overload
    def _post_ultra_execute_order(self, sync: Literal[False], signed_transaction_id: str, request_id: str) -> Coroutine[None, None, PostUltraExecuteOrderResponse]: ...

    def _post_ultra_execute_order(self, sync: bool, signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse | Coroutine[None, None, PostUltraExecuteOrderResponse]:
        """
            This function refers to the POST **[Ultra - Execute Order](https://station.jup.ag/docs/ultra-api/execute-order)** API endpoint, 
            and it is used to execute a swap order created using the Jupiter Ultra API "GET Order" endpoint (`get_ultra_order`). 

            First, it is required to initialize a swap order using the `get_ultra_order` endpoint. From the response, 
            is possible to get the Request ID (`GetUltraOrderResponse.request_id`) and the transaction ID (`GetUltraOrderResponse.transaction_id`).
            The transaction ID **must** be then signed by the payer walled to get the `signed_transaction_id` that can be then used
            to execute the swap order.

            Parameters:
                signed_transaction_id: the transaction ID coming from the `get_ultra_order` response **signed** by the payer wallet.
                request_id: the same request ID coming from the `get_ultra_order` response.

            Returns:
                Swap order execution information provided by Jupiter API.
        """
        # set params
        url = self.url_api_ultra + "execute"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "signedTransaction": signed_transaction_id,
            "requestId": request_id
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostUltraExecuteOrderResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostUltraExecuteOrderResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ultra_balances(self, sync: Literal[True], wallet_public_key: str) -> GetUltraBalancesResponse: ...

    @overload
    def _get_ultra_balances(self, sync: Literal[False], wallet_public_key: str) -> Coroutine[None, None, GetUltraBalancesResponse]: ...

    def _get_ultra_balances(self, sync: bool, wallet_public_key: str) -> GetUltraBalancesResponse | Coroutine[None, None, GetUltraBalancesResponse]:
        """
            This function refers to the GET **[Ultra - Balances](https://station.jup.ag/docs/ultra-api/get-balances)** API endpoint, 
            and it is used to retrieve the token's balances of a wallet using the Jupiter Ultra API.

            Parameters:
                wallet_public_key: public key of the wallet to check.

            Returns:
                Token's balances of the wallet.
        """
        # set params
        url = self.url_api_ultra + f"balances/{wallet_public_key}"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetUltraBalancesResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetUltraBalancesResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _post_trigger_create_order(self, sync: Literal[True], body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse: ...

    @overload
    def _post_trigger_create_order(self, sync: Literal[False], body: PostTriggerCreateOrderBody) -> Coroutine[None, None, PostTriggerCreateOrderResponse]: ...

    def _post_trigger_create_order(self, sync: bool, body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse | Coroutine[None, None, PostTriggerCreateOrderResponse]:
        """
            This function refers to the POST **[Trigger - Create Order](https://station.jup.ag/docs/api/trigger-api/create-order)** API endpoint, 
            and it is used to receive an unsigned transaction to perform the creation of an order via Jupiter API.

            Parameters:
                body: the body to sent to Jupiter API that describe the order.
                    More details in the object definition.

            Returns:
                **Unsigned** transaction created by Jupiter API.
        """

        # set params
        url = self.url_api_trigger + "createOrder"
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
                    json = body.model_dump(by_alias = True, exclude_defaults = True, exclude_none = True)
                )
            except HTTPError as e:
                raise self._raise(e)
            return PostTriggerCreateOrderResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(
                        type = RequestType.POST.value,
                        url = url,
                        headers = headers,
                        json = body.model_dump(by_alias = True, exclude_defaults = True, exclude_none = True)
                    )
                except HTTPError as e:
                    raise self._raise(e)
                return PostTriggerCreateOrderResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_trigger_execute(self, sync: Literal[True], signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse: ...

    @overload
    def _post_trigger_execute(self, sync: Literal[False], signed_transaction_id: str, request_id: str) -> Coroutine[None, None, PostTriggerExecuteResponse]: ...

    def _post_trigger_execute(self, sync: bool, signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse | Coroutine[None, None, PostTriggerExecuteResponse]:
        """
            This function refers to the POST **[Trigger - Execute](https://station.jup.ag/docs/api/trigger-api/execute)** API endpoint, 
            and it is used to execute an order created using the Jupiter Ultra API POST "Trigger - Create Order" endpoint (`post_trigger_create_order`). 

            First, it is required to create a order using the `post_trigger_create_order` endpoint. From the response, 
            is possible to get the Request ID (`PostTriggerCreateOrderResponse.request_id`) and the transaction ID (`PostTriggerCreateOrderResponse.transaction_id`).
            The transaction ID **must** be then signed by the payer walled to get the `signed_transaction_id` that can be then used
            to execute the order.

            The execute endpoint is not used only for creating an order, but it can be also used combined with `post_trigger_cancel_order` 
            to cancel one or more orders.

            Parameters:
                signed_transaction_id: the transaction ID coming from the `post_trigger_create_order` response **signed** by the payer wallet.
                request_id: the same request ID coming from the `post_trigger_create_order` response.

            Returns:
                Order execution information provided by Jupiter API.
        """
        # set params
        url = self.url_api_ultra + "execute"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "signedTransaction": signed_transaction_id,
            "requestId": request_id
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostTriggerExecuteResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostTriggerExecuteResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_trigger_cancel_order(self, sync: Literal[True], user_public_key: str, orders: str | list[str], compute_unit_price: str = 'auto') -> PostTriggerCancelOrderResponse: ...

    @overload
    def _post_trigger_cancel_order(self, sync: Literal[False], user_public_key: str, orders: str | list[str], compute_unit_price: str = 'auto') -> Coroutine[None, None, PostTriggerCancelOrderResponse]: ...

    def _post_trigger_cancel_order(self, sync: bool, user_public_key: str, orders: str | list[str], compute_unit_price: str = 'auto') -> PostTriggerCancelOrderResponse | Coroutine[None, None, PostTriggerCancelOrderResponse]:
        """
            This function refers to the POST **[Trigger - Cancel Order](https://station.jup.ag/docs/api/trigger-api/cancel-order)** API endpoint, 
            and it is used to cancel one or more orders created using the Jupiter Ultra API POST "Trigger - Create Order" endpoint (`post_trigger_create_order`). 

            This endpoint do not directly cancel the order, but it provides the transaction and request ID to it.
            Similarly to the `post_trigger_create_order` endpoint, the transaction ID **must** be signed by the payer walled to get the `signed_transaction_id`
            that can be then used to cancel the order by providing it together with the request ID to the `post_trigger_execute` endpoint.

            Note:
                The endpoint switches to POST **[Trigger - Cancel Orders](https://station.jup.ag/docs/api/trigger-api/cancel-orders)** 
                if more than one order is provided. The logic and response do not change.

            Parameters:
                user_public_key: Public Key of the Owner wallet.
                compute_unit_price: used to determine a transaction's prioritization fee. Defaults to `auto`.
                orders: List of orders Public Keys to cancel.

            Returns:
                Order cancellation information provided by Jupiter API.
        """

        # set params
        url = self.url_api_trigger + "cancelOrder"
        headers = {
            "Content-Type": "application/json"
        }
        body: dict[str, str | list[str]] = {
            "maker": user_public_key,
            "computeUnitPrice": compute_unit_price
        }

        # switch to multiple orders
        if isinstance(orders, list):
            url += "s"
            body["orders"] = orders
        else:
            body["order"] = orders

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostTriggerCancelOrderResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostTriggerCancelOrderResponse(**content_raw.json())
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
                case "CANNOT_COMPUTE_OTHER_AMOUNT_THRESHOLD":
                    return JupiterComputeAmountThresholdError(error.msg)
                case "INVALID_REQUEST":
                    return JupiterInvalidRequest(error.msg)
                case _:
                    return JupiterException(error.model_dump_json())
        except Exception:
            return JupiterException(exception.response.content.decode())