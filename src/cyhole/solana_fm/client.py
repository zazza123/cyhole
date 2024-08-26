from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
from ..solana_fm.param import SolanaFMBlocksPaginationType
from ..solana_fm.schema import (
    GetAccountTransactionsParam,
    GetAccountTransactionsResponse,
    GetAccountTransfersParam,
    GetAccountTransfersResponse,
    GetAccountTransfersCsvExportParam,
    GetAccountTransfersCsvExportResponse,
    GetAccountTransactionsFeesResponse,
    GetBlocksResponse,
    GetBlockResponse,
    PostMultipleBlocksResponse,
    GetSolanaDailyTransactionFeesResponse,
    GetTaggedTokensListResponse
)

if TYPE_CHECKING:
    from ..solana_fm.interaction import SolanaFM

class SolanaFMClient(APIClient):
    """
        Client used for synchronous API calls for `SolanaFM` interaction.
    """

    def __init__(self, interaction: SolanaFM, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: SolanaFM = self._interaction

    def get_account_transactions(self, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, params)

    def get_account_transactions_fees(self, account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions_fees`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions_fees].
        """
        return self._interaction._get_account_transactions_fees(True, account, dt_from, dt_to)

    def get_account_transfers(self, account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers].
        """
        return self._interaction._get_account_transfers(True, account, params)

    def get_account_transfers_csv_export(self, account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers_csv_export`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers_csv_export].
        """
        return self._interaction._get_account_transfers_csv_export(True, account, params)

    def get_blocks(
        self,
        from_block: int | None = None,
        page_size: int = 50,
        page_type: str = SolanaFMBlocksPaginationType.BLOCK_NUMBER.value,
        ascending: bool | None = None
    ) -> GetBlocksResponse:
        """
            Call the SolanaFM's API endpoint **[Get Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_blocks`][cyhole.solana_fm.interaction.SolanaFM._get_blocks].
        """
        return self._interaction._get_blocks(True, from_block, page_size, page_type, ascending)

    def get_block(self, block_number: int) -> GetBlockResponse:
        """
            Call the SolanaFM's API endpoint **[Get Block](https://docs.solana.fm/reference/get_block)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_block`][cyhole.solana_fm.interaction.SolanaFM._get_block].
        """
        return self._interaction._get_block(True, block_number)

    def post_multiple_blocks(self, block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse:
        """
            Call the SolanaFM's API endpoint **[Post Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_blocks`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_blocks].
        """
        return self._interaction._post_multiple_blocks(True, block_numbers, producer_details)

    def get_solana_daily_transaction_fees(self, dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse:
        """
            Call the SolanaFM's API endpoint **[Get Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_solana_daily_transaction_fees`][cyhole.solana_fm.interaction.SolanaFM._get_solana_daily_transaction_fees].
        """
        return self._interaction._get_solana_daily_transaction_fees(True, dt)

    def get_tagged_tokens_list(self) -> GetTaggedTokensListResponse:
        """
            Call the SolanaFM's API endpoint **[Get Tagged Tokens List](https://docs.solana.fm/reference/get_tokens_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_tagged_tokens_list`][cyhole.solana_fm.interaction.SolanaFM._get_tagged_tokens_list].
        """
        return self._interaction._get_tagged_tokens_list(True)

class SolanaFMAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `SolanaFM` interaction.
    """

    def __init__(self, interaction: SolanaFM, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: SolanaFM = self._interaction

    async def get_account_transactions(self, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, params)

    async def get_account_transactions_fees(self, account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions_fees`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions_fees].
        """
        return await self._interaction._get_account_transactions_fees(False, account, dt_from, dt_to)

    async def get_account_transfers(self, account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers].
        """
        return await self._interaction._get_account_transfers(False, account, params)

    async def get_account_transfers_csv_export(self, account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse:
        """
            Call the SolanaFM's API endpoint **[Get Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers_csv_export`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers_csv_export].
        """
        return await self._interaction._get_account_transfers_csv_export(False, account, params)

    async def get_blocks(
        self,
        from_block: int | None = None,
        page_size: int = 50,
        page_type: str = SolanaFMBlocksPaginationType.BLOCK_NUMBER.value,
        ascending: bool | None = None
    ) -> GetBlocksResponse:
        """
            Call the SolanaFM's API endpoint **[Get Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_blocks`][cyhole.solana_fm.interaction.SolanaFM._get_blocks].
        """
        return await self._interaction._get_blocks(False, from_block, page_size, page_type, ascending)

    async def get_block(self, block_number: int) -> GetBlockResponse:
        """
            Call the SolanaFM's API endpoint **[Get Block](https://docs.solana.fm/reference/get_block)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_block`][cyhole.solana_fm.interaction.SolanaFM._get_block].
        """
        return await self._interaction._get_block(False, block_number)

    async def post_multiple_blocks(self, block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse:
        """
            Call the SolanaFM's API endpoint **[Post Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_blocks`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_blocks].
        """
        return await self._interaction._post_multiple_blocks(False, block_numbers, producer_details)

    async def get_solana_daily_transaction_fees(self, dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse:
        """
            Call the SolanaFM's API endpoint **[Get Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_solana_daily_transaction_fees`][cyhole.solana_fm.interaction.SolanaFM._get_solana_daily_transaction_fees].
        """
        return await self._interaction._get_solana_daily_transaction_fees(False, dt)

    async def get_tagged_tokens_list(self) -> GetTaggedTokensListResponse:
        """
            Call the SolanaFM's API endpoint **[Get Tagged Tokens List](https://docs.solana.fm/reference/get_tokens_by_pagination)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_tagged_tokens_list`][cyhole.solana_fm.interaction.SolanaFM._get_tagged_tokens_list].
        """
        return await self._interaction._get_tagged_tokens_list(False)
