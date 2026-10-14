import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from cyhole.gecko import Gecko
from cyhole.gecko.schema import (
    GetNetworksResponse,
    GetDexesResponse,
    GetPoolOHLCVResponse,
    GetPoolTokenInfoResponse,
    GetPoolTradesResponse,
    GetTokenDataResponse,
    GetTokenDataMultipleResponse,
    GetTokenInfoResponse,
    GetRecentlyUpdatedTokensResponse,
    GetTokenOHLCVResponse,
    GetTokenTradesResponse,
    GetTokenHoldersChartResponse,
    GetTopTokenHoldersResponse,
    GetTopTokenTradersResponse,
    GetSimpleTokenPriceResponse,
    GetSearchPoolsResponse,
    GetNetworkNewPoolsResponse,
    GetNewPoolsResponse,
    GetPoolsMultiResponse,
)
from cyhole.gecko.exception import GeckoAddressCountError
from cyhole.gecko.param import GeckoNewPoolsInclude, GeckoPoolInclude

from .config import load_config, MockerManager

config = load_config()
mock_path = Path(config.mock_folder) / config.gecko.mock_folder


# Well-known reference addresses used across the tests. These values are only used to drive live API
# calls when mock fixtures are being (re)generated — under the default mocked-response mode the
# addresses are part of the URL but the HTTP layer is patched and never actually invoked.
TEST_NETWORK = "eth"
TEST_POOL_ADDRESS = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"  # USDC/WETH Uniswap V3 pool
TEST_TOKEN_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # WETH
TEST_TOKEN_ADDRESS_2 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC

# Solana pools used by the New Pools / Multiple Pools Data tests (the mocks were captured on Solana).
TEST_POOLS_NETWORK = "solana"
TEST_POOLS_ADDRESSES = [
    "GKzFauhpZuqRPnMS1yK3LeWkAW4UgmYbESfSxeo71UTL",  # TOAD / PSOL on StonkFun
    "CMBcQWsRuodcP5TjfV1vYc2jKJUM3McxbpBgZRkNkm8Y",  # pump.fun bonding curve
    "EiEaXboo2b59AMu69VLgeLZYFYTq3iuKJNoBKhySeZjK",  # Meteora DAMM v2
]
TEST_POOLS_INCLUDE = ",".join([GeckoPoolInclude.BASE_TOKEN.value, GeckoPoolInclude.QUOTE_TOKEN.value, GeckoPoolInclude.DEX.value])


