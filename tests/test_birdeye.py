import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cyhole.birdeye import Birdeye
from cyhole.birdeye.param import BirdeyeAddressType, BirdeyeTimeFrame, BirdeyeChain, BirdeyeAllTimeTradesTimeFrame
from cyhole.birdeye.schema import (
    GetTokenListResponse,
    GetV3TokenListQuery,
    GetV3TokenListResponse,
    GetV3TokenListScrollQuery,
    GetV3TokenListScrollResponse,
    GetV2TokensNewListingResponse,
    GetV2MarketsResponse,
    GetV3TokenMetaDataResponse,
    GetV3TokenMetaDataMultipleResponse,
    GetV3TokenMarketDataResponse,
    GetV3TokenMarketDataMultipleResponse,
    GetV3TokenTradeDataResponse,
    GetV3TokenTradeDataMultipleResponse,
    GetV3TokenExitLiquidityResponse,
    GetV3TokenExitLiquidityMultipleResponse,
    GetV3TokenMintBurnTxsResponse,
    GetV2TopTradersResponse,
    GetTokenHolderResponse,
    PostTokenHolderBatchResponse,
    GetHolderDistributionResponse,
    GetHolderProfileResponse,
    GetTokenHolderPositionsResponse,
    GetTokenHolderChartResponse,
    PostTokenTransferBody,
    PostTokenTransferResponse,
    PostTokenTransferTotalBody,
    PostTokenTransferTotalResponse,
    GetTokenTrendingResponse,
    GetTokenCreationInfoResponse,
    GetTokenSecurityResponse, GetTokenSecurityDataSolana,
    GetTokenOverviewResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceVolumeSingleResponse,
    PostPriceVolumeMultiResponse,
    GetPriceHistoricalResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse,
    GetV3SearchQuery,
    GetV3SearchResponse,
    GetUtilsV1CreditsResponse,
    GetV3AllTimeTradesResponse,
    GetV3TokenMemeDetailSingleResponse,
)
from cyhole.birdeye.exception import BirdeyeAuthorisationError, BirdeyeTimeRangeError
from cyhole.core.exception import MissingAPIKeyError
from cyhole.core.token.solana import WSOL, USDC, BONK
from cyhole.core.token.ethereum import WETH

# load test config
from .config import load_config, MockerManager
config = load_config()

