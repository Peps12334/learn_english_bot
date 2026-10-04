from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список всех слов'), KeyboardButton(text='Добавить слово')],
    [KeyboardButton(text='Слово')]
], resize_keyboard = True)