class TestGecko:
    """Class grouping all unit tests for Gecko interaction."""

    gecko = Gecko(api_key = config.gecko.api_key)
    mocker = MockerManager(mock_path)

    # -------------------------------------------------------------------
    # Networks
    # -------------------------------------------------------------------

    def test_get_networks_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Networks" — synchronous logic.

        Mock Response File: getNetworks_default.json
        """
        mock_file_name = "getNetworks_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNetworksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_networks()
        assert isinstance(response, GetNetworksResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_networks_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Networks" — asynchronous logic.

        Mock Response File: getNetworks_default.json
        """
        mock_file_name = "getNetworks_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNetworksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_networks()
        assert isinstance(response, GetNetworksResponse)

    # -------------------------------------------------------------------
    # Dexes by Network
    # -------------------------------------------------------------------

    def test_get_dexes_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Dexes by Network" — synchronous logic.

        Mock Response File: getDexes_default.json
        """
        mock_file_name = "getDexes_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDexesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_dexes(TEST_NETWORK)
        assert isinstance(response, GetDexesResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_dexes_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Dexes by Network" — asynchronous logic.

        Mock Response File: getDexes_default.json
        """
        mock_file_name = "getDexes_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDexesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_dexes(TEST_NETWORK)
        assert isinstance(response, GetDexesResponse)

    # -------------------------------------------------------------------
    # Pool OHLCV
    # -------------------------------------------------------------------

    def test_get_pool_ohlcv_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool OHLCV" — synchronous logic.

        Mock Response File: getPoolOhlcv_default.json
        """
        mock_file_name = "getPoolOhlcv_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolOHLCVResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_pool_ohlcv(TEST_NETWORK, TEST_POOL_ADDRESS, "day")
        assert isinstance(response, GetPoolOHLCVResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pool_ohlcv_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool OHLCV" — asynchronous logic.

        Mock Response File: getPoolOhlcv_default.json
        """
        mock_file_name = "getPoolOhlcv_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolOHLCVResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_pool_ohlcv(TEST_NETWORK, TEST_POOL_ADDRESS, "day")
        assert isinstance(response, GetPoolOHLCVResponse)

    # -------------------------------------------------------------------
    # Pool Tokens Info
    # -------------------------------------------------------------------

    def test_get_pool_token_info_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool Tokens Info" — synchronous logic.

        Mock Response File: getPoolTokenInfo_default.json
        """
        mock_file_name = "getPoolTokenInfo_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolTokenInfoResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_pool_token_info(TEST_NETWORK, TEST_POOL_ADDRESS)
        assert isinstance(response, GetPoolTokenInfoResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pool_token_info_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool Tokens Info" — asynchronous logic.

        Mock Response File: getPoolTokenInfo_default.json
        """
        mock_file_name = "getPoolTokenInfo_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolTokenInfoResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_pool_token_info(TEST_NETWORK, TEST_POOL_ADDRESS)
        assert isinstance(response, GetPoolTokenInfoResponse)

    # -------------------------------------------------------------------
    # Pool Trades
    # -------------------------------------------------------------------

    def test_get_pool_trades_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool Trades" — synchronous logic.

        Mock Response File: getPoolTrades_default.json
        """
        mock_file_name = "getPoolTrades_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolTradesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_pool_trades(TEST_NETWORK, TEST_POOL_ADDRESS)
        assert isinstance(response, GetPoolTradesResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pool_trades_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Pool Trades" — asynchronous logic.

        Mock Response File: getPoolTrades_default.json
        """
        mock_file_name = "getPoolTrades_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolTradesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_pool_trades(TEST_NETWORK, TEST_POOL_ADDRESS)
        assert isinstance(response, GetPoolTradesResponse)

    # -------------------------------------------------------------------
    # Token Data — single
    # -------------------------------------------------------------------

    def test_get_token_data_single_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Data (single)" — synchronous logic.

        Mock Response File: getTokenData_single.json
        """
        mock_file_name = "getTokenData_single"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_data(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenDataResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_data_single_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Data (single)" — asynchronous logic.

        Mock Response File: getTokenData_single.json
        """
        mock_file_name = "getTokenData_single"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_data(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenDataResponse)

    # -------------------------------------------------------------------
    # Token Data — multiple
    # -------------------------------------------------------------------

    def test_get_token_data_multiple_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Data (multiple)" — synchronous logic.

        Mock Response File: getTokenData_multiple.json
        """
        mock_file_name = "getTokenData_multiple"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDataMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_data(TEST_NETWORK, [TEST_TOKEN_ADDRESS, TEST_TOKEN_ADDRESS_2])
        assert isinstance(response, GetTokenDataMultipleResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_data_multiple_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Data (multiple)" — asynchronous logic.

        Mock Response File: getTokenData_multiple.json
        """
        mock_file_name = "getTokenData_multiple"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenDataMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_data(TEST_NETWORK, [TEST_TOKEN_ADDRESS, TEST_TOKEN_ADDRESS_2])
        assert isinstance(response, GetTokenDataMultipleResponse)

    # -------------------------------------------------------------------
    # Token Info
    # -------------------------------------------------------------------

    def test_get_token_info_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Info" — synchronous logic.

        Mock Response File: getTokenInfo_default.json
        """
        mock_file_name = "getTokenInfo_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_info(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenInfoResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_info_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Info" — asynchronous logic.

        Mock Response File: getTokenInfo_default.json
        """
        mock_file_name = "getTokenInfo_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_info(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenInfoResponse)

    # -------------------------------------------------------------------
    # Recently Updated Tokens
    # -------------------------------------------------------------------

    def test_get_recently_updated_tokens_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Recently Updated Tokens" — synchronous logic.

        Mock Response File: getRecentlyUpdatedTokens_default.json
        """
        mock_file_name = "getRecentlyUpdatedTokens_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecentlyUpdatedTokensResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_recently_updated_tokens()
        assert isinstance(response, GetRecentlyUpdatedTokensResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_recently_updated_tokens_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Recently Updated Tokens" — asynchronous logic.

        Mock Response File: getRecentlyUpdatedTokens_default.json
        """
        mock_file_name = "getRecentlyUpdatedTokens_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecentlyUpdatedTokensResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_recently_updated_tokens()
        assert isinstance(response, GetRecentlyUpdatedTokensResponse)

    # -------------------------------------------------------------------
    # Token OHLCV
    # -------------------------------------------------------------------

    def test_get_token_ohlcv_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token OHLCV" — synchronous logic.

        Mock Response File: getTokenOhlcv_default.json
        """
        mock_file_name = "getTokenOhlcv_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOHLCVResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_ohlcv(TEST_NETWORK, TEST_TOKEN_ADDRESS, "day")
        assert isinstance(response, GetTokenOHLCVResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_ohlcv_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token OHLCV" — asynchronous logic.

        Mock Response File: getTokenOhlcv_default.json
        """
        mock_file_name = "getTokenOhlcv_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOHLCVResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_ohlcv(TEST_NETWORK, TEST_TOKEN_ADDRESS, "day")
        assert isinstance(response, GetTokenOHLCVResponse)

    # -------------------------------------------------------------------
    # Token Trades
    # -------------------------------------------------------------------

    def test_get_token_trades_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Trades" — synchronous logic.

        Mock Response File: getTokenTrades_default.json
        """
        mock_file_name = "getTokenTrades_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTradesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_trades(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenTradesResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_trades_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Trades" — asynchronous logic.

        Mock Response File: getTokenTrades_default.json
        """
        mock_file_name = "getTokenTrades_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTradesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_trades(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenTradesResponse)

    # -------------------------------------------------------------------
    # Token Holders Chart
    # -------------------------------------------------------------------

    def test_get_token_holders_chart_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Holders Chart" — synchronous logic.

        Mock Response File: getTokenHoldersChart_default.json
        """
        mock_file_name = "getTokenHoldersChart_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersChartResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_token_holders_chart(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenHoldersChartResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holders_chart_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Token Holders Chart" — asynchronous logic.

        Mock Response File: getTokenHoldersChart_default.json
        """
        mock_file_name = "getTokenHoldersChart_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHoldersChartResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_token_holders_chart(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTokenHoldersChartResponse)

    # -------------------------------------------------------------------
    # Top Token Holders
    # -------------------------------------------------------------------

    def test_get_top_token_holders_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Top Token Holders" — synchronous logic.

        Mock Response File: getTopTokenHolders_default.json
        """
        mock_file_name = "getTopTokenHolders_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTopTokenHoldersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_top_token_holders(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTopTokenHoldersResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_top_token_holders_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Top Token Holders" — asynchronous logic.

        Mock Response File: getTopTokenHolders_default.json
        """
        mock_file_name = "getTopTokenHolders_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTopTokenHoldersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_top_token_holders(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTopTokenHoldersResponse)

    # -------------------------------------------------------------------
    # Top Token Traders
    # -------------------------------------------------------------------

    def test_get_top_token_traders_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Top Token Traders" — synchronous logic.

        Mock Response File: getTopTokenTraders_default.json
        """
        mock_file_name = "getTopTokenTraders_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTopTokenTradersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_top_token_traders(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTopTokenTradersResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_top_token_traders_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Top Token Traders" — asynchronous logic.

        Mock Response File: getTopTokenTraders_default.json
        """
        mock_file_name = "getTopTokenTraders_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTopTokenTradersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_top_token_traders(TEST_NETWORK, TEST_TOKEN_ADDRESS)
        assert isinstance(response, GetTopTokenTradersResponse)

    # -------------------------------------------------------------------
    # Simple Token Price
    # -------------------------------------------------------------------

    def test_get_simple_token_price_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Simple Token Price" — synchronous logic.

        Mock Response File: getSimpleTokenPrice_default.json
        """
        mock_file_name = "getSimpleTokenPrice_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSimpleTokenPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_simple_token_price(TEST_NETWORK, [TEST_TOKEN_ADDRESS, TEST_TOKEN_ADDRESS_2])
        assert isinstance(response, GetSimpleTokenPriceResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_simple_token_price_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Simple Token Price" — asynchronous logic.

        Mock Response File: getSimpleTokenPrice_default.json
        """
        mock_file_name = "getSimpleTokenPrice_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSimpleTokenPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_simple_token_price(TEST_NETWORK, [TEST_TOKEN_ADDRESS, TEST_TOKEN_ADDRESS_2])
        assert isinstance(response, GetSimpleTokenPriceResponse)

    # -------------------------------------------------------------------
    # Search Pools
    # -------------------------------------------------------------------

    def test_get_search_pools_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Search Pools" — synchronous logic.

        Mock Response File: getSearchPools_default.json
        """
        mock_file_name = "getSearchPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSearchPoolsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_search_pools("USDC")
        assert isinstance(response, GetSearchPoolsResponse)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_search_pools_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Search Pools" — asynchronous logic.

        Mock Response File: getSearchPools_default.json
        """
        mock_file_name = "getSearchPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSearchPoolsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_search_pools("USDC")
        assert isinstance(response, GetSearchPoolsResponse)

    # -------------------------------------------------------------------
    # New Pools by Network
    # -------------------------------------------------------------------

    def test_get_network_new_pools_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools by Network" — synchronous logic.

        Mock Response File: getNetworkNewPools_default.json
        """
        mock_file_name = "getNetworkNewPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNetworkNewPoolsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_network_new_pools(TEST_POOLS_NETWORK, include = TEST_POOLS_INCLUDE)
        assert isinstance(response, GetNetworkNewPoolsResponse)
        assert 0 < len(response.data) <= 20
        assert response.included is not None

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_network_new_pools_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools by Network" — asynchronous logic.

        Mock Response File: getNetworkNewPools_default.json
        """
        mock_file_name = "getNetworkNewPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNetworkNewPoolsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_network_new_pools(TEST_POOLS_NETWORK, include = TEST_POOLS_INCLUDE)
        assert isinstance(response, GetNetworkNewPoolsResponse)
        assert 0 < len(response.data) <= 20

    def test_get_network_new_pools_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools by Network" — request sent to the API.

        Checks the URL and the query parameters, with and without the optional `include` and `page`.

        Mock Response File: getNetworkNewPools_default.json
        """
        mock_response = self.mocker.load_mock_response("getNetworkNewPools_default", GetNetworkNewPoolsResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.gecko.client.get_network_new_pools(TEST_POOLS_NETWORK)
        args, kwargs = api.call_args
        assert args[0] == "GET"
        assert args[1] == self.gecko.url_api + f"networks/{TEST_POOLS_NETWORK}/new_pools"
        assert kwargs["params"] == {}

        self.gecko.client.get_network_new_pools(TEST_POOLS_NETWORK, include = TEST_POOLS_INCLUDE, page = 3)
        _, kwargs = api.call_args
        assert kwargs["params"] == {"include": "base_token,quote_token,dex", "page": 3}

    # -------------------------------------------------------------------
    # New Pools (all networks)
    # -------------------------------------------------------------------

    def test_get_new_pools_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools" — synchronous logic.

        Mock Response File: getNewPools_default.json
        """
        mock_file_name = "getNewPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNewPoolsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_new_pools()
        assert isinstance(response, GetNewPoolsResponse)
        assert 0 < len(response.data) <= 20
        assert all(pool.relationships is not None and pool.relationships.network is not None for pool in response.data)

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_new_pools_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools" — asynchronous logic.

        Mock Response File: getNewPools_default.json
        """
        mock_file_name = "getNewPools_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetNewPoolsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_new_pools()
        assert isinstance(response, GetNewPoolsResponse)
        assert 0 < len(response.data) <= 20

    def test_get_new_pools_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "New Pools" — request sent to the API.

        Checks the URL and the query parameters, with and without the optional `include` and `page`.

        Mock Response File: getNewPools_default.json
        """
        mock_response = self.mocker.load_mock_response("getNewPools_default", GetNewPoolsResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.gecko.client.get_new_pools()
        args, kwargs = api.call_args
        assert args[0] == "GET"
        assert args[1] == self.gecko.url_api + "networks/new_pools"
        assert kwargs["params"] == {}

        include = ",".join([GeckoNewPoolsInclude.DEX.value, GeckoNewPoolsInclude.NETWORK.value])
        self.gecko.client.get_new_pools(include = include, page = 10)
        _, kwargs = api.call_args
        assert kwargs["params"] == {"include": "dex,network", "page": 10}

    # -------------------------------------------------------------------
    # Multiple Pools Data
    # -------------------------------------------------------------------

    def test_get_pools_multi_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Multiple Pools Data" — synchronous logic.

        Mock Response File: getPoolsMulti_default.json
        """
        mock_file_name = "getPoolsMulti_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolsMultiResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES, include = TEST_POOLS_INCLUDE)
        assert isinstance(response, GetPoolsMultiResponse)
        assert {pool.attributes.address for pool in response.data} <= set(TEST_POOLS_ADDRESSES)
        assert response.included is not None

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pools_multi_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Multiple Pools Data" — asynchronous logic.

        Mock Response File: getPoolsMulti_default.json
        """
        mock_file_name = "getPoolsMulti_default"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolsMultiResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES, include = TEST_POOLS_INCLUDE)
        assert isinstance(response, GetPoolsMultiResponse)

    def test_get_pools_multi_volume_breakdown_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Multiple Pools Data" with `include_volume_breakdown=True` — synchronous logic.

        Mock Response File: getPoolsMulti_volumeBreakdown.json
        """
        mock_file_name = "getPoolsMulti_volumeBreakdown"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolsMultiResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.gecko.client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES[:1], include_volume_breakdown = True)
        assert isinstance(response, GetPoolsMultiResponse)
        for pool in response.data:
            assert pool.attributes.buy_volume_usd is not None
            assert pool.attributes.sell_volume_usd is not None

        if config.mock_file_overwrite and not config.gecko.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_pools_multi_volume_breakdown_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Multiple Pools Data" with `include_volume_breakdown=True` — asynchronous logic.

        Mock Response File: getPoolsMulti_volumeBreakdown.json
        """
        mock_file_name = "getPoolsMulti_volumeBreakdown"
        if config.mock_response or config.gecko.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPoolsMultiResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.gecko.async_client as client:
            response = await client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES[:1], include_volume_breakdown = True)
        assert isinstance(response, GetPoolsMultiResponse)
        for pool in response.data:
            assert pool.attributes.net_buy_volume_usd is not None

    def test_get_pools_multi_request(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Multiple Pools Data" — request sent to the API.

        Checks that the addresses are joined with commas in the path and the optional query parameters.

        Mock Response File: getPoolsMulti_default.json
        """
        mock_response = self.mocker.load_mock_response("getPoolsMulti_default", GetPoolsMultiResponse)
        api = mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        self.gecko.client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES)
        args, kwargs = api.call_args
        assert args[0] == "GET"
        assert args[1] == self.gecko.url_api + f"networks/{TEST_POOLS_NETWORK}/pools/multi/{','.join(TEST_POOLS_ADDRESSES)}"
        assert kwargs["params"] == {}

        self.gecko.client.get_pools_multi(TEST_POOLS_NETWORK, TEST_POOLS_ADDRESSES, include = TEST_POOLS_INCLUDE, include_volume_breakdown = True)
        _, kwargs = api.call_args
        assert kwargs["params"] == {"include": "base_token,quote_token,dex", "include_volume_breakdown": True}

    @pytest.mark.parametrize("count", [0, 31])
    def test_get_pools_multi_address_count_sync(self, mocker: MockerFixture, count: int) -> None:
        """
        Unit Test used to check that "Multiple Pools Data" rejects an empty list or more than 30
        addresses before any request is sent — synchronous logic.
        """
        api = mocker.patch("cyhole.core.client.APIClient.api")
        with pytest.raises(GeckoAddressCountError):
            self.gecko.client.get_pools_multi(TEST_POOLS_NETWORK, [TEST_POOLS_ADDRESSES[0]] * count)
        api.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("count", [0, 31])
    async def test_get_pools_multi_address_count_async(self, mocker: MockerFixture, count: int) -> None:
        """
        Unit Test used to check that "Multiple Pools Data" rejects an empty list or more than 30
        addresses before any request is sent — asynchronous logic.
        """
        api = mocker.patch("cyhole.core.client.AsyncAPIClient.api")
        with pytest.raises(GeckoAddressCountError):
            async with self.gecko.async_client as client:
                await client.get_pools_multi(TEST_POOLS_NETWORK, [TEST_POOLS_ADDRESSES[0]] * count)
        api.assert_not_called()
