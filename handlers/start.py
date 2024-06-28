from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from utils.states import Start
import keyboard
import sqlite3
import math
import os

router = Router()

@router.message(Start.send)
async def total_message(message: Message, state: FSMContext):
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    sqlite_select_query = f"""SELECT user_id from Stats"""
    cur.execute(sqlite_select_query)
    users_id = cur.fetchall()
    cur.close()
    conn.close()

    for x in users_id:
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace("'", '')
        x = x.replace(',', '')
        tg_token = os.environ["tg_test_token"]
        bot = Bot(str(tg_token))
        await bot.send_message(chat_id=int(x), text=message.text)

    await state.set_state(Start.default)

@router.message(F.text.lower() == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.first_name}!\nЗдесь ты можешь попрактиковаться в орфографии для ЕГЭ.\nДля управления используй встроенную или обычную клавиатуру",
        reply_markup=keyboard.start_kb)

@router.message(F.text.lower() == "/admin")
async def start(message: Message, state: FSMContext):
    await message.answer(
        f'Держи, @srcelomac',
        reply_markup=keyboard.start_kb)

@router.message(F.text.lower() == "/total_message")
async def start(message: Message, state: FSMContext):
    if (int(message.chat.id) == 949342178):
        await message.answer(
            f'Сообщение:\n',
            reply_markup=keyboard.start_kb)
        await state.set_state(Start.send)
