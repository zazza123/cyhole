from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..jupiter.schema import (
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
    GetTokenSearchResponse,
    GetTokenTagResponse,
    GetTokenCategoryResponse,
    GetTokenRecentResponse,
    # Ultra API
    GetUltraOrderBody,
    GetUltraOrderResponse,
    GetUltraHoldingsResponse,
    GetUltraShieldResponse,
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
from ..jupiter.param import (
    JupiterTokenTagType,
    JupiterTokenCategory,
    JupiterTokenInterval,
    JupiterOrderStatus,
    JupiterRecurringType,
    JupiterWithdrawMode
)

if TYPE_CHECKING:
    from ..jupiter.interaction import Jupiter

class JupiterClient(APIClient):
    """
        Client used for synchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's GET **[Price](https://dev.jup.ag/api-reference/price/v3/price)** API endpoint for synchronous logic.
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return self._interaction._get_price(True, address, vs_address)

    def get_swap_order(self, params: GetSwapOrderParams) -> GetSwapOrderResponse:
        """
            Call the Jupiter's GET **[Swap - Order](https://developers.jup.ag/docs/api-reference/swap/order)** API endpoint for synchronous logic.
            All the API endpoint details are available on [`Jupiter._get_swap_order`][cyhole.jupiter.interaction.Jupiter._get_swap_order].
        """
        return self._interaction._get_swap_order(True, params)

    def post_swap_execute(self, body: PostSwapExecuteBody) -> PostSwapExecuteResponse:
        """
            Call the Jupiter's POST **[Swap - Execute](https://developers.jup.ag/docs/api-reference/swap/execute)** API endpoint for synchronous logic.
            All the API endpoint details are available on [`Jupiter._post_swap_execute`][cyhole.jupiter.interaction.Jupiter._post_swap_execute].
        """
        return self._interaction._post_swap_execute(True, body)

    def get_swap_build(self, params: GetSwapBuildParams) -> GetSwapBuildResponse:
        """
            Call the Jupiter's GET **[Swap - Build](https://developers.jup.ag/docs/api-reference/swap/build)** API endpoint for synchronous logic.
            All the API endpoint details are available on [`Jupiter._get_swap_build`][cyhole.jupiter.interaction.Jupiter._get_swap_build].
        """
        return self._interaction._get_swap_build(True, params)

    def post_swap_submit(self, body: PostSwapSubmitBody) -> PostSwapSubmitResponse:
        """
            Call the Jupiter's POST **[Swap - Submit](https://developers.jup.ag/docs/swap)** API endpoint for synchronous logic.
            All the API endpoint details are available on [`Jupiter._post_swap_submit`][cyhole.jupiter.interaction.Jupiter._post_swap_submit].
        """
        return self._interaction._post_swap_submit(True, body)

    def get_token_search(self, address: str | list[str]) -> GetTokenSearchResponse:
        """
            Call the Jupiter's GET **[Token Search](https://dev.jup.ag/api-reference/tokens/v2/search)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_search`][cyhole.jupiter.interaction.Jupiter._get_token_search].
        """
        return self._interaction._get_token_search(True, address)

    def get_token_tag(self, tag: str | JupiterTokenTagType) -> GetTokenTagResponse:
        """
            Call the Jupiter's GET **[Token Tag](https://dev.jup.ag/api-reference/tokens/v2/tag)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tag`][cyhole.jupiter.interaction.Jupiter._get_token_tag].
        """
        return self._interaction._get_token_tag(True, tag)

    def get_token_category(self, category: str | JupiterTokenCategory, interval: str | JupiterTokenInterval) -> GetTokenCategoryResponse:
        """
            Call the Jupiter's GET **[Token Category](https://dev.jup.ag/api-reference/tokens/v2/category)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_category`][cyhole.jupiter.interaction.Jupiter._get_token_category].
        """
        return self._interaction._get_token_category(True, category, interval)

    def get_token_recent(self) -> GetTokenRecentResponse:
        """
            Call the Jupiter's GET **[Token Recent](https://dev.jup.ag/api-reference/tokens/v2/recent)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_recent`][cyhole.jupiter.interaction.Jupiter._get_token_recent].
        """
        return self._interaction._get_token_recent(True)

    def get_ultra_order(self, body: GetUltraOrderBody) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra - Get Order](https://jupiter.mintlify.app/api-reference/ultra/order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return self._interaction._get_ultra_order(True, body)

    def post_ultra_execute_order(self, signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse:
        """
            Call the Jupiter's POST **[Ultra - Execute Order](https://jupiter.mintlify.app/api-reference/ultra/execute)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_ultra_execute_order`][cyhole.jupiter.interaction.Jupiter._post_ultra_execute_order].
        """
        return self._interaction._post_ultra_execute_order(True, signed_transaction_id, request_id)

    def get_ultra_holdings(self, address: str) -> GetUltraHoldingsResponse:
        """
            Call the Jupiter's GET **[Ultra - Holdings](https://jupiter.mintlify.app/api-reference/ultra/holdings)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_holdings`][cyhole.jupiter.interaction.Jupiter._get_ultra_holdings].
        """
        return self._interaction._get_ultra_holdings(True, address)

    def get_ultra_shield(self, mints: list[str]) -> GetUltraShieldResponse:
        """
            Call the Jupiter's GET **[Ultra - Shield](https://jupiter.mintlify.app/api-reference/ultra/shield)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_shield`][cyhole.jupiter.interaction.Jupiter._get_ultra_shield].
        """
        return self._interaction._get_ultra_shield(True, mints)

    def post_trigger_create_order(self, body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Create Order](https://station.jup.ag/docs/api/trigger-api/create-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_create_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_create_order].
        """
        return self._interaction._post_trigger_create_order(True, body)

    def post_trigger_execute(self, signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse:
        """
            Call the Jupiter's POST **[Trigger - Execute](https://station.jup.ag/docs/api/trigger-api/execute)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_execute`][cyhole.jupiter.interaction.Jupiter._post_trigger_execute].
        """
        return self._interaction._post_trigger_execute(True, signed_transaction_id, request_id)

    def post_trigger_cancel_order(self, user_public_key: str, orders: str | list[str], compute_unit_price: str = 'auto') -> PostTriggerCancelOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Cancel Order](https://station.jup.ag/docs/api/trigger-api/cancel-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_cancel_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_cancel_order].
        """
        return self._interaction._post_trigger_cancel_order(True, user_public_key, orders, compute_unit_price)

    def get_trigger_orders(
        self,
        user_public_key: str,
        status:  JupiterOrderStatus,
        include_failed: bool = False,
        input_token: str | None = None,
        output_token: str | None = None,
        page: int = 1
    ) -> GetTriggerOrdersResponse:
        """
            Call the Jupiter's GET **[Trigger - Orders](https://dev.jup.ag/docs/api/trigger-api/get-trigger-orders)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_trigger_orders`][cyhole.jupiter.interaction.Jupiter._get_trigger_orders].
        """
        return self._interaction._get_trigger_orders(True, user_public_key, status, include_failed, input_token, output_token, page)

    def post_recurring_create_order(self, body: PostRecurringCreateOrderBody) -> PostRecurringCreateOrderResponse:
        """
            Call the Jupiter's POST **[Recurring - Create Order](https://dev.jup.ag/docs/api/recurring-api/create-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_create_order`][cyhole.jupiter.interaction.Jupiter._post_recurring_create_order].
        """
        return self._interaction._post_recurring_create_order(True, body)

    def get_recurring_orders(
        self,
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1
    ) -> GetRecurringOrdersResponse:
        """
            Call the Jupiter's GET **[Recurring - Orders](https://dev.jup.ag/docs/api/recurring-api/get-recurring-orders)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_recurring_orders`][cyhole.jupiter.interaction.Jupiter._get_recurring_orders].
        """
        return self._interaction._get_recurring_orders(True, user_public_key, status, recurring_type, include_failed, page)

    def post_recurring_withdraw_price(self, order_id: str, user_public_key: str, mode: JupiterWithdrawMode, amount: int | None = None) -> PostRecurringWithdrawPriceResponse:
        """
            Call the Jupiter's POST **[Recurring - Withdraw Price](https://dev.jup.ag/docs/api/recurring-api/price-withdraw)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_withdraw_price`][cyhole.jupiter.interaction.Jupiter._post_recurring_withdraw_price].
        """
        return self._interaction._post_recurring_withdraw_price(True, order_id, user_public_key, mode, amount)

    def post_recurring_deposit_price(self, order_id: str, user_public_key: str, amount: int) -> PostRecurringDepositPriceResponse:
        """
            Call the Jupiter's POST **[Recurring - Deposit Price](https://dev.jup.ag/docs/api/recurring-api/price-deposit)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_deposit_price`][cyhole.jupiter.interaction.Jupiter._post_recurring_deposit_price].
        """
        return self._interaction._post_recurring_deposit_price(True, order_id, user_public_key, amount)

    def post_recurring_cancel_order(self, order_id: str, user_public_key: str, recurring_type: JupiterRecurringType) -> PostRecurringCancelOrderResponse:
        """
            Call the Jupiter's POST **[Recurring - Cancel Order](https://dev.jup.ag/docs/api/recurring-api/cancel-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_cancel_order`][cyhole.jupiter.interaction.Jupiter._post_recurring_cancel_order].
        """
        return self._interaction._post_recurring_cancel_order(True, order_id, user_public_key, recurring_type)

    def post_recurring_execute(self, signed_transaction_id: str, request_id: str) -> PostRecurringExecuteResponse:
        """
            Call the Jupiter's POST **[Recurring - Execute](https://dev.jup.ag/docs/api/recurring-api/execute)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_execute`][cyhole.jupiter.interaction.Jupiter._post_recurring_execute].
        """
        return self._interaction._post_recurring_execute(True, signed_transaction_id, request_id)

class JupiterAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    async def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's GET **[Price](https://dev.jup.ag/api-reference/price/v3/price)** API endpoint for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return await self._interaction._get_price(False, address, vs_address)

    async def get_swap_order(self, params: GetSwapOrderParams) -> GetSwapOrderResponse:
        """
            Call the Jupiter's GET **[Swap - Order](https://developers.jup.ag/docs/api-reference/swap/order)** API endpoint for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._get_swap_order`][cyhole.jupiter.interaction.Jupiter._get_swap_order].
        """
        return await self._interaction._get_swap_order(False, params)

    async def post_swap_execute(self, body: PostSwapExecuteBody) -> PostSwapExecuteResponse:
        """
            Call the Jupiter's POST **[Swap - Execute](https://developers.jup.ag/docs/api-reference/swap/execute)** API endpoint for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._post_swap_execute`][cyhole.jupiter.interaction.Jupiter._post_swap_execute].
        """
        return await self._interaction._post_swap_execute(False, body)

    async def get_swap_build(self, params: GetSwapBuildParams) -> GetSwapBuildResponse:
        """
            Call the Jupiter's GET **[Swap - Build](https://developers.jup.ag/docs/api-reference/swap/build)** API endpoint for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._get_swap_build`][cyhole.jupiter.interaction.Jupiter._get_swap_build].
        """
        return await self._interaction._get_swap_build(False, params)

    async def post_swap_submit(self, body: PostSwapSubmitBody) -> PostSwapSubmitResponse:
        """
            Call the Jupiter's POST **[Swap - Submit](https://developers.jup.ag/docs/swap)** API endpoint for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._post_swap_submit`][cyhole.jupiter.interaction.Jupiter._post_swap_submit].
        """
        return await self._interaction._post_swap_submit(False, body)

    async def get_token_search(self, address: str | list[str]) -> GetTokenSearchResponse:
        """
            Call the Jupiter's GET **[Token Search](https://dev.jup.ag/api-reference/tokens/v2/search)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_search`][cyhole.jupiter.interaction.Jupiter._get_token_search].
        """
        return await self._interaction._get_token_search(False, address)

    async def get_token_tag(self, tag: str | JupiterTokenTagType) -> GetTokenTagResponse:
        """
            Call the Jupiter's GET **[Token Tag](https://dev.jup.ag/api-reference/tokens/v2/tag)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tag`][cyhole.jupiter.interaction.Jupiter._get_token_tag].
        """
        return await self._interaction._get_token_tag(False, tag)

    async def get_token_category(self, category: str | JupiterTokenCategory, interval: str | JupiterTokenInterval) -> GetTokenCategoryResponse:
        """
            Call the Jupiter's GET **[Token Category](https://dev.jup.ag/api-reference/tokens/v2/category)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_category`][cyhole.jupiter.interaction.Jupiter._get_token_category].
        """
        return await self._interaction._get_token_category(False, category, interval)

    async def get_token_recent(self) -> GetTokenRecentResponse:
        """
            Call the Jupiter's GET **[Token Recent](https://dev.jup.ag/api-reference/tokens/v2/recent)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_recent`][cyhole.jupiter.interaction.Jupiter._get_token_recent].
        """
        return await self._interaction._get_token_recent(False)

    async def get_ultra_order(self, body: GetUltraOrderBody) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra - Get Order](https://jupiter.mintlify.app/api-reference/ultra/order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return await self._interaction._get_ultra_order(False, body)

    async def post_ultra_execute_order(self, signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse:
        """
            Call the Jupiter's POST **[Ultra - Execute Order](https://jupiter.mintlify.app/api-reference/ultra/execute)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_ultra_execute_order`][cyhole.jupiter.interaction.Jupiter._post_ultra_execute_order].
        """
        return await self._interaction._post_ultra_execute_order(False, signed_transaction_id, request_id)

    async def get_ultra_holdings(self, address: str) -> GetUltraHoldingsResponse:
        """
            Call the Jupiter's GET **[Ultra - Holdings](https://jupiter.mintlify.app/api-reference/ultra/holdings)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_holdings`][cyhole.jupiter.interaction.Jupiter._get_ultra_holdings].
        """
        return await self._interaction._get_ultra_holdings(False, address)

    async def get_ultra_shield(self, mints: list[str]) -> GetUltraShieldResponse:
        """
            Call the Jupiter's GET **[Ultra - Shield](https://jupiter.mintlify.app/api-reference/ultra/shield)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_shield`][cyhole.jupiter.interaction.Jupiter._get_ultra_shield].
        """
        return await self._interaction._get_ultra_shield(False, mints)

    async def post_trigger_create_order(self, body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Create Order](https://station.jup.ag/docs/api/trigger-api/create-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_create_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_create_order].
        """
        return await self._interaction._post_trigger_create_order(False, body)

    async def post_trigger_execute(self, signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse:
        """
            Call the Jupiter's POST **[Trigger - Execute](https://station.jup.ag/docs/api/trigger-api/execute)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_execute`][cyhole.jupiter.interaction.Jupiter._post_trigger_execute].
        """
        return await self._interaction._post_trigger_execute(False, signed_transaction_id, request_id)

    async def post_trigger_cancel_order(self, user_public_key: str, orders: str | list[str], compute_unit_price: str = 'auto') -> PostTriggerCancelOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Cancel Order](https://station.jup.ag/docs/api/trigger-api/cancel-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_cancel_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_cancel_order].
        """
        return await self._interaction._post_trigger_cancel_order(False, user_public_key, orders, compute_unit_price)

    async def get_trigger_orders(
        self,
        user_public_key: str,
        status:  JupiterOrderStatus,
        include_failed: bool = False,
        input_token: str | None = None,
        output_token: str | None = None,
        page: int = 1
    ) -> GetTriggerOrdersResponse:
        """
            Call the Jupiter's GET **[Trigger - Orders](https://dev.jup.ag/docs/api/trigger-api/get-trigger-orders)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_trigger_orders`][cyhole.jupiter.interaction.Jupiter._get_trigger_orders].
        """
        return await self._interaction._get_trigger_orders(False, user_public_key, status, include_failed, input_token, output_token, page)

    async def post_recurring_create_order(self, body: PostRecurringCreateOrderBody) -> PostRecurringCreateOrderResponse:
        """
            Call the Jupiter's POST **[Recurring - Create Order](https://dev.jup.ag/docs/api/recurring-api/create-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_create_order`][cyhole.jupiter.interaction.Jupiter._post_recurring_create_order].
        """
        return await self._interaction._post_recurring_create_order(False, body)

    async def get_recurring_orders(
        self,
        user_public_key: str,
        status: JupiterOrderStatus,
        recurring_type: JupiterRecurringType,
        include_failed: bool = False,
        page: int = 1
    ) -> GetRecurringOrdersResponse:
        """
            Call the Jupiter's GET **[Recurring - Orders](https://dev.jup.ag/docs/api/recurring-api/get-recurring-orders)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_recurring_orders`][cyhole.jupiter.interaction.Jupiter._get_recurring_orders].
        """
        return await self._interaction._get_recurring_orders(False, user_public_key, status, recurring_type, include_failed, page)

    async def post_recurring_withdraw_price(self, order_id: str, user_public_key: str, mode: JupiterWithdrawMode, amount: int | None = None) -> PostRecurringWithdrawPriceResponse:
        """
            Call the Jupiter's POST **[Recurring - Withdraw Price](https://dev.jup.ag/docs/api/recurring-api/price-withdraw)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_withdraw_price`][cyhole.jupiter.interaction.Jupiter._post_recurring_withdraw_price].
        """
        return await self._interaction._post_recurring_withdraw_price(False, order_id, user_public_key, mode, amount)

    async def post_recurring_deposit_price(self, order_id: str, user_public_key: str, amount: int) -> PostRecurringDepositPriceResponse:
        """
            Call the Jupiter's POST **[Recurring - Deposit Price](https://dev.jup.ag/docs/api/recurring-api/price-deposit)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_deposit_price`][cyhole.jupiter.interaction.Jupiter._post_recurring_deposit_price].
        """
        return await self._interaction._post_recurring_deposit_price(False, order_id, user_public_key, amount)

    async def post_recurring_cancel_order(self, order_id: str, user_public_key: str, recurring_type: JupiterRecurringType) -> PostRecurringCancelOrderResponse:
        """
            Call the Jupiter's POST **[Recurring - Cancel Order](https://dev.jup.ag/docs/api/recurring-api/cancel-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_cancel_order`][cyhole.jupiter.interaction.Jupiter._post_recurring_cancel_order].
        """
        return await self._interaction._post_recurring_cancel_order(False, order_id, user_public_key, recurring_type)

    async def post_recurring_execute(self, signed_transaction_id: str, request_id: str) -> PostRecurringExecuteResponse:
        """
            Call the Jupiter's POST **[Recurring - Execute](https://dev.jup.ag/docs/api/recurring-api/execute)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_recurring_execute`][cyhole.jupiter.interaction.Jupiter._post_recurring_execute].
        """
        return await self._interaction._post_recurring_execute(False, signed_transaction_id, request_id)