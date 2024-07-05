<p align="center">
  <a href="https://zazza123.github.io/cyhole">
    <img src="https://raw.githubusercontent.com/zazza123/cyhole/main/docs/config/images/logo.png" alt="cyhole" height="150px" class="readme">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/cyhole" target="_blank"><img src="https://img.shields.io/pypi/pyversions/cyhole.svg?color=%2334D058" alt="Supported Python Versions" height="18"></a>
  <a href="https://pypi.org/project/cyhole"><img src="https://img.shields.io/pypi/v/cyhole?color=%2334D058&label=pypi" alt="PyPI version" height="18"></a>
  <a href="https://github.com/zazza123/cyhole/actions/workflows/execute-tests.yml?query=branch%3Amain+event%3Apush"><img src="https://github.com/zazza123/cyhole/actions/workflows/execute-tests.yml/badge.svg?branch=main&action=push" alt="Tests" height="18"></a>
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/zazza123/cyhole" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/zazza123/cyhole.svg" alt="Coverage" height="18"></a>
  <a href="https://pepy.tech/project/cyhole" target="_blank"><img src="https://static.pepy.tech/badge/cyhole/month" alt="Statistics" height="18"></a>
  <a href="https://github.com/zazza123/cyhole/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/github/license/zazza123/cyhole.svg" alt="License" height="18"></a>
</p>

---

<p class="readme">
  <b>Documentation</b>: <a href="https://zazza123.github.io/cyhole">https://zazza123.github.io/cyhole</a>
</p>
<hr class="readme">

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

|Site                             |Path             |Connector                                                                      |
|----                             |----             |---------                                                                      |
|[birdeye.so](https://birdeye.so) |`cyhole.birdeye` |[`Birdeye`](https://zazza123.github.io/cyhole/interactions/birdeye/index.html) |
|[jup.ag](https://jup.ag)         |`cyhole.jupiter` |[`Jupiter`](https://zazza123.github.io/cyhole/interactions/jupiter/index.html) |
