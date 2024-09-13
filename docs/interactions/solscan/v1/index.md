# :fontawesome-regular-circle-dot: - Solscan (v1 API)

Solscan ([https://solscan.io/](https://solscan.io/)) is one of the most widly used platform for analysing Solana blockchain. It robustness is provided by its API services that are easy to use and well documented. Currently, there are two versions of the API available, v1 and v2; **this documentation covers the v1 API** (see [here](../v2/index.md) for v2 API documentation).

The access to the API services is provided by an API key that can be obtained by creating an account on the Solscan platform, and purchasing the desired subscription. Official documentation can be accessed from [here](https://pro-api.solscan.io/pro-api-docs/v2.0).

The API connector is [`Solscan`](../v1/interaction.md) class imported from `cyhole.solscan.v1` path. The same connector can be imported from `SolscanV1` class available in `cyhole.solscan`.

## Quick Examples

### Get Tokens Accounts of an Account

Extract the list of tokens accounts associate to an account on the Solana chian in few lines of code by using [`get_account_tokens`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_tokens) in **synchronous** logic.

```py
from cyhole.solscan.v1 import Solscan
#from cyhole.solscan import SolscanV1 as Solscan

account = "ACCOUNT_ID"

# extract tokens account transfers
solscan = Solscan()
response = solscan.client.get_account_tokens(account)
print("Tokens Accounts Extracted:", len(response.tokens))
```

!!! note
    To run this example is assumed that the user has a valid API key stored in `SOLSCAN_API_V1_KEY` environment variable.  
    If the key is not provided during the object creations, then the library will raise an exception.

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.solscan.v1` - Explore the [`Solscan`](../v1/interaction.md) v1 API connector and all its methods. 

    [:octicons-arrow-right-24: Reference](../v1/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.solscan.v1.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../v1/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.solscan.v1.schema` - Extract only what is necessary by exploiting reponse mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../v1/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.solscan.v1.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../v1/exception.md)

</div>

## Endpoints

| Endpoint  | Type      | Method    | `cyhole` Release  | Deprecated    |
| ---       | ---       | ---       | ---               | ---           |
| Account Tokens | `GET` | [`get_account_tokens`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_tokens) | `0.2.3` | - |
| Account Transactions | `GET` | [`get_account_transactions`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_transactions) | `0.2.3` | - |
| Account StakeAccounts | `GET` | [`get_account_stake_accounts`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_stake_accounts) | `0.2.3` | - |
| Account Spl Transfers | `GET` | [`get_account_spl_transfers`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_spl_transfers) | `0.2.3` | - |
| Account Sol Transfers | `GET` | [`get_account_sol_transfers`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_sol_transfers) | `0.2.3` | - |
| Account Export Transactions | `GET` | [`get_account_export_transactions`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_export_transactions) | `0.2.3` | - |
| Account Export Rewards | `GET` | [`get_account_export_rewards`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_export_rewards) | `0.2.3` | - |
| Account Detail | `GET` | [`get_account_detail`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_account_detail) | `0.2.3` | - |
| Token Holders | `GET` | [`get_token_holders`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_token_holders) | `0.2.3` | - |
| Token Meta | `GET` | [`get_token_meta`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_token_meta) | `0.2.3` | - |
| Token Transfer | `GET` | [`get_token_transfer`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_token_transfer) | `0.2.3` | - |
| Token List | `GET` | [`get_token_list`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_token_list) | `0.2.3` | - |
| Market Token Detail | `GET` | [`get_market_token_detail`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_market_token_detail) | `0.2.3` | - |
| Transaction Last | `GET` | [`get_transaction_last`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_transaction_last) | `0.2.3` | - |
| Transaction Detail | `GET` | [`get_transaction_detail`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_transaction_detail) | `0.2.3` | - |
| Block Last | `GET` | [`get_block_last`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_block_last) | `0.2.3` | - |
| Block Detail | `GET` | [`get_block_detail`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_block_detail) | `0.2.3` | - |
| Block Transactions | `GET` | [`get_block_transactions`](../v1/interaction.md#cyhole.solscan.v1.Solscan._get_block_transactions) | `0.2.3` | - |