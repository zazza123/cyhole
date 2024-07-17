# :material-sphere: - Jupiter

Jupiter ([https://jup.ag](https://jup.ag)) is one of the most popular DEX on Solana ecosystem with an active community, the cats! The platform provides many useful services directly from the site, but it also gives the possibility to other developers to create new powerful tools via the many **open to use** API endopints. Jupiter's documentation is well written and can be access from [here](https://station.jup.ag/docs).

The API connector is [`Jupiter`](../jupiter/interaction.md) class imported from `cyhole.jupiter` path.

## Quick Examples

### Get Latest Token Price

Extract the latest `JUP` buy price over `USDC` in few lines of code by using [`get_price`](../jupiter/interaction.md#cyhole.jupiter.Jupiter._get_price) in **asynchronous** logic.

```py
import asyncio
from cyhole.jupiter import Jupiter
from cyhole.core.address.solana import JUP

# get current price of JUP on Solana
async def main() -> None:
    jupiter = Jupiter()
    async with jupiter.async_client as client:
        response = await client.get_price([JUP])
        print("Current JUP/USDC:", response.data[JUP].price)

asyncio.run(main())
```

### Create Limit Order Transaction

Get the transaction for the creation of a new Limit Order by using [`post_limit_order_create`](../jupiter/interaction.md#cyhole.jupiter.Jupiter._post_limit_order_create) in **synchronous** logic.

```py
from solders.keypair import Keypair

from cyhole.jupiter import Jupiter
from cyhole.jupiter.schema import PostLimitOrderCreateBody
from cyhole.core.address.solana import JUP, USDC

jupiter = Jupiter()

# create body for the request
key = Keypair()
body = PostLimitOrderCreateBody(
    user_public_key = "YOUR-WALLET-PUBLIC-KEY",
    input_amount = 100_000,
    output_amount = 100_000,
    input_token = USDC,
    output_token = JUP,
    base = str(key.pubkey())
)

# send request
response = jupiter.client.post_limit_order_create(body)
print("Transaction:", response.transaction)
```

!!! info
    The transaction should be then signed and sent on RPC to be validated and executed.

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.jupiter` - Explore the [`Jupiter`](../jupiter/interaction.md) API connector and all its methods. 

    [:octicons-arrow-right-24: Reference](../jupiter/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.jupiter.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../jupiter/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.jupiter.schema` - Extract only what is necessary by exploiting reponse mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../jupiter/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.jupiter.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../jupiter/exception.md)

</div>