# constant address
TOM_SOL = "842NwDnKYcfMRWAYqsD3hoTWXKKMi28gVABtmaupFcnS"
JRK = "JRKXwVpdyQbF3A4pvQvKYj22syubbEwfwUiobDzSPtJ"

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestBirdeyePublic:
    """
        Class grouping all unit test associate to **PUBLIC** endpoints.
    """
    birdeye = Birdeye(api_key = config.birdeye.api_key)
    mocker = MockerManager(mock_path)

    def test_missing_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key.
        """
        with pytest.raises(MissingAPIKeyError):
            monkeypatch.delenv("BIRDEYE_API_KEY", raising = False)
            Birdeye()

    def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List" 
            for synchronous logic.

            Mock Response File: get_token_list.json
        """
    
        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.birdeye.client.get_token_list(limit = 1)

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List" 
            for asynchronous logic.

            Mock Response File: get_token_list.json
        """
        time.sleep(1)

        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_token_list(limit = 1)

        # actual test
        assert isinstance(response, GetTokenListResponse)

    def test_get_v3_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List (V3)"
            for synchronous logic.

            Mock Response File: get_v3_token_list.json
        """
        mock_file_name = "get_v3_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenListResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.birdeye.client.get_v3_token_list(GetV3TokenListQuery(limit = 1))

        # actual test
        assert isinstance(response, GetV3TokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List (V3)"
            for asynchronous logic.

            Mock Response File: get_v3_token_list.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenListResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_list(GetV3TokenListQuery(limit = 1))

        assert isinstance(response, GetV3TokenListResponse)

    def test_get_v3_token_list_scroll_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List (V3) Scroll"
            for synchronous logic.

            Mock Response File: get_v3_token_list_scroll.json
        """
        mock_file_name = "get_v3_token_list_scroll"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenListScrollResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_list_scroll(GetV3TokenListScrollQuery(limit = 1))

        assert isinstance(response, GetV3TokenListScrollResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_list_scroll_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List (V3) Scroll"
            for asynchronous logic.

            Mock Response File: get_v3_token_list_scroll.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_list_scroll"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenListScrollResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_list_scroll(GetV3TokenListScrollQuery(limit = 1))

        assert isinstance(response, GetV3TokenListScrollResponse)

    def test_get_v2_tokens_new_listing_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - New Listing"
            for synchronous logic.

            Mock Response File: get_v2_tokens_new_listing.json
        """
        mock_file_name = "get_v2_tokens_new_listing"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2TokensNewListingResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v2_tokens_new_listing(limit = 1)
        assert isinstance(response, GetV2TokensNewListingResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v2_tokens_new_listing_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - New Listing"
            for asynchronous logic.

            Mock Response File: get_v2_tokens_new_listing.json
        """
        time.sleep(1)

        mock_file_name = "get_v2_tokens_new_listing"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2TokensNewListingResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v2_tokens_new_listing(limit = 1)

        assert isinstance(response, GetV2TokensNewListingResponse)

    def test_get_v2_markets_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - All Market List"
            for synchronous logic.

            Mock Response File: get_v2_markets.json
        """
        mock_file_name = "get_v2_markets"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2MarketsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v2_markets(address = WSOL.address, limit = 1)
        assert isinstance(response, GetV2MarketsResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v2_markets_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - All Market List"
            for asynchronous logic.

            Mock Response File: get_v2_markets.json
        """
        time.sleep(1)

        mock_file_name = "get_v2_markets"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2MarketsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v2_markets(address = WSOL.address, limit = 1)

        assert isinstance(response, GetV2MarketsResponse)

    def test_get_v3_token_meta_data_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Metadata" with a single token address (synchronous logic).

            Mock Response File: get_v3_token_meta_data_single.json
        """
        mock_file_name = "get_v3_token_meta_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMetaDataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_meta_data(WSOL.address)
        assert isinstance(response, GetV3TokenMetaDataResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_meta_data_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Metadata" with a single token address (asynchronous logic).

            Mock Response File: get_v3_token_meta_data_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_meta_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMetaDataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_meta_data(WSOL.address)

        assert isinstance(response, GetV3TokenMetaDataResponse)

    def test_get_v3_token_meta_data_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Metadata" with a list of token addresses (synchronous logic).

            Mock Response File: get_v3_token_meta_data_multiple.json
        """
        mock_file_name = "get_v3_token_meta_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMetaDataMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_meta_data([WSOL.address, USDC.address])
        assert isinstance(response, GetV3TokenMetaDataMultipleResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_meta_data_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Metadata" with a list of token addresses (asynchronous logic).

            Mock Response File: get_v3_token_meta_data_multiple.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_meta_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMetaDataMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_meta_data([WSOL.address, USDC.address])

        assert isinstance(response, GetV3TokenMetaDataMultipleResponse)

    def test_get_v3_token_market_data_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Market Data" with a single token address (synchronous logic).

            Mock Response File: get_v3_token_market_data_single.json
        """
        mock_file_name = "get_v3_token_market_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMarketDataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_market_data(WSOL.address)
        assert isinstance(response, GetV3TokenMarketDataResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_market_data_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Market Data" with a single token address (asynchronous logic).

            Mock Response File: get_v3_token_market_data_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_market_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMarketDataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_market_data(WSOL.address)

        assert isinstance(response, GetV3TokenMarketDataResponse)

    def test_get_v3_token_market_data_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Market Data" with a list of token addresses (synchronous logic).

            Mock Response File: get_v3_token_market_data_multiple.json
        """
        mock_file_name = "get_v3_token_market_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMarketDataMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_market_data([WSOL.address, USDC.address])
        assert isinstance(response, GetV3TokenMarketDataMultipleResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_market_data_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Market Data" with a list of token addresses (asynchronous logic).

            Mock Response File: get_v3_token_market_data_multiple.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_market_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMarketDataMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_market_data([WSOL.address, USDC.address])

        assert isinstance(response, GetV3TokenMarketDataMultipleResponse)

    def test_get_v3_token_trade_data_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Trade Data" with a single token address (synchronous logic).

            Mock Response File: get_v3_token_trade_data_single.json
        """
        mock_file_name = "get_v3_token_trade_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenTradeDataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_trade_data(WSOL.address)
        assert isinstance(response, GetV3TokenTradeDataResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_trade_data_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Trade Data" with a single token address (asynchronous logic).

            Mock Response File: get_v3_token_trade_data_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_trade_data_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenTradeDataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_trade_data(WSOL.address)

        assert isinstance(response, GetV3TokenTradeDataResponse)

    def test_get_v3_token_trade_data_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Trade Data" with a list of token addresses (synchronous logic).

            Mock Response File: get_v3_token_trade_data_multiple.json
        """
        mock_file_name = "get_v3_token_trade_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenTradeDataMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_trade_data([WSOL.address, USDC.address])
        assert isinstance(response, GetV3TokenTradeDataMultipleResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_trade_data_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Trade Data" with a list of token addresses (asynchronous logic).

            Mock Response File: get_v3_token_trade_data_multiple.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_trade_data_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenTradeDataMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_trade_data([WSOL.address, USDC.address])

        assert isinstance(response, GetV3TokenTradeDataMultipleResponse)

    def test_get_v3_token_exit_liquidity_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Liquidity" with a single token address (synchronous logic).

            Mock Response File: get_v3_token_exit_liquidity_single.json
        """
        mock_file_name = "get_v3_token_exit_liquidity_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenExitLiquidityResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # Birdeye exit-liquidity is Base-chain only; use an EVM address placeholder.
        response = self.birdeye.client.get_v3_token_exit_liquidity("0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42")
        assert isinstance(response, GetV3TokenExitLiquidityResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_exit_liquidity_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Liquidity" with a single token address (asynchronous logic).

            Mock Response File: get_v3_token_exit_liquidity_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_exit_liquidity_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenExitLiquidityResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_exit_liquidity("0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42")

        assert isinstance(response, GetV3TokenExitLiquidityResponse)

    def test_get_v3_token_exit_liquidity_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Liquidity" with a list of token addresses (synchronous logic).

            Mock Response File: get_v3_token_exit_liquidity_multiple.json
        """
        mock_file_name = "get_v3_token_exit_liquidity_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenExitLiquidityMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_exit_liquidity([
            "0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42",
            "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        ])
        assert isinstance(response, GetV3TokenExitLiquidityMultipleResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_exit_liquidity_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "Token - Liquidity" with a list of token addresses (asynchronous logic).

            Mock Response File: get_v3_token_exit_liquidity_multiple.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_exit_liquidity_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenExitLiquidityMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_exit_liquidity([
                "0x60a3E35Cc302bFA44Cb288Bc5a4F316Fdb1adb42",
                "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            ])

        assert isinstance(response, GetV3TokenExitLiquidityMultipleResponse)

    def test_get_v3_all_time_trades_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "All-Time Trades" with a single token address (synchronous logic).

            Mock Response File: get_v3_all_time_trades_single.json
        """
        mock_file_name = "get_v3_all_time_trades_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3AllTimeTradesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_all_time_trades(WSOL.address, BirdeyeAllTimeTradesTimeFrame.ALL_TIME.value)
        assert isinstance(response, GetV3AllTimeTradesResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_all_time_trades_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "All-Time Trades" with a single token address (asynchronous logic).

            Mock Response File: get_v3_all_time_trades_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_all_time_trades_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3AllTimeTradesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_all_time_trades(WSOL.address, BirdeyeAllTimeTradesTimeFrame.ALL_TIME.value)

        assert isinstance(response, GetV3AllTimeTradesResponse)

    def test_get_v3_all_time_trades_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "All-Time Trades" with a list of token addresses (synchronous logic).

            Mock Response File: get_v3_all_time_trades_multiple.json
        """
        mock_file_name = "get_v3_all_time_trades_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3AllTimeTradesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_all_time_trades(
            [WSOL.address, USDC.address],
            BirdeyeAllTimeTradesTimeFrame.ALL_TIME.value
        )
        assert isinstance(response, GetV3AllTimeTradesResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_all_time_trades_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated endpoint
            "All-Time Trades" with a list of token addresses (asynchronous logic).

            Mock Response File: get_v3_all_time_trades_multiple.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_all_time_trades_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3AllTimeTradesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_all_time_trades(
                [WSOL.address, USDC.address],
                BirdeyeAllTimeTradesTimeFrame.ALL_TIME.value
            )

        assert isinstance(response, GetV3AllTimeTradesResponse)

    def test_get_v3_token_meme_detail_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Meme Token Detail - Single"
            for synchronous logic.

            Mock Response File: get_v3_token_meme_detail_single.json
        """
        mock_file_name = "get_v3_token_meme_detail_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMemeDetailSingleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_meme_detail_single("6R3LxpHiE8RjTL7HnvKWtoQCHVA76CR1ebF9MYk61wzS")
        assert isinstance(response, GetV3TokenMemeDetailSingleResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_meme_detail_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Meme Token Detail - Single"
            for asynchronous logic.

            Mock Response File: get_v3_token_meme_detail_single.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_meme_detail_single"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMemeDetailSingleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_meme_detail_single("6R3LxpHiE8RjTL7HnvKWtoQCHVA76CR1ebF9MYk61wzS")

        assert isinstance(response, GetV3TokenMemeDetailSingleResponse)

    def test_get_v3_token_mint_burn_txs_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Mint/Burn"
            for synchronous logic.

            Mock Response File: get_v3_token_mint_burn_txs.json
        """
        mock_file_name = "get_v3_token_mint_burn_txs"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMintBurnTxsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_token_mint_burn_txs("fueL3hBZjLLLJHiFH9cqZoozTG3XQZ53diwFPwbzNim", limit = 1)
        assert isinstance(response, GetV3TokenMintBurnTxsResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_token_mint_burn_txs_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Mint/Burn"
            for asynchronous logic.

            Mock Response File: get_v3_token_mint_burn_txs.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_mint_burn_txs"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3TokenMintBurnTxsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_token_mint_burn_txs("fueL3hBZjLLLJHiFH9cqZoozTG3XQZ53diwFPwbzNim", limit = 1)

        assert isinstance(response, GetV3TokenMintBurnTxsResponse)

    def test_get_v2_tokens_top_traders_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Top Traders"
            for synchronous logic.

            Mock Response File: get_v2_tokens_top_traders.json
        """
        mock_file_name = "get_v2_tokens_top_traders"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2TopTradersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v2_tokens_top_traders(WSOL.address, limit = 1)
        assert isinstance(response, GetV2TopTradersResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v2_tokens_top_traders_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Top Traders"
            for asynchronous logic.

            Mock Response File: get_v2_tokens_top_traders.json
        """
        time.sleep(1)

        mock_file_name = "get_v2_tokens_top_traders"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV2TopTradersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v2_tokens_top_traders(WSOL.address, limit = 1)

        assert isinstance(response, GetV2TopTradersResponse)

    def test_get_token_holder_top_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated Token Holder endpoint
            in its **top-holder ranking** flavour (synchronous logic).

            Mock Response File: get_v3_token_holder.json
        """
        mock_file_name = "get_v3_token_holder"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_holder(WSOL.address, limit = 1)
        assert isinstance(response, GetTokenHolderResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holder_top_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated Token Holder endpoint
            in its **top-holder ranking** flavour (asynchronous logic).

            Mock Response File: get_v3_token_holder.json
        """
        time.sleep(1)

        mock_file_name = "get_v3_token_holder"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_holder(WSOL.address, limit = 1)

        assert isinstance(response, GetTokenHolderResponse)

    def test_get_token_holder_batch_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated Token Holder endpoint
            in its **batch balance lookup** flavour (synchronous logic).

            Mock Response File: post_token_v1_holder_batch.json
        """
        mock_file_name = "post_token_v1_holder_batch"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenHolderBatchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_holder(
            WSOL.address,
            wallets = ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"],
        )
        assert isinstance(response, PostTokenHolderBatchResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holder_batch_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of the consolidated Token Holder endpoint
            in its **batch balance lookup** flavour (asynchronous logic).

            Mock Response File: post_token_v1_holder_batch.json
        """
        time.sleep(1)

        mock_file_name = "post_token_v1_holder_batch"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenHolderBatchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_holder(
                WSOL.address,
                wallets = ["5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"],
            )

        assert isinstance(response, PostTokenHolderBatchResponse)

    def test_get_holder_distribution_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Distribution"
            for synchronous logic.

            Mock Response File: get_holder_v1_distribution.json
        """
        mock_file_name = "get_holder_v1_distribution"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHolderDistributionResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_holder_distribution(WSOL.address, limit = 1)
        assert isinstance(response, GetHolderDistributionResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_holder_distribution_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Distribution"
            for asynchronous logic.

            Mock Response File: get_holder_v1_distribution.json
        """
        time.sleep(1)

        mock_file_name = "get_holder_v1_distribution"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHolderDistributionResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_holder_distribution(WSOL.address, limit = 1)

        assert isinstance(response, GetHolderDistributionResponse)

    def test_get_token_holder_profile_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Profile"
            for synchronous logic.

            Mock Response File: get_token_v1_holder_profile.json
        """
        mock_file_name = "get_token_v1_holder_profile"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHolderProfileResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_holder_profile(WSOL.address)
        assert isinstance(response, GetHolderProfileResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holder_profile_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Profile"
            for asynchronous logic.

            Mock Response File: get_token_v1_holder_profile.json
        """
        time.sleep(1)

        mock_file_name = "get_token_v1_holder_profile"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHolderProfileResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_holder_profile(WSOL.address)

        assert isinstance(response, GetHolderProfileResponse)

    def test_get_token_holder_positions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Positions"
            for synchronous logic.

            Mock Response File: get_token_v1_holder_positions.json
        """
        mock_file_name = "get_token_v1_holder_positions"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderPositionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_holder_positions(WSOL.address, limit = 1)
        assert isinstance(response, GetTokenHolderPositionsResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holder_positions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Positions"
            for asynchronous logic.

            Mock Response File: get_token_v1_holder_positions.json
        """
        time.sleep(1)

        mock_file_name = "get_token_v1_holder_positions"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderPositionsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_holder_positions(WSOL.address, limit = 1)

        assert isinstance(response, GetTokenHolderPositionsResponse)

    def test_get_token_holder_chart_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Chart"
            for synchronous logic.

            Mock Response File: get_token_v1_holder_chart.json
        """
        mock_file_name = "get_token_v1_holder_chart"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderChartResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_holder_chart(WSOL.address, count = 1)
        assert isinstance(response, GetTokenHolderChartResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_holder_chart_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Holder Chart"
            for asynchronous logic.

            Mock Response File: get_token_v1_holder_chart.json
        """
        time.sleep(1)

        mock_file_name = "get_token_v1_holder_chart"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenHolderChartResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_holder_chart(WSOL.address, count = 1)

        assert isinstance(response, GetTokenHolderChartResponse)

    def test_post_token_transfer_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Transfer List"
            for synchronous logic.

            Mock Response File: post_token_v1_transfer.json
        """
        mock_file_name = "post_token_v1_transfer"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenTransferResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostTokenTransferBody(token_address = WSOL.address, limit = 1)
        response = self.birdeye.client.post_token_transfer(body)
        assert isinstance(response, PostTokenTransferResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_token_transfer_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Transfer List"
            for asynchronous logic.

            Mock Response File: post_token_v1_transfer.json
        """
        time.sleep(1)

        mock_file_name = "post_token_v1_transfer"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenTransferResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostTokenTransferBody(token_address = WSOL.address, limit = 1)
        async with self.birdeye.async_client as client:
            response = await client.post_token_transfer(body)

        assert isinstance(response, PostTokenTransferResponse)

    def test_post_token_transfer_total_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Transfer Total"
            for synchronous logic.

            Mock Response File: post_token_v1_transfer_total.json
        """
        mock_file_name = "post_token_v1_transfer_total"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenTransferTotalResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostTokenTransferTotalBody(token_address = WSOL.address)
        response = self.birdeye.client.post_token_transfer_total(body)
        assert isinstance(response, PostTokenTransferTotalResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_token_transfer_total_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Transfer Total"
            for asynchronous logic.

            Mock Response File: post_token_v1_transfer_total.json
        """
        time.sleep(1)

        mock_file_name = "post_token_v1_transfer_total"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenTransferTotalResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostTokenTransferTotalBody(token_address = WSOL.address)
        async with self.birdeye.async_client as client:
            response = await client.post_token_transfer_total(body)

        assert isinstance(response, PostTokenTransferTotalResponse)

    def test_get_token_trending_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Trending List"
            for synchronous logic.

            Mock Response File: get_token_trending.json
        """
        mock_file_name = "get_token_trending"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTrendingResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_token_trending(limit = 1)
        assert isinstance(response, GetTokenTrendingResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_trending_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Trending List"
            for asynchronous logic.

            Mock Response File: get_token_trending.json
        """
        time.sleep(1)

        mock_file_name = "get_token_trending"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTrendingResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_token_trending(limit = 1)

        assert isinstance(response, GetTokenTrendingResponse)

    def test_get_price_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic.

            Mock Response File: get_price.json
        """
        time.sleep(1)

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_price(address = WSOL.address)

        # actual test
        assert isinstance(response, GetPriceResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic.

            Mock Response File: get_price.json
        """
        time.sleep(1)

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_price(address = WSOL.address)

        # actual test
        assert isinstance(response, GetPriceResponse)

    def test_get_price_historical_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Historical" 
            for synchronous logic.

            Mock Response File: get_price_historical.json
        """
        time.sleep(1)

        # load mock response
        mock_file_name = "get_price_historical"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_price_historical(
            address = WSOL.address,
            address_type = BirdeyeAddressType.TOKEN.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1)
        )

        # actual test
        assert isinstance(response, GetPriceHistoricalResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_historical_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Historical" 
            for asynchronous logic.

            Mock Response File: get_price_historical.json
        """
        time.sleep(1)

        # load mock response
        mock_file_name = "get_price_historical"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_price_historical(
                address = WSOL.address,
                address_type = BirdeyeAddressType.TOKEN.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() - timedelta(hours = 1)
            )

        # actual test
        assert isinstance(response, GetPriceHistoricalResponse)

    def test_get_price_historical_incorrect_input_dates_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for synchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            self.birdeye.client.get_price_historical(
                address = WSOL.address,
                address_type = BirdeyeAddressType.TOKEN.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() + timedelta(hours = 1)
            )

    @pytest.mark.asyncio
    async def test_get_price_historical_incorrect_input_dates_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for asynchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            async with self.birdeye.async_client as client:
                await client.get_price_historical(
                    address = WSOL.address,
                    address_type = BirdeyeAddressType.TOKEN.value,
                    timeframe = BirdeyeTimeFrame.MIN15.value,
                    dt_from = datetime.now() + timedelta(hours = 1)
                )

class TestBirdeyePrivate:
    """
        Class grouping all unit test associate to PRIVATE endpoints
    """
    birdeye = Birdeye(api_key = config.birdeye.api_key)
    mocker = MockerManager(mock_path)

    def test_not_authorised_api_sync(self) -> None:
        """
            Unit Test to correcty identify a not Authorised API Key 
            for synchronous logic.
        """
        birdeye = Birdeye(api_key = "xxx-xxx-xxx")
        with pytest.raises(BirdeyeAuthorisationError):
            birdeye.client.get_token_creation_info(address = WSOL.address)

    @pytest.mark.asyncio
    async def test_not_authorised_api_async(self) -> None:
        """
            Unit Test to correcty identify a not Authorised API Key 
            for asynchronous logic.
        """
        birdeye = Birdeye(api_key = "xxx-xxx-xxx")
        with pytest.raises(BirdeyeAuthorisationError):
            async with birdeye.async_client as client:
                await client.get_token_creation_info(address = WSOL.address)

    def test_get_price_multiple_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Multiple" 
            for synchronous logic.

            Mock Response File: get_price_multiple.json
        """

        # load mock response
        mock_file_name = "get_price_multiple"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceMultipleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        tokens_ca = [WSOL.address, USDC.address]
        response = self.birdeye.client.get_price_multiple(list_address = tokens_ca)

        # actual test
        assert isinstance(response, GetPriceMultipleResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_multiple_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Multiple" 
            for asynchronous logic.

            Mock Response File: get_price_multiple.json
        """

        # load mock response
        mock_file_name = "get_price_multiple"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceMultipleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        tokens_ca = [WSOL.address, USDC.address]
        async with self.birdeye.async_client as client:
            response = await client.get_price_multiple(list_address = tokens_ca)

        # actual test
        assert isinstance(response, GetPriceMultipleResponse)

    def test_get_price_volume_single_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price Volume - Single Token" 
            for synchronous logic.

            Mock Response File: get_price_volume_single.json
        """

        # load mock response
        mock_file_name = "get_price_volume_single"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceVolumeSingleResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_price_volume_single(address = WSOL.address)

        # actual test
        assert isinstance(response, GetPriceVolumeSingleResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_volume_single_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price Volume - Single Token" 
            for asynchronous logic.

            Mock Response File: get_price_volume_single.json
        """

        # load mock response
        mock_file_name = "get_price_volume_single"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceVolumeSingleResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_price_volume_single(address = WSOL.address)

        # actual test
        assert isinstance(response, GetPriceVolumeSingleResponse)

    def test_post_price_volume_multi_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price Volume - Multi Token" 
            for synchronous logic.

            Mock Response File: post_price_volume_multi.json
        """

        # load mock response
        mock_file_name = "post_price_volume_multi"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostPriceVolumeMultiResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.post_price_volume_multi(list_address = [WSOL.address, BONK.address])

        # actual test
        assert isinstance(response, PostPriceVolumeMultiResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_price_volume_multi_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price Volume - Multi Token" 
            for asynchronous logic.

            Mock Response File: post_price_volume_multi.json
        """

        # load mock response
        mock_file_name = "post_price_volume_multi"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostPriceVolumeMultiResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.post_price_volume_multi(list_address = [WSOL.address, BONK.address])

        # actual test
        assert isinstance(response, PostPriceVolumeMultiResponse)

    def test_get_token_creation_info_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Creation Token Info" 
            for synchronous logic.

            Mock Response File: get_token_creation_info.json
        """

        # load mock response
        mock_file_name = "get_token_creation_info"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCreationInfoResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_token_creation_info(address = WSOL.address)

        # actual test
        assert isinstance(response, GetTokenCreationInfoResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_creation_info_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Creation Token Info" 
            for asynchronous logic.

            Mock Response File: get_token_creation_info.json
        """

        # load mock response
        mock_file_name = "get_token_creation_info"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCreationInfoResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_token_creation_info(address = WSOL.address)

        # actual test
        assert isinstance(response, GetTokenCreationInfoResponse)

    def test_get_token_security_solana_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" 
            specifically for Solana chain for synchronous logic.

            Mock Response File: get_token_security_solana.json
        """

        # load mock response
        mock_file_name = "get_token_security_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_token_security(JRK)

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, GetTokenSecurityDataSolana)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_security_solana_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" 
            specifically for Solana chain for asynchronous logic.

            Mock Response File: get_token_security_solana.json
        """

        # load mock response
        mock_file_name = "get_token_security_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_token_security(JRK)

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, GetTokenSecurityDataSolana)

    def test_get_token_security_other_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" 
            specifically for other chains for synchronous logic.

            Mock Response File: get_token_security_other.json
        """
        birdeye = Birdeye(api_key = config.birdeye.api_key, chain = BirdeyeChain.ETHEREUM.value)

        # load mock response
        mock_file_name = "get_token_security_other"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = birdeye.client.get_token_security(address = JRK)

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, dict)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_security_other_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" 
            specifically for other chains for asynchronous logic.

            Mock Response File: get_token_security_other.json
        """
        birdeye = Birdeye(api_key = config.birdeye.api_key, chain = BirdeyeChain.ETHEREUM.value)

        # load mock response
        mock_file_name = "get_token_security_other"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with birdeye.async_client as client:
            response = await client.get_token_security(address = JRK)

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, dict)

    def test_get_token_overview_solana_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" 
            specifically for Solana chain for synchronous logic.

            Mock Response File: get_token_overview_solana.json
        """
        token_address = WSOL.address

        # load mock response
        mock_file_name = "get_token_overview_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_token_overview(token_address)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_overview_solana_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" 
            specifically for Solana chain for asynchronous logic.

            Mock Response File: get_token_overview_solana.json
        """
        token_address = WSOL.address

        # load mock response
        mock_file_name = "get_token_overview_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_token_overview(token_address)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

    def test_get_token_overview_ethereum_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" 
            specifically for Ethereum chain for synchronous logic.

            Mock Response File: get_token_overview_ethereum.json
        """
        birdeye = Birdeye(api_key = config.birdeye.api_key, chain = BirdeyeChain.ETHEREUM.value)
        token_address = WETH.address

        # load mock response
        mock_file_name = "get_token_overview_ethereum"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = birdeye.client.get_token_overview(token_address)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_overview_ethereum_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" 
            specifically for Ethereum chain for asynchronous logic.

            Mock Response File: get_token_overview_ethereum.json
        """
        birdeye = Birdeye(api_key = config.birdeye.api_key, chain = BirdeyeChain.ETHEREUM.value)
        token_address = WETH.address

        # load mock response
        mock_file_name = "get_token_overview_ethereum"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with birdeye.async_client as client:
            response = await client.get_token_overview(token_address)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

    def test_get_trades_token_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Token" 
            for synchronous logic.

            Mock Response File: get_trades_token.json
        """

        # load mock response
        mock_file_name = "get_trades_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesTokenResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_trades_token(WSOL.address)

        # actual test
        assert isinstance(response, GetTradesTokenResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_trades_token_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Token" 
            for asynchronous logic.

            Mock Response File: get_trades_token.json
        """

        # load mock response
        mock_file_name = "get_trades_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesTokenResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_trades_token(WSOL.address)

        # actual test
        assert isinstance(response, GetTradesTokenResponse)

    def test_get_trades_pair_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Pair" 
            for synchronous logic.

            Mock Response File: get_trades_pair.json
        """
        # load mock response
        mock_file_name = "get_trades_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesPairResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_trades_pair(address = TOM_SOL)

        # actual test
        assert isinstance(response, GetTradesPairResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_trades_pair_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Pair" 
            for asynchronous logic.

            Mock Response File: get_trades_pair.json
        """
        # load mock response
        mock_file_name = "get_trades_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesPairResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_trades_pair(address = TOM_SOL)

        # actual test
        assert isinstance(response, GetTradesPairResponse)

    def test_get_ohlcv_incorrect_input_dates_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for synchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            self.birdeye.client.get_ohlcv(
                address = WSOL.address,
                address_type = BirdeyeAddressType.TOKEN.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() + timedelta(hours = 1)
            )

    @pytest.mark.asyncio
    async def test_get_ohlcv_incorrect_input_dates_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for asynchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            async with self.birdeye.async_client as client:
                await client.get_ohlcv(
                    address = WSOL.address,
                    address_type = BirdeyeAddressType.TOKEN.value,
                    timeframe = BirdeyeTimeFrame.MIN15.value,
                    dt_from = datetime.now() + timedelta(hours = 1)
                )

    def test_get_ohlcv_token_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Token" 
            for synchronous logic.

            Mock Response File: get_ohlcv_token.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_ohlcv(
            address = WSOL.address,
            address_type = BirdeyeAddressType.TOKEN.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ohlcv_token_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Token" 
            for asynchronous logic.

            Mock Response File: get_ohlcv_token.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_ohlcv(
                address = WSOL.address,
                address_type = BirdeyeAddressType.TOKEN.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() - timedelta(hours = 1),
                dt_to = datetime.now()
            )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

    def test_get_ohlcv_pair_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Pair" 
            for synchronous logic.

            Mock Response File: get_ohlcv_pair.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_ohlcv(
            address = WSOL.address,
            address_type = BirdeyeAddressType.PAIR.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ohlcv_pair_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Pair" 
            for asynchronous logic.

            Mock Response File: get_ohlcv_pair.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_ohlcv(
                address = WSOL.address,
                address_type = BirdeyeAddressType.PAIR.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() - timedelta(hours = 1),
                dt_to = datetime.now()
            )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

    def test_get_ohlcv_base_quote_incorrect_input_dates_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for synchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            self.birdeye.client.get_ohlcv_base_quote(
                base_address = WSOL.address,
                quote_address = USDC.address,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() + timedelta(hours = 1)
            )

    @pytest.mark.asyncio
    async def test_get_ohlcv_base_quote_incorrect_input_dates_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to) 
            for asynchronous logic.
        """

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            async with self.birdeye.async_client as client:
                await client.get_ohlcv_base_quote(
                    base_address = WSOL.address,
                    quote_address = USDC.address,
                    timeframe = BirdeyeTimeFrame.MIN15.value,
                    dt_from = datetime.now() + timedelta(hours = 1)
                )

    def test_get_ohlcv_base_quote_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Base/Quote" 
            for synchronous logic.

            Mock Response File: get_ohlcv_base_quote.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_base_quote"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVBaseQuoteResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_ohlcv_base_quote(
            base_address = WSOL.address,
            quote_address = USDC.address,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVBaseQuoteResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ohlcv_base_quote_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Base/Quote" 
            for asynchronous logic.

            Mock Response File: get_ohlcv_base_quote.json
        """

        # load mock response
        mock_file_name = "get_ohlcv_base_quote"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVBaseQuoteResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_ohlcv_base_quote(
                base_address = WSOL.address,
                quote_address = USDC.address,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() - timedelta(hours = 1),
                dt_to = datetime.now()
            )

        # actual test
        assert isinstance(response, GetOHLCVBaseQuoteResponse)

    def test_get_wallet_supported_networks_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Wallet - Supported Networks" 
            for synchronous logic.

            Mock Response File: get_wallet_supported_networks.json
        """

        # load mock response
        mock_file_name = "get_wallet_supported_networks"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetWalletSupportedNetworksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_wallet_supported_networks()

        # actual test
        assert isinstance(response, GetWalletSupportedNetworksResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_wallet_supported_networks_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Wallet - Supported Networks" 
            for asynchronous logic.

            Mock Response File: get_wallet_supported_networks.json
        """

        # load mock response
        mock_file_name = "get_wallet_supported_networks"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetWalletSupportedNetworksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_wallet_supported_networks()

        # actual test
        assert isinstance(response, GetWalletSupportedNetworksResponse)

    def test_get_v3_search_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Search"
            for synchronous logic.

            Mock Response File: get_v3_search.json
        """
        mock_file_name = "get_v3_search"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3SearchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_v3_search(GetV3SearchQuery(keyword = "SOL", limit = 1))

        assert isinstance(response, GetV3SearchResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_v3_search_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Search"
            for asynchronous logic.

            Mock Response File: get_v3_search.json
        """
        mock_file_name = "get_v3_search"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetV3SearchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_v3_search(GetV3SearchQuery(keyword = "SOL", limit = 1))

        assert isinstance(response, GetV3SearchResponse)

    def test_get_utils_v1_credits_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Utils - Credits"
            for synchronous logic.

            Mock Response File: get_utils_v1_credits.json
        """
        mock_file_name = "get_utils_v1_credits"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUtilsV1CreditsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        response = self.birdeye.client.get_utils_v1_credits()

        assert isinstance(response, GetUtilsV1CreditsResponse)

        if config.mock_file_overwrite and not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_utils_v1_credits_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Utils - Credits"
            for asynchronous logic.

            Mock Response File: get_utils_v1_credits.json
        """
        mock_file_name = "get_utils_v1_credits"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUtilsV1CreditsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        async with self.birdeye.async_client as client:
            response = await client.get_utils_v1_credits()

        assert isinstance(response, GetUtilsV1CreditsResponse)