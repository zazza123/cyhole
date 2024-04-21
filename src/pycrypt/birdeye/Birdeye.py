import os
from datetime import datetime

from ..core.api import APICaller
from ..core.param import RequestType
from ..core.exception import MissingAPIKeyError
from ..birdeye.param import BirdeyeChain, BirdeyeOrder, BirdeyeSort
from ..birdeye.exception import TimeRangeError
from ..birdeye.schema import (
    GetTokenListResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetHistoryResponse
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
        return

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
            raise TimeRangeError(f"Inconsistent timewindow provided: 'dt_from' > 'dt_to'")
        
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