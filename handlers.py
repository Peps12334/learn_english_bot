from confiq import BOT_TOKEN
from words_list import word_list, hard_words, easy_words
from models import Word, User
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
import random
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboard as kb
import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


right_words = 0
wrong_words = 0

router = Router()

class Ans(StatesGroup):
    users_word = State()
    
class Add_word(StatesGroup):
    new_word_en = State()
    new_word_ru = State()
    
def save_word_to_file(en_word: str, ru_word: str):
    word_list[en_word] = ru_word



async def get_or_create_user(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user



@router.message(CommandStart())
async def start(message:Message, session: AsyncSession):
    await get_or_create_user(session, message.from_user.id)
    await message.answer("Привет, я бот, который поможет тебе выучить английский!", reply_markup=kb.main)

@router.message(F.text == 'Слово')
async def word(message:Message, state: FSMContext, session: AsyncSession):
    telegram_id = message.from_user.id
    user_name = await session.execute(select(User.id).where(User.telegram_id == telegram_id))
    user_id = user_name.scalar_one_or_none()
    result = await session.execute(select(Word).where(Word.user_id == user_id))
    words = result.scalars().all()
    if not words:
        await message.answer("В базе нет слов. Добавь первое через «Добавить слово».")
        return
    random_word = random.choice(words)
    await state.update_data(current_word_id = random_word.id)
    await message.answer(random_word.en)
    await state.set_state(Ans.users_word)
    
@router.message(Ans.users_word)
async def users_ans(message:Message, state:FSMContext, session: AsyncSession):
    data = await state.get_data()
    en_word = data.get("current_word_id")
    result = await session.execute(select(Word). where (Word.id == en_word))
    word_list_db = result.scalar_one_or_none()
    user = await get_or_create_user(session, message.from_user.id)
    user_answer = message.text.strip().lower()

    if word_list_db and user_answer == word_list_db.ru.lower():
        user.right_answers += 1
        await message.answer('Правильно!', reply_markup=kb.main)
    else:
        user.wrong_answers += 1
        await message.answer(f'Неправильно, правильный перевод - "{word_list_db.ru}"', reply_markup=kb.main)
    await session.commit()
    await state.clear()

@router.message(F.text == 'Список всех слов')
async def show_word_list(message:Message, session: AsyncSession):
    telegram_id = message.from_user.id
    user_name = await session.execute(select(User.id).where(User.telegram_id == telegram_id))
    user_id = user_name.scalar_one_or_none()
    result = await session.execute(select(Word).where(Word.user_id == user_id))
    words = result.scalars().all()
    if not words:
        await message.answer("Список пуст", reply_markup=kb.main)
        return
    textik = '\n'.join(f'{word_list_db.en} — {word_list_db.ru}' for word_list_db in words)
    await message.answer(textik, reply_markup=kb.main)


@router.message(F.text == 'Добавить слово')
async def add_word1(message:Message, state:FSMContext):
    await state.set_state(Add_word.new_word_ru)
    await message.answer('Введите новое свлово на русском')

@router.message(Add_word.new_word_ru)
async def add_word2(message:Message, state:FSMContext):
    await state.update_data(new_word_ru = message.text.strip().lower())
    await state.set_state(Add_word.new_word_en)
    await message.answer('Введите новое слово на английском')

@router.message(Add_word.new_word_en)
async def add_word3(message:Message, state:FSMContext, session: AsyncSession):
    data =  await state.get_data()
    english_new_word = message.text.strip().lower()
    russian_new_word = data.get('new_word_ru')

    telegram_id = message.from_user.id
    
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    exists = await session.execute(select(Word).where(Word.en == english_new_word))
    if exists.scalar_one_or_none():
        await message.answer('Такое слово уже есть в списке!', reply_markup=kb.main)
        await state.clear()
        return
    
    session.add(Word(en=english_new_word, ru=russian_new_word, user_id=user.id))
    await session.commit()
    await message.answer('Новое слово успешно добавлено!', reply_markup=kb.main)
    await state.clear()


@router.message(F.text == 'Статистика')
async def stats(message:Message, session: AsyncSession):
    telegram_id = message.from_user.id
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    stats = result.scalar_one_or_none()
    await message.answer(f'Количество правильных ответов: {stats.right_answers}\nКоличество неправильных ответов: {stats.wrong_answers}\nПроцент верных ответов: {math.trunc(stats.right_answers/(stats.right_answers+stats.wrong_answers)*100)}%', reply_markup=kb.main)
    