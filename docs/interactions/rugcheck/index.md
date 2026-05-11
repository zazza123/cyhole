# :simple-solana: - Rugcheck

Rugcheck ([https://rugcheck.xyz](https://rugcheck.xyz)) is a Solana token security analysis platform that provides rug-pull risk assessments, insider network detection, liquidity analysis, and community voting on tokens.

No API key is required for public endpoints. Authenticated endpoints require a Bearer token passed as `api_key` to the `Rugcheck` constructor.

The API connector is [`Rugcheck`](../rugcheck/interaction.md) class imported from `cyhole.rugcheck` path.

## Quick Examples

### Token Risk Report Summary

Check the risk score and identified risks for a token using [`get_token_report_summary`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_report_summary) in **synchronous** logic.

```python
from cyhole.rugcheck import Rugcheck

rugcheck = Rugcheck()
summary = rugcheck.client.get_token_report_summary(
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
)
print(f"Score: {summary.score_normalised}/100")
for risk in summary.risks:
    print(f"  [{risk.level}] {risk.name}: {risk.description}")
```

### Full Token Report (async)

Retrieve the complete rug-check report including market data, top holders, and locker info using [`get_token_report`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_report) in **asynchronous** logic.

```python
import asyncio
from cyhole.rugcheck import Rugcheck

async def main() -> None:
    rugcheck = Rugcheck()
    async with rugcheck.async_client as client:
        report = await client.get_token_report(
            "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
        )
    print(f"Token: {report.token_meta.name} ({report.token_meta.symbol})")
    print(f"Score: {report.score_normalised}/100")
    print(f"Total liquidity: ${report.total_market_liquidity:,.2f}")

asyncio.run(main())
```

## Content

The documentation follows the library's structure by providing all the technical details required to use it.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __Connector__

    ---

    `cyhole.rugcheck` - Explore the [`Rugcheck`](../rugcheck/interaction.md) API connector and all its methods.

    [:octicons-arrow-right-24: Reference](../rugcheck/interaction.md)

-   :material-list-status:{ .lg .middle } __API Parameters__

    ---

    `cyhole.rugcheck.param` - Ensure to use the correct parameters during the API calls.

    [:octicons-arrow-right-24: Reference](../rugcheck/param.md)

-   :material-graph:{ .lg .middle } __Response Schema__

    ---

    `cyhole.rugcheck.schema` - Extract only what is necessary by exploiting response mapping thanks to `pydantic` schemes.

    [:octicons-arrow-right-24: Reference](../rugcheck/schema.md)

-   :octicons-stop-24:{ .lg .middle } __Exceptions__

    ---

    `cyhole.rugcheck.exception` - Make sure you intercept all exceptions correctly.

    [:octicons-arrow-right-24: Reference](../rugcheck/exception.md)

</div>

## Endpoints

| Endpoint | Type | Method | `cyhole` Release | Deprecated |
| --- | --- | --- | --- | --- |
| Ping | `GET` | [`get_ping`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_ping) | `0.3.0` | - |
| Maintenance | `GET` | [`get_maintenance`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_maintenance) | `0.3.0` | - |
| Leaderboard | `GET` | [`get_leaderboard`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_leaderboard) | `0.3.0` | - |
| Token Report | `GET` | [`get_token_report`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_report) | `0.3.0` | - |
| Token Report Summary | `GET` | [`get_token_report_summary`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_report_summary) | `0.3.0` | - |
| Token Metadata | `GET` | [`get_token_metadata`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_metadata) | `0.3.0` | - |
| Token Votes | `GET` | [`get_token_votes`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_votes) | `0.3.0` | - |
| Token Insiders Graph | `GET` | [`get_token_insiders_graph`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_insiders_graph) | `0.3.0` | - |
| Token Insiders Networks | `GET` | [`get_token_insiders_networks`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_insiders_networks) | `0.3.0` | - |
| Token Lockers | `GET` | [`get_token_lockers`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_lockers) | `0.3.0` | - |
| Token Lockers Flux | `GET` | [`get_token_lockers_flux`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_token_lockers_flux) | `0.3.0` | - |
| Token Report - Trigger | `POST` | [`post_token_report`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_token_report) | `0.3.0` | - |
| Token Vote | `POST` | [`post_token_vote`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_token_vote) | `0.3.0` | - |
| Stats - New Tokens | `GET` | [`get_stats_new_tokens`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_new_tokens) | `0.3.0` | - |
| Stats - Recent | `GET` | [`get_stats_recent`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_recent) | `0.3.0` | - |
| Stats - Trending | `GET` | [`get_stats_trending`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_trending) | `0.3.0` | - |
| Stats - Verified | `GET` | [`get_stats_verified`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_verified) | `0.3.0` | - |
| Stats - Analytics | `GET` | [`get_stats_analytics`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_analytics) | `0.3.0` | - |
| Stats - Rugs Ticker | `GET` | [`get_stats_rugs_ticker`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_stats_rugs_ticker) | `0.3.0` | - |
| Creator | `GET` | [`get_creator`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_creator) | `0.3.0` | - |
| Domains | `GET` | [`get_domains`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_domains) | `0.3.0` | - |
| Domain Lookup | `GET` | [`get_domain_lookup`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._get_domain_lookup) | `0.3.0` | - |
| Bulk Tokens Report | `POST` | [`post_bulk_tokens_report`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_bulk_tokens_report) | `0.3.0` | - |
| Bulk Tokens Summary | `POST` | [`post_bulk_tokens_summary`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_bulk_tokens_summary) | `0.3.0` | - |
| Tokens Verify Eligible | `POST` | [`post_tokens_verify_eligible`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_tokens_verify_eligible) | `0.3.0` | - |
| Tokens Verify | `POST` | [`post_tokens_verify`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_tokens_verify) | `0.3.0` | - |
| Tokens Verify Transaction | `POST` | [`post_tokens_verify_transaction`](../rugcheck/interaction.md#cyhole.rugcheck.Rugcheck._post_tokens_verify_transaction) | `0.3.0` | - |
