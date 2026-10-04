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
    
class Add_word(StatesGroup):
    new_word_en = State()
    new_word_ru = State()
    
def save_word_to_file(en_word: str, ru_word: str):
    word_list[en_word] = ru_word

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


@router.message(F.text == 'Добавить слово')
async def add_word1(message:Message, state:FSMContext):
    await state.set_state(Add_word.new_word_ru)
    await message.answer('Введите новое свлово на русском')

@router.message(Add_word.new_word_ru)
async def add_word2(message:Message, state:FSMContext):
    await state.update_data(new_word_ru = message.text)
    await state.set_state(Add_word.new_word_en)
    await message.answer('Введите новое свлово на английском')

@router.message(Add_word.new_word_en)
async def add_word3(message:Message, state:FSMContext):
    await state.update_data(new_word_en = message.text)
    data =  await state.get_data()
    english_new_word = data.get('new_word_en')
    russian_new_word = data.get('new_word_ru')
    word_list[english_new_word] = russian_new_word
    await message.answer('Новое слово успешно добавлено!')


@router.message()
async def kal(message:Message):
    await message.answer("Я получил твоё сообщение")