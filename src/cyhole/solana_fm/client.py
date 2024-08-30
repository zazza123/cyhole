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
    GetTaggedTokensListResponse,
    GetTokenInfoV0Response,
    PostTokenMultipleInfoV0Response,
    GetTokenInfoV1Response,
    PostTokenMultipleInfoV1Response,
    PostUserTokenAccountsResponse,
    GetMintTokenAccountsResponse,
    GetOnChainTokenDataResponse,
    GetTokenSupplyResponse,
    GetTransferTransactionsResponse,
    PostMultipleTransferTransactionsResponse,
    GetAllTransferActionsResponse
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
            Call the SolanaFM's API endpoint GET **[Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return self._interaction._get_account_transactions(True, account, params)

    def get_account_transactions_fees(self, account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions_fees`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions_fees].
        """
        return self._interaction._get_account_transactions_fees(True, account, dt_from, dt_to)

    def get_account_transfers(self, account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers].
        """
        return self._interaction._get_account_transfers(True, account, params)

    def get_account_transfers_csv_export(self, account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** for synchronous logic. 
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
            Call the SolanaFM's API endpoint GET **[Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_blocks`][cyhole.solana_fm.interaction.SolanaFM._get_blocks].
        """
        return self._interaction._get_blocks(True, from_block, page_size, page_type, ascending)

    def get_block(self, block_number: int) -> GetBlockResponse:
        """
            Call the SolanaFM's API endpoint GET **[Block](https://docs.solana.fm/reference/get_block)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_block`][cyhole.solana_fm.interaction.SolanaFM._get_block].
        """
        return self._interaction._get_block(True, block_number)

    def post_multiple_blocks(self, block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse:
        """
            Call the SolanaFM's API endpoint POST **[Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_blocks`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_blocks].
        """
        return self._interaction._post_multiple_blocks(True, block_numbers, producer_details)

    def get_solana_daily_transaction_fees(self, dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse:
        """
            Call the SolanaFM's API endpoint GET **[Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_solana_daily_transaction_fees`][cyhole.solana_fm.interaction.SolanaFM._get_solana_daily_transaction_fees].
        """
        return self._interaction._get_solana_daily_transaction_fees(True, dt)

    def get_tagged_tokens_list(self) -> GetTaggedTokensListResponse:
        """
            Call the SolanaFM's API endpoint GET **[Tagged Tokens List](https://docs.solana.fm/reference/get_tokens_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_tagged_tokens_list`][cyhole.solana_fm.interaction.SolanaFM._get_tagged_tokens_list].
        """
        return self._interaction._get_tagged_tokens_list(True)

    def get_token_info_v0(self, address: str) -> GetTokenInfoV0Response:
        """
            Call the SolanaFM's API endpoint GET **[Token Info V0](https://docs.solana.fm/reference/get_token_by_account_hash)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_info_v0`][cyhole.solana_fm.interaction.SolanaFM._get_token_info_v0].
        """
        return self._interaction._get_token_info_v0(True, address)

    def post_token_multiple_info_v0(self, addresses: list[str]) -> PostTokenMultipleInfoV0Response:
        """
            Call the SolanaFM's API endpoint POST **[Token Multiple Info V0](https://docs.solana.fm/reference/get_tokens_by_account_hashes)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_token_multiple_info_v0`][cyhole.solana_fm.interaction.SolanaFM._post_token_multiple_info_v0].
        """
        return self._interaction._post_token_multiple_info_v0(True, addresses)

    def get_token_info_v1(self, address: str) -> GetTokenInfoV1Response:
        """
            Call the SolanaFM's API endpoint GET **[Token Info V1](https://docs.solana.fm/reference/get_one_token)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_info_v1`][cyhole.solana_fm.interaction.SolanaFM._get_token_info_v1].
        """
        return self._interaction._get_token_info_v1(True, address)

    def post_token_multiple_info_v1(self, addresses: list[str]) -> PostTokenMultipleInfoV1Response:
        """
            Call the SolanaFM's API endpoint POST **[Token Multiple Info V1](https://docs.solana.fm/reference/retrieve_multiple_tokens)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_token_multiple_info_v1`][cyhole.solana_fm.interaction.SolanaFM._post_token_multiple_info_v1].
        """
        return self._interaction._post_token_multiple_info_v1(True, addresses)

    def post_user_token_accounts(self, address: str, include_sol_balance: bool = False, tokens: list[str] | None = None) -> PostUserTokenAccountsResponse:
        """
            Call the SolanaFM's API endpoint POST **[User Token Accounts](https://docs.solana.fm/reference/get_user_token_accounts)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_user_token_accounts`][cyhole.solana_fm.interaction.SolanaFM._post_user_token_accounts].
        """
        return self._interaction._post_user_token_accounts(True, address, include_sol_balance, tokens)

    def get_mint_token_accounts(self, address: str, page: int | None = None, page_size: int | None = None) -> GetMintTokenAccountsResponse:
        """
            Call the SolanaFM's API endpoint GET **[Mint Token Accounts](https://docs.solana.fm/reference/get_token_accounts_for_token_mint)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_mint_token_accounts`][cyhole.solana_fm.interaction.SolanaFM._get_mint_token_accounts].
        """
        return self._interaction._get_mint_token_accounts(True, address, page, page_size)

    def get_on_chain_token_data(self, address: str) -> GetOnChainTokenDataResponse:
        """
            Call the SolanaFM's API endpoint GET **[On Chain Token Data](https://docs.solana.fm/reference/get_tfi_token_data)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_on_chain_token_data`][cyhole.solana_fm.interaction.SolanaFM._get_on_chain_token_data].
        """
        return self._interaction._get_on_chain_token_data(True, address)

    def get_token_supply(self, address: str) -> GetTokenSupplyResponse:
        """
            Call the SolanaFM's API endpoint GET **[Token Supply](https://docs.solana.fm/reference/get_token_circulating_supply)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_supply`][cyhole.solana_fm.interaction.SolanaFM._get_token_supply].
        """
        return self._interaction._get_token_supply(True, address)

    def get_transfer_transactions(self, transaction: str) -> GetTransferTransactionsResponse:
        """
            Call the SolanaFM's API endpoint GET **[Transfer Transactions](https://docs.solana.fm/reference/get_transfers)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_transfer_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_transfer_transactions].
        """
        return self._interaction._get_transfer_transactions(True, transaction)

    def post_multiple_transfer_transactions(self, transactions: list[str]) -> PostMultipleTransferTransactionsResponse:
        """
            Call the SolanaFM's API endpoint POST **[Multiple Transfer Transactions](https://docs.solana.fm/reference/post_transfers)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_transfer_transactions`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_transfer_transactions].
        """
        return self._interaction._post_multiple_transfer_transactions(True, transactions)

    def get_all_transfer_actions(self) -> GetAllTransferActionsResponse:
        """
            Call the SolanaFM's API endpoint GET **[All Transfer Actions](https://docs.solana.fm/reference/get_actions)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_all_transfer_actions`][cyhole.solana_fm.interaction.SolanaFM._get_all_transfer_actions].
        """
        return self._interaction._get_all_transfer_actions(True)

class SolanaFMAsyncClient(AsyncAPIClient):
    """
        Client used for asynchronous API calls for `SolanaFM` interaction.
    """

    def __init__(self, interaction: SolanaFM, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: SolanaFM = self._interaction

    async def get_account_transactions(self, account: str, params: GetAccountTransactionsParam = GetAccountTransactionsParam()) -> GetAccountTransactionsResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transactions](https://docs.solana.fm/reference/get_account_transactions)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions].
        """
        return await self._interaction._get_account_transactions(False, account, params)

    async def get_account_transactions_fees(self, account: str, dt_from: datetime | None = None, dt_to: datetime | None = None) -> GetAccountTransactionsFeesResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transactions Fees](https://docs.solana.fm/reference/get_account_tx_fees)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transactions_fees`][cyhole.solana_fm.interaction.SolanaFM._get_account_transactions_fees].
        """
        return await self._interaction._get_account_transactions_fees(False, account, dt_from, dt_to)

    async def get_account_transfers(self, account: str, params: GetAccountTransfersParam = GetAccountTransfersParam()) -> GetAccountTransfersResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transfers](https://docs.solana.fm/reference/get_account_transfers_v1)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_account_transfers`][cyhole.solana_fm.interaction.SolanaFM._get_account_transfers].
        """
        return await self._interaction._get_account_transfers(False, account, params)

    async def get_account_transfers_csv_export(self, account: str, params: GetAccountTransfersCsvExportParam = GetAccountTransfersCsvExportParam()) -> GetAccountTransfersCsvExportResponse:
        """
            Call the SolanaFM's API endpoint GET **[Account Transfers CSV Export](https://docs.solana.fm/reference/download_csv_v1)** for asynchronous logic. 
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
            Call the SolanaFM's API endpoint GET **[Blocks](https://docs.solana.fm/reference/get_blocks_by_pagination)** for synchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_blocks`][cyhole.solana_fm.interaction.SolanaFM._get_blocks].
        """
        return await self._interaction._get_blocks(False, from_block, page_size, page_type, ascending)

    async def get_block(self, block_number: int) -> GetBlockResponse:
        """
            Call the SolanaFM's API endpoint GET **[Block](https://docs.solana.fm/reference/get_block)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_block`][cyhole.solana_fm.interaction.SolanaFM._get_block].
        """
        return await self._interaction._get_block(False, block_number)

    async def post_multiple_blocks(self, block_numbers: list[int], producer_details: bool = True) -> PostMultipleBlocksResponse:
        """
            Call the SolanaFM's API endpoint POST **[Multiple Blocks](https://docs.solana.fm/reference/get_multiple_blocks)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_blocks`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_blocks].
        """
        return await self._interaction._post_multiple_blocks(False, block_numbers, producer_details)

    async def get_solana_daily_transaction_fees(self, dt: datetime = datetime.now()) -> GetSolanaDailyTransactionFeesResponse:
        """
            Call the SolanaFM's API endpoint GET **[Solana Daily Transaction Fees](https://docs.solana.fm/reference/get_daily_tx_fees)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_solana_daily_transaction_fees`][cyhole.solana_fm.interaction.SolanaFM._get_solana_daily_transaction_fees].
        """
        return await self._interaction._get_solana_daily_transaction_fees(False, dt)

    async def get_tagged_tokens_list(self) -> GetTaggedTokensListResponse:
        """
            Call the SolanaFM's API endpoint GET **[Tagged Tokens List](https://docs.solana.fm/reference/get_tokens_by_pagination)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_tagged_tokens_list`][cyhole.solana_fm.interaction.SolanaFM._get_tagged_tokens_list].
        """
        return await self._interaction._get_tagged_tokens_list(False)

    async def get_token_info_v0(self, address: str) -> GetTokenInfoV0Response:
        """
            Call the SolanaFM's API endpoint GET **[Token Info V0](https://docs.solana.fm/reference/get_token_by_account_hash)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_info_v0`][cyhole.solana_fm.interaction.SolanaFM._get_token_info_v0].
        """
        return await self._interaction._get_token_info_v0(False, address)

    async def post_token_multiple_info_v0(self, addresses: list[str]) -> PostTokenMultipleInfoV0Response:
        """
            Call the SolanaFM's API endpoint POST **[Token Multiple Info V0](https://docs.solana.fm/reference/get_tokens_by_account_hashes)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_token_multiple_info_v0`][cyhole.solana_fm.interaction.SolanaFM._post_token_multiple_info_v0].
        """
        return await self._interaction._post_token_multiple_info_v0(False, addresses)

    async def get_token_info_v1(self, address: str) -> GetTokenInfoV1Response:
        """
            Call the SolanaFM's API endpoint GET **[Token Info V1](https://docs.solana.fm/reference/get_one_token)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_info_v1`][cyhole.solana_fm.interaction.SolanaFM._get_token_info_v1].
        """
        return await self._interaction._get_token_info_v1(False, address)

    async def post_token_multiple_info_v1(self, addresses: list[str]) -> PostTokenMultipleInfoV1Response:
        """
            Call the SolanaFM's API endpoint POST **[Token Multiple Info V1](https://docs.solana.fm/reference/retrieve_multiple_tokens)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_token_multiple_info_v1`][cyhole.solana_fm.interaction.SolanaFM._post_token_multiple_info_v1].
        """
        return await self._interaction._post_token_multiple_info_v1(False, addresses)

    async def post_user_token_accounts(self, address: str, include_sol_balance: bool = False, tokens: list[str] | None = None) -> PostUserTokenAccountsResponse:
        """
            Call the SolanaFM's API endpoint POST **[User Token Accounts](https://docs.solana.fm/reference/get_user_token_accounts)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_user_token_accounts`][cyhole.solana_fm.interaction.SolanaFM._post_user_token_accounts].
        """
        return await self._interaction._post_user_token_accounts(False, address, include_sol_balance, tokens)

    async def get_mint_token_accounts(self, address: str, page: int | None = None, page_size: int | None = None) -> GetMintTokenAccountsResponse:
        """
            Call the SolanaFM's API endpoint GET **[Mint Token Accounts](https://docs.solana.fm/reference/get_token_accounts_for_token_mint)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_mint_token_accounts`][cyhole.solana_fm.interaction.SolanaFM._get_mint_token_accounts].
        """
        return await self._interaction._get_mint_token_accounts(False, address, page, page_size)

    async def get_on_chain_token_data(self, address: str) -> GetOnChainTokenDataResponse:
        """
            Call the SolanaFM's API endpoint GET **[On Chain Token Data](https://docs.solana.fm/reference/get_tfi_token_data)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_on_chain_token_data`][cyhole.solana_fm.interaction.SolanaFM._get_on_chain_token_data].
        """
        return await self._interaction._get_on_chain_token_data(False, address)

    async def get_token_supply(self, address: str) -> GetTokenSupplyResponse:
        """
            Call the SolanaFM's API endpoint GET **[Token Supply](https://docs.solana.fm/reference/get_token_circulating_supply)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_token_supply`][cyhole.solana_fm.interaction.SolanaFM._get_token_supply].
        """
        return await self._interaction._get_token_supply(False, address)

    async def get_transfer_transactions(self, transaction: str) -> GetTransferTransactionsResponse:
        """
            Call the SolanaFM's API endpoint GET **[Transfer Transactions](https://docs.solana.fm/reference/get_transfers)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_transfer_transactions`][cyhole.solana_fm.interaction.SolanaFM._get_transfer_transactions].
        """
        return await self._interaction._get_transfer_transactions(False, transaction)

    async def post_multiple_transfer_transactions(self, transactions: list[str]) -> PostMultipleTransferTransactionsResponse:
        """
            Call the SolanaFM's API endpoint POST **[Multiple Transfer Transactions](https://docs.solana.fm/reference/post_transfers)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._post_multiple_transfer_transactions`][cyhole.solana_fm.interaction.SolanaFM._post_multiple_transfer_transactions].
        """
        return await self._interaction._post_multiple_transfer_transactions(False, transactions)

    async def get_all_transfer_actions(self) -> GetAllTransferActionsResponse:
        """
            Call the SolanaFM's API endpoint GET **[All Transfer Actions](https://docs.solana.fm/reference/get_actions)** for asynchronous logic. 
            All the API endopint details are available on [`SolanaFM._get_all_transfer_actions`][cyhole.solana_fm.interaction.SolanaFM._get_all_transfer_actions].
        """
        return await self._interaction._get_all_transfer_actions(False)