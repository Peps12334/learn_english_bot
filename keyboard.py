from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список всех слов'), KeyboardButton(text='Добавить слово')],
    [KeyboardButton(text='Слово'), KeyboardButton(text='Статистика')]
], resize_keyboard = True)