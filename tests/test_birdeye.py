from requests import Response
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
    GetHistoryResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse
)
from cyhole.birdeye.exception import BirdeyeAuthorisationError, BirdeyeTimeRangeError
from cyhole.core.exception import MissingAPIKeyError

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestBirdeyePublic:
    """
        Class grouping all unit test associate to PUBLIC endpoints
    """
    mocker = MockerManager(
        mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
    )

    def test_missing_api_key(self) -> None:
        """
            Unit Test to correcty identify a missing/wrong API Key
        """
        with pytest.raises(MissingAPIKeyError):
            Birdeye()

    def test_get_token_list(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - List".

            Mock Response File: get_token_list.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = client.get_token_list(limit = 1)

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".

            Mock Response File: get_price.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_price(address = "So11111111111111111111111111111111111111112")

        # actual test
        assert isinstance(response, GetPriceResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_multiple(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Multiple".

            Mock Response File: get_price_multiple.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price_multiple"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceMultipleResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        tokens_ca = ["So11111111111111111111111111111111111111112", "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"]
        response = client.get_price_multiple(list_address = tokens_ca)

        # actual test
        assert isinstance(response, GetPriceMultipleResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_historical(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price - Historical".

            Mock Response File: get_price_historical.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_price_historical"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceHistoricalResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_price_historical(
            address = "So11111111111111111111111111111111111111112",
            address_type = BirdeyeAddressType.TOKEN.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1)
        )

        # actual test
        assert isinstance(response, GetPriceHistoricalResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_historical_incorrect_input_dates(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the incorrect dates inputs (dt_from > dt_to).
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        with pytest.raises(BirdeyeTimeRangeError):
            # execute request
            client.get_price_historical(
                address = "So11111111111111111111111111111111111111112",
                address_type = BirdeyeAddressType.TOKEN.value,
                timeframe = BirdeyeTimeFrame.MIN15.value,
                dt_from = datetime.now() + timedelta(hours = 1)
            )

    def test_get_history(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "History".

            Mock Response File: get_history.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_history"
        if config.mock_response or config.birdeye.mock_response_public:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetHistoryResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_history()

        # actual test
        assert isinstance(response, GetHistoryResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_public:
            self.mocker.store_mock_model(mock_file_name, response)

class TestBirdeyePrivate:
    """
        Class grouping all unit test associate to PRIVATE endpoints
    """
    mocker = MockerManager(
        mock_path = Path(config.mock_folder) / config.birdeye.mock_folder
    )

    def test_not_authorised_api(self) -> None:
        """
            Unit Test to correcty identify a not Authorised API Key
        """
        client = Birdeye(api_key = "xxx-xxx-xxx")
        with pytest.raises(BirdeyeAuthorisationError):
            client.get_token_creation_info(address = "So11111111111111111111111111111111111111112")

    def test_get_token_creation_info(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Creation Token Info".

            Mock Response File: get_token_creation_info.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_creation_info"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCreationInfoResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_token_creation_info(address = "So11111111111111111111111111111111111111112")

        # actual test
        assert isinstance(response, GetTokenCreationInfoResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_token_security_solana(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" specifically for Solana chain.

            Mock Response File: get_token_security_solana.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_security_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_token_security(
            address = "JRKXwVpdyQbF3A4pvQvKYj22syubbEwfwUiobDzSPtJ"
        )

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, GetTokenSecurityDataSolana)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_token_security_other(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Security" specifically for other chains.

            Mock Response File: get_token_security_other.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_token_security_other"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSecurityResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_token_security(
            address = "JRKXwVpdyQbF3A4pvQvKYj22syubbEwfwUiobDzSPtJ", 
            chain = BirdeyeChain.ETHEREUM.value
        )

        # actual test
        assert isinstance(response, GetTokenSecurityResponse)
        assert isinstance(response.data, dict)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_token_overview_solana(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" specifically for Solana chain.

            Mock Response File: get_token_overview_solana.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)
        token_address = "So11111111111111111111111111111111111111112"

        # load mock response
        mock_file_name = "get_token_overview_solana"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_token_overview(token_address)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_token_overview_ethereum(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token - Overview" specifically for Ethereum chain.

            Mock Response File: get_token_overview_ethereum.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)
        token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

        # load mock response
        mock_file_name = "get_token_overview_ethereum"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenOverviewResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_token_overview(token_address, BirdeyeChain.ETHEREUM.value)

        # actual test
        assert isinstance(response, GetTokenOverviewResponse)
        assert response.data.address == token_address

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_trades_token(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Token".

            Mock Response File: get_trades_token.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_trades_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesTokenResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_trades_token(address = "SMMzJzseLTFb6pxacL8r5mZMEqjTTGWjNPk4q3JQHTu")

        # actual test
        assert isinstance(response, GetTradesTokenResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)
    
    def test_get_trades_pair(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Trades - Pair".

            Mock Response File: get_trades_pair.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_trades_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTradesPairResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_trades_pair(address = "842NwDnKYcfMRWAYqsD3hoTWXKKMi28gVABtmaupFcnS")

        # actual test
        assert isinstance(response, GetTradesPairResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_ohlcv_token(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Token".

            Mock Response File: get_ohlcv_token.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_ohlcv_token"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_ohlcv(
            address = "So11111111111111111111111111111111111111112",
            address_type = BirdeyeAddressType.TOKEN.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_ohlcv_pair(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Pair".

            Mock Response File: get_ohlcv_pair.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_ohlcv_pair"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVTokenPairResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_ohlcv(
            address = "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT",
            address_type = BirdeyeAddressType.PAIR.value,
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVTokenPairResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_ohlcv_base_quote(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "OHLCV - Base/Quote".

            Mock Response File: get_ohlcv_base_quote.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_ohlcv_base_quote"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetOHLCVBaseQuoteResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_ohlcv_base_quote(
            base_address = "So11111111111111111111111111111111111111112",
            quote_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            timeframe = BirdeyeTimeFrame.MIN15.value,
            dt_from = datetime.now() - timedelta(hours = 1),
            dt_to = datetime.now()
        )

        # actual test
        assert isinstance(response, GetOHLCVBaseQuoteResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_wallet_supported_networks(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Wallet - Supported Networks".

            Mock Response File: get_wallet_supported_networks.json
        """
        client = Birdeye(api_key = config.birdeye.api_key)

        # load mock response
        mock_file_name = "get_wallet_supported_networks"
        if config.mock_response or config.birdeye.mock_response_private:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetWalletSupportedNetworksResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = client.get_wallet_supported_networks()

        # actual test
        assert isinstance(response, GetWalletSupportedNetworksResponse)

        # store request (only not mock)
        if not config.birdeye.mock_response_private:
            self.mocker.store_mock_model(mock_file_name, response)