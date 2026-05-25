# :simple-coingecko: - Gecko

Gecko ([https://www.geckoterminal.com/dex-api](https://www.geckoterminal.com/dex-api)) is the on-chain DEX market-data
service operated by CoinGecko. The v2 API exposes networks, DEXes, pools, tokens, OHLCV candles, trades, holder and
trader analytics across 250+ chains.

No API key is required to call the public `api.geckoterminal.com/api/v2` base URL on its 30 calls/minute free tier.
Paying CoinGecko users can pass an `api_key` to the [`Gecko`](../gecko/interaction.md) constructor so requests are routed
through the higher-rate `pro-api.coingecko.com/api/v3/onchain` mirror; this also unlocks the **Token OHLCV**,
**Token Trades**, **Token Holders Chart**, **Top Token Holders** and **Top Token Traders** endpoints, which return
`401 Unauthorized` on the free tier.

The API connector is the [`Gecko`](../gecko/interaction.md) class imported from `cyhole.gecko`.

## Quick Examples

### List Supported Networks

Retrieve the catalog of indexed networks (chain id, name, coingecko slug) — the first call you typically need before
issuing any other request.

```python
from cyhole.gecko import Gecko

gecko = Gecko()
response = gecko.client.get_networks()

print(f"Indexed networks: {len(response.data)}")
for network in response.data[:5]:
    print(network.id, network.attributes.name)
```

### Fetch a Pool's Recent Candles

Get the trailing OHLCV series for a specific liquidity pool. Useful for charting and trend detection.

```python
from cyhole.gecko import Gecko
from cyhole.gecko.schema import GetPoolOhlcvQuery

gecko = Gecko()
query = GetPoolOhlcvQuery(limit = 50, currency = "usd")

# USDC/WETH on Uniswap V3
response = gecko.client.get_pool_ohlcv(
    network = "eth",
    pool_address = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    timeframe = "day",
    query = query,
)

for ts, open_, high, low, close, volume in response.data.attributes.ohlcv_list:
    print(ts, close, volume)
```

### Bulk Token Metadata Lookup

Fetch price, supply and 24h volume for several tokens in a single call.

```python
import asyncio
from cyhole.gecko import Gecko

gecko = Gecko()

async def main() -> None:
    addresses = [
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    ]
    async with gecko.async_client as client:
        response = await client.get_token_data("eth", addresses)

    for token in response.data:
        print(token.attributes.symbol, token.attributes.price_usd)

asyncio.run(main())
```

### Search Pools by Symbol

Resolve a token symbol or pool name to the canonical pool addresses across networks.

```python
from cyhole.gecko import Gecko

gecko = Gecko()
response = gecko.client.get_search_pools("USDC")

for pool in response.data[:5]:
    print(pool.attributes.name, pool.attributes.address)
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.gecko` - Explore the [`Gecko`](../gecko/interaction.md) API connector and all its methods.

    [:octicons-arrow-right-24: Reference](../gecko/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.gecko.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../gecko/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.gecko.schema` - Extract only what is necessary by exploiting response mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../gecko/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.gecko.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../gecko/exception.md)

</div>

## Endpoints

| Endpoint | Type | Method | `cyhole` Release | Deprecated |
| --- | --- | --- | --- | --- |
| Networks | `GET` | [`get_networks`](../gecko/interaction.md#cyhole.gecko.Gecko._get_networks) | `0.3.1` | - |
| Dexes by Network | `GET` | [`get_dexes`](../gecko/interaction.md#cyhole.gecko.Gecko._get_dexes) | `0.3.1` | - |
| Pool OHLCV | `GET` | [`get_pool_ohlcv`](../gecko/interaction.md#cyhole.gecko.Gecko._get_pool_ohlcv) | `0.3.1` | - |
| Pool Tokens Info | `GET` | [`get_pool_token_info`](../gecko/interaction.md#cyhole.gecko.Gecko._get_pool_token_info) | `0.3.1` | - |
| Pool Trades | `GET` | [`get_pool_trades`](../gecko/interaction.md#cyhole.gecko.Gecko._get_pool_trades) | `0.3.1` | - |
| Token Data (single + multiple) | `GET` | [`get_token_data`](../gecko/interaction.md#cyhole.gecko.Gecko._get_token_data) | `0.3.1` | - |
| Token Info | `GET` | [`get_token_info`](../gecko/interaction.md#cyhole.gecko.Gecko._get_token_info) | `0.3.1` | - |
| Recently Updated Tokens | `GET` | [`get_recently_updated_tokens`](../gecko/interaction.md#cyhole.gecko.Gecko._get_recently_updated_tokens) | `0.3.1` | - |
| Token OHLCV (Pro) | `GET` | [`get_token_ohlcv`](../gecko/interaction.md#cyhole.gecko.Gecko._get_token_ohlcv) | `0.3.1` | - |
| Token Trades (Pro) | `GET` | [`get_token_trades`](../gecko/interaction.md#cyhole.gecko.Gecko._get_token_trades) | `0.3.1` | - |
| Token Holders Chart (Pro) | `GET` | [`get_token_holders_chart`](../gecko/interaction.md#cyhole.gecko.Gecko._get_token_holders_chart) | `0.3.1` | - |
| Top Token Holders (Pro) | `GET` | [`get_top_token_holders`](../gecko/interaction.md#cyhole.gecko.Gecko._get_top_token_holders) | `0.3.1` | - |
| Top Token Traders (Pro) | `GET` | [`get_top_token_traders`](../gecko/interaction.md#cyhole.gecko.Gecko._get_top_token_traders) | `0.3.1` | - |
| Simple Token Price | `GET` | [`get_simple_token_price`](../gecko/interaction.md#cyhole.gecko.Gecko._get_simple_token_price) | `0.3.1` | - |
| Search Pools | `GET` | [`get_search_pools`](../gecko/interaction.md#cyhole.gecko.Gecko._get_search_pools) | `0.3.1` | - |
