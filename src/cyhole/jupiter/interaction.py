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
    def _get_price(self, sync: Literal[True], address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        ...

    @overload
    def _get_price(self, sync: Literal[False], address: list[str], vs_address: str | None = None) -> Coroutine[None, None, GetPriceResponse]:
        ...

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
    def _get_quote(self, sync: Literal[True], input: GetQuoteInput) -> GetQuoteResponse:
        ...

    @overload
    def _get_quote(self, sync: Literal[False], input: GetQuoteInput) -> Coroutine[None, None, GetQuoteResponse]:
        ...

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
    def _get_quote_tokens(self, sync: Literal[True]) -> GetQuoteTokensResponse:
        ...

    @overload
    def _get_quote_tokens(self, sync: Literal[False]) -> Coroutine[None, None, GetQuoteTokensResponse]:
        ...

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
    def _get_quote_program_id_label(self, sync: Literal[True]) -> GetQuoteProgramIdLabelResponse:
        ...

    @overload
    def _get_quote_program_id_label(self, sync: Literal[False]) -> Coroutine[None, None, GetQuoteProgramIdLabelResponse]:
        ...

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
    def _post_swap(self, sync: Literal[True], body: PostSwapBody) -> PostSwapResponse:
        ...

    @overload
    def _post_swap(self, sync: Literal[False], body: PostSwapBody) -> Coroutine[None, None, PostSwapResponse]:
        ...

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