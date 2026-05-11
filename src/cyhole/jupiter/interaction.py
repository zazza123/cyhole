from requests.exceptions import HTTPError
from typing import Any, Coroutine, overload, Literal, Type

from ..core.param import RequestType
from ..core.interaction import Interaction, ResponseModel
from ..jupiter.client import JupiterClient, JupiterAsyncClient
from ..jupiter.schema import (
    JupiterHTTPError,
    # Price API
    GetPriceResponse,
    # Swap API
    GetSwapOrderParams,
    GetSwapOrderResponse,
    PostSwapExecuteBody,
    PostSwapExecuteResponse,
    GetSwapBuildParams,
    GetSwapBuildResponse,
    PostSwapSubmitBody,
    PostSwapSubmitResponse,
    # Token API
    GetTokenInfo,
    GetTokenSearchResponse,
    GetTokenTagResponse,
    GetTokenCategoryResponse,
    GetTokenRecentResponse,
    GetTokenVerifyCheckEligibilityResponse,
    GetTokenVerifyCraftTxnResponse,
    PostTokenVerifyExecuteBody,
    PostTokenVerifyExecuteResponse,
    # Recurring API
    PostRecurringCreateOrderBody,
    PostRecurringCreateOrderResponse,
    GetRecurringOrdersResponse,
    PostRecurringCancelOrderResponse,
    PostRecurringExecuteResponse
)
from ..jupiter.exception import (
    JupiterException,
    JupiterApiTierError,
    JupiterNoRouteFoundError,
    JupiterComputeAmountThresholdError,
    JupiterInvalidRequest
)
from ..jupiter.param import (
    JupiterApiTier,
    JupiterTokenTagType,
    JupiterTokenCategory,
    JupiterTokenInterval,
    JupiterOrderStatus,
    JupiterRecurringType
)

