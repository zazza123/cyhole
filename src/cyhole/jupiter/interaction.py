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
    # Ultra API
    GetUltraOrderResponse,
    GetUltraBalancesResponse,
    PostUltraExecuteOrderResponse,
    # Trigger API
    PostTriggerCreateOrderBody,
    PostTriggerCreateOrderResponse,
    PostTriggerExecuteResponse,
    PostTriggerCancelOrderResponse,
    GetTriggerOrdersResponse,
    # Recurring API
    PostRecurringCreateOrderBody,
    PostRecurringCreateOrderResponse,
    GetRecurringOrdersResponse,
    PostRecurringWithdrawPriceResponse,
    PostRecurringDepositPriceResponse,
    PostRecurringCancelOrderResponse,
    PostRecurringExecuteResponse
)
from ..jupiter.exception import (
    JupiterException,
    JupiterNoRouteFoundError,
    JupiterComputeAmountThresholdError,
    JupiterInvalidRequest
)
from ..jupiter.param import JupiterTokenTagType, JupiterOrderStatus, JupiterRecurringType, JupiterWithdrawMode

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
        self.url_api_ultra = "https://api.jup.ag/ultra/v1/"
        self.url_api_trigger = "https://api.jup.ag/trigger/v1/"
        self.url_api_recurring = "https://api.jup.ag/recurring/v1/"
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
            and it is used to execute an order created using the Jupiter API POST "Trigger - Create Order" endpoint (`post_trigger_create_order`). 

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
        url = self.url_api_trigger + "execute"
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
            and it is used to cancel one or more orders created using the Jupiter API POST "Trigger - Create Order" endpoint (`post_trigger_create_order`). 

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

    @overload
    def _get_trigger_orders(
        self,
        sync: Literal[True],
        user_public_key: str,
        status:  JupiterOrderStatus,
        include_failed: bool = False,
        input_token: str | None = None,
        output_token: str | None = None,
        page: int = 1
    ) -> GetTriggerOrdersResponse: ...

    @overload
    def _get_trigger_orders(
        self,
        sync: Literal[False],
        user_public_key: str,
        status:  JupiterOrderStatus,
        include_failed: bool = False,
        input_token: str | None = None,
        output_token: str | None = None,
        page: int = 1
    ) -> Coroutine[None, None, GetTriggerOrdersResponse]: ...

    def _get_trigger_orders(
        self,
        sync: bool,
        user_public_key: str,
        status:  JupiterOrderStatus,
        include_failed: bool = False,
        input_token: str | None = None,
        output_token: str | None = None,
        page: int = 1
    ) -> GetTriggerOrdersResponse | Coroutine[None, None, GetTriggerOrdersResponse]:
        """
            This function refers to the GET **[Trigger - Orders](https://dev.jup.ag/docs/api/trigger-api/get-trigger-orders)** API endpoint,
            and it is used to retrieve the list of orders associated to a wallet via Jupiter API.

            Parameters:
                user_public_key: Public Key of the Owner wallet.
                status: status of the orders to retrieve.
                include_failed: flag to include failed orders.
                input_token: address of the input token associated to the orders.
                output_token: address of the output token associated to the orders.
                page: specify which 'page' of orders to return.

            Returns:
                List of orders associated to the input wallet.
        """
        # set params
        url = self.url_api_trigger + "getTriggerOrders"
        params = {
            "user": user_public_key,
            "orderStatus": status.value,
            "includeFailedTx": "true" if include_failed else "false",
            "inputMint": input_token,
            "outputMint": output_token,
            "page": page
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(RequestType.GET.value, url, params = params)
            except HTTPError as e:
                raise self._raise(e)
            return GetTriggerOrdersResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                except HTTPError as e:
                    raise self._raise(e)
                return GetTriggerOrdersResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_recurring_create_order(self, sync: Literal[True], body: PostRecurringCreateOrderBody) -> PostRecurringCreateOrderResponse: ...

    @overload
    def _post_recurring_create_order(self, sync: Literal[False], body: PostRecurringCreateOrderBody) -> Coroutine[None, None, PostRecurringCreateOrderResponse]: ...

    def _post_recurring_create_order(self, sync: bool, body: PostRecurringCreateOrderBody) -> PostRecurringCreateOrderResponse | Coroutine[None, None, PostRecurringCreateOrderResponse]:
        """
            This function refers to the POST **[Recurring - Create Order](https://dev.jup.ag/docs/api/recurring-api/create-order)** API endpoint, 
            and it is used to receive an unsigned transaction to perform the creation of an order via Jupiter API.

            The creation order could be of two kinds:
                - *time-based*: these orders are designed to create a set of recurring orders starting 
                    from a initial amount. This amount is divided equally in the number of orders to create,
                    and each order is created with a time interval between them. The time interval is
                    specified at the creation of the order.
                - *price-based*: these orders are designed to create a set of recurring orders starting 
                    from a initial input token amount. This amount is then used to place orders (over a decided 
                    time interval) act to increase the portafolio value by a fixed `USD` amount every time. 
                    For example, if we put an initial 1 `SOL` amount and we want to buy `BONK` over time for 
                    50 `USD` every 1 hour, then the order will proceed to place an order to buy every 1 hour
                    for 50 `USD` of `BONK` using the current price of `SOL` to `BONK`. 
                    **Important**: price-based orders are opened indefinitely until the user closes them.

            Parameters:
                body: the body to sent to Jupiter API that describe the order.
                    More details in the object definition.

            Returns:
                **Unsigned** transaction created by Jupiter API.
        """

        # set params
        url = self.url_api_recurring + "createOrder"
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
            return PostRecurringCreateOrderResponse(**content_raw.json())
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
                return PostRecurringCreateOrderResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_recurring_orders(
        self,
        sync: Literal[True],
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1
    ) -> GetRecurringOrdersResponse: ...

    @overload
    def _get_recurring_orders(
        self,
        sync: Literal[False],
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1
    ) -> Coroutine[None, None, GetRecurringOrdersResponse]: ...

    def _get_recurring_orders(
        self,
        sync: bool,
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1
    ) -> GetRecurringOrdersResponse | Coroutine[None, None, GetRecurringOrdersResponse]:
        """
            This function refers to the GET **[Recurring - Orders](https://dev.jup.ag/docs/api/recurring-api/get-recurring-orders)** API endpoint,
            and it is used to retrieve the list of recurring orders associated to a wallet via Jupiter API.

            Parameters:
                user_public_key: Public Key of the Owner wallet.
                status: status of the orders to retrieve.
                recurring_type: type of the recurring order to retrieve.
                include_failed: flag to include failed orders.
                page: specify which 'page' of orders to return.

            Returns:
                List of orders associated to the input wallet.
        """
        # set params
        url = self.url_api_recurring + "getRecurringOrders"
        params = {
            "user": user_public_key,
            "orderStatus": status.value,
            "recurringType": recurring_type.value,
            "includeFailedTx": "true" if include_failed else "false",
            "page": page
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(RequestType.GET.value, url, params = params)
            except HTTPError as e:
                raise self._raise(e)
            return GetRecurringOrdersResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                except HTTPError as e:
                    raise self._raise(e)
                return GetRecurringOrdersResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_recurring_withdraw_price(self, sync: Literal[True], order_id: str, user_public_key: str, mode: JupiterWithdrawMode, amount: int | None = None) -> PostRecurringWithdrawPriceResponse: ...

    @overload
    def _post_recurring_withdraw_price(self, sync: Literal[False], order_id: str, user_public_key: str, mode: JupiterWithdrawMode, amount: int | None = None) -> Coroutine[None, None, PostRecurringWithdrawPriceResponse]: ...

    def _post_recurring_withdraw_price(self, sync: bool, order_id: str, user_public_key: str, mode: JupiterWithdrawMode, amount: int | None = None) -> PostRecurringWithdrawPriceResponse | Coroutine[None, None, PostRecurringWithdrawPriceResponse]:
        """
            This function refers to the POST **[Recurring - Withdraw Price](https://dev.jup.ag/docs/api/recurring-api/price-withdraw)** API endpoint, 
            and it is used to withdraw the price of a recurring order.

            Parameters:
                order_id: ID of the recurring order.
                user_public_key: Public Key of the Owner wallet.
                mode: mode of the withdrawal. 
                    The available modes are available on [`JupiterWithdrawMode`][cyhole.jupiter.param.JupiterWithdrawMode].
                amount: amount to withdraw. If not provided, then the entire amount will be withdrawn.

            Returns:
                Withdrawal information provided by Jupiter API.
        """
        # set params
        url = self.url_api_recurring + "priceWithdraw"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "order": order_id,
            "user": user_public_key,
            "inputOrOutput": mode.value,
            "amount": amount
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostRecurringWithdrawPriceResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostRecurringWithdrawPriceResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_recurring_deposit_price(self, sync: Literal[True], order_id: str, user_public_key: str, amount: int) -> PostRecurringDepositPriceResponse: ...

    @overload
    def _post_recurring_deposit_price(self, sync: Literal[False], order_id: str, user_public_key: str, amount: int) -> Coroutine[None, None, PostRecurringDepositPriceResponse]: ...

    def _post_recurring_deposit_price(self, sync: bool, order_id: str, user_public_key: str, amount: int) -> PostRecurringDepositPriceResponse | Coroutine[None, None, PostRecurringDepositPriceResponse]:
        """
            This function refers to the POST **[Recurring - Deposit Price](https://dev.jup.ag/docs/api/recurring-api/price-deposit)** API endpoint, 
            and it is used to deposit an amount to a price-based recurring order.

            Parameters:
                order_id: ID of the recurring order.
                user_public_key: Public Key of the Owner wallet.
                amount: amount to deposit.

            Returns:
                Deposit information provided by Jupiter API.
        """
        # set params
        url = self.url_api_recurring + "priceDeposit"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "order": order_id,
            "user": user_public_key,
            "amount": amount
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostRecurringDepositPriceResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostRecurringDepositPriceResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_recurring_cancel_order(self, sync: Literal[True], order_id: str, user_public_key: str, recurring_type: JupiterRecurringType) -> PostRecurringCancelOrderResponse: ...

    @overload
    def _post_recurring_cancel_order(self, sync: Literal[False], order_id: str, user_public_key: str, recurring_type: JupiterRecurringType) -> Coroutine[None, None, PostRecurringCancelOrderResponse]: ...

    def _post_recurring_cancel_order(self, sync: bool, order_id: str, user_public_key: str, recurring_type: JupiterRecurringType) -> PostRecurringCancelOrderResponse | Coroutine[None, None, PostRecurringCancelOrderResponse]:
        """
            This function refers to the POST **[Recurring - Cancel Order](https://dev.jup.ag/docs/api/recurring-api/cancel-order)** API endpoint, 
            and it is used to cancel an order placed using the Jupiter Recurring API.

            Parameters:
                order_id: ID of the recurring order.
                user_public_key: Public Key of the Owner wallet.
                recurring_type: type of the recurring order to retrieve.

            Returns:
                Cancel information provided by Jupiter API.
        """
        # set params
        url = self.url_api_recurring + "cancelOrder"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "order": order_id,
            "user": user_public_key,
            "recurringType": recurring_type.value
        }

        # execute request
        if sync:
            try:
                content_raw = self.client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
            except HTTPError as e:
                raise self._raise(e)
            return PostRecurringCancelOrderResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostRecurringCancelOrderResponse(**content_raw.json())
            return async_request()

    @overload
    def _post_recurring_execute(self, sync: Literal[True], signed_transaction_id: str, request_id: str) -> PostRecurringExecuteResponse: ...

    @overload
    def _post_recurring_execute(self, sync: Literal[False], signed_transaction_id: str, request_id: str) -> Coroutine[None, None, PostRecurringExecuteResponse]: ...

    def _post_recurring_execute(self, sync: bool, signed_transaction_id: str, request_id: str) -> PostRecurringExecuteResponse | Coroutine[None, None, PostRecurringExecuteResponse]:
        """
            This function refers to the POST **[Recurring - Execute](https://dev.jup.ag/docs/api/recurring-api/execute)** API endpoint, 
            and it is used to execute an "action" order using the different endpoints of the Jupiter Recurring API. For example, 
            creating a new recurring order (`post_recurring_create_order`) or canceling an existing one (`post_recurring_cancel_order`).

            First, it is required to call the endpoint of the desired action (create, cancel, deposit, withdraw). From the response, 
            is then possible to get the Request ID (`PostRecurring*Response.request_id`) and the transaction ID (`PostRecurring*Response.transaction_id`).
            The transaction ID **must** be then signed by the payer walled to get the `signed_transaction_id` that can be finally used
            to execute the action.

            Parameters:
                signed_transaction_id: the transaction ID coming from the Recurring API responses **signed** by the payer wallet.
                request_id: the same request ID coming from the responses.

            Returns:
                Order execution information provided by Jupiter API.
        """
        # set params
        url = self.url_api_recurring + "execute"
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
            return PostRecurringExecuteResponse(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type = RequestType.POST.value, url = url, headers = headers, json = body)
                except HTTPError as e:
                    raise self._raise(e)
                return PostRecurringExecuteResponse(**content_raw.json())
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