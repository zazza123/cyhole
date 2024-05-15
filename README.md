<div style="display: flex; align-items: center; justify-content: center;">
  <svg width="6em" height="6em" viewBox="0 0 24 24">
      <path fill = "currentColor" d = "m12 6.7l1.45 3.85L17.3 12l-3.85 1.45L12 17.3l-1.45-3.85L6.7 12l3.85-1.45zM12 1L9 9l-8 3l8 3l3 8l3-8l8-3l-8-3z" />
  </svg>
  <span style="margin-left: 10px; font-size: 4em;">cyhole</span>
</div>

---

**cyhole** is designed to help python's developers to interact to the most popular external API services in crypto world and create automation processes.

Each external API integrated into the library is referred to as an *Interaction*, providing developers with a comprehensive toolkit for retrieving real-time market data, historical trends, account information, and more.

<u>Key Features</u>

  - *Centralized Access*: access multiple cryptocurrency APIs through a single interface.
  - *Comprehensive Coverage*: explore a wide range of cryptocurrency data, including market prices, trading volumes, and blockchain statistics.
  - *Simplified Development*: accelerate the development process by leveraging pre-built API integrations.
  - *Flexible Integration*: seamlessly incorporate cyhole into Python projects, whether building automated trading algorithms or monitoring cryptocurrency portfolios.

The installation is performed via `pip` by running:

```sh
pip install cyhole
```

## Interactions

In **cyhole**, Interactions serve as the fundamental components, akin to the building blocks of a scientific model. Each interaction represents a distinct cryptocurrency API, providing developers with access to essential data and metrics.

The current supported external/interactions APIs are:

|Site                             |Path             |Connector|
|----                             |----             |---------|
|[birdeye.so](https://birdeye.so) |`cyhole.birdeye` |`Birdeye`|
