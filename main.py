import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.main_handler import register_handlers_main

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_handlers_main(dp)

    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
from aiogram import types, Router
from aiogram.filters import Command