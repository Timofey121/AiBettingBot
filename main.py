import asyncio

from data.config import ADMINS
from handlers.users.Check import check
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def test(dispatcher):
    while True:
        try:
            await check(dispatcher)
        except Exception as ex:
            print(ex)
        await asyncio.sleep(30)


async def main():
    asyncio.create_task(test(dp))
    await dp.start_polling(on_startup(dp))


if __name__ == '__main__':
    asyncio.run(main())
