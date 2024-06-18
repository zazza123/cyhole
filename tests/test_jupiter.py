import pytest
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.jupiter import Jupiter
from cyhole.jupiter.schema import (
    GetPriceResponse,
    GetQuoteInput,
    GetQuoteResponse
)
from cyhole.jupiter.param import JupiterSwapDex, JupiterSwapMode
from cyhole.jupiter.exception import JupiterNoRouteFoundError
from cyhole.core.address.solana import SOL, JUP
from cyhole.core.address.ethereum import WETH
from cyhole.core.exception import ParamUnknownError

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.jupiter.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

# set client, mocker
_client = Jupiter()
_mocker = MockerManager(mock_path)

class TestJupiter:
    """
        Class grouping all unit tests.
    """
    client = _client
    mocker = _mocker

    def test_get_price_token_address(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".  
            Only one token address.

            Mock Response File: get_price_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = self.client.get_price([JUP])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert JUP in response.data

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_token_symbol(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".  
            Only one token symbol.

            Mock Response File: get_price_token_symbol.json
        """

        token_symbol = "JUP"
        # load mock response
        mock_file_name = "get_price_token_symbol"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = self.client.get_price([token_symbol])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert token_symbol in response.data

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_multiple_token_address(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".  
            More then one token addresses.

            Mock Response File: get_price_multiple_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_multiple_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = self.client.get_price([JUP, SOL])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert (JUP in response.data) and (SOL in response.data)

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_vs_address(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".  
            Provide a different comparison token.

            Mock Response File: get_price_vs_address.json
        """

        # load mock response
        mock_file_name = "get_price_vs_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = self.client.get_price([SOL], vs_address = JUP)

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert SOL in response.data
        assert response.data[SOL].vs_token == JUP

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_unknown_address(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price".  
            Provide an unknown token address.

            Mock Response File: get_price_unknown_address.json
        """

        # load mock response
        mock_file_name = "get_price_unknown_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
            
        # execute request
        response = self.client.get_price([WETH])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data == {}

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_quote(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote".

            Mock Response File: get_quote_base.json
        """

        # load mock response
        mock_file_name = "get_quote_base"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount
        )
        response = self.client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)
        assert response.input_amount == amount
        assert response.input_token == SOL
        assert response.output_token == JUP

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_quote_force_route(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            forcing a route and mode.

            Mock Response File: get_quote_force_rooute.json
        """

        # load mock response
        mock_file_name = "get_quote_force_rooute"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount,
            dexes = [JupiterSwapDex.METEORA_DLMM.value],
            swap_mode = JupiterSwapMode.EXACT_IN.value
        )
        response = self.client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)

        # store request (only not mock)
        if not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_quote_error_route_not_found(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when no route is found.
        """

        # define input
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = 1
        )

        # actual test
        with pytest.raises(JupiterNoRouteFoundError):
            self.client.get_quote(input)


    def test_get_quote_error_unknown_dex(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when a not supported DEX is used.
        """

        # actual test
        with pytest.raises(ParamUnknownError):
            GetQuoteInput(
                input_token = SOL,
                output_token = JUP,
                amount = 1000,
                dexes = ["XXX"]
            )

    def test_get_quote_error_unknown_mode(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when a not supported MODE is used.
        """

        # actual test
        with pytest.raises(ParamUnknownError):
            GetQuoteInput(
                input_token = SOL,
                output_token = JUP,
                amount = 1000,
                swap_mode = "XXX"
            )