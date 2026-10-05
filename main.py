from confiq import BOT_TOKEN
from aiogram import Bot, Dispatcher
from handlers import router
import logging
import asyncio
import sys

print("=== БОТ ЗАПУСКАЕТСЯ ===", flush=True)
print(f"Токен получен: {bool(BOT_TOKEN)}", flush=True)

bot = Bot(token=str(BOT_TOKEN))
dp = Dispatcher()

async def main():
    print("=== ВХОД В main() ===", flush=True)
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("=== Webhook удалён, начинаю polling ===", flush=True)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"=== КРИТИЧЕСКАЯ ОШИБКА: {e} ===", flush=True)
        raise