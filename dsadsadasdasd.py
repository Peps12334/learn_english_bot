import json
from aiogram import Bot, Dispatcher, html
from aiogram.types import Message

# ... инициализация бота и диспетчера ...
dp = Dispatcher()

@dp.message()
async def send_pretty_dict(message: Message):
  my_dict = {
      'status': 'success',
      'user': {'id': 12345, 'username': 'ivan_dev', 'role': 'admin'},
      'permissions': ['read', 'write', 'delete'],
      'metadata': {'ip': '127.0.0.1', 'device': 'Server'},
  }

  # 1. Быстро превращаем словарь в красивую строку с отступами
  # ensure_ascii=False сохраняет русский текст (не превращает его в \u0430)
  formatted_json = json.dumps(my_dict, indent=2, ensure_ascii=False)

  # 2. Оборачиваем в HTML-теги для моноширинного шрифта
  # Использование html.pre_code автоматически экранирует спецсимволы (<, >, &)
  response_text = html.pre_code(formatted_json)

  # 3. Отправляем пользователю (парсинг HTML включен по умолчанию в aiogram 3)
  await message.answer(response_text)
