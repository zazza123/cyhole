<p align="center">
  <a href="https://zazza123.github.io/cyhole">
    <img src="https://raw.githubusercontent.com/zazza123/cyhole/main/docs/config/images/logo.png" alt="cyhole" height="150px" class="img-logo">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/cyhole"><img src="https://img.shields.io/pypi/v/cyhole?color=%2334D058&label=pypi%20package" alt="PyPI version" height="18"></a>
</p>


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

---

**Documentation**: [https://zazza123.github.io/cyhole](https://zazza123.github.io/cyhole)

## Interactions

In **cyhole**, Interactions serve as the fundamental components, akin to the building blocks of a scientific model. Each interaction represents a distinct cryptocurrency API, providing developers with access to essential data and metrics.

The current supported external/interactions APIs are:

|Site                             |Path             |Connector|
|----                             |----             |---------|
|[birdeye.so](https://birdeye.so) |`cyhole.birdeye` |`Birdeye`|
