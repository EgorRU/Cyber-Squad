from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher
from client import client
from admin import admin
from other import other
from config import bot
import asyncio


dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(client)
    dp.include_router(admin)
    dp.include_router(other)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())