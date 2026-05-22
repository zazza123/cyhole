# :material-lightning-bolt: - Helius

Helius ([https://www.helius.dev](https://www.helius.dev)) is an enhanced Solana RPC provider offering
developer-focused infrastructure tools, including the **Digital Asset Standard (DAS) API** — a unified,
high-performance interface for querying on-chain digital assets such as NFTs, compressed NFTs (cNFTs),
fungible tokens, and inscriptions.

All DAS endpoints require an API key obtained from the [Helius Dashboard](https://dashboard.helius.dev).
The key is passed as a URL query parameter (`?api-key=YOUR_KEY`) on every request.

The API connector is the [`Helius`](../helius/interaction.md) class imported from `cyhole.helius`.

## Quick Examples

### Retrieve a Single Asset

Fetch the full on-chain record for an NFT by its mint address, including metadata, ownership, royalties,
and compression state.

```python
from cyhole.helius import Helius

helius = Helius(api_key="your-api-key")
response = helius.client.post_get_asset("4ZkS7zADmEFnkLPMHqJfPvHDN8oqfPjqDFGEQHiqPbEz")

asset = response.result
print(asset.id)                        # mint address
print(asset.ownership.owner)           # current owner wallet
print(asset.content.metadata.name)     # NFT name
```

### Enumerate a Wallet Portfolio

Retrieve all digital assets owned by a wallet, including fungible tokens and native SOL balance.

```python
import asyncio
from cyhole.helius import Helius
from cyhole.helius.schema import PostGetAssetsByOwnerBody, HeliusDisplayOptions

helius = Helius(api_key="your-api-key")

async def main():
    body = PostGetAssetsByOwnerBody(
        owner_address="YourWalletAddressHere",
        display_options=HeliusDisplayOptions(
            show_fungible=True,
            show_native_balance=True,
        ),
    )
    async with helius.async_client as client:
        response = await client.post_get_assets_by_owner(body)

    print(f"Total assets: {response.result.total}")
    for asset in response.result.items:
        print(asset.id, asset.content.metadata.name if asset.content else "")

asyncio.run(main())
```

### Search Assets by Collection

Find all NFTs in a collection and sort them by most recent activity.

```python
from cyhole.helius import Helius
from cyhole.helius.schema import PostGetAssetsByGroupBody, HeliusSortConfig
from cyhole.helius.param import HeliusSortBy, HeliusSortDirection

helius = Helius(api_key="your-api-key")

body = PostGetAssetsByGroupBody(
    group_key="collection",
    group_value="CollectionMintAddressHere",
    sort_by=HeliusSortConfig(
        sort_by=HeliusSortBy.RECENT_ACTION.value,
        sort_direction=HeliusSortDirection.DESC.value,
    ),
    limit=50,
)
response = helius.client.post_get_assets_by_group(body)
print(f"Collection size: {response.result.total}")
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.helius` - Explore the [`Helius`](../helius/interaction.md) API connector and all its methods.

    [:octicons-arrow-right-24: Reference](../helius/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.helius.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../helius/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.helius.schema` - Extract only what is necessary by exploiting response mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../helius/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.helius.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../helius/exception.md)

</div>

## Endpoints

| Endpoint | Type | Method | `cyhole` Release | Deprecated |
| --- | --- | --- | --- | --- |
| getAsset | `POST` | [`post_get_asset`](../helius/interaction.md#cyhole.helius.Helius._post_get_asset) | `0.3.0` | - |
| getAssetBatch | `POST` | [`post_get_asset_batch`](../helius/interaction.md#cyhole.helius.Helius._post_get_asset_batch) | `0.3.0` | - |
| getAssetProof | `POST` | [`post_get_asset_proof`](../helius/interaction.md#cyhole.helius.Helius._post_get_asset_proof) | `0.3.0` | - |
| getAssetProofBatch | `POST` | [`post_get_asset_proof_batch`](../helius/interaction.md#cyhole.helius.Helius._post_get_asset_proof_batch) | `0.3.0` | - |
| getAssetsByOwner | `POST` | [`post_get_assets_by_owner`](../helius/interaction.md#cyhole.helius.Helius._post_get_assets_by_owner) | `0.3.0` | - |
| getAssetsByGroup | `POST` | [`post_get_assets_by_group`](../helius/interaction.md#cyhole.helius.Helius._post_get_assets_by_group) | `0.3.0` | - |
| getAssetsByCreator | `POST` | [`post_get_assets_by_creator`](../helius/interaction.md#cyhole.helius.Helius._post_get_assets_by_creator) | `0.3.0` | - |
| getAssetsByAuthority | `POST` | [`post_get_assets_by_authority`](../helius/interaction.md#cyhole.helius.Helius._post_get_assets_by_authority) | `0.3.0` | - |
| searchAssets | `POST` | [`post_search_assets`](../helius/interaction.md#cyhole.helius.Helius._post_search_assets) | `0.3.0` | - |
| getSignaturesForAsset | `POST` | [`post_get_signatures_for_asset`](../helius/interaction.md#cyhole.helius.Helius._post_get_signatures_for_asset) | `0.3.0` | - |
| getNftEditions | `POST` | [`post_get_nft_editions`](../helius/interaction.md#cyhole.helius.Helius._post_get_nft_editions) | `0.3.0` | - |
| getTokenAccounts | `POST` | [`post_get_token_accounts`](../helius/interaction.md#cyhole.helius.Helius._post_get_token_accounts) | `0.3.0` | - |
| getTransfersByAddress | `POST` | [`post_get_transfers_by_address`](../helius/interaction.md#cyhole.helius.Helius._post_get_transfers_by_address) | `0.3.0` | - |
| getTransactionsForAddress | `POST` | [`post_get_transactions_for_address`](../helius/interaction.md#cyhole.helius.Helius._post_get_transactions_for_address) | `0.3.0` | - |
| getTransactionsByAddress | `GET` | [`get_transactions_by_address`](../helius/interaction.md#cyhole.helius.Helius._get_transactions_by_address) | `0.3.1` | - |
