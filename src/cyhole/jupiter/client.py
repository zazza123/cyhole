from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..jupiter.schema import (
    GetPriceResponse,
    GetQuoteInput,
    GetQuoteResponse,
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    PostSwapInstructionsResponse,
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
    GetUltraOrderResponse
)
from ..jupiter.param import JupiterTokenTagType

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
            Call the Jupiter's GET **[Price](https://station.jup.ag/docs/utility/price-api)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return self._interaction._get_price(True, address, extra_info, vs_address)

    def get_quote(self, input: GetQuoteInput) -> GetQuoteResponse:
        """
            Call the Jupiter's GET **[Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return self._interaction._get_quote(True, input)

    def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's GET **[Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return self._interaction._get_quote_program_id_label(True)

    def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's POST **[Swap](https://station.jup.ag/docs/api/swap)** API endpoint for synchronous logic. 
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
            Call the Jupiter's GET **[Token](https://station.jup.ag/docs/api/token-information)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_info`][cyhole.jupiter.interaction.Jupiter._get_token_info].
        """
        return self._interaction._get_token_info(True, address)

    def get_token_market_mints(self, address: str) -> GetTokenMarketMintsResponse:
        """
            Call the Jupiter's GET **[Token Market Mints](https://station.jup.ag/docs/api/mints-in-market)** API for synchronous logic.
            All the API endpoint details are available on [`Jupiter._get_token_market_mints`][cyhole.jupiter.interaction.Jupiter._get_token_market_mints].
        """
        return self._interaction._get_token_market_mints(True, address)

    def get_token_new(self, limit: int = 10, offset: int | None = None) -> GetTokenNewResponse:
        """
            Call the Jupiter's GET **[New Token](https://station.jup.ag/docs/api/new)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_new`][cyhole.jupiter.interaction.Jupiter._get_token_new].
        """
        return self._interaction._get_token_new(True, limit, offset)

    def get_token_tagged(self, tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse:
        """
            Call the Jupiter's GET **[Tagged Token]https://station.jup.ag/docs/api/tagged)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tagged`][cyhole.jupiter.interaction.Jupiter._get_token_tagged].
        """
        return self._interaction._get_token_tagged(True, tag)

    def post_limit_order_create(self, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse:
        """
            Call the Jupiter's POST **[Limit Order - Create](https://station.jup.ag/docs/swap-api/limit-order-api#create-limit-order-transaction)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_limit_order_create`][cyhole.jupiter.interaction.Jupiter._post_limit_order_create].
        """
        return self._interaction._post_limit_order_create(True, body)

    def post_limit_order_cancel(self, body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse:
        """
            Call the Jupiter's POST **[Limit Order - Cancel](https://station.jup.ag/docs/swap-api/limit-order-api#cancel-limit-order-transaction)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_limit_order_cancel`][cyhole.jupiter.interaction.Jupiter._post_limit_order_cancel].
        """
        return self._interaction._post_limit_order_cancel(True, body)

    def get_limit_order_open(self, wallet: str, input_token: str | None = None, output_token: str | None = None) -> GetLimitOrderOpenResponse:
        """
            Call the Jupiter's GET **[Limit Order - Open](https://station.jup.ag/docs/swap-api/limit-order-api#view-open-orders)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_limit_order_open`][cyhole.jupiter.interaction.Jupiter._get_limit_order_open].
        """
        return self._interaction._get_limit_order_open(True, wallet, input_token, output_token)

    def get_limit_order_history(self, wallet: str, page: int = 1) -> GetLimitOrderHistoryResponse:
        """
            Call the Jupiter's GET **[Limit Order - History](https://station.jup.ag/docs/swap-api/limit-order-api#view-order-history)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_limit_order_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_history].
        """
        return self._interaction._get_limit_order_history(True, wallet, page)

    def get_ultra_order(self, input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra Order](https://station.jup.ag/docs/ultra-api/get-order)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return self._interaction._get_ultra_order(True, input_token, output_token, input_amount, taker_wallet_key)

class JupiterAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    async def get_price(self, address: list[str], extra_info: bool = False, vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's GET **[Price](https://station.jup.ag/docs/utility/price-api)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return await self._interaction._get_price(False, address, extra_info, vs_address)

    async def get_quote(self, input: GetQuoteInput) -> GetQuoteResponse:
        """
            Call the Jupiter's GET **[Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return await self._interaction._get_quote(False, input)

    async def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's GET **[Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint for synchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return await self._interaction._get_quote_program_id_label(False)

    async def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's POST **[Swap](https://station.jup.ag/docs/api/swap)** API endpoint for asynchronous logic. 
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
            Call the Jupiter's GET **[Token](https://station.jup.ag/docs/api/token-information)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_info`][cyhole.jupiter.interaction.Jupiter._get_token_info].
        """
        return await self._interaction._get_token_info(False, address)

    async def get_token_market_mints(self, address: str) -> GetTokenMarketMintsResponse:
        """
            Call the Jupiter's GET **[Token Market Mints](https://station.jup.ag/docs/api/mints-in-market)** API for asynchronous logic.
            All the API endpoint details are available on [`Jupiter._get_token_market_mints`][cyhole.jupiter.interaction.Jupiter._get_token_market_mints].
        """
        return await self._interaction._get_token_market_mints(False, address)

    async def get_token_tagged(self, tag: str | JupiterTokenTagType) -> GetTokenTaggedResponse:
        """
            Call the Jupiter's GET **[Tagged Token]https://station.jup.ag/docs/api/tagged)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_tagged`][cyhole.jupiter.interaction.Jupiter._get_token_tagged].
        """
        return await self._interaction._get_token_tagged(False, tag)

    async def get_token_new(self, limit: int = 10, offset: int | None = None) -> GetTokenNewResponse:
        """
            Call the Jupiter's GET **[New Token](https://station.jup.ag/docs/api/new)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_token_new`][cyhole.jupiter.interaction.Jupiter._get_token_new].
        """
        return await self._interaction._get_token_new(False, limit, offset)

    async def post_limit_order_create(self, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse:
        """
            Call the Jupiter's POST **[Limit Order - Create](https://station.jup.ag/docs/swap-api/limit-order-api#create-limit-order-transaction)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_limit_order_create`][cyhole.jupiter.interaction.Jupiter._post_limit_order_create].
        """
        return await self._interaction._post_limit_order_create(False, body)

    async def post_limit_order_cancel(self, body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse:
        """
            Call the Jupiter's POST **[Limit Order - Cancel](https://station.jup.ag/docs/swap-api/limit-order-api#cancel-limit-order-transaction)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._post_limit_order_cancel`][cyhole.jupiter.interaction.Jupiter._post_limit_order_cancel].
        """
        return await self._interaction._post_limit_order_cancel(False, body)

    async def get_limit_order_open(self, wallet: str, input_token: str | None = None, output_token: str | None = None) -> GetLimitOrderOpenResponse:
        """
            Call the Jupiter's GET **[Limit Order - Open](https://station.jup.ag/docs/swap-api/limit-order-api#view-open-orders)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_limit_order_open`][cyhole.jupiter.interaction.Jupiter._get_limit_order_open].
        """
        return await self._interaction._get_limit_order_open(False, wallet, input_token, output_token)

    async def get_limit_order_history(self, wallet: str, page: int = 1) -> GetLimitOrderHistoryResponse:
        """
            Call the Jupiter's GET **[Limit Order - History](https://station.jup.ag/docs/swap-api/limit-order-api#view-order-history)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_limit_order_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_history].
        """
        return await self._interaction._get_limit_order_history(False, wallet, page)

    async def get_ultra_order(self, input_token: str, output_token: str, input_amount: int, taker_wallet_key: str | None = None) -> GetUltraOrderResponse:
        """
            Call the Jupiter's GET **[Ultra Order](https://station.jup.ag/docs/ultra-api/get-order)** API endpoint for asynchronous logic. 
            All the API endpoint details are available on [`Jupiter._get_ultra_order`][cyhole.jupiter.interaction.Jupiter._get_ultra_order].
        """
        return await self._interaction._get_ultra_order(False, input_token, output_token, input_amount, taker_wallet_key)