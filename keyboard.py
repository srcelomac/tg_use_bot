from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Тренировка"),
            KeyboardButton(text="Моя статистика"),
            KeyboardButton(text="Добавить слово")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

training_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="4"),
            KeyboardButton(text="9"),
            KeyboardButton(text="10"),
            KeyboardButton(text="11"),
            KeyboardButton(text="12"),
            KeyboardButton(text="13"),
            KeyboardButton(text="14"),
            KeyboardButton(text="15")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=True
)

stop_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Стоп")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=True
)