class Jupiter(Interaction):
    """
        Class used to connect [Jupiter](https://jup.ag) API, one of them most popular Solana DEX. 
        To have access Jupiter API is **not** required an API key if you are using the `lite` API tier. 
        If using the `pro` or `ultra` API tiers, an API key is required.

        Check supported API tiers at: [https://dev.jup.ag/portal/rate-limit](https://dev.jup.ag/portal/rate-limit)

        Check [https://dev.jup.ag/api-reference](https://dev.jup.ag/api-reference) for all the details on the available endpoints.

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

    tier: JupiterApiTier
    """API tier used by the connetor"""

    api_key: str | None
    """API key used to connect to Jupiter API."""

    def __init__(self, 
        tier: JupiterApiTier = JupiterApiTier.LITE,
        api_key: str | None = None,
        headers: Any | None = None
    ) -> None:
        # headers setup
        headers = {
            "Content-Type": "application/json"
        }

        # tier
        self.tier = tier

        # api key
        self.api_key = api_key
        if self.tier != JupiterApiTier.LITE and api_key is None:
            raise JupiterApiTierError(f"API Key is required for {self.tier.name} tier")

        if self.api_key:
            headers["x-api-key"] = self.api_key

        # init super
        super().__init__(headers)
        self.headers: dict[str, str]

        # clients
        self.client = JupiterClient(self, headers = self.headers)
        self.async_client = JupiterAsyncClient(self, self.headers)

        # API urls
        self.url_api_recurring = "https://api.jup.ag/recurring/v1/"
        return

    @property
    def url_api_root(self) -> str:
        """API root URL based in API tier."""
        match self.tier:
            case JupiterApiTier.LITE:
                return "https://lite-api.jup.ag"
            case JupiterApiTier.PRO | JupiterApiTier.ULTRA:
                return "https://api.jup.ag"

    @property
    def url_api_price(self) -> str:
        """Price API URL composed according to API tier"""
        return self.url_api_root + "/price/v3"

    @property
    def url_api_swap(self) -> str:
        """Swap API URL composed according to API tier"""
        return self.url_api_root + "/swap/v2/"

    @property
    def url_api_tx(self) -> str:
        """Transaction submission API URL composed according to API tier"""
        return self.url_api_root + "/tx/v1/"

    @property
    def url_api_token(self) -> str:
        """Token API URL composed according to API tier"""
        return self.url_api_root + "/tokens/v2/"

    def api_return_model(self, sync: bool, type: str, url: str, response_model: Type[ResponseModel], *args: tuple, **kwargs: Any) -> ResponseModel | Coroutine[None, None, ResponseModel]:
        """
            Overwrite of base function to handle Jupiter API responses.
        """
        if sync:
            try:
                content_raw = self.client.api(type, url, *args, **kwargs)
            except HTTPError as e:
                raise self._raise(e)
            return response_model(**content_raw.json())
        else:
            async def async_request():
                try:
                    content_raw = await self.async_client.api(type, url, *args, **kwargs)
                except HTTPError as e:
                    raise self._raise(e)
                return response_model(**content_raw.json())
            return async_request()

    @overload
    def _get_price(self, sync: Literal[True], address: list[str]) -> GetPriceResponse: ...

    @overload
    def _get_price(self, sync: Literal[False], address: list[str]) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(self, sync: bool, address: list[str]) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the GET **[Price](https://developers.jup.ag/docs/price)** API endpoint,
            and it is used to get the current USD price for up to 50 tokens on Solana from [Jupiter](https://jup.ag).

            Returns `None` for a token when price data is unavailable or unreliable
            (e.g. no trades in the last 7 days, or flagged as suspicious).

            Parameters:
                address: list of token mint addresses to query. Maximum 50 per request.
                    For example, `So11111111111111111111111111111111111111112`.

            Returns:
                mapping of token mint address to price data.
        """

        # set params
        params: dict[str, str] = {
            "ids": ",".join(address)
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, self.url_api_price, params = params)
            return GetPriceResponse.model_validate(content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, self.url_api_price, params = params)
                return GetPriceResponse.model_validate(content_raw.json())
            return async_request()

    @overload
    def _get_swap_order(self, sync: Literal[True], params: GetSwapOrderParams) -> GetSwapOrderResponse: ...

    @overload
    def _get_swap_order(self, sync: Literal[False], params: GetSwapOrderParams) -> Coroutine[None, None, GetSwapOrderResponse]: ...

    def _get_swap_order(self, sync: bool, params: GetSwapOrderParams) -> GetSwapOrderResponse | Coroutine[None, None, GetSwapOrderResponse]:
        """
            This function refers to the GET **[Swap - Order](https://developers.jup.ag/docs/api-reference/swap/order)** API endpoint,
            and it is used to get a swap quote and a fully assembled transaction using Jupiter Swap v2 API.

            The Meta-Aggregator path competes across all routing engines (Metis, JupiterZ RFQ, DFlow, OKX)
            to return the best price. When `taker` is provided the response includes a ready-to-sign
            base64-encoded transaction; combine with `post_swap_execute` to land it on-chain.

            Parameters:
                params: input params describing the swap. See [`GetSwapOrderParams`][cyhole.jupiter.schema.GetSwapOrderParams].

            Returns:
                Quote and assembled transaction from Jupiter Swap v2 API.
        """
        url = self.url_api_swap + "order"
        return self.api_return_model(sync, RequestType.GET.value, url, GetSwapOrderResponse,
            params = params.model_dump(by_alias = True, exclude_defaults = True)
        )

    @overload
    def _post_swap_execute(self, sync: Literal[True], body: PostSwapExecuteBody) -> PostSwapExecuteResponse: ...

    @overload
    def _post_swap_execute(self, sync: Literal[False], body: PostSwapExecuteBody) -> Coroutine[None, None, PostSwapExecuteResponse]: ...

    def _post_swap_execute(self, sync: bool, body: PostSwapExecuteBody) -> PostSwapExecuteResponse | Coroutine[None, None, PostSwapExecuteResponse]:
        """
            This function refers to the POST **[Swap - Execute](https://developers.jup.ag/docs/api-reference/swap/execute)** API endpoint,
            and it is used to execute a signed swap transaction created by `get_swap_order`.

            First call `get_swap_order` with a valid `taker` to obtain the base64 transaction and the
            `request_id`. Sign the transaction with the taker's wallet, then submit both via this endpoint.

            Parameters:
                body: signed transaction and request ID from `get_swap_order`.
                    See [`PostSwapExecuteBody`][cyhole.jupiter.schema.PostSwapExecuteBody].

            Returns:
                Execution result including status, signature, and amount details.
        """
        url = self.url_api_swap + "execute"
        return self.api_return_model(sync, RequestType.POST.value, url, PostSwapExecuteResponse,
            json = body.model_dump(by_alias = True, exclude_none = True)
        )

    @overload
    def _get_swap_build(self, sync: Literal[True], params: GetSwapBuildParams) -> GetSwapBuildResponse: ...

    @overload
    def _get_swap_build(self, sync: Literal[False], params: GetSwapBuildParams) -> Coroutine[None, None, GetSwapBuildResponse]: ...

    def _get_swap_build(self, sync: bool, params: GetSwapBuildParams) -> GetSwapBuildResponse | Coroutine[None, None, GetSwapBuildResponse]:
        """
            This function refers to the GET **[Swap - Build](https://developers.jup.ag/docs/api-reference/swap/build)** API endpoint,
            and it is used to get raw swap instructions for custom transaction building using Jupiter Swap v2 Router path.

            Unlike `get_swap_order`, this endpoint returns individual Solana instructions rather than an assembled
            transaction, allowing integrators to compose their own transaction. Routing is handled exclusively
            by the Metis on-chain router (no RFQ market makers). Combine with `post_swap_submit` to land the
            transaction via Jupiter's infrastructure.

            Parameters:
                params: input params describing the swap. See [`GetSwapBuildParams`][cyhole.jupiter.schema.GetSwapBuildParams].

            Returns:
                Raw instructions and route plan for custom transaction assembly.
        """
        url = self.url_api_swap + "build"
        return self.api_return_model(sync, RequestType.GET.value, url, GetSwapBuildResponse,
            params = params.model_dump(by_alias = True, exclude_defaults = True)
        )

    @overload
    def _post_swap_submit(self, sync: Literal[True], body: PostSwapSubmitBody) -> PostSwapSubmitResponse: ...

    @overload
    def _post_swap_submit(self, sync: Literal[False], body: PostSwapSubmitBody) -> Coroutine[None, None, PostSwapSubmitResponse]: ...

    def _post_swap_submit(self, sync: bool, body: PostSwapSubmitBody) -> PostSwapSubmitResponse | Coroutine[None, None, PostSwapSubmitResponse]:
        """
            This function refers to the POST **[Swap - Submit](https://developers.jup.ag/docs/swap)** API endpoint,
            and it is used to submit any signed Solana transaction through Jupiter's proprietary landing pipeline.

            The transaction must include a SOL tip (minimum 0.001 SOL / 1,000,000 lamports) to incentivise
            validators. This endpoint is zero-credit-cost and available on all plans including keyless access.

            Parameters:
                body: base64-encoded signed Solana transaction.
                    See [`PostSwapSubmitBody`][cyhole.jupiter.schema.PostSwapSubmitBody].

            Returns:
                Transaction signature after successful submission.
        """
        url = self.url_api_tx + "submit"
        return self.api_return_model(sync, RequestType.POST.value, url, PostSwapSubmitResponse,
            json = body.model_dump(by_alias = True)
        )

    @overload
    def _get_token_search(self, sync: Literal[True], address: str | list[str]) -> GetTokenSearchResponse: ...

    @overload
    def _get_token_search(self, sync: Literal[False], address: str | list[str]) -> Coroutine[None, None, GetTokenSearchResponse]: ...

    def _get_token_search(self, sync: bool, address: str | list[str]) -> GetTokenSearchResponse | Coroutine[None, None, GetTokenSearchResponse]:
        """
            This function refers to the GET **[Token Search](https://dev.jup.ag/api-reference/tokens/v2/search)** API endpoint,
            with a specific focus on retrieving the information of a list of token given its addresses, names or symbols.

            Parameters:
                address: list of addresses, names or symbols of the tokens to check. 
                    For example, `So11111111111111111111111111111111111111112` or `USDC`.

            Returns:
                Information of the tokens.
        """
        # set url
        url = self.url_api_token + "search"

        # single
        if isinstance(address, str):
            address = [address]

        # set params
        params = {
            "query" : ",".join(address)
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            tokens = [GetTokenInfo(**token) for token in content_raw.json()["tokens"]]
            return GetTokenSearchResponse(tokens = tokens)
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                tokens = [GetTokenInfo(**token) for token in content_raw.json()["tokens"]]
                return GetTokenSearchResponse(tokens = tokens)
            return async_request()

    @overload
    def _get_token_tag(self, sync: Literal[True], tag: str | JupiterTokenTagType) -> GetTokenTagResponse: ...

    @overload
    def _get_token_tag(self, sync: Literal[False], tag: str | JupiterTokenTagType) -> Coroutine[None, None, GetTokenTagResponse]: ...

    def _get_token_tag(self, sync: bool, tag: str | JupiterTokenTagType) -> GetTokenTagResponse | Coroutine[None, None, GetTokenTagResponse]:
        """
            This function refers to the GET **[Token Tag](https://dev.jup.ag/api-reference/tokens/v2/tag)** API endpoint, 
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
        url = self.url_api_token + "tag"
        params = {
            "query" : tag_str
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenTagResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenTagResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_token_category(self, sync: Literal[True], category: str | JupiterTokenCategory, interval: str | JupiterTokenInterval) -> GetTokenCategoryResponse: ...

    @overload
    def _get_token_category(self, sync: Literal[False], category: str | JupiterTokenCategory, interval: str | JupiterTokenInterval) -> Coroutine[None, None, GetTokenCategoryResponse]: ...

    def _get_token_category(self, sync: bool, category: str | JupiterTokenCategory, interval: str | JupiterTokenInterval) -> GetTokenCategoryResponse | Coroutine[None, None, GetTokenCategoryResponse]:
        """
            This function refers to the GET **[Token Category](https://dev.jup.ag/api-reference/tokens/v2/category)** API endpoint, 
            and it is used to retrieved the list of token according to a category in a specific interval.

            Parameters:
                category: category to filter by.
                interval: time range to consider to extract.

            Returns:
                List of Jupiter's tokens list.
        """
        # check inputs
        category_str = category if isinstance(category, str) else category.value
        JupiterTokenCategory.check(category_str)

        interval_str = interval if isinstance(interval, str) else interval.value
        JupiterTokenInterval.check(interval_str)

        # set params
        url = self.url_api_token + f"{category_str}/{interval_str}"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetTokenCategoryResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetTokenCategoryResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_token_recent(self, sync: Literal[True], limit: int | None = None) -> GetTokenRecentResponse: ...

    @overload
    def _get_token_recent(self, sync: Literal[False], limit: int | None = None) -> Coroutine[None, None, GetTokenRecentResponse]: ...

    def _get_token_recent(self, sync: bool, limit: int | None = None) -> GetTokenRecentResponse | Coroutine[None, None, GetTokenRecentResponse]:
        """
            This function refers to the GET **[Token Recent](https://dev.jup.ag/api-reference/tokens/v2/recent)** API endpoint,
            and it is used to retrieve the list of recently created tokens with their first pool information.

            Parameters:
                limit: maximum number of tokens to return. API defaults to `30` when not provided.

            Returns:
                List of Jupiter's recently created tokens.
        """
        # set params
        url = self.url_api_token + "recent"
        params = {}
        if limit is not None:
            params["limit"] = limit

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenRecentResponse(tokens = content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenRecentResponse(tokens = content_raw.json())
            return async_request()

    @overload
    def _get_token_verify_check_eligibility(self, sync: Literal[True], token_id: str) -> GetTokenVerifyCheckEligibilityResponse: ...

    @overload
    def _get_token_verify_check_eligibility(self, sync: Literal[False], token_id: str) -> Coroutine[None, None, GetTokenVerifyCheckEligibilityResponse]: ...

    def _get_token_verify_check_eligibility(self, sync: bool, token_id: str) -> GetTokenVerifyCheckEligibilityResponse | Coroutine[None, None, GetTokenVerifyCheckEligibilityResponse]:
        """
            This function refers to the GET **[Token Verify - Check Eligibility](https://developers.jup.ag/docs/tokens/verification)** API endpoint,
            and it is used to determine whether a token is eligible for express verification on Jupiter.

            Parameters:
                token_id: mint address of the token to check.

            Returns:
                Eligibility status indicating whether verification and metadata updates are permitted.

            Raises:
                JupiterException: if the API returns an error.
        """
        url = self.url_api_token + "verify/express/check-eligibility"
        params = {"tokenId": token_id}
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenVerifyCheckEligibilityResponse, params = params)

    @overload
    def _get_token_verify_craft_txn(self, sync: Literal[True], sender_address: str) -> GetTokenVerifyCraftTxnResponse: ...

    @overload
    def _get_token_verify_craft_txn(self, sync: Literal[False], sender_address: str) -> Coroutine[None, None, GetTokenVerifyCraftTxnResponse]: ...

    def _get_token_verify_craft_txn(self, sync: bool, sender_address: str) -> GetTokenVerifyCraftTxnResponse | Coroutine[None, None, GetTokenVerifyCraftTxnResponse]:
        """
            This function refers to the GET **[Token Verify - Craft Transaction](https://developers.jup.ag/docs/tokens/verification)** API endpoint,
            and it is used to obtain an unsigned transaction for the 1000 JUP express verification payment.

            Parameters:
                sender_address: wallet address that will sign and submit the payment transaction.

            Returns:
                Unsigned transaction details including the base64-encoded transaction and a `request_id`
                required by the execute step.

            Raises:
                JupiterException: if the API returns an error.
        """
        url = self.url_api_token + "verify/express/craft-txn"
        params = {"senderAddress": sender_address}
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenVerifyCraftTxnResponse, params = params)

    @overload
    def _post_token_verify_execute(self, sync: Literal[True], body: PostTokenVerifyExecuteBody) -> PostTokenVerifyExecuteResponse: ...

    @overload
    def _post_token_verify_execute(self, sync: Literal[False], body: PostTokenVerifyExecuteBody) -> Coroutine[None, None, PostTokenVerifyExecuteResponse]: ...

    def _post_token_verify_execute(self, sync: bool, body: PostTokenVerifyExecuteBody) -> PostTokenVerifyExecuteResponse | Coroutine[None, None, PostTokenVerifyExecuteResponse]:
        """
            This function refers to the POST **[Token Verify - Execute](https://developers.jup.ag/docs/tokens/verification)** API endpoint,
            and it is used to submit a signed verification transaction and project details to complete the express verification flow.

            Parameters:
                body: the body containing the signed transaction, request ID, sender address, token mint,
                    Twitter handle, description, and optional token metadata.

            Returns:
                Verification execution result including submission status and on-chain transaction signature.

            Raises:
                JupiterException: if the API returns an error.
        """
        url = self.url_api_token + "verify/express/execute"
        headers = {"Content-Type": "application/json"}

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
            return PostTokenVerifyExecuteResponse(**content_raw.json())
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
                return PostTokenVerifyExecuteResponse(**content_raw.json())
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
        page: int = 1,
        input_mint: str | None = None,
        output_mint: str | None = None
    ) -> GetRecurringOrdersResponse: ...

    @overload
    def _get_recurring_orders(
        self,
        sync: Literal[False],
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1,
        input_mint: str | None = None,
        output_mint: str | None = None
    ) -> Coroutine[None, None, GetRecurringOrdersResponse]: ...

    def _get_recurring_orders(
        self,
        sync: bool,
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1,
        input_mint: str | None = None,
        output_mint: str | None = None
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
                input_mint: filter orders by input token mint address.
                output_mint: filter orders by output token mint address.

            Returns:
                List of orders associated to the input wallet.
        """
        # set params
        url = self.url_api_recurring + "getRecurringOrders"
        params: dict = {
            "user": user_public_key,
            "orderStatus": status.value,
            "recurringType": recurring_type.value,
            "includeFailedTx": "true" if include_failed else "false",
            "page": page
        }
        if input_mint:
            params["inputMint"] = input_mint
        if output_mint:
            params["outputMint"] = output_mint

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