from typing import Any, Coroutine, overload, Literal, Type

from ..core.param import RequestType
from ..core.interaction import Interaction, ResponseModel
from ..dex_screener.client import DexScreenerClient, DexScreenerAsyncClient
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


class DexScreener(Interaction):
    """
    Class used to connect [DexScreener](https://dexscreener.com) API.

    No API key is required for the public endpoints documented here.

    **Example**

    ```python
    import asyncio
    from cyhole.dex_screener import DexScreener

    dex = DexScreener()

    # sync
    response = dex.client.get_token_profiles_latest()
    print(response.root[0].chain_id)

    # async
    async def main():
        async with dex.async_client as client:
            response = await client.get_search("SOL/USDC")
            print(response.pairs[0].pair_address)

    asyncio.run(main())
    ```
    """

    def __init__(self, headers: Any | None = None) -> None:
        super().__init__(headers)
        self.client = DexScreenerClient(self)
        self.async_client = DexScreenerAsyncClient(self)
        self.url_api = "https://api.dexscreener.com/"

    def api_return_model(
        self,
        sync: bool,
        type: str,
        url: str,
        response_model: Type[ResponseModel],
        *args: tuple,
        **kwargs: Any,
    ) -> ResponseModel | Coroutine[None, None, ResponseModel]:
        """
        Override to support both `BaseModel` (dict JSON) and `RootModel` (array JSON) responses.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            type: request type ([`RequestType`][cyhole.core.param.RequestType]).
            url: API endpoint URL.
            response_model: Pydantic model used to parse the response.
            args: positional arguments forwarded to the client.
            kwargs: keyword arguments forwarded to the client.

        Returns:
            Parsed response model or a coroutine that returns it.
        """
        if sync:
            content_raw = self.client.api(type, url, *args, **kwargs)
            return response_model.model_validate(content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(type, url, *args, **kwargs)
                return response_model.model_validate(content_raw.json())
            return async_request()

    # -----------------------------------------------------------------------
    # Token Profiles
    # -----------------------------------------------------------------------

    @overload
    def _get_token_profiles_latest(self, sync: Literal[True]) -> GetTokenProfilesLatestResponse: ...
    @overload
    def _get_token_profiles_latest(self, sync: Literal[False]) -> Coroutine[None, None, GetTokenProfilesLatestResponse]: ...

    def _get_token_profiles_latest(self, sync: bool) -> GetTokenProfilesLatestResponse | Coroutine[None, None, GetTokenProfilesLatestResponse]:
        """
        This function refers to the **GET Token Profiles Latest** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetTokenProfilesLatestResponse: list of the newest token profiles.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "token-profiles/latest/v1"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenProfilesLatestResponse)

    # -----------------------------------------------------------------------
    # Community Takeovers
    # -----------------------------------------------------------------------

    @overload
    def _get_community_takeover(self, sync: Literal[True]) -> GetCommunityTakeoverResponse: ...
    @overload
    def _get_community_takeover(self, sync: Literal[False]) -> Coroutine[None, None, GetCommunityTakeoverResponse]: ...

    def _get_community_takeover(self, sync: bool) -> GetCommunityTakeoverResponse | Coroutine[None, None, GetCommunityTakeoverResponse]:
        """
        This function refers to the **GET Community Takeovers Latest** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetCommunityTakeoverResponse: list of the latest community takeovers.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "community-takeovers/latest/v1"
        return self.api_return_model(sync, RequestType.GET.value, url, GetCommunityTakeoverResponse)

    # -----------------------------------------------------------------------
    # Ads
    # -----------------------------------------------------------------------

    @overload
    def _get_ads_latest(self, sync: Literal[True]) -> GetAdsLatestResponse: ...
    @overload
    def _get_ads_latest(self, sync: Literal[False]) -> Coroutine[None, None, GetAdsLatestResponse]: ...

    def _get_ads_latest(self, sync: bool) -> GetAdsLatestResponse | Coroutine[None, None, GetAdsLatestResponse]:
        """
        This function refers to the **GET Ads Latest** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetAdsLatestResponse: list of the latest advertisements.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "ads/latest/v1"
        return self.api_return_model(sync, RequestType.GET.value, url, GetAdsLatestResponse)

    # -----------------------------------------------------------------------
    # Token Boosts
    # -----------------------------------------------------------------------

    @overload
    def _get_token_boosts_latest(self, sync: Literal[True]) -> GetTokenBoostsLatestResponse: ...
    @overload
    def _get_token_boosts_latest(self, sync: Literal[False]) -> Coroutine[None, None, GetTokenBoostsLatestResponse]: ...

    def _get_token_boosts_latest(self, sync: bool) -> GetTokenBoostsLatestResponse | Coroutine[None, None, GetTokenBoostsLatestResponse]:
        """
        This function refers to the **GET Token Boosts Latest** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetTokenBoostsLatestResponse: list of the latest boosted tokens.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "token-boosts/latest/v1"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenBoostsLatestResponse)

    @overload
    def _get_token_boosts_top(self, sync: Literal[True]) -> GetTokenBoostsTopResponse: ...
    @overload
    def _get_token_boosts_top(self, sync: Literal[False]) -> Coroutine[None, None, GetTokenBoostsTopResponse]: ...

    def _get_token_boosts_top(self, sync: bool) -> GetTokenBoostsTopResponse | Coroutine[None, None, GetTokenBoostsTopResponse]:
        """
        This function refers to the **GET Token Boosts Top** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetTokenBoostsTopResponse: list of tokens with the most active boosts.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "token-boosts/top/v1"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenBoostsTopResponse)

    # -----------------------------------------------------------------------
    # Orders
    # -----------------------------------------------------------------------

    @overload
    def _get_orders(self, sync: Literal[True], chain_id: str, token_address: str) -> GetOrdersResponse: ...
    @overload
    def _get_orders(self, sync: Literal[False], chain_id: str, token_address: str) -> Coroutine[None, None, GetOrdersResponse]: ...

    def _get_orders(self, sync: bool, chain_id: str, token_address: str) -> GetOrdersResponse | Coroutine[None, None, GetOrdersResponse]:
        """
        This function refers to the **GET Orders** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            chain_id: blockchain identifier (e.g. ``"solana"``, ``"ethereum"``).
            token_address: token contract address.

        Returns:
            GetOrdersResponse: list of paid orders for the given token.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + f"orders/v1/{chain_id}/{token_address}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetOrdersResponse)

    # -----------------------------------------------------------------------
    # Pairs
    # -----------------------------------------------------------------------

    @overload
    def _get_pairs(self, sync: Literal[True], chain_id: str, pair_id: str) -> GetPairsResponse: ...
    @overload
    def _get_pairs(self, sync: Literal[False], chain_id: str, pair_id: str) -> Coroutine[None, None, GetPairsResponse]: ...

    def _get_pairs(self, sync: bool, chain_id: str, pair_id: str) -> GetPairsResponse | Coroutine[None, None, GetPairsResponse]:
        """
        This function refers to the **GET Pairs** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            chain_id: blockchain identifier (e.g. ``"solana"``).
            pair_id: pair contract address.

        Returns:
            GetPairsResponse: pair data for the given chain and pair address.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + f"latest/dex/pairs/{chain_id}/{pair_id}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetPairsResponse)

    # -----------------------------------------------------------------------
    # Tokens
    # -----------------------------------------------------------------------

    @overload
    def _get_tokens(self, sync: Literal[True], chain_id: str, token_addresses: str) -> GetTokensResponse: ...
    @overload
    def _get_tokens(self, sync: Literal[False], chain_id: str, token_addresses: str) -> Coroutine[None, None, GetTokensResponse]: ...

    def _get_tokens(self, sync: bool, chain_id: str, token_addresses: str) -> GetTokensResponse | Coroutine[None, None, GetTokensResponse]:
        """
        This function refers to the **GET Tokens** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            chain_id: blockchain identifier (e.g. ``"solana"``).
            token_addresses: comma-separated token addresses (up to 30).

        Returns:
            GetTokensResponse: list of pairs for the given token addresses.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + f"tokens/v1/{chain_id}/{token_addresses}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokensResponse)

    @overload
    def _get_token_pairs(self, sync: Literal[True], chain_id: str, token_address: str) -> GetTokenPairsResponse: ...
    @overload
    def _get_token_pairs(self, sync: Literal[False], chain_id: str, token_address: str) -> Coroutine[None, None, GetTokenPairsResponse]: ...

    def _get_token_pairs(self, sync: bool, chain_id: str, token_address: str) -> GetTokenPairsResponse | Coroutine[None, None, GetTokenPairsResponse]:
        """
        This function refers to the **GET Token Pairs** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            chain_id: blockchain identifier (e.g. ``"solana"``).
            token_address: token contract address.

        Returns:
            GetTokenPairsResponse: list of all pools for the given token.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + f"token-pairs/v1/{chain_id}/{token_address}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenPairsResponse)

    # -----------------------------------------------------------------------
    # Search
    # -----------------------------------------------------------------------

    @overload
    def _get_search(self, sync: Literal[True], query: str) -> GetSearchResponse: ...
    @overload
    def _get_search(self, sync: Literal[False], query: str) -> Coroutine[None, None, GetSearchResponse]: ...

    def _get_search(self, sync: bool, query: str) -> GetSearchResponse | Coroutine[None, None, GetSearchResponse]:
        """
        This function refers to the **GET Search** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            query: search query string (e.g. ``"SOL/USDC"``).

        Returns:
            GetSearchResponse: matching pairs for the given query.

        Raises:
            DexScreenerException: if the API returns an error.
        """
        url = self.url_api + "latest/dex/search"
        params = {"q": query}
        return self.api_return_model(sync, RequestType.GET.value, url, GetSearchResponse, params = params)
