from requests.exceptions import HTTPError

from ..core.api import APICaller
from ..core.param import RequestType
from ..jupiter.schema import (
    JupiterHTTPError,
    GetPriceResponse,
    GetQuoteInput,
    GetQuoteResponse
)
from ..jupiter.exception import (
    JupiterException,
    JupiterNoRouteFoundError
)

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
        self.url_api_quote = "https://quote-api.jup.ag/v6/quote"
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

    def get_quote(self, input: GetQuoteInput) -> GetQuoteResponse:
        """
            This function refers to the **[Get Quote](https://station.jup.ag/api-v6/get-quote)** API endpoint, 
            and it is used to get a quote for swapping a specific amount of tokens.  
            The function can be combined with the `post_swap` to implement a payment mechanism.

            Parameters:
                input: an input schema used to describe the request.
                    More details in the object definition.

            Returns:
                Quote found by Jupiter API.
        """
        # set params
        params = input.model_dump(
            by_alias = True, 
            exclude_defaults = True
        )

        # execute request
        try:
            content_raw = self.api(RequestType.GET.value, self.url_api_quote, params = params)
        except HTTPError as e:
            raise self._raise(e)

        # parse response
        content = GetQuoteResponse(**content_raw.json())

        return content

    def _raise(self, exception: HTTPError) -> JupiterException:
        """
            Internal function used to raise the correct 
            Jupiter exception according to the error code 
            provided by the API.

            Parameters:
                exception: the HTTP error returned from Jupiter API.

            Raises:
                JupiterNoRouteFoundError: for error code `COULD_NOT_FIND_ANY_ROUTE` 
                    during the creation of a quote.
                JupiterException: general exception raised when an unknown 
                    error code is found.
        """
        error = JupiterHTTPError(**exception.response.json())
        match error.code:
            case "COULD_NOT_FIND_ANY_ROUTE":
                return JupiterNoRouteFoundError(error.msg)
            case _:
                return JupiterException(error.model_dump())