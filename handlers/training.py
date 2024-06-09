from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

import keyboard

router = Router()

@router.message(F.text.lower() == "тренировка")
async def training(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=keyboard.training_kb
    )

#@router.message(F.text.lower() == "моя статистика")
#async def stats(message: Message):
#    await message.answer(
#        "Жаль...",
#    )

@router.message(F.text.lower() == "добавить слово")
async def stats(message: Message):
    await message.answer(
        "Жаль...tra",
        reply_markup=keyboard.training_kb
    )