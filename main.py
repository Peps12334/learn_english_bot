from confiq import BOT_TOKEN
from aiogram import Bot, Dispatcher, F, Router
import logging
from handlers import router
from database import init_db
from middlewares import DbSessionMiddleware

bot = Bot(token=str(BOT_TOKEN))
dp = Dispatcher()

async def main():
    await init_db()
    dp.update.middleware(DbSessionMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass