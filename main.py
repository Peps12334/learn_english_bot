from confiq import BOT_TOKEN
from words_list import word_list
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
import random
from handlers import router

bot = Bot(token=str(BOT_TOKEN))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass