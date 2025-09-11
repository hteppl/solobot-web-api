<p align="center">
  <img src="https://pocomacho.ru/static/images/bot_mobile.png" alt="logo-main" height="400">
</p>

# solobot-web-api

[![LICENSE](https://img.shields.io/pypi/l/solobot-web-api)](LICENSE)
[![Supported Versions](https://img.shields.io/pypi/pyversions/aiohttp.svg)](https://pypi.org/project/solobot-web-api)
[![PyPI Version](https://img.shields.io/pypi/v/solobot-web-api?color=%23e04f1f)](https://pypi.org/project/solobot-web-api)

#### Клиент для взаимодействия с АПИ [SoloBot Web API](https://github.com/Vladless/Solo_bot/).

Powered by [🥕 Морковный Бот](https://t.me/morkowniy_bot)

## Установка

Библиотека `solobot-web-api` доступна для скачивания через PyPI:

```console
$ python -m pip install solobot-web-api
```

Библиотека работает на версии Python 3.9+ и использует `aiohttp`.

## Версия АПИ и документация

Базовый апи эндпоинт: `https://pocomacho.ru/solonetbot/api/v1/modules`

Официальные примеры использования и документация: https://pocomacho.ru/solonetbot/api/swagger

## Примеры

Вы можете найти примеры схем в документации: https://pocomacho.ru/solonetbot/api/openapi.json

**Выдать лицензию пользователю:**

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

**Проверить, активна ли лицензия:**

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

**Отозвать лицензию:**

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

**Загрузить ZIP архив проекта:**

```python
# в разработке
```

Этот проект использует лицензию [MIT](../LICENSE).