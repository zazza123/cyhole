# :simple-solana: - Rugcheck

Rugcheck ([https://rugcheck.xyz](https://rugcheck.xyz)) is a Solana token security analysis platform that provides rug-pull risk assessments, insider network detection, liquidity analysis, and community voting on tokens.

No API key is required for public endpoints. Authenticated endpoints require a Bearer token passed as `api_key` to the `Rugcheck` constructor.

The API connector is [`Rugcheck`](interaction.md) class imported from `cyhole.rugcheck` path.

## Quick Examples

### Token Risk Report Summary

Check the risk score and identified risks for a token in a single lightweight call.

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

### Full Token Report

Retrieve the complete rug-check report including market data, top holders, and locker information.

```python
from cyhole.rugcheck import Rugcheck

rugcheck = Rugcheck()
report = rugcheck.client.get_token_report(
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
)
print(f"Token: {report.token_meta.name} ({report.token_meta.symbol})")
print(f"Score: {report.score_normalised}/100")
print(f"Total liquidity: ${report.total_market_liquidity:,.2f}")
print(f"Top holders: {len(report.top_holders)}")
```

### Async Usage

```python
import asyncio
from cyhole.rugcheck import Rugcheck

async def main():
    rugcheck = Rugcheck()
    async with rugcheck.async_client as client:
        summary = await client.get_token_report_summary(
            "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
        )
    print(f"Score: {summary.score_normalised}/100")

asyncio.run(main())
```

## Content

| | |
|---|---|
| [Client](client.md) | [Interaction](interaction.md) |
| [Parameters](param.md) | [Schema](schema.md) |
| [Exceptions](exception.md) | |
