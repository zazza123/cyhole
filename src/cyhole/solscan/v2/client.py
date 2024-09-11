from __future__ import annotations
from datetime import datetime
from requests import Response, HTTPError
from typing import TYPE_CHECKING, Any, cast

from ...core.client import APIClient, AsyncAPIClient
from ...solscan.v2.param import (
    SolscanTransactionFilterType,
    SolscanReturnLimitType,
    SolscanNFTItemSortType,
    SolscanNFTPageSizeType,
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
    GetTokenMetaResponse,
    GetNFTNewsResponse,
    GetNFTActivitiesParam,
    GetNFTActivitiesResponse,
    GetNFTCollectionListsParam,
    GetNFTCollectionListsResponse,
    GetNFTCollectionItemsResponse,
    GetTransactionLastResponse,
    GetTransactionActionsResponse,
    GetBlockLastResponse,
    GetBlockTransactionsResponse,
    GetBlockDetailResponse
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

    def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> Response:
        # overide function to manage client specific exceptions
        try:
            return super().api(type, url, *args, **kwargs)
        except HTTPError as e:
            raise self._interaction._raise(e)

    def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.v2.interaction.Solscan._get_account_transfers].
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
            All the API endopint details are available on [`Solscan._get_account_token_nft_account`][cyhole.solscan.v2.interaction.Solscan._get_account_token_nft_account].
        """
        return self._interaction._get_account_token_nft_account(True, account, account_type, page, page_size, hide_zero)

    def get_account_defi_activities(self, account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_defi_activities`][cyhole.solscan.v2.interaction.Solscan._get_account_defi_activities].
        """
        return self._interaction._get_account_defi_activities(True, account, params)

    def get_account_balance_change_activities(self, account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_balance_change_activities`][cyhole.solscan.v2.interaction.Solscan._get_account_balance_change_activities].
        """
        return self._interaction._get_account_balance_change_activities(True, account, params)

    def get_account_transactions(self, account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.v2.interaction.Solscan._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, before_transaction, limit)

    def get_account_stake(self, account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake`][cyhole.solscan.v2.interaction.Solscan._get_account_stake].
        """
        return self._interaction._get_account_stake(True, account, page, limit)

    def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.v2.interaction.Solscan._get_account_detail].
        """
        return self._interaction._get_account_detail(True, account)

    def get_account_rewards_export(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Rewards Export](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_rewards_export`][cyhole.solscan.v2.interaction.Solscan._get_account_rewards_export].
        """
        return self._interaction._get_account_rewards_export(True, account, dt_from, dt_to)

    def get_token_transfer(self, token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.v2.interaction.Solscan._get_token_transfer].
        """
        return self._interaction._get_token_transfer(True, token, params)

    def get_token_defi_activities(self, token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_defi_activities`][cyhole.solscan.v2.interaction.Solscan._get_token_defi_activities].
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
            All the API endopint details are available on [`Solscan._get_token_markets`][cyhole.solscan.v2.interaction.Solscan._get_token_markets].
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
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.v2.interaction.Solscan._get_token_list].
        """
        return self._interaction._get_token_list(True, sort_by, order_by, page, page_size)

    def get_token_trending(self, limit: int = 10) -> GetTokenTrendingResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_trending`][cyhole.solscan.v2.interaction.Solscan._get_token_trending].
        """
        return self._interaction._get_token_trending(True, limit)

    def get_token_price(self, token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_price`][cyhole.solscan.v2.interaction.Solscan._get_token_price].
        """
        return self._interaction._get_token_price(True, token, time_range)

    def get_token_holders(self, token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.v2.interaction.Solscan._get_token_holders].
        """
        return self._interaction._get_token_holders(True, token, amount_range, page, page_size)

    def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.v2.interaction.Solscan._get_token_meta].
        """
        return self._interaction._get_token_meta(True, token)

    def get_nft_news(self, filter: str = "created_time", page: int = 1, page_size: int = SolscanNFTPageSizeType.SIZE_12.value) -> GetNFTNewsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT News](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-news)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_news`][cyhole.solscan.v2.interaction.Solscan._get_nft_news].
        """
        return self._interaction._get_nft_news(True, filter, page, page_size)

    def get_nft_activities(self, params: GetNFTActivitiesParam = GetNFTActivitiesParam()) -> GetNFTActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_activities`][cyhole.solscan.v2.interaction.Solscan._get_nft_activities].
        """
        return self._interaction._get_nft_activities(True, params)

    def get_nft_collection_lists(self, params: GetNFTCollectionListsParam = GetNFTCollectionListsParam()) -> GetNFTCollectionListsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_collection_lists`][cyhole.solscan.v2.interaction.Solscan._get_nft_collection_lists].
        """
        return self._interaction._get_nft_collection_lists(True, params)

    def get_nft_collection_items(
        self,
        collection: str,
        sort_by: str = SolscanNFTItemSortType.LAST_TRADE.value,
        page: int = 1,
        page_size: int = SolscanNFTPageSizeType.SIZE_12.value
    ) -> GetNFTCollectionItemsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Collection Items](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-items)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_collection_items`][cyhole.solscan.v2.interaction.Solscan._get_nft_collection_items].
        """
        return self._interaction._get_nft_collection_items(True, collection, sort_by, page, page_size)

    def get_transaction_last(self, limit: int = SolscanReturnLimitType.LIMIT_10.value, filter: str = SolscanTransactionFilterType.EXCEPT_VOTE.value) -> GetTransactionLastResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-last)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_last`][cyhole.solscan.v2.interaction.Solscan._get_transaction_last].
        """
        return self._interaction._get_transaction_last(True, limit, filter)

    def get_transaction_actions(self, transaction: str) -> GetTransactionActionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Transaction Actions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-actions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_actions`][cyhole.solscan.v2.interaction.Solscan._get_transaction_actions].
        """
        return self._interaction._get_transaction_actions(True, transaction)

    def get_block_last(self, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockLastResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-last)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_last`][cyhole.solscan.v2.interaction.Solscan._get_block_last].
        """
        return self._interaction._get_block_last(True, page_size)

    def get_block_transactions(self, block: int, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-transactions)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_transactions`][cyhole.solscan.v2.interaction.Solscan._get_block_transactions].
        """
        return self._interaction._get_block_transactions(True, block, page, page_size)

    def get_block_detail(self, block: int) -> GetBlockDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-detail)** for synchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_detail`][cyhole.solscan.v2.interaction.Solscan._get_block_detail].
        """
        return self._interaction._get_block_detail(True, block)

class SolscanAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `Solscan` interaction on **V2** API.
    """

    def __init__(self, interaction: Solscan, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction = cast('Solscan', self._interaction)

    async def api(self, type: str, url: str, *args: tuple, **kwargs: dict[str, Any]) -> Response:
        # overide function to manage client specific exceptions
        try:
            return await super().api(type, url, *args, **kwargs)
        except HTTPError as e:
            raise self._interaction._raise(e)

    async def get_account_transfers(self, account: str, params: GetAccountTransferParam = GetAccountTransferParam()) -> GetAccountTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transfers`][cyhole.solscan.v2.interaction.Solscan._get_account_transfers].
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
            All the API endopint details are available on [`Solscan._get_account_token_nft_account`][cyhole.solscan.v2.interaction.Solscan._get_account_token_nft_account].
        """
        return await self._interaction._get_account_token_nft_account(False, account, account_type, page, page_size, hide_zero)

    async def get_account_defi_activities(self, account: str, params: GetAccountDefiActivitiesParam = GetAccountDefiActivitiesParam()) -> GetAccountDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-defi-activities)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_defi_activities`][cyhole.solscan.v2.interaction.Solscan._get_account_defi_activities].
        """
        return await self._interaction._get_account_defi_activities(False, account, params)

    async def get_account_balance_change_activities(self, account: str, params: GetAccountBalanceChangeActivitiesParam = GetAccountBalanceChangeActivitiesParam()) -> GetAccountBalanceChangeActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Balance Change Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-balance_change)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_balance_change_activities`][cyhole.solscan.v2.interaction.Solscan._get_account_balance_change_activities].
        """
        return await self._interaction._get_account_balance_change_activities(False, account, params)

    async def get_account_transactions(self, account: str, before_transaction: str | None = None, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_transactions`][cyhole.solscan.v2.interaction.Solscan._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, before_transaction, limit)

    async def get_account_stake(self, account: str, page: int = 1, limit: int = SolscanReturnLimitType.LIMIT_10.value) -> GetAccountStakeResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Stake](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-stake)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_stake`][cyhole.solscan.v2.interaction.Solscan._get_account_stake].
        """
        return await self._interaction._get_account_stake(False, account, page, limit)

    async def get_account_detail(self, account: str) -> GetAccountDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_detail`][cyhole.solscan.v2.interaction.Solscan._get_account_detail].
        """
        return await self._interaction._get_account_detail(False, account)

    async def get_account_rewards_export(self, account: str, dt_from: datetime, dt_to: datetime) -> GetAccountRewardsExportResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Account Rewards Export](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-reward-export)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_account_rewards_export`][cyhole.solscan.v2.interaction.Solscan._get_account_rewards_export].
        """
        return await self._interaction._get_account_rewards_export(False, account, dt_from, dt_to)

    async def get_token_transfer(self, token: str, params: GetTokenTransferParam = GetTokenTransferParam()) -> GetTokenTransferResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Transfer](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-transfer)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_transfer`][cyhole.solscan.v2.interaction.Solscan._get_token_transfer].
        """
        return await self._interaction._get_token_transfer(False, token, params)

    async def get_token_defi_activities(self, token: str, params: GetTokenDefiActivitiesParam = GetTokenDefiActivitiesParam()) -> GetTokenDefiActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token DeFi Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-defi-activities)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_defi_activities`][cyhole.solscan.v2.interaction.Solscan._get_token_defi_activities].
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
            All the API endopint details are available on [`Solscan._get_token_markets`][cyhole.solscan.v2.interaction.Solscan._get_token_markets].
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
            All the API endopint details are available on [`Solscan._get_token_list`][cyhole.solscan.v2.interaction.Solscan._get_token_list].
        """
        return await self._interaction._get_token_list(False, sort_by, order_by, page, page_size)

    async def get_token_trending(self, limit: int = 10) -> GetTokenTrendingResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Trending](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-trending)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_trending`][cyhole.solscan.v2.interaction.Solscan._get_token_trending].
        """
        return await self._interaction._get_token_trending(False, limit)

    async def get_token_price(self, token: str, time_range: datetime | tuple[datetime, datetime] = datetime.now()) -> GetTokenPriceResponse:                
        """
            Call the Solscan's **V2** API endpoint GET **[Token Price](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-price)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_price`][cyhole.solscan.v2.interaction.Solscan._get_token_price].
        """
        return await self._interaction._get_token_price(False, token, time_range)

    async def get_token_holders(self, token: str, amount_range: tuple[int, int] | None = None, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetTokenHoldersResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Holders](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-holders)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_holders`][cyhole.solscan.v2.interaction.Solscan._get_token_holders].
        """
        return await self._interaction._get_token_holders(False, token, amount_range, page, page_size)

    async def get_token_meta(self, token: str) -> GetTokenMetaResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Token Meta](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-token-meta)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_token_meta`][cyhole.solscan.v2.interaction.Solscan._get_token_meta].
        """
        return await self._interaction._get_token_meta(False, token)

    async def get_nft_news(self, filter: str = "created_time", page: int = 1, page_size: int = SolscanNFTPageSizeType.SIZE_12.value) -> GetNFTNewsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT News](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-news)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_news`][cyhole.solscan.v2.interaction.Solscan._get_nft_news].
        """
        return await self._interaction._get_nft_news(False, filter, page, page_size)

    async def get_nft_activities(self, params: GetNFTActivitiesParam = GetNFTActivitiesParam()) -> GetNFTActivitiesResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Activities](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-activities)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_activities`][cyhole.solscan.v2.interaction.Solscan._get_nft_activities].
        """
        return await self._interaction._get_nft_activities(False, params)

    async def get_nft_collection_lists(self, params: GetNFTCollectionListsParam = GetNFTCollectionListsParam()) -> GetNFTCollectionListsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Collection Lists](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-lists)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_collection_lists`][cyhole.solscan.v2.interaction.Solscan._get_nft_collection_lists].
        """
        return await self._interaction._get_nft_collection_lists(False, params)

    async def get_nft_collection_items(
        self,
        collection: str,
        sort_by: str = SolscanNFTItemSortType.LAST_TRADE.value,
        page: int = 1,
        page_size: int = SolscanNFTPageSizeType.SIZE_12.value
    ) -> GetNFTCollectionItemsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[NFT Collection Items](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-nft-collection-items)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_nft_collection_items`][cyhole.solscan.v2.interaction.Solscan._get_nft_collection_items].
        """
        return await self._interaction._get_nft_collection_items(False, collection, sort_by, page, page_size)

    async def get_transaction_last(self, limit: int = SolscanReturnLimitType.LIMIT_10.value, filter: str = SolscanTransactionFilterType.EXCEPT_VOTE.value) -> GetTransactionLastResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Transaction Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-last)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_last`][cyhole.solscan.v2.interaction.Solscan._get_transaction_last].
        """
        return await self._interaction._get_transaction_last(False, limit, filter)

    async def get_transaction_actions(self, transaction: str) -> GetTransactionActionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Transaction Actions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-transaction-actions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_transaction_actions`][cyhole.solscan.v2.interaction.Solscan._get_transaction_actions].
        """
        return await self._interaction._get_transaction_actions(False, transaction)

    async def get_block_last(self, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockLastResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Last](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-last)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_last`][cyhole.solscan.v2.interaction.Solscan._get_block_last].
        """
        return await self._interaction._get_block_last(False, page_size)

    async def get_block_transactions(self, block: int, page: int = 1, page_size: int = SolscanPageSizeType.SIZE_10.value) -> GetBlockTransactionsResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Transactions](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-transactions)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_transactions`][cyhole.solscan.v2.interaction.Solscan._get_block_transactions].
        """
        return await self._interaction._get_block_transactions(False, block, page, page_size)

    async def get_block_detail(self, block: int) -> GetBlockDetailResponse:
        """
            Call the Solscan's **V2** API endpoint GET **[Block Detail](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-block-detail)** for asynchronous logic. 
            All the API endopint details are available on [`Solscan._get_block_detail`][cyhole.solscan.v2.interaction.Solscan._get_block_detail].
        """
        return await self._interaction._get_block_detail(False, block)