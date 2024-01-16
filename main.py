from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
from client import client
from other import other, create_db
from config import bot
import asyncio


dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(client)
    dp.include_router(other)
    await create_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())