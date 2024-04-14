import os

from ..core.api import APICaller
from ..core.param import RequestType
from ..birdeye.param import BirdeyeChain, BirdeyeOrder, BirdeyeSort
from ..birdeye.schema import GetTokenListResponse

class Birdeye(APICaller):
    """
        Class used to connect https://birdeye.so API. \\  
        To have access Birdeye API (public or private) is required to have a valid API key.

        Check https://docs.birdeye.so for all the details on the available endpoints.

        If the API key is not provided during the object creation, then it is automatically 
        retrieved from ENV variable BIRDEYE_API_KEY.
    """
    def __init__(self, api_key: str | None = None) -> None:

        # set API
        self.api_key = api_key
        if api_key is None:
            self.api_key = os.environ.get("BIRDEYE_API_KEY")
        
        # header
        self.header = {
            "X-API-KEY": self.api_key
        }

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
                The supported chains are available on 'pycrypt.birdeye.chain'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: Solana.

            - sort_by (str) [optional] : define the type of sorting to apply in the 
                extraction; e.g. USD volume in the last 24h. \\
                The sorting types are available on 'pycrypt.birdeye.sort'. \\
                Import them from the library to use the correct identifier. \\
                Default Value: sort by last 24h USD volume.

            - order_by (str) [optional] : define the type of ordering to apply in the 
                extraction; e.g. ascending or descending. \\
                The sorting types are available on 'pycrypt.birdeye.order'. \\
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