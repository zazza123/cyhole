import os
import requests
from typing import Any
from datetime import datetime

from ..core.api import APICaller
from ..core.param import RequestType
from ..core.exception import MissingAPIKeyError, AuthorizationAPIKeyError
from ..birdeye.exception import BirdeyeTimeRangeError, BirdeyeAuthorisationError
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
    GetHistoryResponse,
    GetTradesTokenResponse,
    GetTradesPairResponse,
    GetOHLCVTokenPairResponse,
    GetOHLCVBaseQuoteResponse,
    GetWalletSupportedNetworksResponse
)

class Birdeye(APICaller):
    """
        Class used to connect [https://birdeye.so](https://birdeye.so) API.
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check [https://docs.birdeye.so](https://docs.birdeye.so) for all the details on the available endpoints.

        !!! info
            If the API key is not provided during the object creation, then it is automatically 
            retrieved from ENV variable **BIRDEYE_API_KEY**.

        Parameters:
            api_key: specify the API key to use for the connection.

        **Example**

        ```python
        from cyhole.birdeye import Birdeye

        # get current token list on Solana
        birdeye = Birdeye()
        token_list = Birdeye().get_token_list()
        ```

        Raises:
            MissingAPIKeyError: if no API Key was available during the object creation.
    """
    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key if api_key is not None else os.environ.get("BIRDEYE_API_KEY")
        if self.api_key is None:
            raise MissingAPIKeyError("no API key is provided during object's creation.")

        # header setup
        header = {
            "X-API-KEY": self.api_key
        }
        super().__init__(header)

        self.url_api_public = "https://public-api.birdeye.so/defi/"
        self.url_api_private = "https://public-api.birdeye.so/defi/"
        self.url_api_private_wallet = "https://public-api.birdeye.so/v1/wallet"
        return

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        # overide function to manage client specific exceptions
        try:
            return super().api(type, url, *args, **kwargs)
        except AuthorizationAPIKeyError:
            raise BirdeyeAuthorisationError

    def get_token_list(
        self,
        chain: str = BirdeyeChain.SOLANA.value,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenListResponse:
        """
            This function refers to the PUBLIC endpoint **Token - List** and is used 
            to get the list of Birdeye tokens according on a specific chain.

            Parameters:
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.
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
        BirdeyeChain.check(chain)
        BirdeyeSort.check(sort_by)
        BirdeyeOrder.check(order_by)

        # set params
        url = self.url_api_public + "tokenlist"
        params = {
            "x-chain" : chain,
            "sort_by" : sort_by,
            "sort_type" : order_by,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTokenListResponse(**content_raw.json())

        return content

    def get_token_creation_info(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenCreationInfoResponse:
        """
            This function refers to the PRIVATE endpoint **Token - Creation Token Info** and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.
            
            Returns:
                token's creation information.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "token_creation_info"
        params = {
            "x-chain" : chain,
            "address" : address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTokenCreationInfoResponse(**content_raw.json())

        return content

    def get_token_security(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenSecurityResponse:
        """
            This function refers to the PRIVATE endpoint **Token - Security** and is used 
            to get the useful information related to the security of a token  on a specific
            chain calculated by Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.
            
            Returns:
                token's security information.
                    Observe that the content of `data` value depends on the selected chain.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "token_security"
        params = {
            "x-chain" : chain,
            "address" : address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTokenSecurityResponse(**content_raw.json())

        return content

    def get_token_overview(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenOverviewResponse:
        """
            This function refers to the PRIVATE endpoint **Token - Overview** and is used 
            to get all kind of information (token/mint/creator adresses, high level statistics, ...)
            of a token on a specific chain calculated by Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.
            
            Returns:
                token's information.
                    Observe that the content of `data` value depends on the selected chain.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "token_overview"
        params = {
            "x-chain" : chain,
            "address" : address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetTokenOverviewResponse(**content_raw.json())

        return content

    def get_price(
        self,
        address: str,
        include_liquidity: bool | None = None,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetPriceResponse:
        """
            This function refers to the PUBLIC endpoint **Price** and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.

            Returns:
                token's price returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "price"
        params = {
            "x-chain" : chain,
            "address" : address,
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetPriceResponse(**content_raw.json())

        return content

    def get_price_multiple(
        self,
        list_address: list[str],
        include_liquidity: bool | None = None,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetPriceMultipleResponse:
        """
            This function refers to the PUBLIC endpoint **Price - Multiple** and is used 
            to get the current price of multeple tokens on a specific chain on Birdeye.

            Parameters:
                list_address: CA of the tokens to search on the chain.
                include_liquidity: include the current liquidity of the token.
                    Default Value: `None` (`False`)
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.

            Returns:
                list of tokens returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "multi_price"
        params = {
            "x-chain" : chain,
            "list_address" : ",".join(list_address),
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetPriceMultipleResponse(**content_raw.json())

        return content

    def get_price_historical(
        self,
        address: str,
        address_type: str,
        timeframe: str,
        dt_from: datetime,
        dt_to: datetime | None = None,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetPriceHistoricalResponse:
        """
            This function refers to the PUBLIC endpoint **Price - Historical** and is used 
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
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)
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
            "x-chain" : chain,
            "address" : address,
            "address_type" : address_type,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetPriceHistoricalResponse(**content_raw.json())

        return content

    def get_history(self, chain: str = BirdeyeChain.SOLANA.value) -> GetHistoryResponse:
        """
            This function refers to the PUBLIC endpoint **History** and is used 
            to get the history of prices of a token according on a specific chain on Birdeye.

            Parameters:
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)

        # set params
        url = self.url_api_public + "history"
        params = {
            "x-chain" : chain
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetHistoryResponse(**content_raw.json())

        return content

    def get_trades_token(
            self,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            chain: str = BirdeyeChain.SOLANA.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse:
        """
            This function refers to the PRIVATE endpoint **Trades - Token** and is used 
            to get the associated trades of a token according on a specific chain on Birdeye.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
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
        BirdeyeChain.check(chain)
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/token"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "x-chain" : chain,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTradesTokenResponse(**content_raw.json())

        return content

    def get_trades_pair(
            self,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            chain: str = BirdeyeChain.SOLANA.value,
            order_by: str = BirdeyeOrder.DESCENDING.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesPairResponse:
        """
            This function refers to the PRIVATE endpoint **Trades - Pair** and is used 
            to get the associated trades of a tokens pair according on a specific chain on Birdeye. 
            Use the 'Trades - Token' endpoint to retrieve the trades associated to a specific token.

            Parameters:
                address: CA of the token to search on the chain.
                trade_type: the type of transactions to extract.
                    The supported chains are available on [`BirdeyeTradeType`][cyhole.birdeye.param.BirdeyeTradeType].
                    Import them from the library to use the correct identifier.
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
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
        BirdeyeChain.check(chain)
        BirdeyeOrder.check(order_by)
        BirdeyeTradeType.check(trade_type)

        # set params
        url = self.url_api_private + "txs/pair"
        params = {
            "address" : address,
            "tx_type" : trade_type,
            "x-chain" : chain,
            "sort_type": order_by,
            "offset" : offset,
            "limit": limit
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTradesPairResponse(**content_raw.json())

        return content

    def get_ohlcv(
            self,
            address: str,
            address_type: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVTokenPairResponse:
        """
            This function refers to the PRIVATE endpoint **OHLCV - Token/Pair** and is used to get the 
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
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.

            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)
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
            "x-chain" : chain,
            "address" : address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetOHLCVTokenPairResponse(**content_raw.json())

        return content

    def get_ohlcv_base_quote(
            self,
            base_address: str,
            quote_address: str,
            timeframe: str,
            dt_from: datetime,
            dt_to: datetime | None = None,
            chain: str = BirdeyeChain.SOLANA.value
    ) -> GetOHLCVBaseQuoteResponse:
        """
            This function refers to the PRIVATE endpoint **OHLCV - Base/Quote** and is used to get the 
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
                chain: identifier of the chain to check.
                    The supported chains are available on [`BirdeyeChain`][cyhole.birdeye.param.BirdeyeChain].
                    Import them from the library to use the correct identifier.
            Returns:
                list of prices returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # check param consistency
        BirdeyeChain.check(chain)
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
            "x-chain" : chain,
            "base_address" : base_address,
            "quote_address" : quote_address,
            "type" : timeframe,
            "time_from" : int(dt_from.timestamp()),
            "time_to" : int(dt_to.timestamp())
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetOHLCVBaseQuoteResponse(**content_raw.json())

        return content

    def get_wallet_supported_networks(self) -> GetWalletSupportedNetworksResponse:
        """
            This function refers to the PRIVATE endpoint **Wallet - Supported Networks** and 
            it is used to get the list of supported chains on Birdeye.

            Returns:
                list of chains returned by birdeye.so.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
        """
        url = self.url_api_private_wallet + "/list_supported_chain"

        # execute request
        content_raw = self.api(RequestType.GET.value, url)

        # parse response
        content = GetWalletSupportedNetworksResponse(**content_raw.json())

        return content