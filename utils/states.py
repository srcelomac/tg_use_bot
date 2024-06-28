from aiogram.fsm.state import StatesGroup, State

# class Start(StatesGroup):
#     mode = State()
#     task = State()

class Base(StatesGroup):
    mode = State()
    task = State()
    exercise = State()
    svg = State()
    add = State()
    key = State()
    step = State()
    answer_true = State()
    answer_false = State()
    flag_training = State()
    flag_add = State()
    word_was = State()
    task_id = State()

class Start(StatesGroup):
    default = State()
    send = State()
