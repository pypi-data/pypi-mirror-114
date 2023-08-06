# lndpy

Modern pythonic bindings for the [lightning network daemon (lnd)](https://github.com/lightningnetwork/lnd/).

## Features

- Standard lnd gRPC bindings built natively as part of the CI pipeline from the latest released version
- Supports Python 3.6+
- Pythonic interface to auto-generated gRPC functions (coming soon)
- Documentation generated automatically from gRPC binding docs (coming soon)

## Installation

Install as usual with `pip` or any other packaging tool of choice from PyPI:

```bash
$ pip install lndpy
```

### Usage

Example usage:

```python
from lndpy import Lnd
info = Lnd().get_info()
print(info)
```

## Development

`pipenv` is the recommended tool of choice for local development. First, checkout the git repository. Then, create and sync a new virtualenv with the development dependencies:

```bash
$ git clone https://github.com/yuvadm/lndpy
$ cd lndpy
$ pipenv sync --dev
```

As an optional step, install pre-commit hooks:

```bash
$ pipenv run pre-commit install
```

Next, fetch and build the lnd proto files:

```bash
$ pipenv run buildprotos
```

In order to build the gRPC .proto files you will also need https://github.com/googleapis/googleapis checked out next to lndpy.

Run the tests to ensure they were built properly:

```bash
$ pipenv run test
```

## License

[MIT License](LICENSE)

Copyright Ⓒ 2021 Yuval Adam
