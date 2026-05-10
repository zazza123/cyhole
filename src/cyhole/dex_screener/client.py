from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..dex_screener.schema import (
    GetTokenProfilesLatestResponse,
    GetCommunityTakeoverResponse,
    GetAdsLatestResponse,
    GetTokenBoostsLatestResponse,
    GetTokenBoostsTopResponse,
    GetOrdersResponse,
    GetPairsResponse,
    GetTokensResponse,
    GetTokenPairsResponse,
    GetSearchResponse,
)

if TYPE_CHECKING:
    from ..dex_screener.interaction import DexScreener


class DexScreenerClient(APIClient):
    """Client for synchronous API calls for `DexScreener` interaction."""

    def __init__(self, interaction: DexScreener, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: DexScreener = self._interaction

    def get_token_profiles_latest(self) -> GetTokenProfilesLatestResponse:
        """
        Call the DexScreener's GET **[Token Profiles Latest](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_profiles_latest`][cyhole.dex_screener.interaction.DexScreener._get_token_profiles_latest].
        """
        return self._interaction._get_token_profiles_latest(True)

    def get_community_takeover(self) -> GetCommunityTakeoverResponse:
        """
        Call the DexScreener's GET **[Community Takeovers Latest](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_community_takeover`][cyhole.dex_screener.interaction.DexScreener._get_community_takeover].
        """
        return self._interaction._get_community_takeover(True)

    def get_ads_latest(self) -> GetAdsLatestResponse:
        """
        Call the DexScreener's GET **[Ads Latest](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_ads_latest`][cyhole.dex_screener.interaction.DexScreener._get_ads_latest].
        """
        return self._interaction._get_ads_latest(True)

    def get_token_boosts_latest(self) -> GetTokenBoostsLatestResponse:
        """
        Call the DexScreener's GET **[Token Boosts Latest](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_boosts_latest`][cyhole.dex_screener.interaction.DexScreener._get_token_boosts_latest].
        """
        return self._interaction._get_token_boosts_latest(True)

    def get_token_boosts_top(self) -> GetTokenBoostsTopResponse:
        """
        Call the DexScreener's GET **[Token Boosts Top](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_boosts_top`][cyhole.dex_screener.interaction.DexScreener._get_token_boosts_top].
        """
        return self._interaction._get_token_boosts_top(True)

    def get_orders(self, chain_id: str, token_address: str) -> GetOrdersResponse:
        """
        Call the DexScreener's GET **[Orders](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_orders`][cyhole.dex_screener.interaction.DexScreener._get_orders].
        """
        return self._interaction._get_orders(True, chain_id, token_address)

    def get_pairs(self, chain_id: str, pair_id: str) -> GetPairsResponse:
        """
        Call the DexScreener's GET **[Pairs](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_pairs`][cyhole.dex_screener.interaction.DexScreener._get_pairs].
        """
        return self._interaction._get_pairs(True, chain_id, pair_id)

    def get_tokens(self, chain_id: str, token_addresses: str) -> GetTokensResponse:
        """
        Call the DexScreener's GET **[Tokens](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_tokens`][cyhole.dex_screener.interaction.DexScreener._get_tokens].
        """
        return self._interaction._get_tokens(True, chain_id, token_addresses)

    def get_token_pairs(self, chain_id: str, token_address: str) -> GetTokenPairsResponse:
        """
        Call the DexScreener's GET **[Token Pairs](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_pairs`][cyhole.dex_screener.interaction.DexScreener._get_token_pairs].
        """
        return self._interaction._get_token_pairs(True, chain_id, token_address)

    def get_search(self, query: str) -> GetSearchResponse:
        """
        Call the DexScreener's GET **[Search](https://docs.dexscreener.com/api/reference)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`DexScreener._get_search`][cyhole.dex_screener.interaction.DexScreener._get_search].
        """
        return self._interaction._get_search(True, query)


class DexScreenerAsyncClient(AsyncAPIClient):
    """Client for asynchronous API calls for `DexScreener` interaction."""

    def __init__(self, interaction: DexScreener, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: DexScreener = self._interaction

    async def get_token_profiles_latest(self) -> GetTokenProfilesLatestResponse:
        """
        Call the DexScreener's GET **[Token Profiles Latest](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_profiles_latest`][cyhole.dex_screener.interaction.DexScreener._get_token_profiles_latest].
        """
        return await self._interaction._get_token_profiles_latest(False)

    async def get_community_takeover(self) -> GetCommunityTakeoverResponse:
        """
        Call the DexScreener's GET **[Community Takeovers Latest](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_community_takeover`][cyhole.dex_screener.interaction.DexScreener._get_community_takeover].
        """
        return await self._interaction._get_community_takeover(False)

    async def get_ads_latest(self) -> GetAdsLatestResponse:
        """
        Call the DexScreener's GET **[Ads Latest](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_ads_latest`][cyhole.dex_screener.interaction.DexScreener._get_ads_latest].
        """
        return await self._interaction._get_ads_latest(False)

    async def get_token_boosts_latest(self) -> GetTokenBoostsLatestResponse:
        """
        Call the DexScreener's GET **[Token Boosts Latest](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_boosts_latest`][cyhole.dex_screener.interaction.DexScreener._get_token_boosts_latest].
        """
        return await self._interaction._get_token_boosts_latest(False)

    async def get_token_boosts_top(self) -> GetTokenBoostsTopResponse:
        """
        Call the DexScreener's GET **[Token Boosts Top](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_boosts_top`][cyhole.dex_screener.interaction.DexScreener._get_token_boosts_top].
        """
        return await self._interaction._get_token_boosts_top(False)

    async def get_orders(self, chain_id: str, token_address: str) -> GetOrdersResponse:
        """
        Call the DexScreener's GET **[Orders](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_orders`][cyhole.dex_screener.interaction.DexScreener._get_orders].
        """
        return await self._interaction._get_orders(False, chain_id, token_address)

    async def get_pairs(self, chain_id: str, pair_id: str) -> GetPairsResponse:
        """
        Call the DexScreener's GET **[Pairs](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_pairs`][cyhole.dex_screener.interaction.DexScreener._get_pairs].
        """
        return await self._interaction._get_pairs(False, chain_id, pair_id)

    async def get_tokens(self, chain_id: str, token_addresses: str) -> GetTokensResponse:
        """
        Call the DexScreener's GET **[Tokens](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_tokens`][cyhole.dex_screener.interaction.DexScreener._get_tokens].
        """
        return await self._interaction._get_tokens(False, chain_id, token_addresses)

    async def get_token_pairs(self, chain_id: str, token_address: str) -> GetTokenPairsResponse:
        """
        Call the DexScreener's GET **[Token Pairs](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_token_pairs`][cyhole.dex_screener.interaction.DexScreener._get_token_pairs].
        """
        return await self._interaction._get_token_pairs(False, chain_id, token_address)

    async def get_search(self, query: str) -> GetSearchResponse:
        """
        Call the DexScreener's GET **[Search](https://docs.dexscreener.com/api/reference)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`DexScreener._get_search`][cyhole.dex_screener.interaction.DexScreener._get_search].
        """
        return await self._interaction._get_search(False, query)
