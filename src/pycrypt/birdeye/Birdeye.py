import os
from typing import Callable
from datetime import datetime

from pydantic import BaseModel

from ..core.api import APICaller
from ..core.param import RequestType
from ..core.exception import MissingAPIKeyError, AuthorizationAPIKeyError
from ..birdeye.param import (
    BirdeyeChain,
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTradeType,
    BirdeyeAddressType
)
from ..birdeye.exception import (
    BirdeyeTimeRangeError,
    BirdeyeAuthorisationError,
    BirdeyeAddressTypeUnknownError
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
        Class used to connect https://birdeye.so API. \\  
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check https://docs.birdeye.so for all the details on the available endpoints.

        If the API key is not provided during the object creation, then it is automatically 
        retrieved from ENV variable BIRDEYE_API_KEY.

        Example

        ```python
        from pycrypt.birdeye import Birdeye

        # get current token list on Solana
        birdeye = Birdeye()
        token_list = Birdeye().get_token_list()
        ```
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

    def _api_authorisation(api_call: Callable[..., BaseModel]) -> Callable[..., BaseModel]:
        """
            Decorator function used for internal validation for the API calls. \\
            Intercepting an authentication failure during the call.

            Args:
                - api_call (Callable[..., BaseModel]) [mandatory]: the class function used to call an endpoint. \\
                    By assumption, all the results of a successful call is an object associated to a class inherited from pydantic.BaseModel.
        """
        def api_wrapper(self, *args, **kwargs) -> None:
            try:
                response_schema = api_call(self, *args, **kwargs)
            except AuthorizationAPIKeyError:
                raise BirdeyeAuthorisationError
            return response_schema
        return api_wrapper

    @_api_authorisation
    def get_token_list(
        self,
        chain: str = BirdeyeChain.SOLANA.value,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenListResponse:
        """
            This function refers to the PUBLIC endpoint 'Token - List' and is used 
            to get the list of Birdeye tokens according on a specific chain.

            Args:

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            - sort_by (str) [optional] : define the type of sorting to apply in the 
                extraction; e.g. USD volume in the last 24h. \\
                The sorting types are available on 'pycrypt.birdeye.param.BirdeyeSort'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: sort by last 24h USD volume.

            - order_by (str) [optional] : define the type of ordering to apply in the 
                extraction; e.g. ascending or descending. \\
                The sorting types are available on 'pycrypt.birdeye.param.BirdeyeOrder'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: descending.

            - offset (int) [optional] : offset to apply in the extraction. \\
                Default Value: None

            - limit (int) [optional] : limit the number of returned records in the extraction. \\
                Default Value: None

            Return:

            - (birdeye.schema.GetTokenListResponse) : list of tokens returned by birdeye.so
        """

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
        content = GetTokenListResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_token_creation_info(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenCreationInfoResponse:
        """
            This function refers to the PRIVATE endpoint 'Token - Creation Token Info' and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.
            
            Return:

            - (birdeye.schema.GetTokenCreationInfoResponse) : token's creation information.
        """

        # set params
        url = self.url_api_public + "token_creation_info"
        params = {
            "x-chain" : chain,
            "address" : address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetTokenCreationInfoResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_token_security(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenSecurityResponse:
        """
            This function refers to the PRIVATE endpoint 'Token - Security' and is used 
            to get the useful information related to the security of a token  on a specific
            chain calculated by Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.
            
            Return:

            - (birdeye.schema.GetTokenSecurityResponse) : token's security information. \\
                Observe that the content of 'data' value depends on the selected chain.
        """

        # set params
        url = self.url_api_public + "token_security"
        params = {
            "x-chain" : chain,
            "address" : address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetTokenSecurityResponse(**content_raw.json())

        return content.data

    @_api_authorisation
    def get_token_overview(
        self,
        address: str,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetTokenOverviewResponse:
        """
            This function refers to the PRIVATE endpoint 'Token - Overview' and is used 
            to get all kind of information (token/mint/creator adresses, high level statistics, ...)
            of a token on a specific chain calculated by Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.
            
            Return:

            - (birdeye.schema.GetTokenOverviewResponse) : token's information. \\
                Observe that the content of 'data' value depends on the selected chain.
        """

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

    @_api_authorisation
    def get_price(
        self,
        address: str,
        include_liquidity: bool | None = None,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetPriceResponse:
        """
            This function refers to the PUBLIC endpoint 'Price' and is used 
            to get the current price of a token according on a specific chain on Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - include_liquidity (bool) [mandatory] : include the current liquidity of the token. \\
                Default Value: None (False)

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetPriceResponse) : token's price returned by birdeye.so
        """

        # set params
        url = self.url_api_public + "price"
        params = {
            "x-chain" : chain,
            "address" : address,
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetPriceResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_price_multiple(
        self,
        list_address: list[str],
        include_liquidity: bool | None = None,
        chain: str = BirdeyeChain.SOLANA.value
    ) -> GetPriceMultipleResponse:
        """
            This function refers to the PUBLIC endpoint 'Price - Multiple' and is used 
            to get the current price of multeple tokens on a specific chain on Birdeye.

            Args:

            - list_address (list[str]) [mandatory] : CA of the tokens to search on the chain.

            - include_liquidity (bool) [mandatory] : include the current liquidity of the token. \\
                Default Value: None (False)

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetPriceMultipleResponse) : list of tokens returned by birdeye.so
        """

        # set params
        url = self.url_api_public + "multi_price"
        params = {
            "x-chain" : chain,
            "list_address" : ",".join(list_address),
            "include_liquidity" : str(include_liquidity).lower() if include_liquidity else None
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetPriceMultipleResponse(**content_raw.json())

        return content

    @_api_authorisation
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
            This function refers to the PUBLIC endpoint 'Price - Historical' and is used 
            to get the history of prices of a token according on a specific chain on Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - address_type (str) [mandatory] : the type of address involved in the extraction. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeAddressType'. \\
                Import them from the library to use the correct identifier.

            - timeframe (str) [mandatory] : the type of timeframe involved in the extraction. \\
                The timeframe is used to define intervall between a measure and the next one. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeTimeFrame'. \\
                Import them from the library to use the correct identifier.

            - dt_from (datetime) [optional] : beginning time to take take price data.

            - dt_to (datetime) [optional] : end time to take take price data. \\
                It should be 'dt_from' < 'dt_to'. \\
                If not ptovided (None), the current time is used.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetPriceHistoricalResponse) : list of prices returned by birdeye.so
        """

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError(f"Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

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
        content = GetPriceHistoricalResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_history(self, chain: str = BirdeyeChain.SOLANA.value) -> GetHistoryResponse:
        """
            This function refers to the PUBLIC endpoint 'History' and is used 
            to get the history of prices of a token according on a specific chain on Birdeye.

            Args:

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetHistoryResponse) : list of prices returned by birdeye.so
        """

        # set params
        url = self.url_api_public + "history_price"
        params = {
            "x-chain" : chain
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)
        content = GetHistoryResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_trades_token(
            self,
            address: str,
            trade_type: str = BirdeyeTradeType.SWAP.value,
            chain: str = BirdeyeChain.SOLANA.value,
            offset: int | None = None,
            limit: int | None = None
    ) -> GetTradesTokenResponse:
        """
            This function refers to the PRIVATE endpoint 'Trades - Token' and is used 
            to get the associated trades of a token according on a specific chain on Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - trade_type (str) [optional] : the type of transactions to extract. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeTradeType'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Swap.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            - offset (int) [optional] : offset to apply in the extraction. \\
                Default Value: None

            - limit (int) [optional] : limit the number of returned records in the extraction. \\
                Default Value: None

            Return:

            - (birdeye.schema.GetTradesTokenResponse) : list of prices returned by birdeye.so
        """

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
        content = GetTradesTokenResponse(**content_raw.json())

        return content

    @_api_authorisation
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
            This function refers to the PRIVATE endpoint 'Trades - Pair' and is used 
            to get the associated trades of a tokens pair according on a specific chain on Birdeye. \\
            Use the 'Trades - Token' endpoint to retrieve the trades associated to a specific token.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - trade_type (str) [optional] : the type of transactions to extract. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeTradeType'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Swap.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            - order_by (str) [optional] : define the type of ordering to apply in the 
                extraction; e.g. ascending or descending. \\
                The sorting types are available on 'pycrypt.birdeye.param.BirdeyeOrder'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: descending.

            - offset (int) [optional] : offset to apply in the extraction. \\
                Default Value: None

            - limit (int) [optional] : limit the number of returned records in the extraction. \\
                Default Value: None

            Return:

            - (birdeye.schema.GetTradesPairResponse) : list of prices returned by birdeye.so
        """

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
        content = GetTradesPairResponse(**content_raw.json())

        return content

    @_api_authorisation
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
            This function refers to the PRIVATE endpoint 'OHLCV - Token/Pair' and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific token/pair on a chain on Birdeye.

            Args:

            - address (str) [mandatory] : CA of the token to search on the chain.

            - address_type (str) [mandatory] : the type of address involved in the extraction (token/pair). \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeAddressType'. \\
                Import them from the library to use the correct identifier.

            - timeframe (str) [mandatory] : the type of timeframe involved in the extraction. \\
                The timeframe is used to define intervall between a measure and the next one. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeTimeFrame'. \\
                Import them from the library to use the correct identifier.

            - dt_from (datetime) [optional] : beginning time to take take price data.

            - dt_to (datetime) [optional] : end time to take take price data. \\
                It should be 'dt_from' < 'dt_to'. \\
                If not ptovided (None), the current time is used.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetOHLCVTokenPairResponse) : list of prices returned by birdeye.so
        """
        # check address type
        if address_type not in BirdeyeAddressType:
            raise BirdeyeAddressTypeUnknownError(f"address type '{address_type}' not supported. \nAdmissible values: {list(BirdeyeAddressType.__members__)}")

        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError(f"Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

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
        content = GetOHLCVTokenPairResponse(**content_raw.json())

        return content

    @_api_authorisation
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
            This function refers to the PRIVATE endpoint 'OHLCV - Base/Quote' and is used to get the 
            Open, High, Low, Close, and Volume (OHLCV) data for a specific base/quote combination 
            on a chain on Birdeye.

            Args:

            - base_address (str) [mandatory] : CA of the token to search on the chain.

            - quote_address (str) [mandatory] : CA of the token to search on the chain.

            - timeframe (str) [mandatory] : the type of timeframe involved in the extraction. \\
                The timeframe is used to define intervall between a measure and the next one. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeTimeFrame'. \\
                Import them from the library to use the correct identifier.

            - dt_from (datetime) [optional] : beginning time to take take price data.

            - dt_to (datetime) [optional] : end time to take take price data. \\
                It should be 'dt_from' < 'dt_to'. \\
                If not ptovided (None), the current time is used.

            - chain (str) [optional] : identifier of the chain to check. \\
                The supported chains are available on 'pycrypt.birdeye.param.BirdeyeChain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            Return:

            - (birdeye.schema.GetOHLCVBaseQuoteResponse) : list of prices returned by birdeye.so
        """
        # set default
        if dt_to is None:
            dt_to = datetime.now()

        # check consistency
        if dt_from > dt_to:
            raise BirdeyeTimeRangeError(f"Inconsistent timewindow provided: 'dt_from' > 'dt_to'")

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
        content = GetOHLCVBaseQuoteResponse(**content_raw.json())

        return content

    @_api_authorisation
    def get_wallet_supported_networks(self) -> GetWalletSupportedNetworksResponse:
        """
            This function refers to the PRIVATE endpoint 'Wallet - Supported Networks' and 
            it is used to get the list of supported chains on Birdeye.

            Return:

            - (birdeye.schema.GetWalletSupportedNetworksResponse) : list of chains returned by birdeye.so
        """
        url = self.url_api_private_wallet + "/list_supported_chain"

        # execute request
        content_raw = self.api(RequestType.GET.value, url)
        content = GetWalletSupportedNetworksResponse(**content_raw.json())

        return content