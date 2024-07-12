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