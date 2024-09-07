from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient
from ...solscan.v2.param import (
    SolscanReturnLimitType,
    SolscanPageSizeType,
    SolscanOrderType,
    SolscanSortType
)
from ...solscan.v2.schema import (
    GetAccountTransferParam,
    GetAccountTransferResponse,
    GetAccountTokenNFTAccountResponse,
    GetAccountDefiActivitiesParam,
    GetAccountDefiActivitiesResponse,
    GetAccountBalanceChangeActivitiesParam,
    GetAccountBalanceChangeActivitiesResponse,
    GetAccountTransactionsResponse,
    GetAccountStakeResponse,
    GetAccountDetailResponse,
    GetAccountRewardsExportResponse,
    GetTokenTransferParam,
    GetTokenTransferResponse,
    GetTokenDefiActivitiesParam,
    GetTokenDefiActivitiesResponse,
    GetTokenMarketsResponse,
    GetTokenListResponse,
    GetTokenTrendingResponse,
    GetTokenPriceResponse,
    GetTokenHoldersResponse,
    GetTokenMetaResponse
)

if TYPE_CHECKING:
    from ...solscan.v2.interaction import Solscan

class SolscanClient(APIClient):
    """
        Client used for synchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.interaction.v2.Solscan._get_account_transfers].
        """
        return self._interaction._get_account_transfers(True, account, params)

    def get_account_token_nft_account(
        self, 
        account: str,
        account_type: str,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value,
        hide_zero: bool = True
    ) -> GetAccountTokenNFTAccountResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Token/NFT Account](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-token-accounts)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_token_nft_account`][cyhole.solscan.interaction.v2.Solscan._get_account_token_nft_account].
        """
        return self._interaction._get_account_token_nft_account(True, account, account_type, page, page_size, hide_zero)

    def get_account_defi_activities(self, account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_defi_activities`][cyhole.solscan.interaction.v2.Solscan._get_account_defi_activities].
        """
        return self._interaction._get_account_defi_activities(True, account, params)

    def get_account_balance_change_activities(self, account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_balance_change_activities`][cyhole.solscan.interaction.v2.Solscan._get_account_balance_change_activities].
        """
        return self._interaction._get_account_balance_change_activities(True, account, params)

    def get_account_transactions(self, account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.interaction.v2.Solscan._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, before_transaction, limit)

    def get_account_stake(self, account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake`][cyhole.solscan.interaction.v2.Solscan._get_account_stake].
        """
        return self._interaction._get_account_stake(True, account, page, limit)

    def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.interaction.v2.Solscan._get_account_detail].
        """
        return self._interaction._get_account_detail(True, account)

    def get_account_rewards_export(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Rewards Export](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_rewards_export`][cyhole.solscan.interaction.v2.Solscan._get_account_rewards_export].
        """
        return self._interaction._get_account_rewards_export(True, account, dt_from, dt_to)

    def get_token_transfer(self, token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.interaction.v2.Solscan._get_token_transfer].
        """
        return self._interaction._get_token_transfer(True, token, params)

    def get_token_defi_activities(self, token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_defi_activities`][cyhole.solscan.interaction.v2.Solscan._get_token_defi_activities].
        """
        return self._interaction._get_token_defi_activities(True, token, params)

    def get_token_markets(
        self,
        tokens: str | list[str],
        program_address: str | list[str] | None  = None,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenMarketsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Markets](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-markets)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_markets`][cyhole.solscan.interaction.v2.Solscan._get_token_markets].
        """
        return self._interaction._get_token_markets(True, tokens, program_address, page, page_size)

    def get_token_list(
        self,
        sort_by: str = SolscanSortType.MARKET_CAP.value,
        order_by: str = SolscanOrderType.DESCENDING.value,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenListResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-list)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.interaction.v2.Solscan._get_token_list].
        """
        return self._interaction._get_token_list(True, sort_by, order_by, page, page_size)

    def get_token_trending(self, limit: int = 10) -> GetTokenTrendingResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_trending`][cyhole.solscan.interaction.v2.Solscan._get_token_trending].
        """
        return self._interaction._get_token_trending(True, limit)

    def get_token_price(self, token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_price`][cyhole.solscan.interaction.v2.Solscan._get_token_price].
        """
        return self._interaction._get_token_price(True, token, time_range)

    def get_token_holders(self, token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.interaction.v2.Solscan._get_token_holders].
        """
        return self._interaction._get_token_holders(True, token, amount_range, page, page_size)

    def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.interaction.v2.Solscan._get_token_meta].
        """
        return self._interaction._get_token_meta(True, token)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.interaction.v2.Solscan._get_account_transfers].
        """
        return await self._interaction._get_account_transfers(False, account, params)

    async def get_account_token_nft_account(
        self, 
        account: str,
        account_type: str,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value,
        hide_zero: bool = True
    ) -> GetAccountTokenNFTAccountResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Token/NFT Account](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-token-accounts)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_token_nft_account`][cyhole.solscan.interaction.v2.Solscan._get_account_token_nft_account].
        """
        return await self._interaction._get_account_token_nft_account(False, account, account_type, page, page_size, hide_zero)

    async def get_account_defi_activities(self, account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_defi_activities`][cyhole.solscan.interaction.v2.Solscan._get_account_defi_activities].
        """
        return await self._interaction._get_account_defi_activities(False, account, params)

    async def get_account_balance_change_activities(self, account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_balance_change_activities`][cyhole.solscan.interaction.v2.Solscan._get_account_balance_change_activities].
        """
        return await self._interaction._get_account_balance_change_activities(False, account, params)

    async def get_account_transactions(self, account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.interaction.v2.Solscan._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, before_transaction, limit)

    async def get_account_stake(self, account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake`][cyhole.solscan.interaction.v2.Solscan._get_account_stake].
        """
        return await self._interaction._get_account_stake(False, account, page, limit)

    async def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.interaction.v2.Solscan._get_account_detail].
        """
        return await self._interaction._get_account_detail(False, account)

    async def get_account_rewards_export(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Rewards Export](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_rewards_export`][cyhole.solscan.interaction.v2.Solscan._get_account_rewards_export].
        """
        return await self._interaction._get_account_rewards_export(False, account, dt_from, dt_to)

    async def get_token_transfer(self, token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.interaction.v2.Solscan._get_token_transfer].
        """
        return await self._interaction._get_token_transfer(False, token, params)

    async def get_token_defi_activities(self, token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_defi_activities`][cyhole.solscan.interaction.v2.Solscan._get_token_defi_activities].
        """
        return await self._interaction._get_token_defi_activities(False, token, params)

    async def get_token_markets(
        self,
        tokens: str | list[str],
        program_address: str | list[str] | None  = None,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenMarketsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Markets](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-markets)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_markets`][cyhole.solscan.interaction.v2.Solscan._get_token_markets].
        """
        return await self._interaction._get_token_markets(False, tokens, program_address, page, page_size)

    async def get_token_list(
        self,
        sort_by: str = SolscanSortType.MARKET_CAP.value,
        order_by: str = SolscanOrderType.DESCENDING.value,
        page: int = 1,
        page_size: int = SolscanPageSizeType.SIZE_10.value
    ) -> GetTokenListResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token List](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-list)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.interaction.v2.Solscan._get_token_list].
        """
        return await self._interaction._get_token_list(False, sort_by, order_by, page, page_size)

    async def get_token_trending(self, limit: int = 10) -> GetTokenTrendingResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_trending`][cyhole.solscan.interaction.v2.Solscan._get_token_trending].
        """
        return await self._interaction._get_token_trending(False, limit)

    async def get_token_price(self, token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse:                
        """
            Call the Solscan's **V2** API endpoint GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_price`][cyhole.solscan.interaction.v2.Solscan._get_token_price].
        """
        return await self._interaction._get_token_price(False, token, time_range)

    async def get_token_holders(self, token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.interaction.v2.Solscan._get_token_holders].
        """
        return await self._interaction._get_token_holders(False, token, amount_range, page, page_size)

    async def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.interaction.v2.Solscan._get_token_meta].
        """
        return await self._interaction._get_token_meta(False, token)