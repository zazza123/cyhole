import pytest
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.jupiter import Jupiter
from cyhole.jupiter.schema import (
    GetPriceResponse,
    GetQuoteParams,
    GetQuoteResponse,
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    PostSwapInstructionsResponse,
    GetTokenInfoResponse,
    GetTokenMarketMintsResponse,
    GetTokenTaggedResponse,
    GetTokenNewResponse,
    PostTriggerCreateOrderParams,
    GetUltraOrderResponse,
    GetUltraBalancesResponse,
    PostTriggerCreateOrderBody, PostTriggerCreateOrderResponse,
    PostTriggerCancelOrderResponse,
    GetTriggerOrdersResponse,
)
from cyhole.jupiter.param import JupiterSwapDex, JupiterSwapMode, JupiterTokenTagType, JupiterOrderStatus
from cyhole.jupiter.exception import JupiterNoRouteFoundError, JupiterException, JupiterComputeAmountThresholdError
from cyhole.core.token.solana import WSOL, JUP, USDC, BONK
from cyhole.core.token.ethereum import WETH
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
        response = self.jupiter.client.get_price([JUP.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert JUP.address in response.data

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
            response = await client.get_price([JUP.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert JUP.address in response.data

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
        response = self.jupiter.client.get_price([JUP.address, WSOL.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert (JUP.address in response.data) and (WSOL.address in response.data)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

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
            response = await client.get_price([JUP.address, WSOL.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert (JUP.address in response.data) and (WSOL.address in response.data)

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
        response = self.jupiter.client.get_price([WSOL.address, BONK.address], vs_address = JUP.address)

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert WSOL.address in response.data
        assert BONK.address in response.data

        # check vs token
        jup_data = response.data[JUP.address]
        assert jup_data is not None
        assert jup_data.price == "1"

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
            response = await client.get_price([WSOL.address], vs_address = JUP.address)

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert WSOL.address in response.data

        # check vs token
        jup_data = response.data[JUP.address]
        assert jup_data is not None
        assert jup_data.price == "1"

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
        response = self.jupiter.client.get_price([WETH.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data[WETH.address] is None

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
            response = await client.get_price([WETH.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data[WETH.address] is None

    def test_get_price_with_extra_info_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for synchronous logic. Set extra info to True.

            Mock Response File: get_price_with_extra_info.json
        """

        # load mock response
        mock_file_name = "get_price_with_extra_info"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
            
        # execute request
        response = self.jupiter.client.get_price([JUP.address], extra_info = True)

        # actual test
        assert isinstance(response, GetPriceResponse)

        # check extra info
        jup_data = response.data[JUP.address]
        assert jup_data is not None
        assert jup_data.extra_info is not None

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_price_with_extra_info_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Price" 
            for asynchronous logic. Set extra info to True.

            Mock Response File: get_price_with_extra_info.json
        """

        # load mock response
        mock_file_name = "get_price_with_extra_info"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPriceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            
        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_price([JUP.address], extra_info = True)

        # actual test
        assert isinstance(response, GetPriceResponse)

        # check extra info
        jup_data = response.data[JUP.address]
        assert jup_data is not None
        assert jup_data.extra_info is not None

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
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = amount
        )
        response = self.jupiter.client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)
        assert response.input_amount == str(amount)
        assert response.input_token == WSOL.address
        assert response.output_token == JUP.address

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
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = amount
        )
        async with self.jupiter.async_client as client:
            response = await client.get_quote(input)

        # actual test
        assert isinstance(response, GetQuoteResponse)
        assert response.input_amount == str(amount)
        assert response.input_token == WSOL.address
        assert response.output_token == JUP.address

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
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
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
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
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
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1
        )

        # actual test
        with pytest.raises((JupiterNoRouteFoundError, JupiterComputeAmountThresholdError)):
            self.jupiter.client.get_quote(input)

    @pytest.mark.asyncio
    async def test_get_quote_error_route_not_found_async(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when no route is found for asynchronous logic.
        """

        # define input
        input = GetQuoteParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1
        )

        # actual test
        with pytest.raises((JupiterNoRouteFoundError, JupiterComputeAmountThresholdError)):
            async with self.jupiter.async_client as client:
                await client.get_quote(input)

    def test_get_quote_error_unknown_dex(self) -> None:
        """
            Unit Test used to check the response schema of endpoint "Quote" 
            when a not supported DEX is used.
        """

        # actual test
        with pytest.raises(ParamUnknownError):
            GetQuoteParams(
                input_token = WSOL.address,
                output_token = JUP.address,
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
            GetQuoteParams(
                input_token = WSOL.address,
                output_token = JUP.address,
                amount = 1000,
                swap_mode = "XXX"
            )

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
            content = self.mocker.adjust_content_json(str(mock_response.json()["dexes"]))
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
            content = self.mocker.adjust_content_json(str(mock_response.json()["dexes"]))
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

            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        else:
            quote_response = self.jupiter.client.get_quote(
                input = GetQuoteParams(input_token = USDC.address, output_token = JUP.address, amount = USDC.from_decimals(10))
            )

        # execute request
        body = PostSwapBody(user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3", quote_response = quote_response)
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
        async with self.jupiter.async_client as client:

            # load mock response
            mock_file_name = "post_swap"
            if config.mock_response or config.jupiter.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

                quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
            else:
                quote_response = await client.get_quote(
                    input = GetQuoteParams(input_token = USDC.address, output_token = JUP.address, amount = USDC.from_decimals(10))
                )

            # execute request
            body = PostSwapBody(user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3", quote_response = quote_response)
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

    def test_post_swap_instructions_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST 
            "Swap Instructions" for synchronous logic.

            Mock Response File: post_swap_instructions.json
        """

        # load mock response
        mock_file_name = "post_swap_instructions"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapInstructionsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

            quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
        else:
            quote_response = self.jupiter.client.get_quote(
                input = GetQuoteParams(input_token = USDC.address, output_token = JUP.address, amount = USDC.from_decimals(10))
            )

        # execute request
        body = PostSwapBody(user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3", quote_response = quote_response)
        response = self.jupiter.client.post_swap_instructions(body)

        # actual test
        assert isinstance(response, PostSwapInstructionsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_swap_instructions_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint POST 
            "Swap Instructions" for asynchronous logic.

            Mock Response File: post_swap_instructions.json
        """
        async with self.jupiter.async_client as client:

            # load mock response
            mock_file_name = "post_swap_instructions"
            if config.mock_response or config.jupiter.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapInstructionsResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

                quote_response = self.mocker.load_mock_model("get_quote_base", GetQuoteResponse)
            else:
                quote_response = await client.get_quote(
                    input = GetQuoteParams(input_token = USDC.address, output_token = JUP.address, amount = USDC.from_decimals(10))
                )

            # execute request
            body = PostSwapBody(user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3", quote_response = quote_response)
            response = await client.post_swap_instructions(body)

        # actual test
        assert isinstance(response, PostSwapInstructionsResponse)

    def test_get_token_info_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Info" 
            for synchronous logic.

            Mock Response File: get_token_info.json
        """

        # load mock response
        mock_file_name = "get_token_info"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_info(JUP.address)

        # actual test
        assert isinstance(response, GetTokenInfoResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_info_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Info" 
            for synchronous logic.

            Mock Response File: get_token_info.json
        """

        # load mock response
        mock_file_name = "get_token_info"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInfoResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_info(JUP.address)

        # actual test
        assert isinstance(response, GetTokenInfoResponse)

    def test_get_token_market_mints_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Market Mints" 
            for synchronous logic.

            Mock Response File: get_token_market_mints.json
        """

        # load mock response
        mock_file_name = "get_token_market_mints"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMarketMintsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["mints"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        market_address = "BVRbyLjjfSBcoyiYFuxbgKYnWuiFaF9CSXEa5vdSZ9Hh"
        response = self.jupiter.client.get_token_market_mints(market_address)

        # actual test
        assert isinstance(response, GetTokenMarketMintsResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_market_mints_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Market Mints" 
            for asynchronous logic.

            Mock Response File: get_token_market_mints.json
        """

        # load mock response
        mock_file_name = "get_token_market_mints"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMarketMintsResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["mints"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        market_address = "BVRbyLjjfSBcoyiYFuxbgKYnWuiFaF9CSXEa5vdSZ9Hh"
        async with self.jupiter.async_client as client:
            response = await client.get_token_market_mints(market_address)

        # actual test
        assert isinstance(response, GetTokenMarketMintsResponse)

    def test_get_token_tagged_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Tagged Token" 
            for synchronous logic.

            Mock Response File: get_token_tagged.json
        """

        # load mock response
        mock_file_name = "get_token_tagged"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTaggedResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_tagged(JupiterTokenTagType.MOONSHOT)

        # actual test
        assert isinstance(response, GetTokenTaggedResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:2]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_tagged_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Tagged Token" 
            for asynchronous logic.

            Mock Response File: get_token_tagged.json
        """

        # load mock response
        mock_file_name = "get_token_tagged"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTaggedResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_tagged("moonshot")

        # actual test
        assert isinstance(response, GetTokenTaggedResponse)

    def test_get_token_new_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "New Token" 
            for synchronous logic.

            Mock Response File: get_token_new.json
        """

        # load mock response
        mock_file_name = "get_token_new"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenNewResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_new()

        # actual test
        assert isinstance(response, GetTokenNewResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:2]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_new_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "New Token" 
            for asynchronous logic.

            Mock Response File: get_token_new.json
        """

        # load mock response
        mock_file_name = "get_token_new"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenNewResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_new()

        # actual test
        assert isinstance(response, GetTokenNewResponse)

    def test_get_ultra_order_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Ultra Order" 
            for synchronous logic.

            Mock Response File: get_ultra_order.json
        """

        # load mock response
        mock_file_name = "get_ultra_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUltraOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_ultra_order(
            input_token = USDC.address,
            output_token = JUP.address,
            input_amount = USDC.from_decimals(10),
        )

        # actual test
        assert isinstance(response, GetUltraOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ultra_order_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Ultra Order" 
            for asynchronous logic.

            Mock Response File: get_ultra_order.json
        """

        # load mock response
        mock_file_name = "get_ultra_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUltraOrderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_ultra_order(
                input_token = USDC.address,
                output_token = JUP.address,
                input_amount = USDC.from_decimals(10),
            )

        # actual test
        assert isinstance(response, GetUltraOrderResponse)

    def test_get_ultra_balances_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Ultra - Balances" for synchronous logic.

            Mock Response File: get_ultra_balances.json
        """

        # load mock response
        mock_file_name = "get_ultra_balances"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUltraBalancesResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_ultra_balances("G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF")

        # actual test
        assert isinstance(response, GetUltraBalancesResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            # store only three random balances
            response.tokens = dict(list(response.tokens.items())[0:3])
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ultra_balances_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Ultra - Balances" for asynchronous logic.

            Mock Response File: get_ultra_balances.json
        """

        # load mock response
        mock_file_name = "get_ultra_balances"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetUltraBalancesResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_ultra_balances("G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF")

        # actual test
        assert isinstance(response, GetUltraBalancesResponse)

    def test_post_trigger_create_order_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Trigger - Create Order" for synchronous logic.

            Mock Response File: post_trigger_create_order.json
        """

        # load mock response
        mock_file_name = "post_trigger_create_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTriggerCreateOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostTriggerCreateOrderBody(
            maker_wallet_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            payer_wallet_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC.address,
            output_token = JUP.address,
            params = PostTriggerCreateOrderParams(
                input_amount = USDC.from_decimals(10),
                output_amount = JUP.from_decimals(10)
            )
        )
        response = self.jupiter.client.post_trigger_create_order(body)

        # actual test
        assert isinstance(response, PostTriggerCreateOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_trigger_create_order_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Trigger - Create Order" for asynchronous logic.

            Mock Response File: post_trigger_create_order.json
        """

        # load mock response
        mock_file_name = "post_trigger_create_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTriggerCreateOrderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        body = PostTriggerCreateOrderBody(
            maker_wallet_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            payer_wallet_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC.address,
            output_token = JUP.address,
            params = PostTriggerCreateOrderParams(
                input_amount = USDC.from_decimals(10),
                output_amount = JUP.from_decimals(10)
            )
        )
        async with self.jupiter.async_client as client:
            response = await client.post_trigger_create_order(body)

        # actual test
        assert isinstance(response, PostTriggerCreateOrderResponse)

    def test_get_trigger_orders_active_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Trigger - Orders" for synchronous logic.

            Mock Response File: get_trigger_orders_active.json
        """

        # load mock response
        mock_file_name = "get_trigger_orders_active"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTriggerOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_trigger_orders(
            user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF",
            status = JupiterOrderStatus.ACTIVE,
            output_token = WSOL.address
        )

        # actual test
        assert isinstance(response, GetTriggerOrdersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = response.orders[0:5]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_trigger_orders_active_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Trigger - Orders" for asynchronous logic.

            Mock Response File: get_trigger_orders_active.json
        """

        # load mock response
        mock_file_name = "get_trigger_orders_active"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTriggerOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_trigger_orders(
                user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF",
                status = JupiterOrderStatus.ACTIVE,
                output_token = WSOL.address
            )

        # actual test
        assert isinstance(response, GetTriggerOrdersResponse)

    def test_get_trigger_orders_history_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Trigger - Orders" for synchronous logic.

            Mock Response File: get_trigger_orders_history.json
        """

        # load mock response
        mock_file_name = "get_trigger_orders_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTriggerOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_trigger_orders(
            user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF",
            status = JupiterOrderStatus.HISTORY,
            output_token = WSOL.address
        )

        # actual test
        assert isinstance(response, GetTriggerOrdersResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.orders = [response.orders[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_trigger_orders_history_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Trigger - Orders" for asynchronous logic.

            Mock Response File: get_trigger_orders_history.json
        """

        # load mock response
        mock_file_name = "get_trigger_orders_history"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTriggerOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_trigger_orders(
                user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF",
                status = JupiterOrderStatus.ACTIVE,
                output_token = WSOL.address
            )

        # actual test
        assert isinstance(response, GetTriggerOrdersResponse)

    def test_post_trigger_cancel_order_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Trigger - Cancel Order" for synchronous logic.

            Mock Response File: post_trigger_cancel_order.json
        """
        user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF"
        order_key = ""

        # load mock response
        mock_file_name = "post_trigger_cancel_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTriggerCancelOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
        else:
            # find open orders
            open_orders = self.jupiter.client.get_trigger_orders(
                user_public_key = user_public_key,
                status = JupiterOrderStatus.ACTIVE,
                output_token = WSOL.address
            )
            order = open_orders.orders[0]

            # set inputs
            order_key = order.order_key

        # execute request
        response = self.jupiter.client.post_trigger_cancel_order(user_public_key, order_key)

        # actual test
        assert isinstance(response, PostTriggerCancelOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_trigger_cancel_order_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Trigger - Cancel Order" for asynchronous logic.

            Mock Response File: post_trigger_cancel_order.json
        """
        user_public_key = "G96b5mAiKrrDXwsXtnVBh2Gse3HeCwjpAPeJjjAnHANF"
        order_key = ""

        async with self.jupiter.async_client as client:
            # load mock response
            mock_file_name = "post_trigger_cancel_order"
            if config.mock_response or config.jupiter.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, PostTriggerCancelOrderResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            else:
                # find open orders
                open_orders = await client.get_trigger_orders(
                    user_public_key = user_public_key,
                    status = JupiterOrderStatus.ACTIVE,
                    output_token = WSOL.address
                )
                order = open_orders.orders[0]

                # set inputs
                order_key = order.order_key

            # execute request
            response = await client.post_trigger_cancel_order(user_public_key, order_key)

        # actual test
        assert isinstance(response, PostTriggerCancelOrderResponse)