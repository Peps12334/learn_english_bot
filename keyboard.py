from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список всех слов')],
    [KeyboardButton(text='Слово')]
], resize_keyboard = True)