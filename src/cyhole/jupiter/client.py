from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..jupiter.schema import (
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
from ..jupiter.param import JupiterTokenListType

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
            Call the Jupiter's **[Price](https://station.jup.ag/docs/apis/price-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return self._interaction._get_price(True, address, vs_address)

    def get_quote(self, input: GetQuoteInput) -> GetQuoteResponse:
        """
            Call the Jupiter's **[Get Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return self._interaction._get_quote(True, input)

    def get_quote_tokens(self) -> GetQuoteTokensResponse:
        """
            Call the Jupiter's **[Get Quote Tokens](https://station.jup.ag/api-v6/get-tokens)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote_tokens`][cyhole.jupiter.interaction.Jupiter._get_quote_tokens].
        """
        return self._interaction._get_quote_tokens(True)

    def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's **[Get Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return self._interaction._get_quote_program_id_label(True)

    def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's **[Post Swap](https://station.jup.ag/api-v6/post-swap)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._post_swap`][cyhole.jupiter.interaction.Jupiter._post_swap].
        """
        return self._interaction._post_swap(True, body)

    def get_token_list(self, type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> GetTokenListResponse:
        """
            Call the Jupiter's **[Token List](https://station.jup.ag/docs/token-list/token-list-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_token_list`][cyhole.jupiter.interaction.Jupiter._get_token_list].
        """
        return self._interaction._get_token_list(True, type, banned)

    def post_limit_order_create(self, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse:
        """
            Call the Jupiter's **[Post Limit Order - Create](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._post_limit_order_create`][cyhole.jupiter.interaction.Jupiter._post_limit_order_create].
        """
        return self._interaction._post_limit_order_create(True, body)

    def post_limit_order_cancel(self, body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse:
        """
            Call the Jupiter's **[Post Limit Order - Cancel](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._post_limit_order_cancel`][cyhole.jupiter.interaction.Jupiter._post_limit_order_cancel].
        """
        return self._interaction._post_limit_order_cancel(True, body)

    def get_limit_order_open(
            self,
            wallet: str | None = None,
            input_token: str | None = None,
            output_token: str | None = None
        ) -> GetLimitOrderOpenResponse:
        """
            Call the Jupiter's **[Get Limit Order - Open](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_open`][cyhole.jupiter.interaction.Jupiter._get_limit_order_open].
        """
        return self._interaction._get_limit_order_open(True, wallet, input_token, output_token)

    def get_limit_order_history(
        self,
        wallet: str,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderHistoryResponse:
        """
            Call the Jupiter's **[Get Limit Order - History](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_history].
        """
        return self._interaction._get_limit_order_history(True, wallet, cursor, skip, take)

    def get_limit_order_trade_history(
        self,
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderTradeHistoryResponse:
        """
            Call the Jupiter's **[Get Limit Order - Trade History](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_trade_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_trade_history].
        """
        return self._interaction._get_limit_order_trade_history(True, wallet, input_token, output_token, cursor, skip, take)

class JupiterAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Jupiter` interaction.
    """

    def __init__(self, interaction: Jupiter, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Jupiter = self._interaction

    async def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            Call the Jupiter's **[Price](https://station.jup.ag/docs/apis/price-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_price`][cyhole.jupiter.interaction.Jupiter._get_price].
        """
        return await self._interaction._get_price(False, address, vs_address)

    async def get_quote(self, input: GetQuoteInput) -> GetQuoteResponse:
        """
            Call the Jupiter's **[Get Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote`][cyhole.jupiter.interaction.Jupiter._get_quote].
        """
        return await self._interaction._get_quote(False, input)

    async def get_quote_tokens(self) -> GetQuoteTokensResponse:
        """
            Call the Jupiter's **[Get Quote Tokens](https://station.jup.ag/api-v6/get-tokens)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote_tokens`][cyhole.jupiter.interaction.Jupiter._get_quote_tokens].
        """
        return await self._interaction._get_quote_tokens(False)

    async def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            Call the Jupiter's **[Get Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint for synchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return await self._interaction._get_quote_program_id_label(False)

    async def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            Call the Jupiter's **[Post Swap](https://station.jup.ag/api-v6/post-swap)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_quote_program_id_label`][cyhole.jupiter.interaction.Jupiter._get_quote_program_id_label].
        """
        return await self._interaction._post_swap(False, body)

    async def get_token_list(self, type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> GetTokenListResponse:
        """
            Call the Jupiter's **[Token List](https://station.jup.ag/docs/token-list/token-list-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_token_list`][cyhole.jupiter.interaction.Jupiter._get_token_list].
        """
        return await self._interaction._get_token_list(False, type, banned)

    async def post_limit_order_create(self, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse:
        """
            Call the Jupiter's **[Post Limit Order - Create](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._post_limit_order_create`][cyhole.jupiter.interaction.Jupiter._post_limit_order_create].
        """
        return await self._interaction._post_limit_order_create(False, body)

    async def post_limit_order_cancel(self, body: PostLimitOrderCancelBody) -> PostLimitOrderCancelResponse:
        """
            Call the Jupiter's **[Post Limit Order - Cancel](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._post_limit_order_cancel`][cyhole.jupiter.interaction.Jupiter._post_limit_order_cancel].
        """
        return await self._interaction._post_limit_order_cancel(False, body)

    async def get_limit_order_open(
            self,
            wallet: str | None = None,
            input_token: str | None = None,
            output_token: str | None = None
        ) -> GetLimitOrderOpenResponse:
        """
            Call the Jupiter's **[Get Limit Order - Open](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_open`][cyhole.jupiter.interaction.Jupiter._get_limit_order_open].
        """
        return await self._interaction._get_limit_order_open(False, wallet, input_token, output_token)

    async def get_limit_order_history(
        self,
        wallet: str,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderHistoryResponse:
        """
            Call the Jupiter's **[Get Limit Order - History](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_history].
        """
        return await self._interaction._get_limit_order_history(False, wallet, cursor, skip, take)

    async def get_limit_order_trade_history(
        self,
        wallet: str | None = None,
        input_token: str | None = None,
        output_token: str | None = None,
        cursor: int | None = None,
        skip: int | None = None,
        take: int | None = None
    ) -> GetLimitOrderTradeHistoryResponse:
        """
            Call the Jupiter's **[Get Limit Order - Trade History](https://station.jup.ag/docs/limit-order/limit-order-api)** API endpoint for asynchronous logic. 
            All the API endopint details are available on [`Jupiter._get_limit_order_trade_history`][cyhole.jupiter.interaction.Jupiter._get_limit_order_trade_history].
        """
        return await self._interaction._get_limit_order_trade_history(False, wallet, input_token, output_token, cursor, skip, take)