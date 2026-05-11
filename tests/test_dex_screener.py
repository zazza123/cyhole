import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from cyhole.dex_screener import DexScreener
from cyhole.dex_screener.schema import (
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

from .config import load_config, MockerManager

config = load_config()
mock_path = Path(config.mock_folder) / config.dex_screener.mock_folder


class TestDexScreener:
    """Class grouping all unit tests for DexScreener interaction."""

    dex = DexScreener()
    mocker = MockerManager(mock_path)

    # -----------------------------------------------------------------------
    # Token Profiles Latest
    # -----------------------------------------------------------------------

    def test_get_token_profiles_latest_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Profiles Latest" — synchronous logic.

        Mock Response File: getTokenProfilesLatest_default.json
        """
        mock_file_name = "getTokenProfilesLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenProfilesLatestResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_token_profiles_latest()
        assert isinstance(response, GetTokenProfilesLatestResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_profiles_latest_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Profiles Latest" — asynchronous logic.

        Mock Response File: getTokenProfilesLatest_default.json
        """
        mock_file_name = "getTokenProfilesLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenProfilesLatestResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_token_profiles_latest()
        assert isinstance(response, GetTokenProfilesLatestResponse)

    # -----------------------------------------------------------------------
    # Community Takeover
    # -----------------------------------------------------------------------

    def test_get_community_takeover_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Community Takeovers Latest" — synchronous logic.

        Mock Response File: getCommunityTakeover_default.json
        """
        mock_file_name = "getCommunityTakeover_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetCommunityTakeoverResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_community_takeover()
        assert isinstance(response, GetCommunityTakeoverResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_community_takeover_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Community Takeovers Latest" — asynchronous logic.

        Mock Response File: getCommunityTakeover_default.json
        """
        mock_file_name = "getCommunityTakeover_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetCommunityTakeoverResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_community_takeover()
        assert isinstance(response, GetCommunityTakeoverResponse)

    # -----------------------------------------------------------------------
    # Ads Latest
    # -----------------------------------------------------------------------

    def test_get_ads_latest_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Ads Latest" — synchronous logic.

        Mock Response File: getAdsLatest_default.json
        """
        mock_file_name = "getAdsLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAdsLatestResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_ads_latest()
        assert isinstance(response, GetAdsLatestResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ads_latest_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Ads Latest" — asynchronous logic.

        Mock Response File: getAdsLatest_default.json
        """
        mock_file_name = "getAdsLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetAdsLatestResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_ads_latest()
        assert isinstance(response, GetAdsLatestResponse)

    # -----------------------------------------------------------------------
    # Token Boosts Latest
    # -----------------------------------------------------------------------

    def test_get_token_boosts_latest_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Boosts Latest" — synchronous logic.

        Mock Response File: getTokenBoostsLatest_default.json
        """
        mock_file_name = "getTokenBoostsLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenBoostsLatestResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_token_boosts_latest()
        assert isinstance(response, GetTokenBoostsLatestResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_boosts_latest_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Boosts Latest" — asynchronous logic.

        Mock Response File: getTokenBoostsLatest_default.json
        """
        mock_file_name = "getTokenBoostsLatest_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenBoostsLatestResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_token_boosts_latest()
        assert isinstance(response, GetTokenBoostsLatestResponse)

    # -----------------------------------------------------------------------
    # Token Boosts Top
    # -----------------------------------------------------------------------

    def test_get_token_boosts_top_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Boosts Top" — synchronous logic.

        Mock Response File: getTokenBoostsTop_default.json
        """
        mock_file_name = "getTokenBoostsTop_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenBoostsTopResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_token_boosts_top()
        assert isinstance(response, GetTokenBoostsTopResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_boosts_top_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Boosts Top" — asynchronous logic.

        Mock Response File: getTokenBoostsTop_default.json
        """
        mock_file_name = "getTokenBoostsTop_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenBoostsTopResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_token_boosts_top()
        assert isinstance(response, GetTokenBoostsTopResponse)

    # -----------------------------------------------------------------------
    # Orders
    # -----------------------------------------------------------------------

    def test_get_orders_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Orders" — synchronous logic.

        Mock Response File: getOrders_default.json
        """
        mock_file_name = "getOrders_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_orders("solana", "A55XjvzRU4KtR3Lrys8PpLZQvPojPqvnv5bJVHMYy3Jv")
        assert isinstance(response, GetOrdersResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_orders_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Orders" — asynchronous logic.

        Mock Response File: getOrders_default.json
        """
        mock_file_name = "getOrders_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_orders("solana", "A55XjvzRU4KtR3Lrys8PpLZQvPojPqvnv5bJVHMYy3Jv")
        assert isinstance(response, GetOrdersResponse)

    # -----------------------------------------------------------------------
    # Pairs
    # -----------------------------------------------------------------------

    def test_get_pairs_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pairs" — synchronous logic.

        Mock Response File: getPairs_default.json
        """
        mock_file_name = "getPairs_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPairsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_pairs("solana", "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
        assert isinstance(response, GetPairsResponse)
        assert response.pairs is not None
        assert len(response.pairs) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pairs_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pairs" — asynchronous logic.

        Mock Response File: getPairs_default.json
        """
        mock_file_name = "getPairs_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPairsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_pairs("solana", "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
        assert isinstance(response, GetPairsResponse)

    # -----------------------------------------------------------------------
    # Tokens
    # -----------------------------------------------------------------------

    def test_get_tokens_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Tokens" — synchronous logic.

        Mock Response File: getTokens_default.json
        """
        mock_file_name = "getTokens_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokensResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_tokens("solana", "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
        assert isinstance(response, GetTokensResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_tokens_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Tokens" — asynchronous logic.

        Mock Response File: getTokens_default.json
        """
        mock_file_name = "getTokens_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokensResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_tokens("solana", "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
        assert isinstance(response, GetTokensResponse)

    # -----------------------------------------------------------------------
    # Token Pairs
    # -----------------------------------------------------------------------

    def test_get_token_pairs_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Pairs" — synchronous logic.

        Mock Response File: getTokenPairs_default.json
        """
        mock_file_name = "getTokenPairs_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenPairsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_token_pairs("solana", "So11111111111111111111111111111111111111112")
        assert isinstance(response, GetTokenPairsResponse)
        assert len(response.root) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_pairs_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Pairs" — asynchronous logic.

        Mock Response File: getTokenPairs_default.json
        """
        mock_file_name = "getTokenPairs_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenPairsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_token_pairs("solana", "So11111111111111111111111111111111111111112")
        assert isinstance(response, GetTokenPairsResponse)

    # -----------------------------------------------------------------------
    # Search
    # -----------------------------------------------------------------------

    def test_get_search_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Search" — synchronous logic.

        Mock Response File: getSearch_default.json
        """
        mock_file_name = "getSearch_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSearchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.dex.client.get_search("SOL/USDC")
        assert isinstance(response, GetSearchResponse)
        assert len(response.pairs) > 0

        if config.mock_file_overwrite and not config.dex_screener.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_search_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Search" — asynchronous logic.

        Mock Response File: getSearch_default.json
        """
        mock_file_name = "getSearch_default"
        if config.mock_response or config.dex_screener.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSearchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.dex.async_client as client:
            response = await client.get_search("SOL/USDC")
        assert isinstance(response, GetSearchResponse)
