from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..jupiter.schema import (
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
    PostRecurringCancelOrderResponse
)
from ..jupiter.param import JupiterTokenTagType, JupiterOrderStatus, JupiterRecurringType, JupiterWithdrawMode

if TYPE_CHECKING:
    from ..jupiter.interaction import Jupiter

class JupiterClient(APIClient):
    """
        Client used for synchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    def get_price(self, address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's GET **[Price](https://station.jup.ag/docs/api/price-api/price)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return self._interaction._get_price(True, address, extra_info, vs_address)

    def get_quote(self, input: GetQuoteParams) -> GetQuoteResponse:
        """
            Call the Jupiter's GET **[Quote](https://station.jup.ag/docs/api/swap-api/quote)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return self._interaction._get_quote(True, input)

    def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's GET **[Quote Program ID to Label](https://station.jup.ag/docs/api/swap-api/program-id-to-label)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return self._interaction._get_quote_program_id_label(True)

    def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's POST **[Swap](https://station.jup.ag/docs/api/swap-api/swap)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_swap`][cyhole.jupiter.interaction.Jupiter._post_swap]. 
            Observe that this method is a wrapper around the `_post_swap` method with `with_instructions` set to `False`.
        """
        return self._interaction._post_swap(True, body, False)

    def post_swap_instructions(self, body: PostSwapBody) -> PostSwapInstructionsResponse:
        """
            Call the Jupiter's POST **[Swap Instructions](https://station.jup.ag/docs/api/swap-instructions)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_swap`][cyhole.jupiter.interaction.Jupiter._post_swap]. 
            Observe that this method is a wrapper around the `_post_swap` method with `with_instructions` set to `True`.
        """
        return self._interaction._post_swap(True, body, True)

    def get_token_info(self, address: str) -> GetTokenInfoResponse:
        """
            Call the Jupiter's GET **[Token](https://station.jup.ag/docs/api/token-api/token-information)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_info`][cyhole.jupiter.interaction.Jupiter._get_token_info].
        """
        return self._interaction._get_token_info(True, address)

    def get_token_market_mints(self, address: str) -> GetTokenMarketMintsResponse:
        """
            Call the Jupiter's GET **[Token Market Mints](https://station.jup.ag/docs/api/token-api/mints-in-market)** API for synchronous logic.
            All the API endpoint details are available on [`Jupiter._get_token_market_mints`][cyhole.jupiter.interaction.Jupiter._get_token_market_mints].
        """
        return self._interaction._get_token_market_mints(True, address)

    def get_token_new(self, limit: int = 10, offset: int | None = None) -> GetTokenNewResponse:
        """
            Call the Jupiter's GET **[New Token](https://station.jup.ag/docs/api/token-api/new)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_new`][cyhole.jupiter.interaction.Jupiter._get_token_new].
        """
        return self._interaction._get_token_new(True, limit, offset)

    def get_token_tagged(self, tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse:
        """
            Call the Jupiter's GET **[Tagged Token]https://station.jup.ag/docs/api/token-api/tagged)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tagged`][cyhole.jupiter.interaction.Jupiter._get_token_tagged].
        """
        return self._interaction._get_token_tagged(True, tag)

    def get_ultra_order(self, input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra - Get Order](https://station.jup.ag/docs/ultra-api/get-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return self._interaction._get_ultra_order(True, input_token, output_token, input_amount, taker_wallet_key)

    def post_ultra_execute_order(self, signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse:
        """
            Call the Jupiter's POST **[Ultra - Execute Order](https://station.jup.ag/docs/ultra-api/execute-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_ultra_execute_order`][cyhole.jupiter.interaction.Jupiter._post_ultra_execute_order].
        """
        return self._interaction._post_ultra_execute_order(True, signed_transaction_id, request_id)

    def get_ultra_balances(self, wallet_public_key: str) -> GetUltraBalancesResponse:
        """
            Call the Jupiter's GET **[Ultra - Balances](https://station.jup.ag/docs/api/ultra-api/balances)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_balances`][cyhole.jupiter.interaction.Jupiter._get_ultra_balances].
        """
        return self._interaction._get_ultra_balances(True, wallet_public_key)

    def post_trigger_create_order(self, body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Create Order](https://station.jup.ag/docs/api/trigger-api/create-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_create_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_create_order].
        """
        return self._interaction._post_trigger_create_order(True, body)

    def post_trigger_execute(self, signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse:
        """
            Call the Jupiter's POST **[Trigger - Execute](https://station.jup.ag/docs/api/trigger-api/execute)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_execute_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_execute_order].
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

class JupiterAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    async def get_price(self, address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's GET **[Price](https://station.jup.ag/docs/api/price-api/price)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return await self._interaction._get_price(False, address, extra_info, vs_address)

    async def get_quote(self, input: GetQuoteParams) -> GetQuoteResponse:
        """
            Call the Jupiter's GET **[Quote](https://station.jup.ag/docs/api/swap-api/quote)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return await self._interaction._get_quote(False, input)

    async def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's GET **[Quote Program ID to Label](https://station.jup.ag/docs/api/swap-api/program-id-to-label)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return await self._interaction._get_quote_program_id_label(False)

    async def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's POST **[Swap](https://station.jup.ag/docs/api/swap-api/swap)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_swap`][cyhole.jupiter.interaction.Jupiter._post_swap].
            Observe that this method is a wrapper around the `_post_swap` method with `with_instructions` set to `False`.
        """
        return await self._interaction._post_swap(False, body, False)

    async def post_swap_instructions(self, body: PostSwapBody) -> PostSwapInstructionsResponse:
        """
            Call the Jupiter's POST **[Swap Instructions](https://station.jup.ag/docs/api/swap-instructions)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_swap`][cyhole.jupiter.interaction.Jupiter._post_swap].
            Observe that this method is a wrapper around the `_post_swap` method with `with_instructions` set to `True`.
        """
        return await self._interaction._post_swap(False, body, True)

    async def get_token_info(self, address: str) -> GetTokenInfoResponse:
        """
            Call the Jupiter's GET **[Token](https://station.jup.ag/docs/api/token-api/token-information)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_info`][cyhole.jupiter.interaction.Jupiter._get_token_info].
        """
        return await self._interaction._get_token_info(False, address)

    async def get_token_market_mints(self, address: str) -> GetTokenMarketMintsResponse:
        """
            Call the Jupiter's GET **[Token Market Mints](https://station.jup.ag/docs/api/token-api/mints-in-market)** API for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._get_token_market_mints`][cyhole.jupiter.interaction.Jupiter._get_token_market_mints].
        """
        return await self._interaction._get_token_market_mints(False, address)

    async def get_token_tagged(self, tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse:
        """
            Call the Jupiter's GET **[Tagged Token]https://station.jup.ag/docs/api/token-api/tagged)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tagged`][cyhole.jupiter.interaction.Jupiter._get_token_tagged].
        """
        return await self._interaction._get_token_tagged(False, tag)

    async def get_token_new(self, limit: int = 10, offset: int | None = None) -> GetTokenNewResponse:
        """
            Call the Jupiter's GET **[New Token](https://station.jup.ag/docs/api/token-api/new)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_new`][cyhole.jupiter.interaction.Jupiter._get_token_new].
        """
        return await self._interaction._get_token_new(False, limit, offset)

    async def get_ultra_order(self, input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra - Get Order](https://station.jup.ag/docs/ultra-api/get-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return await self._interaction._get_ultra_order(False, input_token, output_token, input_amount, taker_wallet_key)

    async def post_ultra_execute_order(self, signed_transaction_id: str, request_id: str) -> PostUltraExecuteOrderResponse:
        """
            Call the Jupiter's POST **[Ultra - Execute Order](https://station.jup.ag/docs/ultra-api/execute-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_ultra_execute_order`][cyhole.jupiter.interaction.Jupiter._post_ultra_execute_order].
        """
        return await self._interaction._post_ultra_execute_order(False, signed_transaction_id, request_id)

    async def get_ultra_balances(self, wallet_public_key: str) -> GetUltraBalancesResponse:
        """
            Call the Jupiter's GET **[Ultra - Balances](https://station.jup.ag/docs/api/ultra-api/balances)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_balances`][cyhole.jupiter.interaction.Jupiter._get_ultra_balances].
        """
        return await self._interaction._get_ultra_balances(False, wallet_public_key)

    async def post_trigger_create_order(self, body: PostTriggerCreateOrderBody) -> PostTriggerCreateOrderResponse:
        """
            Call the Jupiter's POST **[Trigger - Create Order](https://station.jup.ag/docs/api/trigger-api/create-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_create_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_create_order].
        """
        return await self._interaction._post_trigger_create_order(False, body)

    async def post_trigger_execute(self, signed_transaction_id: str, request_id: str) -> PostTriggerExecuteResponse:
        """
            Call the Jupiter's POST **[Trigger - Execute](https://station.jup.ag/docs/api/trigger-api/execute)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_trigger_execute_order`][cyhole.jupiter.interaction.Jupiter._post_trigger_execute_order].
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