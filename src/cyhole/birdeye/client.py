from __future__ import annotations
import requests
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..core.exception import AuthorizationAPIKeyError
from ..birdeye.exception import BirdeyeAuthorisationError
from ..birdeye.param import (
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTradeType
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

if TYPE_CHECKING:
    from ..birdeye.interaction import Birdeye

class BirdeyeClient(APIClient):
    """
        Client used for synchronous API calls for `Birdeye` interaction.
    """

    def __init__(self, interaction: Birdeye, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Birdeye = self._interaction

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        # overide function to manage client specific exceptions
        try:
            return super().api(type, url, *args, **kwargs)
        except AuthorizationAPIKeyError:
            raise BirdeyeAuthorisationError

    def get_token_list(self, sort_by: str = BirdeyeSort.SORT_V24HUSD.value, order_by: str = BirdeyeOrder.DESCENDING.value, offset: int | None = None, limit: int | None = None) -> GetTokenListResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Token - List](https://docs.birdeye.so/reference/get_defi-tokenlist)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_list`][cyhole.birdeye.interaction.Birdeye._get_token_list].
        """
        return self._interaction._get_token_list(True, sort_by, order_by, offset, limit)

    def get_token_creation_info(self, address: str) -> GetTokenCreationInfoResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get_defi-token-creation-info)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_creation_info`][cyhole.birdeye.interaction.Birdeye._get_token_creation_info].
        """
        return self._interaction._get_token_creation_info(True, address)

    def get_token_security(self, address: str) -> GetTokenSecurityResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get_defi-token-security)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_security`][cyhole.birdeye.interaction.Birdeye._get_token_security].
        """
        return self._interaction._get_token_security(True, address)

    def get_token_overview(self, address: str) -> GetTokenOverviewResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get_defi-token-overview)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_overview`][cyhole.birdeye.interaction.Birdeye._get_token_overview].
        """
        return self._interaction._get_token_overview(True, address)

    def get_price(self, address: str, include_liquidity: bool | None = None) -> GetPriceResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price](https://docs.birdeye.so/reference/get_defi-price)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price`][cyhole.birdeye.interaction.Birdeye._get_price].
        """
        return self._interaction._get_price(True, address, include_liquidity)

    def get_price_multiple(self, list_address: list[str], include_liquidity: bool | None = None) -> GetPriceMultipleResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price - Multiple](https://docs.birdeye.so/reference/get_defi-multi-price)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_multiple`][cyhole.birdeye.interaction.Birdeye._get_price_multiple].
        """
        return self._interaction._get_price_multiple(True, list_address, include_liquidity)

    def get_price_historical(self, address: str, address_type: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetPriceHistoricalResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price - Historical](https://docs.birdeye.so/reference/get_defi-history-price)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_historical`][cyhole.birdeye.interaction.Birdeye._get_price_historical].
        """
        return self._interaction._get_price_historical(True, address, address_type, timeframe, dt_from, dt_to)

    def get_trades_token(self, address: str, trade_type: str = BirdeyeTradeType.SWAP.value, offset: int | None = None, limit: int | None = None) -> GetTradesTokenResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Trades - Token](https://docs.birdeye.so/reference/get_defi-txs-token)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_trades_token`][cyhole.birdeye.interaction.Birdeye._get_trades_token].
        """
        return self._interaction._get_trades_token(True, address, trade_type, offset, limit)

    def get_trades_pair(self, address: str, trade_type: str = BirdeyeTradeType.SWAP.value, order_by: str = BirdeyeOrder.DESCENDING.value, offset: int | None = None, limit: int | None = None) -> GetTradesPairResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Trades - Pair](https://docs.birdeye.so/reference/get_defi-txs-pair)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_trades_pair`][cyhole.birdeye.interaction.Birdeye._get_trades_pair].
        """
        return self._interaction._get_trades_pair(True, address, trade_type, order_by, offset, limit)

    def get_ohlcv(self, address: str, address_type: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetOHLCVTokenPairResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[OHLCV - Token/Pair](https://docs.birdeye.so/reference/get_defi-ohlcv)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_ohlcv`][cyhole.birdeye.interaction.Birdeye._get_ohlcv].
        """
        return self._interaction._get_ohlcv(True, address, address_type, timeframe, dt_from, dt_to)

    def get_ohlcv_base_quote(self, base_address: str, quote_address: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetOHLCVBaseQuoteResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[OHLCV - Base/Quote](https://docs.birdeye.so/reference/get_defi-ohlcv-base-quote)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_ohlcv_base_quote`][cyhole.birdeye.interaction.Birdeye._get_ohlcv_base_quote].
        """
        return self._interaction._get_ohlcv_base_quote(True, base_address, quote_address, timeframe, dt_from, dt_to)

    def get_wallet_supported_networks(self) -> GetWalletSupportedNetworksResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Wallet - Supported Networks](https://docs.birdeye.so/reference/get_v1-wallet-list-supported-chain)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_wallet_supported_networks`][cyhole.birdeye.interaction.Birdeye._get_wallet_supported_networks].
        """
        return self._interaction._get_wallet_supported_networks(True)

class BirdeyeAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Birdeye` interaction.
    """

    def __init__(self, interaction: Birdeye, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Birdeye = self._interaction

    async def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> requests.Response:
        # overide function to manage client specific exceptions
        try:
            return await super().api(type, url, *args, **kwargs)
        except AuthorizationAPIKeyError:
            raise BirdeyeAuthorisationError

    async def get_token_list(self, sort_by: str = BirdeyeSort.SORT_V24HUSD.value, order_by: str = BirdeyeOrder.DESCENDING.value, offset: int | None = None, limit: int | None = None
    ) -> GetTokenListResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Token - List](https://docs.birdeye.so/reference/get_defi-tokenlist)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_list`][cyhole.birdeye.interaction.Birdeye._get_token_list].
        """
        return await self._interaction._get_token_list(False, sort_by, order_by, offset, limit)

    async def get_token_creation_info(self, address: str) -> GetTokenCreationInfoResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get_defi-token-creation-info)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_creation_info`][cyhole.birdeye.interaction.Birdeye._get_token_creation_info].
        """
        return await self._interaction._get_token_creation_info(False, address)

    async def get_token_security(self, address: str) -> GetTokenSecurityResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get_defi-token-security)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_security`][cyhole.birdeye.interaction.Birdeye._get_token_security].
        """
        return await self._interaction._get_token_security(False, address)

    async def get_token_overview(self, address: str) -> GetTokenOverviewResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get_defi-token-overview)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_token_overview`][cyhole.birdeye.interaction.Birdeye._get_token_overview].
        """
        return await self._interaction._get_token_overview(False, address)

    async def get_price(self, address: str, include_liquidity: bool | None = None) -> GetPriceResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price](https://docs.birdeye.so/reference/get_defi-price)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price`][cyhole.birdeye.interaction.Birdeye._get_price].
        """
        return await self._interaction._get_price(False, address, include_liquidity)

    async def get_price_multiple(self, list_address: list[str], include_liquidity: bool | None = None) -> GetPriceMultipleResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price - Multiple](https://docs.birdeye.so/reference/get_defi-multi-price)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_multiple`][cyhole.birdeye.interaction.Birdeye._get_price_multiple].
        """
        return await self._interaction._get_price_multiple(False, list_address, include_liquidity)

    async def get_price_historical(self, address: str, address_type: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetPriceHistoricalResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Price - Historical](https://docs.birdeye.so/reference/get_defi-history-price)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_historical`][cyhole.birdeye.interaction.Birdeye._get_price_historical].
        """
        return await self._interaction._get_price_historical(False, address, address_type, timeframe, dt_from, dt_to)

    async def get_trades_token(self, address: str, trade_type: str = BirdeyeTradeType.SWAP.value, offset: int | None = None, limit: int | None = None) -> GetTradesTokenResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Trades - Token](https://docs.birdeye.so/reference/get_defi-txs-token)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_trades_token`][cyhole.birdeye.interaction.Birdeye._get_trades_token].
        """
        return await self._interaction._get_trades_token(False, address, trade_type, offset, limit)

    async def get_trades_pair(self, address: str, trade_type: str = BirdeyeTradeType.SWAP.value, order_by: str = BirdeyeOrder.DESCENDING.value, offset: int | None = None, limit: int | None = None) -> GetTradesPairResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Trades - Pair](https://docs.birdeye.so/reference/get_defi-txs-pair)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_trades_pair`][cyhole.birdeye.interaction.Birdeye._get_trades_pair].
        """
        return await self._interaction._get_trades_pair(False, address, trade_type, order_by, offset, limit)

    async def get_ohlcv(self, address: str, address_type: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetOHLCVTokenPairResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[OHLCV - Token/Pair](https://docs.birdeye.so/reference/get_defi-ohlcv)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_ohlcv`][cyhole.birdeye.interaction.Birdeye._get_ohlcv].
        """
        return await self._interaction._get_ohlcv(False, address, address_type, timeframe, dt_from, dt_to)

    async def get_ohlcv_base_quote(self, base_address: str, quote_address: str, timeframe: str, dt_from: datetime, dt_to: datetime | None = None) -> GetOHLCVBaseQuoteResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[OHLCV - Base/Quote](https://docs.birdeye.so/reference/get_defi-ohlcv-base-quote)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_ohlcv_base_quote`][cyhole.birdeye.interaction.Birdeye._get_ohlcv_base_quote].
        """
        return await self._interaction._get_ohlcv_base_quote(False, base_address, quote_address, timeframe, dt_from, dt_to)

    async def get_wallet_supported_networks(self) -> GetWalletSupportedNetworksResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Wallet - Supported Networks](https://docs.birdeye.so/reference/get_v1-wallet-list-supported-chain)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_wallet_supported_networks`][cyhole.birdeye.interaction.Birdeye._get_wallet_supported_networks].
        """
        return await self._interaction._get_wallet_supported_networks(False)