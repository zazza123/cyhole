from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from cyhole.birdeye import Birdeye
from cyhole.birdeye.param import BirdeyeAddressType, BirdeyeTimeFrame, BirdeyeChain
from cyhole.birdeye.schema import (
    GetTokenListResponse,
    GetTokenCreationInfoResponse,
    GetTokenSecurityResponse, GetTokenSecurityDataSolana,
    GetTokenOverviewResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse
)
from cyhole.birdeye.exception import BirdeyeAuthorisationError, BirdeyeTimeRangeError
from cyhole.core.exception import MissingAPIKeyError
from cyhole.core.address.solana import SOL, USDC
from cyhole.core.address.ethereum import WETH

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

    def test_missing_api_key(self) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key.
        """
        with pytest.raises(MissingAPIKeyError):
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

    def test_get_price_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic.

            Mock Response File: get_price.json
        """

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_price(address = SOL)

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

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_price(address = SOL)

        # actual test
        assert isinstance(response, GetPriceResponse)

    def test_get_price_historical_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Historical" 
            for synchronous logic.

            Mock Response File: get_price_historical.json
        """

        # load mock response
        mock_file_name = "get_price_historical"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.birdeye.client.get_price_historical(
            address = SOL,
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

        # load mock response
        mock_file_name = "get_price_historical"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.birdeye.async_client as client:
            response = await client.get_price_historical(
                address = SOL,
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
                address = SOL,
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
                    address = SOL,
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
            birdeye.client.get_token_creation_info(address = SOL)

    @pytest.mark.asyncio
    async def test_not_authorised_api_async(self) -> None:
        """
            Unit Test to correcty identify a not Authorised API Key 
            for asynchronous logic.
        """
        birdeye = Birdeye(api_key = "xxx-xxx-xxx")
        with pytest.raises(BirdeyeAuthorisationError):
            async with birdeye.async_client as client:
                await client.get_token_creation_info(address = SOL)

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
        tokens_ca = [SOL, USDC]
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
        tokens_ca = [SOL, USDC]
        async with self.birdeye.async_client as client:
            response = await client.get_price_multiple(list_address = tokens_ca)

        # actual test
        assert isinstance(response, GetPriceMultipleResponse)

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
        response = self.birdeye.client.get_token_creation_info(address = SOL)

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
            response = await client.get_token_creation_info(address = SOL)

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
        token_address = SOL

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
        token_address = SOL

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
        token_address = WETH

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
        token_address = WETH

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
        response = self.birdeye.client.get_trades_token(SOL)

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
            response = await client.get_trades_token(SOL)

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
                address = SOL,
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
                    address = SOL,
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
            address = SOL,
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
                address = SOL,
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
            address = SOL,
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
                address = SOL,
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
                base_address = SOL,
                quote_address = USDC,
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
                    base_address = SOL,
                    quote_address = USDC,
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
            base_address = SOL,
            quote_address = USDC,
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
                base_address = SOL,
                quote_address = USDC,
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