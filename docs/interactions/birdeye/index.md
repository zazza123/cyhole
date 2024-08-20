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

## Endpoints

| Endpoint  | Type      | Method    | `cyhole` Release  | Deprecated    |
| ---       | ---       | ---       | ---               | ---           |
| Token - List | `GET` | [`get_token_list`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_list) | `0.0.1-alpha` | - |
| Token - Creation Token Info | `GET` | [`get_token_creation_info`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_creation_info) | `0.0.1-alpha` | - |
| Token - Security | `GET` | [`get_token_security`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_security) | `0.0.1-alpha` | - |
| Token - Overview | `GET` | [`get_token_overview`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_token_overview) | `0.0.1-alpha` | - |
| Price | `GET` | [`get_price`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_price) | `0.0.1-alpha` | - |
| Price - Multiple | `GET` | [`get_price_multiple`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_price_multiple) | `0.0.1-alpha` | - |
| Price - Historical | `GET` | [`get_price_historical`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_price_historical) | `0.0.1-alpha` | - |
| Price Volume - Single Token | `GET` | [`get_price_volume_single`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_price_volume_single) | `0.2.1` | - |
| Price Volume - Multiple Token | `POST` | [`post_price_volume_multi`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._post_price_volume_multi) | `0.2.1` | - |
| Trades - Token | `GET` | [`get_trades_token`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_trades_token) | `0.0.1-alpha` | - |
| Trades - Pair | `GET` | [`get_trades_pair`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_trades_pair) | `0.0.1-alpha` | - |
| OHLCV - Token/Pair | `GET` | [`get_ohlcv`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_ohlcv) | `0.0.1-alpha` | - |
| OHLCV - Base/Quote | `GET` | [`get_ohlcv_base_quote`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_ohlcv_base_quote) | `0.0.1-alpha` | - |
| Wallet - Supported Networks | `GET` | [`get_wallet_supported_networks`](../birdeye/interaction.md#cyhole.birdeye.Birdeye._get_wallet_supported_networks) | `0.0.1-alpha` | - |
| History | `GET` | `get_history` | `0.0.1-alpha` | `0.2.0` |
