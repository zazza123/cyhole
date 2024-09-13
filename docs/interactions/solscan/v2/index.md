# :fontawesome-regular-circle-dot: - Solscan (v2 API)

Solscan ([https://solscan.io/](https://solscan.io/)) is one of the most widly used platform for analysing Solana blockchain. It robustness is provided by its API services that are easy to use and well documented. Currently, there are two versions of the API available, v1 and v2; this documentation covers the v2 API (see [here](../v1/index.md) for v1 API documentation).

The access to the API services is provided by an API key that can be obtained by creating an account on the Solscan platform, and purchasing the desired subscription. Official documentation can be accessed from [here](https://pro-api.solscan.io/pro-api-docs/v2.0).

The API connector is [`Solscan`](../v2/interaction.md) class imported from `cyhole.solscan.v2` path. The same connector can be imported from `SolscanV2` class available in `cyhole.solscan`.

## Quick Examples

### Get Latest SPL Transfers of an Account

Extract the latest incoming SPL transfers executed by an account on the Solana chian in few lines of code by using [`get_account_transfers`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_transfers) in **asynchronous** logic.

```py
import asyncio
from cyhole.solscan.v2 import Solscan
#from cyhole.solscan import SolscanV2 as Solscan
from cyhole.solscan.v2.schema import GetAccountTransferParam
from cyhole.solscan.v2.param import SolscanActivityTransferType, SolscanFlowType

account = "ACCOUNT_ID"

# set params
params = GetAccountTransferParam(
    activity_type = SolscanActivityTransferType.SPL_TRANSFER.value,
    flow_direction = SolscanFlowType.INCOMING.value
)

# extract latest transfers
async def main() -> None:
    solscan = Solscan()
    async with solscan.async_client as client:
        response = await client.get_account_transfers(account, params = params)
        print("Transfers Extracted:", len(response.data))

asyncio.run(main())
```

!!! note
    To run this example is assumed that the user has a valid API key stored in `SOLSCAN_API_V2_KEY` environment variable.  
    If the key is not provided during the object creations, then the library will raise an exception.

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.solscan.v2` - Explore the [`Solscan`](../v2/interaction.md) v2 API connector and all its methods. 

    [:octicons-arrow-right-24: Reference](../v2/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.solscan.v2.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../v2/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.solscan.v2.schema` - Extract only what is necessary by exploiting reponse mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../v2/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.solscan.v2.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../v2/exception.md)

</div>

## Endpoints

| Endpoint  | Type      | Method    | `cyhole` Release  | Deprecated    |
| ---       | ---       | ---       | ---               | ---           |
| Account Transfer | `GET` | [`get_account_transfers`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_transfers) | `0.2.3` | - |
| Account Transfer | `GET` | [`get_account_transfers`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_transfers) | `0.2.3` | - |
| Account Token NFT Account | `GET` | [`get_account_token_nft_account`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_token_nft_account) | `0.2.3` | - |
| Account Defi Activities | `GET` | [`get_account_defi_activities`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_defi_activities) | `0.2.3` | - |
| Account Balance Change Activities | `GET` | [`get_account_balance_change_activities`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_balance_change_activities) | `0.2.3` | - |
| Account Transactions | `GET` | [`get_account_transactions`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_transactions) | `0.2.3` | - |
| Account Stake | `GET` | [`get_account_stake`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_stake) | `0.2.3` | - |
| Account Detail | `GET` | [`get_account_detail`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_detail) | `0.2.3` | - |
| Account Rewards Export | `GET` | [`get_account_rewards_export`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_account_rewards_export) | `0.2.3` | - |
| Token Transfer | `GET` | [`get_token_transfer`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_transfer) | `0.2.3` | - |
| Token DeFi Activities | `GET` | [`get_token_defi_activities`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_defi_activities) | `0.2.3` | - |
| Token Markets | `GET` | [`get_token_markets`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_markets) | `0.2.3` | - |
| Token List | `GET` | [`get_token_list`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_list) | `0.2.3` | - |
| Token Trending | `GET` | [`get_token_trending`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_trending) | `0.2.3` | - |
| Token Price | `GET` | [`get_token_price`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_price) | `0.2.3` | - |
| Token Holders | `GET` | [`get_token_holders`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_holders) | `0.2.3` | - |
| Token Meta | `GET` | [`get_token_meta`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_token_meta) | `0.2.3` | - |
| NFT News | `GET` | [`get_nft_news`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_nft_news) | `0.2.3` | - |
| NFT Activities | `GET` | [`get_nft_activities`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_nft_activities) | `0.2.3` | - |
| NFT Collection Lists | `GET` | [`get_nft_collection_lists`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_nft_collection_lists) | `0.2.3` | - |
| NFT Collection Items | `GET` | [`get_nft_collection_items`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_nft_collection_items) | `0.2.3` | - |
| Transaction Last | `GET` | [`get_transaction_last`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_transaction_last) | `0.2.3` | - |
| Transaction Actions | `GET` | [`get_transaction_actions`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_transaction_actions) | `0.2.3` | - |
| Block Last | `GET` | [`get_block_last`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_block_last) | `0.2.3` | - |
| Block Transactions | `GET` | [`get_block_transactions`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_block_transactions) | `0.2.3` | - |
| Block Detail | `GET` | [`get_block_detail`](../v2/interaction.md#cyhole.solscan.v2.Solscan._get_block_detail) | `0.2.3` | - |