# :material-bird: - Birdeye

Birdeye ([https://birdeye.so](https://birdeye.so)) is a popular treading crypto platform connected to different blockchains that provides tokens data and pairs' prices in real time. The access to both their public and private APIs is managed by a valid API key requestable on their site.

The API connector is [`Birdeye`](../birdeye/interaction.md) class imported from `cyhole.birdeye` path.

## Quick Example

Extract the latest tokens from Ethereum chain sorted in descending order by USD volume in few lines of code by using [`get_token_list`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_list) in **synchronous** and **asynchronous** logic.

```py
import asyncio
import asyncio
from cyhole.birdeye import Birdeye
from cyhole.birdeye.param import BirdeyeChain

birdeye = Birdeye(chain = BirdeyeChain.ETHEREUM.value)

# synchronous
response = birdeye.client.get_token_list(limit = 1)
token = response.data.tokens[0]
print(f"Highest 24h USD volume token: '{token.name}', volume: {round(token.volume_24h_usd, 2)}.")

# asynchronous
async def main() -> None:
    async with birdeye.async_client as client:
        response = await client.get_token_list(limit = 1)
        token = response.data.tokens[0]
        print(f"Highest 24h USD volume token: '{token.name}', volume: {round(token.volume_24h_usd, 2)}.")

asyncio.run(main())
```

!!! note
    To run this example is assumed that the user has a valid API key stored in `BIRDEYE_API_KEY` environment variable.  
    If the key is not provided during the object creations, then the library will raise an exception.

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.birdeye` - Explore the [`Birdeye`](../birdeye/interaction.md) API connector and all its methods. 

    [:octicons-arrow-right-24: Reference](../birdeye/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.birdeye.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../birdeye/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.birdeye.schema` - Extract only what is necessary by exploiting reponse mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../birdeye/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.birdeye.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../birdeye/exception.md)

</div>
