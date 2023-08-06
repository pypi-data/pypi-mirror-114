# Crypkit TheGraph Handlers

Integrations of Ethereum services through https://thegraph.com


## Status

|   Service   |  Mainnet   |  Polygon   |    Links     |
|------------|:----------------:|:------------:|:------------|
| Uniswap v2 | &#x2714; | &#x2717; | [GitHub](https://github.com/Uniswap/uniswap-v2-subgraph/)
| Uniswap v3 | &#x2717; | &#x2717; | [GitHub](https://github.com/Uniswap/uniswap-v3-subgraph/)
| SushiSwap | &#x2717; | &#x2717; | [GitHub](https://github.com/sushiswap/sushiswap-subgraph)
| Balancer | &#x2717; | &#x2717; | [v1](https://github.com/balancer-labs/balancer-subgraph), [v2](https://github.com/balancer-labs/balancer-subgraph-v2)
| Curve.fi | &#x2717; | &#x2717; | [GitHub](https://github.com/curvefi/curve-subgraph)


## Developing

In a separate virtual environment, type

```
(your_venv) $ pip install -e .[all]
```

which will install all the dependencies. Since then, for testing, you can either use `tox` as your test runner or `pytest` directly.

Formatting and linting is done by

```
$ tox -e linters
```

which will run `black`, `flake8`, `isort` and `mypy`. Absence of `mypy` errors is not enforced (for now), but adherence to the formatting standards is required.
