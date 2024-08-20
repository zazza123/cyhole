# :simple-airplayaudio: - SolanaFM

SolanaFM ([https://solana.fm/](https://solana.fm/)) is a platform that provides a wide range of services for Solana blockchain, including on-chain exploration, API integration, and analytics. The services are designed to be user-friendly and easy to use, with free access to their APIs for developers. The documentation is well written and can be access from [here](https://docs.solana.fm/).

The API connector is [`SolanaFM`](../solana_fm/interaction.md) class imported from `cyhole.solana_fm` path.

## Quick Examples

### Get Latest Transactions of an Account

Extract the latest transactions executed by an account on the Solana chian in few lines of code by using [`get_account_transactions`](../solana_fm/interaction.md#cyhole.solana_fm.SolanaFM._get_account_transactions) in **asynchronous** logic.

```py
import asyncio
from cyhole.solana_fm import SolanaFM

account = "ACCOUNT_ID"

# extract latest transactions
async def main() -> None:
    solana_fm = SolanaFM()
    async with solana_fm.async_client as client:
        response = await client.get_account_transactions(account)
        print("Transactions Extracted:", len(response.result.data))

asyncio.run(main())
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.solana_fm` - Explore the [`SolanaFM`](../solana_fm/interaction.md) API connector and all its methods. 

    [:octicons-arrow-right-24: Reference](../solana_fm/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.solana_fm.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../solana_fm/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.solana_fm.schema` - Extract only what is necessary by exploiting reponse mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../solana_fm/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.solana_fm.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../solana_fm/exception.md)

</div>

## Endpoints

| Endpoint  | Type      | Method    | `cyhole` Release  | Deprecated    |
| ---       | ---       | ---       | ---               | ---           |
| Account Transactions | `GET` | [`get_account_transactions`](../solana_fm/interaction.md#cyhole.solana_fm.SolanaFM._get_account_transactions) | `0.2.1` | - |