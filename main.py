import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
import string
import sqlite3
import math
import keyboard
from handlers import base, start
import os


conn = sqlite3.connect('tasks.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Tasks (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER, task_id INTEGER, words TEXT, answers TEXT)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('stats.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Stats (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER UNIQUE, rights INTEGER DEFAULT 0, wrongs INTEGER DEFAULT 0)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('training.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Training (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER, rights STRING, wrongs STRING)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('variables.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Variables (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER UNIQUE, step INTEGER DEFAULT 0, answer_true INTEGER DEFAULT 0, answer_false INTEGER DEFAULT 0, task_id INTEGER DEFAULT 0, flag_training BOOLEAN DEFAULT False, flag_add BOOLEAN DEFAULT False, word_was BOOLEAN DEFAULT False)')
conn.commit()
cur.close()
conn.close()


async def main():
    tg_token = os.environ["tg_test_token"]
    bot = Bot(str(tg_token))
    dp = Dispatcher()

    dp.include_routers(start.router)
    dp.include_routers(base.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
