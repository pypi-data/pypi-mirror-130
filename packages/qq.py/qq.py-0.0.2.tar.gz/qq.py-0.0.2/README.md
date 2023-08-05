# QQ.py

用 Python 编写的用于 QQ频道机器人 现代化、易于使用、功能丰富(? 且异步的 API sdk。

## 主要特点

- 使用 ``async`` 和 ``await`` 的现代 Pythonic API。

## 快速示例
```python
import asyncio
from qq import *


async def main():
    client = Client('BotAppID', 'Bot Token')
    guild_lsit = await client.get_all_guid()
    for guilds in guild_lsit:
        guilds = await client.get_guild(guilds.id)
        print(guilds.name)

if __name__ == '__main__':
    asyncio.run(main())
```
输出Bot当前加入的所有频道的名字