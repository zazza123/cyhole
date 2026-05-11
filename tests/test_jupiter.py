import pytest
from pathlib import Path

from pytest_mock import MockerFixture

from cyhole.jupiter import Jupiter
from cyhole.jupiter.schema import (
    GetPriceResponse,
    GetSwapOrderParams,
    GetSwapOrderResponse,
    PostSwapExecuteBody,
    PostSwapExecuteResponse,
    GetSwapBuildParams,
    GetSwapBuildResponse,
    PostSwapSubmitBody,
    PostSwapSubmitResponse,
    GetTokenSearchResponse,
    GetTokenTagResponse,
    GetTokenCategoryResponse,
    GetTokenRecentResponse,
    GetTokenVerifyCheckEligibilityResponse,
    GetTokenVerifyCraftTxnResponse,
    PostTokenVerifyExecuteBody,
    PostTokenVerifyExecuteResponse,
    PostRecurringCreateOrderBody,
    PostRecurringCreateOrderTime, PostRecurringCreateOrderTimeParams,
    PostRecurringCreateOrderPrice, PostRecurringCreateOrderPriceParams,
    PostRecurringCreateOrderResponse,
    GetRecurringOrdersResponse,
    PostRecurringCancelOrderResponse
)
from cyhole.jupiter.param import JupiterTokenTagType, JupiterTokenInterval, JupiterTokenCategory, JupiterOrderStatus, JupiterRecurringType
from cyhole.core.token.solana import WSOL, JUP, USDC
from cyhole.core.token.ethereum import WETH

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
            response = await client.get_price([WETH.address])

        # actual test
        assert isinstance(response, GetPriceResponse)
        assert response.data == {}

    def test_get_swap_order_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Order" for synchronous logic.

            Mock Response File: get_swap_order_default.json
        """
        mock_file_name = "get_swap_order_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSwapOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        params = GetSwapOrderParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1_000_000_000
        )
        response = self.jupiter.client.get_swap_order(params)

        assert isinstance(response, GetSwapOrderResponse)

        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_swap_order_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Order" for asynchronous logic.

            Mock Response File: get_swap_order_default.json
        """
        mock_file_name = "get_swap_order_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSwapOrderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        params = GetSwapOrderParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1_000_000_000
        )
        async with self.jupiter.async_client as client:
            response = await client.get_swap_order(params)

        assert isinstance(response, GetSwapOrderResponse)

    def test_post_swap_execute_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Execute" for synchronous logic.

            Mock Response File: post_swap_execute_default.json
        """
        mock_file_name = "post_swap_execute_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapExecuteResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostSwapExecuteBody(
            signed_transaction = "FAKE_SIGNED_TX_BASE64",
            request_id = "req-12345678-abcd-efgh-ijkl-1234567890ab"
        )
        response = self.jupiter.client.post_swap_execute(body)

        assert isinstance(response, PostSwapExecuteResponse)

        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_swap_execute_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Execute" for asynchronous logic.

            Mock Response File: post_swap_execute_default.json
        """
        mock_file_name = "post_swap_execute_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapExecuteResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostSwapExecuteBody(
            signed_transaction = "FAKE_SIGNED_TX_BASE64",
            request_id = "req-12345678-abcd-efgh-ijkl-1234567890ab"
        )
        async with self.jupiter.async_client as client:
            response = await client.post_swap_execute(body)

        assert isinstance(response, PostSwapExecuteResponse)

    def test_get_swap_build_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Build" for synchronous logic.

            Mock Response File: get_swap_build_default.json
        """
        mock_file_name = "get_swap_build_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSwapBuildResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        params = GetSwapBuildParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1_000_000_000
        )
        response = self.jupiter.client.get_swap_build(params)

        assert isinstance(response, GetSwapBuildResponse)

        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_swap_build_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Build" for asynchronous logic.

            Mock Response File: get_swap_build_default.json
        """
        mock_file_name = "get_swap_build_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetSwapBuildResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        params = GetSwapBuildParams(
            input_token = WSOL.address,
            output_token = JUP.address,
            amount = 1_000_000_000
        )
        async with self.jupiter.async_client as client:
            response = await client.get_swap_build(params)

        assert isinstance(response, GetSwapBuildResponse)

    def test_post_swap_submit_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Submit" for synchronous logic.

            Mock Response File: post_swap_submit_default.json
        """
        mock_file_name = "post_swap_submit_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapSubmitResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        body = PostSwapSubmitBody(signed_transaction = "FAKE_SIGNED_TX_BASE64")
        response = self.jupiter.client.post_swap_submit(body)

        assert isinstance(response, PostSwapSubmitResponse)

        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_swap_submit_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Swap - Submit" for asynchronous logic.

            Mock Response File: post_swap_submit_default.json
        """
        mock_file_name = "post_swap_submit_default"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostSwapSubmitResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        body = PostSwapSubmitBody(signed_transaction = "FAKE_SIGNED_TX_BASE64")
        async with self.jupiter.async_client as client:
            response = await client.post_swap_submit(body)

        assert isinstance(response, PostSwapSubmitResponse)

    def test_get_token_search_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Search" 
            for synchronous logic.

            Mock Response File: get_token_search.json
        """

        # load mock response
        mock_file_name = "get_token_search"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSearchResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_search(JUP.address)

        # actual test
        assert isinstance(response, GetTokenSearchResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_search_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Info" 
            for synchronous logic.

            Mock Response File: get_token_search.json
        """

        # load mock response
        mock_file_name = "get_token_search"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenSearchResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_search([JUP.address, WSOL.address])

        # actual test
        assert isinstance(response, GetTokenSearchResponse)

    def test_get_token_tag_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Tag" 
            for synchronous logic.

            Mock Response File: get_token_tag.json
        """

        # load mock response
        mock_file_name = "get_token_tag"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTagResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_tag(JupiterTokenTagType.VERIFIED)

        # actual test
        assert isinstance(response, GetTokenTagResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:2]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_tag_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Tag" 
            for asynchronous logic.

            Mock Response File: get_token_tag.json
        """

        # load mock response
        mock_file_name = "get_token_tag"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenTagResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_tag("lst")

        # actual test
        assert isinstance(response, GetTokenTagResponse)

    def test_get_token_category_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Category" 
            for synchronous logic.

            Mock Response File: get_token_category.json
        """

        # load mock response
        mock_file_name = "get_token_category"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCategoryResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_category(JupiterTokenCategory.TOP_TRENDING, JupiterTokenInterval.FIVE_MINUTES)

        # actual test
        assert isinstance(response, GetTokenCategoryResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:2]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_category_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Category" 
            for asynchronous logic.

            Mock Response File: get_token_category.json
        """

        # load mock response
        mock_file_name = "get_token_category"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenCategoryResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_category("toporganicscore", "5m")

        # actual test
        assert isinstance(response, GetTokenCategoryResponse)

    def test_get_token_recent_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Recent" 
            for synchronous logic.

            Mock Response File: get_token_recent.json
        """

        # load mock response
        mock_file_name = "get_token_recent"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenRecentResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_recent()

        # actual test
        assert isinstance(response, GetTokenRecentResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.tokens = response.tokens[0:2]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_recent_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint "Token Recent" 
            for asynchronous logic.

            Mock Response File: get_token_recent.json
        """

        # load mock response
        mock_file_name = "get_token_recent"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenRecentResponse)

            # response content to be adjusted
            content = self.mocker.adjust_content_json(str(mock_response.json()["tokens"]))
            mock_response._content = content

            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_recent()

        # actual test
        assert isinstance(response, GetTokenRecentResponse)


    def test_post_recurring_create_order_time_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Create Order" time-based for synchronous logic.

            Mock Response File: post_recurring_create_order_time.json
        """

        # load mock response
        mock_file_name = "post_recurring_create_order_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCreateOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostRecurringCreateOrderBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC.address,
            output_token = JUP.address,
            params = PostRecurringCreateOrderTimeParams(
                time = PostRecurringCreateOrderTime(
                    deposit_amount_raw = USDC.from_decimals(110),
                    order_count = 10,
                    interval_unix_time = 60*60
                )
            )
        )
        response = self.jupiter.client.post_recurring_create_order(body)

        # actual test
        assert isinstance(response, PostRecurringCreateOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_recurring_create_order_time_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Create Order" time-based for asynchronous logic.

            Mock Response File: post_recurring_create_order_time.json
        """

        # load mock response
        mock_file_name = "post_recurring_create_order_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCreateOrderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            body = PostRecurringCreateOrderBody(
                user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
                input_token = USDC.address,
                output_token = JUP.address,
                params = PostRecurringCreateOrderTimeParams(
                    time = PostRecurringCreateOrderTime(
                        deposit_amount_raw = USDC.from_decimals(110),
                        order_count = 10,
                        interval_unix_time = 60*60
                    )
                )
            )
            response = await client.post_recurring_create_order(body)

        # actual test
        assert isinstance(response, PostRecurringCreateOrderResponse)

    def test_post_recurring_create_order_price_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Create Order" price-based for synchronous logic.

            Mock Response File: post_recurring_create_order_price.json
        """

        # load mock response
        mock_file_name = "post_recurring_create_order_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCreateOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostRecurringCreateOrderBody(
            user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            input_token = USDC.address,
            output_token = JUP.address,
            params = PostRecurringCreateOrderPriceParams(
                price = PostRecurringCreateOrderPrice(
                    deposit_amount_raw = USDC.from_decimals(110),
                    increment_usdc_value_raw = USDC.from_decimals(10),
                    interval_unix_time = 60*60
                )
            )
        )
        response = self.jupiter.client.post_recurring_create_order(body)

        # actual test
        assert isinstance(response, PostRecurringCreateOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_recurring_create_order_price_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Create Order" price-based for asynchronous logic.

            Mock Response File: post_recurring_create_order_price.json
        """

        # load mock response
        mock_file_name = "post_recurring_create_order_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCreateOrderResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            body = PostRecurringCreateOrderBody(
                user_public_key = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
                input_token = USDC.address,
                output_token = JUP.address,
                params = PostRecurringCreateOrderPriceParams(
                    price = PostRecurringCreateOrderPrice(
                        deposit_amount_raw = USDC.from_decimals(110),
                        increment_usdc_value_raw = USDC.from_decimals(10),
                        interval_unix_time = 60*60
                    )
                )
            )
            response = await client.post_recurring_create_order(body)

        # actual test
        assert isinstance(response, PostRecurringCreateOrderResponse)

    def test_get_recurring_orders_active_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Recurring - Orders" active orders for synchronous logic.

            Mock Response File:
                - get_recurring_orders_active_price.json
                - get_recurring_orders_active_time.json
                - get_recurring_orders_active_all.json
        """

        # Active Price-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "EKqKLCF9Sdn7UoCtcP6UmtjyXqVMacMLd5sCa1WgQ1MV",
            status = JupiterOrderStatus.ACTIVE,
            recurring_type = JupiterRecurringType.PRICE
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.price

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.price = [response.price[0]]
            self.mocker.store_mock_model(mock_file_name, response)

        # Active Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
            status = JupiterOrderStatus.ACTIVE,
            recurring_type = JupiterRecurringType.TIME
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.time

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.time = [response.time[0]]
            self.mocker.store_mock_model(mock_file_name, response)

        # All Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_all"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
            status = JupiterOrderStatus.ACTIVE,
            recurring_type = JupiterRecurringType.ALL
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.all

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.all = [response.all[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_recurring_orders_active_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Recurring - Orders" active orders for asynchronous logic.

            Mock Response File:
                - get_recurring_orders_active_price.json
                - get_recurring_orders_active_time.json
                - get_recurring_orders_active_all.json
        """

        # Active Price-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "EKqKLCF9Sdn7UoCtcP6UmtjyXqVMacMLd5sCa1WgQ1MV",
                status = JupiterOrderStatus.ACTIVE,
                recurring_type = JupiterRecurringType.PRICE
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.price

        # Active Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
                status = JupiterOrderStatus.ACTIVE,
                recurring_type = JupiterRecurringType.TIME
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.time

        # All Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_active_all"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
                status = JupiterOrderStatus.ACTIVE,
                recurring_type = JupiterRecurringType.ALL
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.all

    def test_get_recurring_history_active_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Recurring - Orders" history orders for synchronous logic.

            Mock Response File:
                - get_recurring_orders_history_price.json
                - get_recurring_orders_history_time.json
                - get_recurring_orders_history_all.json
        """

        # Active Price-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "5dMXLJ8GYQxcHe2fjpttVkEpRrxcajRXZqJHCiCbWS4H",
            status = JupiterOrderStatus.HISTORY,
            recurring_type = JupiterRecurringType.PRICE
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.price

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.price = [response.price[0]]
            self.mocker.store_mock_model(mock_file_name, response)

        # Active Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
            status = JupiterOrderStatus.HISTORY,
            recurring_type = JupiterRecurringType.TIME
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.time

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.time = [response.time[0]]
            self.mocker.store_mock_model(mock_file_name, response)

        # All Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_all"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_recurring_orders(
            user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
            status = JupiterOrderStatus.HISTORY,
            recurring_type = JupiterRecurringType.ALL
        )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.all

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            response.all = [response.all[0]]
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_recurring_history_active_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            GET "Recurring - Orders" history orders for asynchronous logic.

            Mock Response File:
                - get_recurring_orders_history_price.json
                - get_recurring_orders_history_time.json
                - get_recurring_orders_history_all.json
        """

        # Active Price-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_price"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "5dMXLJ8GYQxcHe2fjpttVkEpRrxcajRXZqJHCiCbWS4H",
                status = JupiterOrderStatus.HISTORY,
                recurring_type = JupiterRecurringType.PRICE
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.price

        # Active Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_time"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
                status = JupiterOrderStatus.HISTORY,
                recurring_type = JupiterRecurringType.TIME
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.time

        # All Time-based Orders
        # load mock responses
        mock_file_name = "get_recurring_orders_history_all"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetRecurringOrdersResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_recurring_orders(
                user_public_key = "3CEhwPQoxcjZ7Qtj5QQJRwjCpnoxTtJY1cy21MHmTMi2",
                status = JupiterOrderStatus.HISTORY,
                recurring_type = JupiterRecurringType.ALL
            )

        # actual test
        assert isinstance(response, GetRecurringOrdersResponse)
        assert response.all

    def test_post_recurring_cancel_order_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Cancel Order" for synchronous logic.

            Mock Response File: post_recurring_cancel_order.json
        """
        user_public_key = "EKqKLCF9Sdn7UoCtcP6UmtjyXqVMacMLd5sCa1WgQ1MV"
        order_key = ""

        # load mock response
        mock_file_name = "post_recurring_cancel_order"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCancelOrderResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)
        else:
            # find open orders
            open_orders = self.jupiter.client.get_recurring_orders(
                user_public_key = user_public_key,
                status = JupiterOrderStatus.ACTIVE,
                recurring_type = JupiterRecurringType.PRICE
            )
            order = open_orders.price[0] # type: ignore

            # set inputs
            order_key = order.order_key

        # execute request
        response = self.jupiter.client.post_recurring_cancel_order(order_key, user_public_key, JupiterRecurringType.PRICE)

        # actual test
        assert isinstance(response, PostRecurringCancelOrderResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_recurring_cancel_order_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint 
            POST "Recurring - Cancel Order" for asynchronous logic.

            Mock Response File: post_recurring_cancel_order.json
        """
        user_public_key = "EKqKLCF9Sdn7UoCtcP6UmtjyXqVMacMLd5sCa1WgQ1MV"
        order_key = ""

        async with self.jupiter.async_client as client:
            # load mock response
            mock_file_name = "post_recurring_cancel_order"
            if config.mock_response or config.jupiter.mock_response:
                mock_response = self.mocker.load_mock_response(mock_file_name, PostRecurringCancelOrderResponse)
                mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)
            else:
                # find open orders
                open_orders = await client.get_recurring_orders(
                    user_public_key = user_public_key,
                    status = JupiterOrderStatus.ACTIVE,
                    recurring_type = JupiterRecurringType.PRICE
                )
                order = open_orders.price[0] # type: ignore

                # set inputs
                order_key = order.order_key

            # execute request
            response = await client.post_recurring_cancel_order(order_key, user_public_key, JupiterRecurringType.PRICE)

        # actual test
        assert isinstance(response, PostRecurringCancelOrderResponse)

    def test_get_token_verify_check_eligibility_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            "Token Verify - Check Eligibility" for synchronous logic.

            Mock Response File: get_token_verify_check_eligibility.json
        """

        # load mock response
        mock_file_name = "get_token_verify_check_eligibility"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVerifyCheckEligibilityResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_verify_check_eligibility(JUP.address)

        # actual test
        assert isinstance(response, GetTokenVerifyCheckEligibilityResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_verify_check_eligibility_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            "Token Verify - Check Eligibility" for asynchronous logic.

            Mock Response File: get_token_verify_check_eligibility.json
        """

        # load mock response
        mock_file_name = "get_token_verify_check_eligibility"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVerifyCheckEligibilityResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_verify_check_eligibility(JUP.address)

        # actual test
        assert isinstance(response, GetTokenVerifyCheckEligibilityResponse)

    def test_get_token_verify_craft_txn_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            "Token Verify - Craft Transaction" for synchronous logic.

            Mock Response File: get_token_verify_craft_txn.json
        """

        # load mock response
        mock_file_name = "get_token_verify_craft_txn"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVerifyCraftTxnResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        response = self.jupiter.client.get_token_verify_craft_txn("REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3")

        # actual test
        assert isinstance(response, GetTokenVerifyCraftTxnResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_verify_craft_txn_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            "Token Verify - Craft Transaction" for asynchronous logic.

            Mock Response File: get_token_verify_craft_txn.json
        """

        # load mock response
        mock_file_name = "get_token_verify_craft_txn"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVerifyCraftTxnResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        async with self.jupiter.async_client as client:
            response = await client.get_token_verify_craft_txn("REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3")

        # actual test
        assert isinstance(response, GetTokenVerifyCraftTxnResponse)

    def test_post_token_verify_execute_sync(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            POST "Token Verify - Execute" for synchronous logic.

            Mock Response File: post_token_verify_execute.json
        """

        # load mock response
        mock_file_name = "post_token_verify_execute"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenVerifyExecuteResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value = mock_response)

        # execute request
        body = PostTokenVerifyExecuteBody(
            transaction = "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAHCw==",
            request_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            sender_address = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            token_id = JUP.address,
            twitter_handle = "https://x.com/JupiterExchange",
            description = "Test verification submission"
        )
        response = self.jupiter.client.post_token_verify_execute(body)

        # actual test
        assert isinstance(response, PostTokenVerifyExecuteResponse)

        # store request (only not mock)
        if config.mock_file_overwrite and not config.jupiter.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_post_token_verify_execute_async(self, mocker: MockerFixture) -> None:
        """
            Unit Test used to check the response schema of endpoint
            POST "Token Verify - Execute" for asynchronous logic.

            Mock Response File: post_token_verify_execute.json
        """

        # load mock response
        mock_file_name = "post_token_verify_execute"
        if config.mock_response or config.jupiter.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenVerifyExecuteResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value = mock_response)

        # execute request
        body = PostTokenVerifyExecuteBody(
            transaction = "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAQAHCw==",
            request_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            sender_address = "REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3",
            token_id = JUP.address,
            twitter_handle = "https://x.com/JupiterExchange",
            description = "Test verification submission"
        )
        async with self.jupiter.async_client as client:
            response = await client.post_token_verify_execute(body)

        # actual test
        assert isinstance(response, PostTokenVerifyExecuteResponse)