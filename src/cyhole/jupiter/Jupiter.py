from ..core.api import APICaller
from ..core.param import RequestType
from ..jupiter.schema import GetPriceResponse

class Jupiter(APICaller):
    """
        Class used to connect [Jupiter](https://jup.ag) API, one of them most popular Solana DEX. 
        To have access Jupiter API is **not** required an API key.

        Check [https://station.jup.ag/docs/api](https://station.jup.ag/docs/api) for all the details on the available endpoints.

        **Example**

        ```python
        from cyhole.jupiter import Jupiter
        from cyhole.core.address.solana import JUP

        # get current price of JUP on Solana
        api = Jupiter()
        price = api.get_price([JUP])
        ```
    """

    def __init__(self) -> None:
        super().__init__()

        self.url_api_price = "https://price.jup.ag/v6/price"
        return

    def get_price(self, address: list[str], vs_address: str | None = None) -> GetPriceResponse:
        """
            This function refers to the **[Price](https://station.jup.ag/docs/apis/price-api)** API endpoint, 
            and it is used to get the current price of a list of tokens on Solana chain with respect to another token. 

            The API returns the unit buy price for the tokens; by default, the price is provided according to 
            the value of `USDC` token. It is also possible to provide another comparison token in the request.

            !!! info
                Observe that when the token address/symbol or comparison token address/symbol are not found, 
                the response provided will have an empty `data` object.

            Parameters:
                address: list of tokens involved in the request.
                    It is possible to provide the Solana tokens' addresses or their symbols. 
                    For example, `SOL` is equivalent to `So11111111111111111111111111111111111111112`.
                vs_address: comparison token address/symbol.
                    Default Value: `None` (`USDC`)

            Returns:
                tokens' prices.

            Raises:
                BirdeyeAuthorisationError: if the API key provided does not give access to related endpoint.
                ParamUnknownError: if one of the input parameter belonging to the value list is aligned to it.
        """
        # set params
        params = {
            "ids": ",".join(address),
            "vsToken": vs_address
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, self.url_api_price, params = params)

        # parse response
        content = GetPriceResponse(**content_raw.json())

        return content