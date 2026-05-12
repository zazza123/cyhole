from __future__ import annotations
import requests
from datetime import datetime
from typing import TYPE_CHECKING, Any, overload

from ..core.client import APIClient, AsyncAPIClient
from ..core.exception import AuthorizationAPIKeyError
from ..birdeye.exception import BirdeyeAuthorisationError
from ..birdeye.param import (
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTradeType,
    BirdeyeHourTimeFrame,
    BirdeyeV2MarketsSortBy,
    BirdeyeMintBurnType,
    BirdeyeV2TopTradersSortBy,
    BirdeyeV2TopTradersTimeFrame,
    BirdeyeHolderDistributionAddressType,
    BirdeyeHolderDistributionMode,
)
from ..birdeye.schema import (
    GetTokenListResponse,
    GetV3TokenListQuery,
    GetV3TokenListResponse,
    GetV3TokenListScrollQuery,
    GetV3TokenListScrollResponse,
    GetV2TokensNewListingResponse,
    GetV2MarketsResponse,
    GetV3TokenMetaDataResponse,
    GetV3TokenMetaDataMultipleResponse,
    GetV3TokenMarketDataResponse,
    GetV3TokenMarketDataMultipleResponse,
    GetV3TokenTradeDataResponse,
    GetV3TokenTradeDataMultipleResponse,
    GetV3TokenExitLiquidityResponse,
    GetV3TokenExitLiquidityMultipleResponse,
    GetV3TokenMintBurnTxsResponse,
    GetV2TopTradersResponse,
    GetTokenHolderResponse,
    PostTokenHolderBatchResponse,
    GetHolderDistributionResponse,
    GetHolderProfileResponse,
    GetTokenHolderPositionsResponse,
    GetTokenSecurityResponse,
    GetTokenCreationInfoResponse,
    GetTokenOverviewResponse,
    GetPriceResponse,
    GetPriceMultipleResponse,
    GetPriceHistoricalResponse,
    GetPriceVolumeSingleResponse,
    PostPriceVolumeMultiResponse,
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

    def get_token_list(
        self,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        min_liquidity: float | None = None,
        max_liquidity: float | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenListResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Token - List (V1)](https://docs.birdeye.so/reference/get-defi-tokenlist)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_list`][cyhole.birdeye.interaction.Birdeye._get_token_list].
        """
        return self._interaction._get_token_list(True, sort_by, order_by, offset, limit, min_liquidity, max_liquidity, ui_amount_mode)

    def get_v3_token_list(self, query: GetV3TokenListQuery | None = None) -> GetV3TokenListResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - List (V3)](https://docs.birdeye.so/reference/get-defi-v3-token-list)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_list`][cyhole.birdeye.interaction.Birdeye._get_v3_token_list].
        """
        return self._interaction._get_v3_token_list(True, query)

    def get_v3_token_list_scroll(self, query: GetV3TokenListScrollQuery | None = None) -> GetV3TokenListScrollResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - List (V3) Scroll](https://docs.birdeye.so/reference/get-defi-v3-token-list-scroll)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_list_scroll`][cyhole.birdeye.interaction.Birdeye._get_v3_token_list_scroll].
        """
        return self._interaction._get_v3_token_list_scroll(True, query)

    def get_v2_tokens_new_listing(
        self,
        time_to: int | None = None,
        limit: int | None = None,
        meme_platform_enabled: bool | None = None
    ) -> GetV2TokensNewListingResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - New Listing](https://docs.birdeye.so/reference/get-defi-v2-tokens-new_listing)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_tokens_new_listing`][cyhole.birdeye.interaction.Birdeye._get_v2_tokens_new_listing].
        """
        return self._interaction._get_v2_tokens_new_listing(True, time_to, limit, meme_platform_enabled)

    def get_v2_markets(
        self,
        address: str,
        sort_by: str = BirdeyeV2MarketsSortBy.LIQUIDITY.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV2MarketsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - All Market List](https://docs.birdeye.so/reference/get-defi-v2-markets)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_markets`][cyhole.birdeye.interaction.Birdeye._get_v2_markets].
        """
        return self._interaction._get_v2_markets(True, address, sort_by, sort_type, offset, limit)

    @overload
    def get_v3_token_meta_data(self, address: str) -> GetV3TokenMetaDataResponse: ...

    @overload
    def get_v3_token_meta_data(self, address: list[str]) -> GetV3TokenMetaDataMultipleResponse: ...

    def get_v3_token_meta_data(self, address: str | list[str]) -> GetV3TokenMetaDataResponse | GetV3TokenMetaDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Metadata endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-single)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-multiple)**) for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_meta_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_meta_data].
        """
        return self._interaction._get_v3_token_meta_data(True, address)

    @overload
    def get_v3_token_market_data(self, address: str, ui_amount_mode: str | None = None) -> GetV3TokenMarketDataResponse: ...

    @overload
    def get_v3_token_market_data(self, address: list[str], ui_amount_mode: str | None = None) -> GetV3TokenMarketDataMultipleResponse: ...

    def get_v3_token_market_data(self, address: str | list[str], ui_amount_mode: str | None = None) -> GetV3TokenMarketDataResponse | GetV3TokenMarketDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Market Data endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-market-data)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-market-data-multiple)**) for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_market_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_market_data].
        """
        return self._interaction._get_v3_token_market_data(True, address, ui_amount_mode)

    @overload
    def get_v3_token_trade_data(self, address: str, frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataResponse: ...

    @overload
    def get_v3_token_trade_data(self, address: list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataMultipleResponse: ...

    def get_v3_token_trade_data(self, address: str | list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataResponse | GetV3TokenTradeDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Trade Data endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-single)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-multiple)**) for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_trade_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_trade_data].
        """
        return self._interaction._get_v3_token_trade_data(True, address, frames, ui_amount_mode)

    @overload
    def get_v3_token_exit_liquidity(self, address: str) -> GetV3TokenExitLiquidityResponse: ...

    @overload
    def get_v3_token_exit_liquidity(self, address: list[str]) -> GetV3TokenExitLiquidityMultipleResponse: ...

    def get_v3_token_exit_liquidity(self, address: str | list[str]) -> GetV3TokenExitLiquidityResponse | GetV3TokenExitLiquidityMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Liquidity endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity-multiple)**) for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_exit_liquidity`][cyhole.birdeye.interaction.Birdeye._get_v3_token_exit_liquidity].
        """
        return self._interaction._get_v3_token_exit_liquidity(True, address)

    def get_v3_token_mint_burn_txs(
        self,
        address: str,
        type: str = BirdeyeMintBurnType.ALL.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        after_time: int | None = None,
        before_time: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV3TokenMintBurnTxsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Mint/Burn](https://docs.birdeye.so/reference/get-defi-v3-token-mint-burn-txs)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_mint_burn_txs`][cyhole.birdeye.interaction.Birdeye._get_v3_token_mint_burn_txs].
        """
        return self._interaction._get_v3_token_mint_burn_txs(True, address, type, sort_type, after_time, before_time, offset, limit)

    def get_v2_tokens_top_traders(
        self,
        address: str,
        time_frame: str = BirdeyeV2TopTradersTimeFrame.H24.value,
        sort_by: str = BirdeyeV2TopTradersSortBy.VOLUME.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetV2TopTradersResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Top Traders](https://docs.birdeye.so/reference/get-defi-v2-tokens-top_traders)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_tokens_top_traders`][cyhole.birdeye.interaction.Birdeye._get_v2_tokens_top_traders].
        """
        return self._interaction._get_v2_tokens_top_traders(True, address, time_frame, sort_by, sort_type, offset, limit, ui_amount_mode)

    @overload
    def get_token_holder(self, token_address: str, wallets: None = None, offset: int | None = None, limit: int | None = None, ui_amount_mode: str | None = None) -> GetTokenHolderResponse: ...

    @overload
    def get_token_holder(self, token_address: str, wallets: list[str], offset: int | None = None, limit: int | None = None, ui_amount_mode: str | None = None) -> PostTokenHolderBatchResponse: ...

    def get_token_holder(
        self,
        token_address: str,
        wallets: list[str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenHolderResponse | PostTokenHolderBatchResponse:
        """
            Call the Birdeye's **PRIVATE** Token Holder endpoints (**[top-holder ranking](https://docs.birdeye.so/reference/get-defi-v3-token-holder)** /
            **[batch balance lookup](https://docs.birdeye.so/reference/post-token-v1-holder-batch)**) for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder`][cyhole.birdeye.interaction.Birdeye._get_token_holder].
        """
        return self._interaction._get_token_holder(True, token_address, wallets, offset, limit, ui_amount_mode)

    def get_holder_distribution(
        self,
        token_address: str,
        address_type: str = BirdeyeHolderDistributionAddressType.WALLET.value,
        mode: str = BirdeyeHolderDistributionMode.TOP.value,
        top_n: int | None = None,
        min_percent: float | None = None,
        max_percent: float | None = None,
        include_list: bool | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetHolderDistributionResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Distribution](https://docs.birdeye.so/reference/get-holder-v1-distribution)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_holder_distribution`][cyhole.birdeye.interaction.Birdeye._get_holder_distribution].
        """
        return self._interaction._get_holder_distribution(True, token_address, address_type, mode, top_n, min_percent, max_percent, include_list, offset, limit)

    def get_token_holder_profile(
        self,
        token_address: str,
        interval: str = "1h",
        ui_amount_mode: str | None = None,
        include_zero_balance: bool | None = None
    ) -> GetHolderProfileResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Profile](https://docs.birdeye.so/reference/get-token-v1-holder-profile)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder_profile`][cyhole.birdeye.interaction.Birdeye._get_token_holder_profile].
        """
        return self._interaction._get_token_holder_profile(True, token_address, interval, ui_amount_mode, include_zero_balance)

    def get_token_holder_positions(
        self,
        token_address: str,
        labels: str | None = None,
        order_type: str = BirdeyeOrder.DESCENDING.value,
        ui_amount_mode: str | None = None,
        include_zero_balance: bool | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenHolderPositionsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Positions](https://docs.birdeye.so/reference/get-token-v1-holder-positions)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder_positions`][cyhole.birdeye.interaction.Birdeye._get_token_holder_positions].
        """
        return self._interaction._get_token_holder_positions(True, token_address, labels, order_type, ui_amount_mode, include_zero_balance, offset, limit)

    def get_token_creation_info(self, address: str) -> GetTokenCreationInfoResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get-defi-token_creation_info)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_creation_info`][cyhole.birdeye.interaction.Birdeye._get_token_creation_info].
        """
        return self._interaction._get_token_creation_info(True, address)

    def get_token_security(self, address: str) -> GetTokenSecurityResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get-defi-token_security)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_security`][cyhole.birdeye.interaction.Birdeye._get_token_security].
        """
        return self._interaction._get_token_security(True, address)

    def get_token_overview(
        self,
        address: str,
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenOverviewResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get-defi-token_overview)** for synchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_overview`][cyhole.birdeye.interaction.Birdeye._get_token_overview].
        """
        return self._interaction._get_token_overview(True, address, frames, ui_amount_mode)

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

    def get_price_volume_single(self, address: str, timeframe: str = BirdeyeHourTimeFrame.H24.value) -> GetPriceVolumeSingleResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Price Volume - Single Token](https://docs.birdeye.so/reference/get_defi-price-volume-single)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_volume_single`][cyhole.birdeye.interaction.Birdeye._get_price_volume_single].
        """
        return self._interaction._get_price_volume_single(True, address, timeframe)

    def post_price_volume_multi(self, list_address: list[str], timeframe: str = BirdeyeHourTimeFrame.H24.value) -> PostPriceVolumeMultiResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Price Volume - Multiple Token](https://docs.birdeye.so/reference/get_defi-price-volume-single)** for synchronous logic. 
            All the API endopint details are available on [`Birdeye._post_price_volume_multi`][cyhole.birdeye.interaction.Birdeye._post_price_volume_multi].
        """
        return self._interaction._post_price_volume_multi(True, list_address, timeframe)

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

    async def get_token_list(
        self,
        sort_by: str = BirdeyeSort.SORT_V24HUSD.value,
        order_by: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        min_liquidity: float | None = None,
        max_liquidity: float | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenListResponse:
        """
            Call the Birdeye's **PUBLIC** API endpoint **[Token - List (V1)](https://docs.birdeye.so/reference/get-defi-tokenlist)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_list`][cyhole.birdeye.interaction.Birdeye._get_token_list].
        """
        return await self._interaction._get_token_list(False, sort_by, order_by, offset, limit, min_liquidity, max_liquidity, ui_amount_mode)

    async def get_v3_token_list(self, query: GetV3TokenListQuery | None = None) -> GetV3TokenListResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - List (V3)](https://docs.birdeye.so/reference/get-defi-v3-token-list)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_list`][cyhole.birdeye.interaction.Birdeye._get_v3_token_list].
        """
        return await self._interaction._get_v3_token_list(False, query)

    async def get_v3_token_list_scroll(self, query: GetV3TokenListScrollQuery | None = None) -> GetV3TokenListScrollResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - List (V3) Scroll](https://docs.birdeye.so/reference/get-defi-v3-token-list-scroll)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_list_scroll`][cyhole.birdeye.interaction.Birdeye._get_v3_token_list_scroll].
        """
        return await self._interaction._get_v3_token_list_scroll(False, query)

    async def get_v2_tokens_new_listing(
        self,
        time_to: int | None = None,
        limit: int | None = None,
        meme_platform_enabled: bool | None = None
    ) -> GetV2TokensNewListingResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - New Listing](https://docs.birdeye.so/reference/get-defi-v2-tokens-new_listing)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_tokens_new_listing`][cyhole.birdeye.interaction.Birdeye._get_v2_tokens_new_listing].
        """
        return await self._interaction._get_v2_tokens_new_listing(False, time_to, limit, meme_platform_enabled)

    async def get_v2_markets(
        self,
        address: str,
        sort_by: str = BirdeyeV2MarketsSortBy.LIQUIDITY.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV2MarketsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - All Market List](https://docs.birdeye.so/reference/get-defi-v2-markets)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_markets`][cyhole.birdeye.interaction.Birdeye._get_v2_markets].
        """
        return await self._interaction._get_v2_markets(False, address, sort_by, sort_type, offset, limit)

    @overload
    async def get_v3_token_meta_data(self, address: str) -> GetV3TokenMetaDataResponse: ...

    @overload
    async def get_v3_token_meta_data(self, address: list[str]) -> GetV3TokenMetaDataMultipleResponse: ...

    async def get_v3_token_meta_data(self, address: str | list[str]) -> GetV3TokenMetaDataResponse | GetV3TokenMetaDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Metadata endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-single)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-meta-data-multiple)**) for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_meta_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_meta_data].
        """
        return await self._interaction._get_v3_token_meta_data(False, address)

    @overload
    async def get_v3_token_market_data(self, address: str, ui_amount_mode: str | None = None) -> GetV3TokenMarketDataResponse: ...

    @overload
    async def get_v3_token_market_data(self, address: list[str], ui_amount_mode: str | None = None) -> GetV3TokenMarketDataMultipleResponse: ...

    async def get_v3_token_market_data(self, address: str | list[str], ui_amount_mode: str | None = None) -> GetV3TokenMarketDataResponse | GetV3TokenMarketDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Market Data endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-market-data)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-market-data-multiple)**) for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_market_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_market_data].
        """
        return await self._interaction._get_v3_token_market_data(False, address, ui_amount_mode)

    @overload
    async def get_v3_token_trade_data(self, address: str, frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataResponse: ...

    @overload
    async def get_v3_token_trade_data(self, address: list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataMultipleResponse: ...

    async def get_v3_token_trade_data(self, address: str | list[str], frames: str | None = None, ui_amount_mode: str | None = None) -> GetV3TokenTradeDataResponse | GetV3TokenTradeDataMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Trade Data endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-single)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-trade-data-multiple)**) for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_trade_data`][cyhole.birdeye.interaction.Birdeye._get_v3_token_trade_data].
        """
        return await self._interaction._get_v3_token_trade_data(False, address, frames, ui_amount_mode)

    @overload
    async def get_v3_token_exit_liquidity(self, address: str) -> GetV3TokenExitLiquidityResponse: ...

    @overload
    async def get_v3_token_exit_liquidity(self, address: list[str]) -> GetV3TokenExitLiquidityMultipleResponse: ...

    async def get_v3_token_exit_liquidity(self, address: str | list[str]) -> GetV3TokenExitLiquidityResponse | GetV3TokenExitLiquidityMultipleResponse:
        """
            Call the Birdeye's **PRIVATE** v3 Token - Liquidity endpoints (**[single](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity)** /
            **[multiple](https://docs.birdeye.so/reference/get-defi-v3-token-exit-liquidity-multiple)**) for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_exit_liquidity`][cyhole.birdeye.interaction.Birdeye._get_v3_token_exit_liquidity].
        """
        return await self._interaction._get_v3_token_exit_liquidity(False, address)

    async def get_v3_token_mint_burn_txs(
        self,
        address: str,
        type: str = BirdeyeMintBurnType.ALL.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        after_time: int | None = None,
        before_time: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetV3TokenMintBurnTxsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Mint/Burn](https://docs.birdeye.so/reference/get-defi-v3-token-mint-burn-txs)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v3_token_mint_burn_txs`][cyhole.birdeye.interaction.Birdeye._get_v3_token_mint_burn_txs].
        """
        return await self._interaction._get_v3_token_mint_burn_txs(False, address, type, sort_type, after_time, before_time, offset, limit)

    async def get_v2_tokens_top_traders(
        self,
        address: str,
        time_frame: str = BirdeyeV2TopTradersTimeFrame.H24.value,
        sort_by: str = BirdeyeV2TopTradersSortBy.VOLUME.value,
        sort_type: str = BirdeyeOrder.DESCENDING.value,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetV2TopTradersResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Top Traders](https://docs.birdeye.so/reference/get-defi-v2-tokens-top_traders)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_v2_tokens_top_traders`][cyhole.birdeye.interaction.Birdeye._get_v2_tokens_top_traders].
        """
        return await self._interaction._get_v2_tokens_top_traders(False, address, time_frame, sort_by, sort_type, offset, limit, ui_amount_mode)

    @overload
    async def get_token_holder(self, token_address: str, wallets: None = None, offset: int | None = None, limit: int | None = None, ui_amount_mode: str | None = None) -> GetTokenHolderResponse: ...

    @overload
    async def get_token_holder(self, token_address: str, wallets: list[str], offset: int | None = None, limit: int | None = None, ui_amount_mode: str | None = None) -> PostTokenHolderBatchResponse: ...

    async def get_token_holder(
        self,
        token_address: str,
        wallets: list[str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenHolderResponse | PostTokenHolderBatchResponse:
        """
            Call the Birdeye's **PRIVATE** Token Holder endpoints (**[top-holder ranking](https://docs.birdeye.so/reference/get-defi-v3-token-holder)** /
            **[batch balance lookup](https://docs.birdeye.so/reference/post-token-v1-holder-batch)**) for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder`][cyhole.birdeye.interaction.Birdeye._get_token_holder].
        """
        return await self._interaction._get_token_holder(False, token_address, wallets, offset, limit, ui_amount_mode)

    async def get_holder_distribution(
        self,
        token_address: str,
        address_type: str = BirdeyeHolderDistributionAddressType.WALLET.value,
        mode: str = BirdeyeHolderDistributionMode.TOP.value,
        top_n: int | None = None,
        min_percent: float | None = None,
        max_percent: float | None = None,
        include_list: bool | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetHolderDistributionResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Distribution](https://docs.birdeye.so/reference/get-holder-v1-distribution)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_holder_distribution`][cyhole.birdeye.interaction.Birdeye._get_holder_distribution].
        """
        return await self._interaction._get_holder_distribution(False, token_address, address_type, mode, top_n, min_percent, max_percent, include_list, offset, limit)

    async def get_token_holder_profile(
        self,
        token_address: str,
        interval: str = "1h",
        ui_amount_mode: str | None = None,
        include_zero_balance: bool | None = None
    ) -> GetHolderProfileResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Profile](https://docs.birdeye.so/reference/get-token-v1-holder-profile)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder_profile`][cyhole.birdeye.interaction.Birdeye._get_token_holder_profile].
        """
        return await self._interaction._get_token_holder_profile(False, token_address, interval, ui_amount_mode, include_zero_balance)

    async def get_token_holder_positions(
        self,
        token_address: str,
        labels: str | None = None,
        order_type: str = BirdeyeOrder.DESCENDING.value,
        ui_amount_mode: str | None = None,
        include_zero_balance: bool | None = None,
        offset: int | None = None,
        limit: int | None = None
    ) -> GetTokenHolderPositionsResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Holder Positions](https://docs.birdeye.so/reference/get-token-v1-holder-positions)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_holder_positions`][cyhole.birdeye.interaction.Birdeye._get_token_holder_positions].
        """
        return await self._interaction._get_token_holder_positions(False, token_address, labels, order_type, ui_amount_mode, include_zero_balance, offset, limit)

    async def get_token_creation_info(self, address: str) -> GetTokenCreationInfoResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Creation Token Info](https://docs.birdeye.so/reference/get-defi-token_creation_info)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_creation_info`][cyhole.birdeye.interaction.Birdeye._get_token_creation_info].
        """
        return await self._interaction._get_token_creation_info(False, address)

    async def get_token_security(self, address: str) -> GetTokenSecurityResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Security](https://docs.birdeye.so/reference/get-defi-token_security)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_security`][cyhole.birdeye.interaction.Birdeye._get_token_security].
        """
        return await self._interaction._get_token_security(False, address)

    async def get_token_overview(
        self,
        address: str,
        frames: str | None = None,
        ui_amount_mode: str | None = None
    ) -> GetTokenOverviewResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Token - Overview](https://docs.birdeye.so/reference/get-defi-token_overview)** for asynchronous logic.
            All the API endpoint details are available on [`Birdeye._get_token_overview`][cyhole.birdeye.interaction.Birdeye._get_token_overview].
        """
        return await self._interaction._get_token_overview(False, address, frames, ui_amount_mode)

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

    async def get_price_volume_single(self, address: str, timeframe: str = BirdeyeHourTimeFrame.H24.value) -> GetPriceVolumeSingleResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Price Volume - Single Token](https://docs.birdeye.so/reference/get_defi-price-volume-single)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._get_price_volume_single`][cyhole.birdeye.interaction.Birdeye._get_price_volume_single].
        """
        return await self._interaction._get_price_volume_single(False, address, timeframe)

    async def post_price_volume_multi(self, list_address: list[str], timeframe: str = BirdeyeHourTimeFrame.H24.value) -> PostPriceVolumeMultiResponse:
        """
            Call the Birdeye's **PRIVATE** API endpoint **[Price Volume - Multiple Token](https://docs.birdeye.so/reference/get_defi-price-volume-single)** for asynchronous logic. 
            All the API endopint details are available on [`Birdeye._post_price_volume_multi`][cyhole.birdeye.interaction.Birdeye._post_price_volume_multi].
        """
        return await self._interaction._post_price_volume_multi(False, list_address, timeframe)

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