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
from cyhole.jupiter.exception import JupiterNoRouteFoundError, JupiterException
from cyhole.core.address.solana import SOL, JUP, USDC, BONK
from cyhole.core.address.ethereum import WETH
from cyhole.core.exception import ParamUnknownError

# load test config
from .config import load_config, MockerManager
config = load_config()

# create resources folder
mock_path = Path(config.mock_folder) / config.jupiter.mock_folder
mock_path.mkdir(parents = True, exist_ok = True)

class TestJupiter:
    """
        Class grouping all unit tests.
    """
    jupiter = Jupiter()
    mocker = MockerManager(mock_path)

    def test_get_price_token_address_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. Only one token address.

            Mock Response File: get_price_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([JUP])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert JUP in response.data

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_token_address_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. Only one token address.

            Mock Response File: get_price_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([JUP])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert JUP in response.data

    def test_get_price_token_symbol_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. Only one token symbol.

            Mock Response File: get_price_token_symbol.json
        """

        token_symbol = "JUP"
        # load mock response
        mock_file_name = "get_price_token_symbol"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([token_symbol])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert token_symbol in response.data

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_token_symbol_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. Only one token symbol.

            Mock Response File: get_price_token_symbol.json
        """

        token_symbol = "JUP"
        # load mock response
        mock_file_name = "get_price_token_symbol"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([token_symbol])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert token_symbol in response.data

    def test_get_price_multiple_token_address_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. More then one token addresses.

            Mock Response File: get_price_multiple_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_multiple_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([JUP, SOL])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert (JUP in response.data) and (SOL in response.data)

    @pytest.mark.asyncio
    async def test_get_price_multiple_token_address_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. More then one token addresses.

            Mock Response File: get_price_multiple_token_address.json
        """

        # load mock response
        mock_file_name = "get_price_multiple_token_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([JUP, SOL])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert (JUP in response.data) and (SOL in response.data)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_price_vs_address_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. Provide a different comparison token.

            Mock Response File: get_price_vs_address.json
        """

        # load mock response
        mock_file_name = "get_price_vs_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([SOL], vs_address = JUP)

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert SOL in response.data
        assert response.data[SOL].vs_token == JUP

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_vs_address_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. Provide a different comparison token.

            Mock Response File: get_price_vs_address.json
        """

        # load mock response
        mock_file_name = "get_price_vs_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([SOL], vs_address = JUP)

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert SOL in response.data
        assert response.data[SOL].vs_token == JUP

    def test_get_price_unknown_address_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. Provide an unknown token address.

            Mock Response File: get_price_unknown_address.json
        """

        # load mock response
        mock_file_name = "get_price_unknown_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([WETH])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data == {}

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_unknown_address_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. Provide an unknown token address.

            Mock Response File: get_price_unknown_address.json
        """

        # load mock response
        mock_file_name = "get_price_unknown_address"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([WETH])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data == {}

    def test_get_quote_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" for synchronous logic.

            Mock Response File: get_quote_base.json
        """

        # load mock response
        mock_file_name = "get_quote_base"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount
        )
        response = self.jupiter.client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)
        assert response.input_amount == str(amount)
        assert response.input_token == SOL
        assert response.output_token == JUP

    @pytest.mark.asyncio
    async def test_get_quote_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" for asynchronous logic.

            Mock Response File: get_quote_base.json
        """

        # load mock response
        mock_file_name = "get_quote_base"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount
        )
        async with self.jupiter.async_client as client:
            response = await client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)
        assert response.input_amount == str(amount)
        assert response.input_token == SOL
        assert response.output_token == JUP

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    def test_get_quote_force_route_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            forcing a route and mode for synchronous logic.

            Mock Response File: get_quote_force_rooute.json
        """

        # load mock response
        mock_file_name = "get_quote_force_rooute"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount,
            dexes = [JupiterSwapDex.METEORA_DLMM.value],
            swap_mode = JupiterSwapMode.EXACT_IN.value
        )
        response = self.jupiter.client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_quote_force_route_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            forcing a route and mode for asynchronous logic.

            Mock Response File: get_quote_force_rooute.json
        """

        # load mock response
        mock_file_name = "get_quote_force_rooute"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        amount = 1000
        # execute request
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = amount,
            dexes = [JupiterSwapDex.METEORA_DLMM.value],
            swap_mode = JupiterSwapMode.EXACT_IN.value
        )

        async with self.jupiter.async_client as client:
            response = await client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)

    def test_get_quote_error_route_not_found_sync(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when no route is found for synchronous logic.
        """

        # define input
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = 1
        )

        # actual test
        with pytest.raises(JupiterNoRouteFoundError):
            self.jupiter.client.get_quote(input)

    @pytest.mark.asyncio
    async def test_get_quote_error_route_not_found_async(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when no route is found for asynchronous logic.
        """

        # define input
        input = GetQuoteInput(
            input_token = SOL,
            output_token = JUP,
            amount = 1
        )

        # actual test
        with pytest.raises(JupiterNoRouteFoundError):
            async with self.jupiter.async_client as client:
                await client.get_quote(input)

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

    def test_get_quote_tokens_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Tokens" for synchronous logic.

            Mock Response File: get_quote_tokens.json
        """

        # load mock response
        mock_file_name = "get_quote_tokens"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteTokensResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_quote_tokens()

        # actual test
        assert isinstance(response, GetQuoteTokensResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_quote_tokens_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Tokens" for asynchronous logic.

            Mock Response File: get_quote_tokens.json
        """

        # load mock response
        mock_file_name = "get_quote_tokens"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteTokensResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_quote_tokens()

        # actual test
        assert isinstance(response, GetQuoteTokensResponse)

    def test_get_quote_program_id_label_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Program ID to Label" 
            for synchronous logic.

            Mock Response File: get_quote_program_id_label.json
        """

        # load mock response
        mock_file_name = "get_quote_program_id_label"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteProgramIdLabelResponse)

            # response content to be adjusted
            content = str(mock_response.json()["dexes"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_quote_program_id_label()

        # actual test
        assert isinstance(response, GetQuoteProgramIdLabelResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_quote_program_id_label_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote/Program ID to Label" 
            for asynchronous logic.

            Mock Response File: get_quote_program_id_label.json
        """

        # load mock response
        mock_file_name = "get_quote_program_id_label"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetQuoteProgramIdLabelResponse)

            # response content to be adjusted
            content = str(mock_response.json()["dexes"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_quote_program_id_label()

        # actual test
        assert isinstance(response, GetQuoteProgramIdLabelResponse)

    def test_post_swap_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Swap" 
            for synchronous logic.

            Mock Response File: post_swap.json
        """

        # load mock response
        mock_file_name = "post_swap"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostSwapBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        response = self.jupiter.client.post_swap(body)

        # actual test
        assert isinstance(response, PostSwapResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_swap_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Swap" 
            for asynchronous logic.

            Mock Response File: post_swap.json
        """

        # load mock response
        mock_file_name = "post_swap"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        body = PostSwapBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        async with self.jupiter.async_client as client:
            response = await client.post_swap(body)

        # actual test
        assert isinstance(response, PostSwapResponse)

    def test_post_swap_invalid_request_sync(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap" 
            when an invalid field is provided in the body for synchronous logic.
        """
        body = PostSwapBody(
            user_public_key = "XXX",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        with pytest.raises(JupiterException):
            self.jupiter.client.post_swap(body)

    @pytest.mark.asyncio
    async def test_post_swap_invalid_request_async(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap" 
            when an invalid field is provided in the body for asynchronous logic.
        """
        body = PostSwapBody(
            user_public_key = "XXX",
            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        )
        with pytest.raises(JupiterException):
            async with self.jupiter.async_client as client:
                await client.post_swap(body)

    def test_get_token_list_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token List" 
            for synchronous logic.

            Mock Response File: get_token_list.json
        """

        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_list()

        # actual test
        assert isinstance(response, GetTokenListResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:10]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_list_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token List" 
            for asynchronous logic.

            Mock Response File: get_token_list.json
        """

        # load mock response
        mock_file_name = "get_token_list"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenListResponse)

            # response content to be adjusted
            content = str(mock_response.json()["tokens"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_list()

        # actual test
        assert isinstance(response, GetTokenListResponse)

    def test_post_limit_order_create_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Create" 
            for synchronous logic.

            Mock Response File: post_limit_order_create.json
        """

        # load mock response
        mock_file_name = "post_limit_order_create"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCreateResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostLimitOrderCreateBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC,
            input_amount = 100_000,
            output_token = JUP,
            output_amount = 100_000,
            base = "5pVyoAeURQHNMVU7DmfMHvCDNmTEYXWfEwc136GYhTKG"
        )
        response = self.jupiter.client.post_limit_order_create(body)

        # actual test
        assert isinstance(response, PostLimitOrderCreateResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_limit_order_create_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Create" 
            for asynchronous logic.

            Mock Response File: post_limit_order_create.json
        """

        # load mock response
        mock_file_name = "post_limit_order_create"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCreateResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        body = PostLimitOrderCreateBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC,
            input_amount = 100_000,
            output_token = JUP,
            output_amount = 100_000,
            base = "5pVyoAeURQHNMVU7DmfMHvCDNmTEYXWfEwc136GYhTKG"
        )
        async with self.jupiter.async_client as client:
            response = await client.post_limit_order_create(body)

        # actual test
        assert isinstance(response, PostLimitOrderCreateResponse)

    def test_post_limit_order_cancel_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Cancel" 
            for synchronous logic.

            Mock Response File: post_limit_order_cancel.json
        """
        user_public_key = ""
        fee_payer_public_key = ""
        orders = []

        # load mock response
        mock_file_name = "post_limit_order_cancel"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCancelResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
        else:
            # find open orders
            open_orders = self.jupiter.client.get_limit_order_open(input_token = JUP, output_token = BONK)
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
        response = self.jupiter.client.post_limit_order_cancel(body)

        # actual test
        assert isinstance(response, PostLimitOrderCancelResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_limit_order_cancel_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST "Limit Order Cancel" 
            for asynchronous logic.

            Mock Response File: post_limit_order_cancel.json
        """
        user_public_key = ""
        fee_payer_public_key = ""
        orders = []

        async with self.jupiter.async_client as client:
            # load mock response
            mock_file_name = "post_limit_order_cancel"
            if config.mock_response or config.jupiter.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, PostLimitOrderCancelResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            else:
                # find open orders
                open_orders = await client.get_limit_order_open(input_token = JUP, output_token = BONK)
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
            response = await client.post_limit_order_cancel(body)

        # actual test
        assert isinstance(response, PostLimitOrderCancelResponse)

    def test_post_limit_order_cancel_invalid_request_sync(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order Cancel" 
            when an invalid field is provided in the body for synchronous logic.
        """
        body = PostLimitOrderCancelBody(
            user_public_key = "",
            fee_payer_public_key = "",
            orders = []
        )
        with pytest.raises(JupiterException):
            self.jupiter.client.post_limit_order_cancel(body)

    @pytest.mark.asyncio
    async def test_post_limit_order_cancel_invalid_request_async(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order Cancel" 
            when an invalid field is provided in the body for asynchronous logic.
        """
        body = PostLimitOrderCancelBody(
            user_public_key = "",
            fee_payer_public_key = "",
            orders = []
        )
        with pytest.raises(JupiterException):
            async with self.jupiter.async_client as client:
                await client.post_limit_order_cancel(body)

    def test_get_limit_order_open_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Open" 
            for synchronous logic.

            Mock Response File: get_limit_order_open.json
        """

        # load mock response
        mock_file_name = "get_limit_order_open"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderOpenResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_limit_order_open(input_token = JUP, output_token = BONK)

        # actual test
        assert isinstance(response, GetLimitOrderOpenResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = response.orders[0:5]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_limit_order_open_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Open" 
            for asynchronous logic.

            Mock Response File: get_limit_order_open.json
        """

        # load mock response
        mock_file_name = "get_limit_order_open"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderOpenResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_limit_order_open(input_token = JUP, output_token = BONK)

        # actual test
        assert isinstance(response, GetLimitOrderOpenResponse)

    def test_get_limit_order_history_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - History" 
            for synchronous logic.

            Mock Response File: get_limit_order_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_limit_order_history(
            wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
            take = 1
        )

        # actual test
        assert isinstance(response, GetLimitOrderHistoryResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = [response.orders[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_limit_order_history_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - History" 
            for asynchronous logic.

            Mock Response File: get_limit_order_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_limit_order_history(
                wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
                take = 1
            )

        # actual test
        assert isinstance(response, GetLimitOrderHistoryResponse)

    def test_get_limit_order_trade_history_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Trade History" 
            for synchronous logic.

            Mock Response File: get_limit_order_trade_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_trade_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderTradeHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_limit_order_trade_history(
            wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
            take = 1
        )

        # actual test
        assert isinstance(response, GetLimitOrderTradeHistoryResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = [response.orders[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_limit_order_trade_history_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Limit Order - Trade History" 
            for asynchronous logic.

            Mock Response File: get_limit_order_trade_history.json
        """

        # load mock response
        mock_file_name = "get_limit_order_trade_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLimitOrderTradeHistoryResponse)

            # response content to be adjusted
            content = str(mock_response.json()["orders"]).replace("'", '"').encode()
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_limit_order_trade_history(
                wallet = "Hq9YQ2sz6A318tdNbFWMpML6AjWX3wDTLPVx26m719qG",
                take = 1
            )

        # actual test
        assert isinstance(response, GetLimitOrderTradeHistoryResponse)