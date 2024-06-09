from aiogram.fsm.state import StatesGroup, State

class Start(StatesGroup):
    mode = State()
    task = State()

class Main_menu(StatesGroup):
    mode = State()
    task = State()
    exercise = State()
    svg = State()
    add = State()