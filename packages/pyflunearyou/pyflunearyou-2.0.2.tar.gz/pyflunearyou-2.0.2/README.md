# 🤒 pyflunearyou: A Python3 API for Flu Near You

[![CI](https://github.com/bachya/pyflunearyou/workflows/CI/badge.svg)](https://github.com/bachya/pyflunearyou/actions)
[![PyPi](https://img.shields.io/pypi/v/pyflunearyou.svg)](https://pypi.python.org/pypi/pyflunearyou)
[![Version](https://img.shields.io/pypi/pyversions/pyflunearyou.svg)](https://pypi.python.org/pypi/pyflunearyou)
[![License](https://img.shields.io/pypi/l/pyflunearyou.svg)](https://github.com/bachya/pyflunearyou/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyflunearyou/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/pyflunearyou)
[![Maintainability](https://api.codeclimate.com/v1/badges/dee8556060c7d0e7f2d1/maintainability)](https://codeclimate.com/github/bachya/pyflunearyou/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pyflunearyou` is a simple Python library for retrieving UV-related information
from [Flu Near You](https://flunearyou.org/#!/).

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```python
pip install pyflunearyou
```

# Python Versions

`pyflunearyou` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9

# Usage

```python
import asyncio

from aiohttp import ClientSession

from pyflunearyou import Client


async def main() -> None:
    """Run!"""
    client = Client()

    # Get user data for a specific latitude/longitude:
    await client.user_reports.status_by_coordinates(<LATITUDE>, <LONGITUDE>)

    # Get user data for a specific ZIP code:
    await client.user_reports.status_by_zip("<ZIP_CODE>")

    # Get CDC data for a specific latitude/longitude:
    await client.cdc_reports.status_by_coordinates(<LATITUDE>, <LONGITUDE>)

    # Get CDC data for a specific state:
    await client.cdc_reports.status_by_state('<USA_CANADA_STATE_NAME>')

asyncio.run(main())
```

By default, the library creates a new connection to Flu Near You with each coroutine. If
you are calling a large number of coroutines (or merely want to squeeze out every second
of runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from pyflunearyou import Client


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        client = Client(session=session)

        # ...

asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyflunearyou/issues)
  or [initiate a discussion on one](https://github.com/bachya/pyflunearyou/issues/new).
2. [Fork the repository](https://github.com/bachya/pyflunearyou/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
