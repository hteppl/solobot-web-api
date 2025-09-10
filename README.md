<p align="center">
  <img src="https://pocomacho.ru/static/images/bot_mobile.png" alt="logo-main" height="400">
</p>

# solobot-web-api

[![LICENSE](https://img.shields.io/pypi/l/solobot-web-api)](LICENSE)
[![Supported Versions](https://img.shields.io/pypi/pyversions/aiohttp.svg)](https://pypi.org/project/solobot-web-api)
[![PyPI Version](https://img.shields.io/pypi/v/solobot-web-api?color=%23e04f1f)](https://pypi.org/project/solobot-web-api)

#### Python library for interacting with [SoloBot Web API](https://github.com/Vladless/Solo_bot/).

README also available in:

- [Русский](docs/README_ru.md)

Powered by [🥕 Морковный Бот](https://t.me/morkowniy_bot)

## Installing

`solobot-web-api` is available on PyPI:

```console
$ python -m pip install solobot-web-api
```

Officially supports Python 3.9+ and requires `aiohttp`.

## API Version and Reference

Base api url: `https://pocomacho.ru/solonetbot/api/v1/modules`

API reference and official docs: https://pocomacho.ru/solonetbot/api/swagger

## Usage Examples

You can find a raw scheme example in the docs: https://pocomacho.ru/solonetbot/api/swagger

**Grant a license to a user:**

```python
import asyncio
from solowebapi import SoloWebAPI


async def main():
    api = SoloWebAPI("username", "password")
    active = await api.grant_license("example_module", 123)
    print("License active:", active)
    await api.close()


asyncio.run(main())
```

**Check if a license is active:**

```python
import asyncio
from solowebapi import SoloWebAPI


async def main():
    api = SoloWebAPI("username", "password")
    is_active = await api.check_license("example_module", 123)
    print("License active:", is_active)
    await api.close()


asyncio.run(main())
```

**Revoke a license:**

```python
import asyncio
from solowebapi import SoloWebAPI


async def main():
    api = SoloWebAPI("username", "password")
    revoked = await api.revoke_license("example_module", 123)
    print("License revoked:", revoked)
    await api.close()


asyncio.run(main())
```

This project is licensed under the [MIT License](LICENSE).