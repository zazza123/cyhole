import pytest
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.jupiter import Jupiter
from cyhole.jupiter.schema import (
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
from cyhole.jupiter.param import JupiterSwapDex, JupiterSwapMode
from cyhole.jupiter.exception import JupiterNoRouteFoundError, JupiterInvalidRequest, JupiterException
from cyhole.core.address.solana import SOL, JUP, USDC, BONK
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        assert response.input_amount == str(amount)
        assert response.input_token == SOL
        assert response.output_token == JUP

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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
        if config.mock_file_overwrite and not config.jupiter.mock_response:
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

    def test_get_quote_tokens(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Tokens".

            Mock Response File: get_quote_tokens.json
        """

        # load mock response
        mock_file_name = "get_quote_tokens"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteTokensResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_quote_tokens()

        # actual test
        assert isinstance(response, GetQuoteTokensResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_quote_program_id_label(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Program ID to Label".

            Mock Response File: get_quote_program_id_label.json
        """

        # load mock response
        mock_file_name = "get_quote_program_id_label"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteProgramIdLabelResponse)

            # response content to be adjusted
            content = str(mock_response.json()["dexes"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_quote_program_id_label()

        # actual test
        assert isinstance(response, GetQuoteProgramIdLabelResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_post_swap(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Swap".

            Mock Response File: post_swap.json
        """

        # load mock response
        mock_file_name = "post_swap"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        body = PostSwapBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        response = self.client.post_swap(body)

        # actual test
        assert isinstance(response, PostSwapResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_post_swap_invalid_request(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap" 
            when an invalid field is provided in the body.
        """
        body = PostSwapBody(
            user_public_key = "XXX",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        with pytest.raises(JupiterInvalidRequest):
            self.client.post_swap(body)
    
    def test_get_token_list(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token List".

            Mock Response File: get_token_list.json
        """

        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_token_list()

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:10]
            self.mocker.store_mock_model(mock_file_name, response)

    def test_post_limit_order_create(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Create".

            Mock Response File: post_limit_order_create.json
        """

        # load mock response
        mock_file_name = "post_limit_order_create"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCreateResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        body = PostLimitOrderCreateBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC,
            input_amount = 100_000,
            output_token = JUP,
            output_amount = 100_000,
            base = "5pVyoAeURQHNMVU7DmfMHvCDNmTEYXWfEwc136GYhTKG"
        )
        response = self.client.post_limit_order_create(body)

        # actual test
        assert isinstance(response, PostLimitOrderCreateResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_post_limit_order_cancel(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Cancel".

            Mock Response File: post_limit_order_cancel.json
        """
        user_public_key = ""
        fee_payer_public_key = ""
        orders = []

        # load mock response
        mock_file_name = "post_limit_order_cancel"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCancelResponse)
            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)
        else:
            # find open orders
            open_orders = self.client.get_limit_order_open(input_token = JUP, output_token = BONK)
            order = open_orders.orders[0]

            # set inputs
            user_public_key = order.account.maker
            fee_payer_public_key = order.account.maker
            orders = [order.public_key]

        # create input
        body = PostLimitOrderCancelBody(
            user_public_key = user_public_key,
            fee_payer_public_key = fee_payer_public_key,
            orders = orders
        )

        # execute request
        response = self.client.post_limit_order_cancel(body)

        # actual test
        assert isinstance(response, PostLimitOrderCancelResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_post_limit_order_cancel_invalid_request(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order Cancel" 
            when an invalid field is provided in the body.
        """
        body = PostLimitOrderCancelBody(
            user_public_key = "",
            fee_payer_public_key = "",
            orders = []
        )
        with pytest.raises(JupiterException):
            self.client.post_limit_order_cancel(body)

    def test_get_limit_order_open(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Open".

            Mock Response File: get_limit_order_open.json
        """

        # load mock response
        mock_file_name = "get_limit_order_open"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderOpenResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_limit_order_open(input_token = JUP, output_token = BONK)

        # actual test
        assert isinstance(response, GetLimitOrderOpenResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = response.orders[0:5]
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_limit_order_history(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - History".

            Mock Response File: get_limit_order_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_limit_order_history(
            wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
            take = 1
        )

        # actual test
        assert isinstance(response, GetLimitOrderHistoryResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = [response.orders[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_limit_order_trade_history(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Trade History".

            Mock Response File: get_limit_order_trade_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_trade_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderTradeHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.api.APICaller.api", return_value = mock_response)

        # execute request
        response = self.client.get_limit_order_trade_history(
            wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
            take = 1
        )

        # actual test
        assert isinstance(response, GetLimitOrderTradeHistoryResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = [response.orders[0]]
            self.mocker.store_mock_model(mock_file_name, response)