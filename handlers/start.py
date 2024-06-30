from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from utils.states import Start, Base
import keyboard
import sqlite3
import math
import os

async def get_stats(chat_id):
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    cur.execute(f'SELECT COUNT (*) from Stats where user_id = {chat_id}')
    tmp = str(cur.fetchall()[0])
    tmp = tmp.replace('(', '')
    tmp = tmp.replace(')', '')
    tmp = tmp.replace("'", '')
    tmp = tmp.replace(',', '')
    cnt = int(tmp)
    if (cnt == 0):
        cur.execute('INSERT INTO Stats (user_id, rights, wrongs) VALUES (?, ?, ?)',
                    (chat_id, 0, 0))
    conn.commit()
    cur.close()
    conn.close()


router = Router()

@router.message(Start.send)
async def total_message(message: Message, state: FSMContext):
    t = message.text
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    sqlite_select_query = f"""SELECT user_id from Stats"""
    cur.execute(sqlite_select_query)
    users_id = cur.fetchall()
    print(type(users_id))
    cur.close()
    conn.close()

    tg_token = os.environ["tg_test_token"]
    bot = Bot(str(tg_token))

    for i in range(len(users_id)):
        x = str(users_id[i])
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace("'", '')
        x = x.replace(',', '')
        if (x != ''):
            try:
                await bot.send_message(chat_id=int(x), text=t)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {x}: {e}")

    await state.set_state(Start.default)

@router.message(F.text.lower() == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.first_name}!\nЗдесь ты можешь попрактиковаться в орфографии для ЕГЭ.\nДля управления используй встроенную или обычную клавиатуру",
        reply_markup=keyboard.start_kb)
    await get_stats(message.chat.id)
    await state.update_data(key=message.chat.id)
    await state.set_state(Base.mode)

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
