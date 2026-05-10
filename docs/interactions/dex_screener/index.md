# :simple-eagle: - DexScreener

DexScreener ([https://dexscreener.com](https://dexscreener.com)) is a real-time DEX analytics platform that aggregates trading pair data across multiple blockchains and decentralized exchanges. It provides live price feeds, liquidity metrics, transaction volumes, token profile information, and boost activity.

No API key is required for the public endpoints.

The API connector is [`DexScreener`](../dex_screener/interaction.md) class imported from `cyhole.dex_screener` path.

## Quick Examples

### Search Trading Pairs

Search for pairs matching a query string using [`get_search`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_search) in **synchronous** logic.

```python
from cyhole.dex_screener import DexScreener

dex = DexScreener()
response = dex.client.get_search("SOL/USDC")
for pair in response.pairs:
    print(pair.pair_address, pair.price_usd)
```

### Get Token Boosts (async)

Retrieve the tokens with the most active boosts using [`get_token_boosts_top`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_token_boosts_top) in **asynchronous** logic.

```python
import asyncio
from cyhole.dex_screener import DexScreener

async def main() -> None:
    dex = DexScreener()
    async with dex.async_client as client:
        response = await client.get_token_boosts_top()
        for boost in response.root:
            print(boost.chain_id, boost.token_address, boost.total_amount)

asyncio.run(main())
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.dex_screener` - Explore the [`DexScreener`](../dex_screener/interaction.md) API connector and all its methods.

    [:octicons-arrow-right-24: Reference](../dex_screener/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.dex_screener.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../dex_screener/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.dex_screener.schema` - Extract only what is necessary by exploiting response mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../dex_screener/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.dex_screener.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../dex_screener/exception.md)

</div>

## Endpoints

| Endpoint  | Type      | Method    | `cyhole` Release  | Deprecated    |
| ---       | ---       | ---       | ---               | ---           |
| Token Profiles - Latest | `GET` | [`get_token_profiles_latest`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_token_profiles_latest) | `0.3.0` | - |
| Community Takeover - Latest | `GET` | [`get_community_takeover`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_community_takeover) | `0.3.0` | - |
| Ads - Latest | `GET` | [`get_ads_latest`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_ads_latest) | `0.3.0` | - |
| Token Boosts - Latest | `GET` | [`get_token_boosts_latest`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_token_boosts_latest) | `0.3.0` | - |
| Token Boosts - Top | `GET` | [`get_token_boosts_top`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_token_boosts_top) | `0.3.0` | - |
| Orders | `GET` | [`get_orders`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_orders) | `0.3.0` | - |
| Pairs | `GET` | [`get_pairs`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_pairs) | `0.3.0` | - |
| Tokens | `GET` | [`get_tokens`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_tokens) | `0.3.0` | - |
| Token Pairs | `GET` | [`get_token_pairs`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_token_pairs) | `0.3.0` | - |
| Search | `GET` | [`get_search`](../dex_screener/interaction.md#cyhole.dex_screener.DexScreener._get_search) | `0.3.0` | - |
