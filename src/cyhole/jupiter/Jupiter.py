from requests.exceptions import HTTPError

from ..core.api import APICaller
from ..core.param import RequestType
from ..jupiter.schema import (
    JupiterHTTPError,
    GetPriceResponse,
    GetQuoteInput,
    GetQuoteResponse,
    GetQuoteTokensResponse,
    GetQuoteProgramIdLabelResponse,
    PostSwapBody,
    PostSwapResponse,
    GetTokenListResponse,
    PostLimitOrderCreateBody,
    PostLimitOrderCreateResponse
)
from ..jupiter.exception import (
    JupiterException,
    JupiterNoRouteFoundError,
    JupiterInvalidRequest
)
from ..jupiter.param import JupiterTokenListType

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
        self.url_api_quote = "https://quote-api.jup.ag/v6/"
        self.url_api_token = "https://token.jup.ag/"
        self.url_api_limit = "https://jup.ag/api/limit/v1/"
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
        url = self.url_api_quote + "quote"
        params = input.model_dump(
            by_alias = True, 
            exclude_defaults = True
        )

        # execute request
        try:
            content_raw = self.api(RequestType.GET.value, url, params = params)
        except HTTPError as e:
            raise self._raise(e)

        # parse response
        content = GetQuoteResponse(**content_raw.json())

        return content

    def get_quote_tokens(self) -> GetQuoteTokensResponse:
        """
            This function refers to the **[Get Quote Tokens](https://station.jup.ag/api-v6/get-tokens)** API endpoint, 
            and it is used to get the list of the current supported tradable tokens. 

            Returns:
                List of tradable tokens.
        """
        # set params
        url = self.url_api_quote + "tokens"

        # execute request
        content_raw = self.api(RequestType.GET.value, url)

        # parse response
        content = GetQuoteTokensResponse(tokens = content_raw.json())

        return content

    def get_quote_program_id_label(self) -> GetQuoteProgramIdLabelResponse:
        """
            This function refers to the **[Get Quote Program ID to Label](https://station.jup.ag/api-v6/get-program-id-to-label)** API endpoint, 
            and it is used to get the list of supported DEXes to use in quote endpoint. 

            Returns:
                List of DEXs addresses and labels.
        """
        # set params
        url = self.url_api_quote + "program-id-to-label"

        # execute request
        content_raw = self.api(RequestType.GET.value, url)

        # parse response
        content = GetQuoteProgramIdLabelResponse(dexes = content_raw.json())

        return content

    def post_swap(self, body: PostSwapBody) -> PostSwapResponse:
        """
            This function refers to the **[Post Swap](https://station.jup.ag/api-v6/post-swap)** API endpoint, 
            and it is used to recive the transaction to perform the swap initialised from `get_quote` 
            endopoint for the desired pair.  
            The function should be combined with the `get_quote` endpoint.

            Parameters:
                body: the body to sent to Jupiter API that describe the swap.
                    More details in the object definition.

            Returns:
                Transaction found by Jupiter API.
        """
        # set params
        url = self.url_api_quote + "swap"
        headers = {
            "Content-Type": "application/json"
        }

        # execute request
        try:
            content_raw = self.api(
                type = RequestType.POST.value,
                url = url,
                headers = headers,
                json = body.model_dump(by_alias = True, exclude_defaults = True)
            )
        except HTTPError as e:
            raise self._raise(e)
        # parse response
        content = PostSwapResponse(**content_raw.json())

        return content

    def get_token_list(self, type: str = JupiterTokenListType.STRICT.value, banned: None | bool = None) -> GetTokenListResponse:
        """
            This function refers to the **[Token List](https://station.jup.ag/docs/token-list/token-list-api)** API endpoint, 
            and it is used to retrieved the list of tokens eligible for trading, managed by Jupiter.  
            Choose the tokens list according to `type` field.

            Parameters:
                type: Jupiter manages the tradable tokens through a set of tags in order to guarantee its 
                    core values and provide a secure service. There are two types of lists currently available:  
                    - Strict the most secure list that includes only the tokens with tags `old-registry`, `community`, or `wormhole`.
                    - All all the tokens are included expect the banned ones.
                    The supported types are available on [`JupiterTokenListType`][cyhole.jupiter.param.JupiterTokenListType].
                banned: this flag can be used **only** on `All` type, and it enables the inclusion of banned tokens.

            Returns:
                List of Jupiter's tokens list.
        """
        # check param consistency
        JupiterTokenListType.check(type)

        # set params
        url = self.url_api_token + type
        params = {
            "includeBanned" : banned
        }

        # execute request
        content_raw = self.api(RequestType.GET.value, url, params = params)

        # parse response
        content = GetTokenListResponse(tokens = content_raw.json())

        return content

    def post_limit_order_create(self, body: PostLimitOrderCreateBody) -> PostLimitOrderCreateResponse:

        # set params
        url = self.url_api_limit + "createOrder"
        headers = {
            "Content-Type": "application/json"
        }

        # execute request
        try:
            content_raw = self.api(
                type = RequestType.POST.value,
                url = url,
                headers = headers,
                json = body.model_dump(by_alias = True, exclude_defaults = True)
            )
        except HTTPError as e:
            raise self._raise(e)

        # parse response
        content = PostLimitOrderCreateResponse(**content_raw.json())
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
            case "INVALID_REQUEST":
                return JupiterInvalidRequest(error.msg)
            case _:
                return JupiterException(error.model_dump_json())