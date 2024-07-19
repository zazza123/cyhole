import os
from typing import Coroutine, Literal, overload
from datetime import datetime

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..core.exception import MissingAPIKeyError
from ..birdeye.client import BirdeyeClient, BirdeyeAsyncClient
from ..birdeye.exception import BirdeyeTimeRangeError
from ..birdeye.param import (
    BirdeyeChain,
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTimeFrame,
    BirdeyeTradeType,
    BirdeyeAddressType
)
from ..birdeye.schema import (
    GetTokenListResponse,
    GetTokenSecurityResponse,
    GetTokenCreationInfoResponse,
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

class Birdeye(Interaction):
    """
        Class used to connect [https://birdeye.so](https://birdeye.so) API.
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check [https://docs.birdeye.so](https://docs.birdeye.so) for all the details on the available endpoints.

        !!! info
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from ENV variable **BIRDEYE_API_KEY**.

        Parameters:
            api_key: specify the API key to use for the connection.
            chain: identifier of the chain to use in all the requests.
                The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                Import them from the library to use the correct identifier.

        **Example**
        ```python
        import asyncio
        from cyhole.birdeye import Birdeye

        birdeye = Birdeye()

        # Get current token list on Solana
        # synchronous
        response = birdeye.client.get_token_list()
        print(f"Currently listed {len(response.data.tokens)} tokens on Solana")

        # asynchronous
        async def main() -> None:
            async with birdeye.async_client as client:
                response = await client.get_token_list()
                print(f"Currently listed {len(response.data.tokens)} tokens on Solana")

        asyncio.run(main())
        ```

        Raises:
            MissingAPIKeyError: if no API Key was available during the object creation.
    """
    def __init__(self, api_key: str | None = None, chain: str = BirdeyeChain.SOLANA.value) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("BIRDEYE_API_KEY")
        if self.api_key is None:
            raise MissingAPIKeyError("no API key is provided during object's creation.")

        # input check

        # headers setup
        headers = {
            "X-API-KEY": self.api_key,
            "x-chain": chain
        }
        super().__init__(headers)
        self.headers: dict[str, str]

        # clients
        self.client = BirdeyeClient(self, headers = headers)
        self.async_client = BirdeyeAsyncClient(self, headers = headers)

        # API urls
        self.url_api_public = "https://public-api.birdeye.so/defi/"
        self.url_api_private = "https://public-api.birdeye.so/defi/"
        self.url_api_private_wallet = "https://public-api.birdeye.so/v1/wallet"
        return

    @overload
    def _get_token_list(
        self,
        sync: Literal[True],
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenListResponse: ...

    @overload
    def _get_token_list(
        self,
        sync: Literal[False],
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> Coroutine[None, None, GetTokenListResponse]: ...

    def _get_token_list(
        self,
        sync: bool,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenListResponse | Coroutine[None, None, GetTokenListResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Token - List](https://docs.birdeye.so/reference/get_defi-tokenlist)** and is used 
            to get the list of Birdeye tokens according on a specific chain.

            Parameters:
                sort_by: define the type of sorting to apply in the
                    extraction; e.g. USD volume in the last 24h.
                    The sorting types are available on [`BirdeyeSort`][cyhole.birdeye.param.BirdeyeSort].
                    Import them from the library to use the correct identifier.
                order_by: define the type of ordering to apply in the 
                    extraction; e.g. ascending or descending.
                    The sorting types are available on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
                    Import them from the library to use the correct identifier.
                offset: offset to apply in the extraction.
                limit: limit the number of returned records in the extraction.

            Returns:
                list of tokens returned by birdeye.so

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeSort.check(sort_by)
        BirdeyeOrder.check(order_by)

        # set params
        url = self.url_api_public + "tokenlist"
        params = {
            "sort_by" : sort_by,
            "sort_type" : order_by,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenListResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenListResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_creation_info(
        self,
        sync: Literal[True],
        address: str
    ) -> GetTokenCreationInfoResponse: ...

    @overload
    def _get_token_creation_info(
        self,
        sync: Literal[False],
        address: str
    ) -> Coroutine[None, None, GetTokenCreationInfoResponse]: ...

    def _get_token_creation_info(
        self,
        sync: bool,
        address: str
    ) -> GetTokenCreationInfoResponse | Coroutine[None, None, GetTokenCreationInfoResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get_defi-token-creation-info)** and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
            
            Returns:
                token's creation information.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "token_creation_info"
        params = {
            "address" : address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenCreationInfoResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenCreationInfoResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_security(
        self,
        sync: Literal[True],
        address: str
    ) -> GetTokenSecurityResponse: ...

    @overload
    def _get_token_security(
        self,
        sync: Literal[False],
        address: str
    ) -> Coroutine[None, None, GetTokenSecurityResponse]: ...

    def _get_token_security(
        self,
        sync: bool,
        address: str
    ) -> GetTokenSecurityResponse | Coroutine[None, None, GetTokenSecurityResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get_defi-token-security)** and is used 
            to get the useful information related to the security of a token  on a specific
            chain calculated by Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
            
            Returns:
                token's security information.
                    Observe that the content of `data` value depends on the selected chain.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "token_security"
        params = {
            "address" : address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenSecurityResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenSecurityResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_token_overview(
        self,
        sync: Literal[True],
        address: str
    ) -> GetTokenOverviewResponse: ...

    @overload
    def _get_token_overview(
        self,
        sync: Literal[False],
        address: str
    ) -> Coroutine[None, None, GetTokenOverviewResponse]: ...

    def _get_token_overview(
        self,
        sync: bool,
        address: str
    ) -> GetTokenOverviewResponse | Coroutine[None, None, GetTokenOverviewResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get_defi-token-overview)** and is used 
            to get all kind of information (token/mint/creator adresses, high level statistics, ...)
            of a token on a specific chain calculated by Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
            
            Returns:
                token's information.
                    Observe that the content of `data` value depends on the selected chain.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "token_overview"
        params = {
            "address" : address
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTokenOverviewResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTokenOverviewResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price(
        self,
        sync: Literal[True],
        address: str,
        include_liquidity: bool | None = None
    ) -> GetPriceResponse: ...

    @overload
    def _get_price(
        self,
        sync: Literal[False],
        address: str,
        include_liquidity: bool | None = None
    ) -> Coroutine[None, None, GetPriceResponse]: ...

    def _get_price(
        self,
        sync: bool,
        address: str,
        include_liquidity: bool | None = None
    ) -> GetPriceResponse | Coroutine[None, None, GetPriceResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Price](https://docs.birdeye.so/reference/get_defi-price)** and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)

            Returns:
                token's price returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """        # set params
        url = self.url_api_public + "price"
        params = {
            "address" : address,
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price_multiple(
        self,
        sync: Literal[True],
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> GetPriceMultipleResponse: ...

    @overload
    def _get_price_multiple(
        self,
        sync: Literal[False],
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> Coroutine[None, None, GetPriceMultipleResponse]: ...

    def _get_price_multiple(
        self,
        sync: bool,
        list_address: list[str],
        include_liquidity: bool | None = None
    ) -> GetPriceMultipleResponse | Coroutine[None, None, GetPriceMultipleResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Price - Multiple](https://docs.birdeye.so/reference/get_defi-multi-price)** and is used 
            to get the current price of multeple tokens on a specific chain on Birdeye.

            Parameters:
                list_address: CA of the tokens to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)

            Returns:
                list of tokens returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        url = self.url_api_public + "multi_price"
        params = {
            "list_address" : ",".join(list_address),
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceMultipleResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceMultipleResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_price_historical(
        self,
        sync: Literal[True],
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> GetPriceHistoricalResponse: ...

    @overload
    def _get_price_historical(
        self,
        sync: Literal[False],
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> Coroutine[None, None, GetPriceHistoricalResponse]: ...

    def _get_price_historical(
        self,
        sync: bool,
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None
    ) -> GetPriceHistoricalResponse | Coroutine[None, None, GetPriceHistoricalResponse]:
        """
            This function refers to the **PUBLIC** API endpoint **[Price - Historical](https://docs.birdeye.so/reference/get_defi-history-price)** and is used 
            to get the history of prices of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                address_type: the type of address involved in the extraction.
                    The supported chains are available on [`BirdeyeAddressType`][cyhole.birdeye.param.BirdeyeAddressType].
                    Import them from the library to use the correct identifier.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeAddressType.check(address_type)
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "history_price"
        params = {
            "address" : address,
            "address_type" : address_type,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetPriceHistoricalResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetPriceHistoricalResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_trades_token(
            self,
            sync: Literal[True],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse: ...

    @overload
    def _get_trades_token(
            self,
            sync: Literal[False],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> Coroutine[None, None, GetTradesTokenResponse]: ...

    def _get_trades_token(
            self,
            sync: bool,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse | Coroutine[None, None, GetTradesTokenResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Trades - Token](https://docs.birdeye.so/reference/get_defi-txs-token)** and is used 
            to get the associated trades of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                offset: offset to apply in the extraction.
                limit: limit the number of returned records in the extraction.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/token"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTradesTokenResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTradesTokenResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_trades_pair(
            self,
            sync: Literal[True],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesPairResponse: ...

    @overload
    def _get_trades_pair(
            self,
            sync: Literal[False],
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> Coroutine[None, None, GetTradesPairResponse]: ...

    def _get_trades_pair(
            self,
            sync: bool,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesPairResponse | Coroutine[None, None, GetTradesPairResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Trades - Pair](https://docs.birdeye.so/reference/get_defi-txs-pair)** and is used 
            to get the associated trades of a tokens pair according on a specific chain on Birdeye. 
            Use the 'Trades - Token' endpoint to retrieve the trades associated to a specific token.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                order_by: define the type of ordering to apply in the 
                    extraction; e.g. ascending or descending.
                    The sorting types are available on [`BirdeyeOrder`][cyhole.birdeye.param.BirdeyeOrder].
                    Import them from the library to use the correct identifier.
                offset: offset to apply in the extraction.
                limit: limit the number of returned records in the extraction.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeOrder.check(order_by)
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/pair"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "sort_type": order_by,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetTradesPairResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetTradesPairResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ohlcv(
            self,
            sync: Literal[True],
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVTokenPairResponse: ...

    @overload
    def _get_ohlcv(
            self,
            sync: Literal[False],
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> Coroutine[None, None, GetOHLCVTokenPairResponse]: ...

    def _get_ohlcv(
            self,
            sync: bool,
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVTokenPairResponse | Coroutine[None, None, GetOHLCVTokenPairResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[OHLCV - Token/Pair](https://docs.birdeye.so/reference/get_defi-ohlcv)** and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific token/pair on a chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                address_type: the type of address involved in the extraction (token/pair).
                    The supported chains are available on [`BirdeyeAddressType`][cyhole.birdeye.param.BirdeyeAddressType].
                    Import them from the library to use the correct identifier.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeAddressType.check(address_type)
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "ohlcv"
        if address_type == BirdeyeAddressType.PAIR.value:
            url = url + "/" + BirdeyeAddressType.PAIR.value
        params = {
            "address" : address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetOHLCVTokenPairResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetOHLCVTokenPairResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_ohlcv_base_quote(
            self,
            sync: Literal[True],
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVBaseQuoteResponse: ...

    @overload
    def _get_ohlcv_base_quote(
            self,
            sync: Literal[False],
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> Coroutine[None, None, GetOHLCVBaseQuoteResponse]: ...

    def _get_ohlcv_base_quote(
            self,
            sync: bool,
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVBaseQuoteResponse | Coroutine[None, None, GetOHLCVBaseQuoteResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[OHLCV - Base/Quote](https://docs.birdeye.so/reference/get_defi-ohlcv-base-quote)** and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific base/quote combination 
            on a chain on Birdeye.

            Parameters:
                base_address: CA of the token to search on the chain.
                quote_address: CA of the token to search on the chain.
                timeframe: the type of timeframe involved in the extraction.
                    The timeframe is used to define intervall between a measure and the next one.
                    The supported chains are available on [`BirdeyeTimeFrame`][cyhole.birdeye.param.BirdeyeTimeFrame].
                    Import them from the library to use the correct identifier.
                dt_from: beginning time to take take price data.
                dt_to: end time to take take price data.
                    It should be `dt_from` < `dt_to`.
                    If not ptovided (None), the current time is used.
            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeTimeFrame.check(timeframe)

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError("Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

        # set params
        url = self.url_api_public + "ohlcv/base_quote"
        params = {
            "base_address" : base_address,
            "quote_address" : quote_address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url, params = params)
            return GetOHLCVBaseQuoteResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url, params = params)
                return GetOHLCVBaseQuoteResponse(**content_raw.json())
            return async_request()

    @overload
    def _get_wallet_supported_networks(self, sync: Literal[True]) -> GetWalletSupportedNetworksResponse: ...

    @overload
    def _get_wallet_supported_networks(self, sync: Literal[False]) -> Coroutine[None, None, GetWalletSupportedNetworksResponse]: ...

    def _get_wallet_supported_networks(self, sync: bool) -> GetWalletSupportedNetworksResponse | Coroutine[None, None, GetWalletSupportedNetworksResponse]:
        """
            This function refers to the **PRIVATE** API endpoint **[Wallet - Supported Networks](https://docs.birdeye.so/reference/get_v1-wallet-list-supported-chain)** and 
            it is used to get the list of supported chains on Birdeye.

            Returns:
                list of chains returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        url = self.url_api_private_wallet + "/list_supported_chain"

        # execute request
        if sync:
            content_raw = self.client.api(RequestType.GET.value, url)
            return GetWalletSupportedNetworksResponse(**content_raw.json())
        else:
            async def async_request():
                content_raw = await self.async_client.api(RequestType.GET.value, url)
                return GetWalletSupportedNetworksResponse(**content_raw.json())
            return async_request()