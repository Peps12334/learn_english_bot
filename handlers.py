from confiq import BOT_TOKEN
from words_list import word_list
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
import random
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboard as kb
from aiogram.utils.formatting import Pre


router = Router()

class Ans(StatesGroup):
    users_word = State()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Привет, я бот, который поможет тебе выучить английский!", reply_markup=kb.main)

@router.message(F.text == 'Слово')
async def word(message:Message, state: FSMContext):
    random_word = random.choice(list(word_list.keys()))
    await state.update_data(current_word = random_word)
    await message.answer(random_word)
    await state.set_state(Ans.users_word)

@router.message(Ans.users_word)
async def users_ans(message:Message, state:FSMContext):
    data = await state.get_data()
    en_word = data.get("current_word")
    correct_ru_word = word_list[en_word]
    user_answer = message.text.strip().lower()
    if user_answer == correct_ru_word:
        await message.answer('Правильно!', reply_markup=kb.main)
    else:
        await message.answer(f'Неправильно, правильный перевод - "{correct_ru_word}"', reply_markup=kb.main)

    await state.clear()

@router.message(F.text == 'Список всех слов')
async def show_word_list(message:Message):
    textik = '\n'.join([f'{key} — {value}' for key, value in word_list.items()])
    await message.answer(textik, reply_markup=kb.main)

@router.message()
async def kal(message:Message):
    await message.answer("Я получил твоё сообщение")
