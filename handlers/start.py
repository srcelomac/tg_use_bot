from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from utils.states import Start
import keyboard
import sqlite3
import math

router = Router()
step = 0
answer_true = 0
answer_false = 0
task_id = 0

async def stats(message: Message):
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    sqlite_select_query = f"""SELECT rights from Stats where user_id = {message.chat.id}"""
    cur.execute(sqlite_select_query)
    right = str(cur.fetchall()[0])
    sqlite_select_query = f"""SELECT wrongs from Stats where user_id = {message.chat.id}"""
    cur.execute(sqlite_select_query)
    wrong = str(cur.fetchall()[0])
    right = right.replace('(', '')
    right = right.replace(')', '')
    right = right.replace("'", '')
    right = right.replace(',', '')
    wrong = wrong.replace('(', '')
    wrong = wrong.replace(')', '')
    wrong = wrong.replace("'", '')
    wrong = wrong.replace(',', '')
    # print(right)
    # print(wrong)
    cor = int(right)
    uncor = int(wrong)
    cur.close()
    conn.close()
    if (cor + uncor == 0):
        await message.answer(
            "Ты пока не выполнил ни одного задания :(",
            reply_markup=keyboard.start_kb
        )
    else:
        await message.answer(
            f'Ты сделал верно {cor} из {cor + uncor} заданий ({math.ceil(cor / (cor + uncor) * 100)}%). Что-то ещё?',
            reply_markup=keyboard.start_kb
        )

async def training(message):
    '''
    try:
        global task_id
        global step
        global answer_true
        global answer_false
        global task_words
        if (step == 0):
            if (message.text.lower() == "стоп" or message.text.strip() == "Стоп"):
                # main_menu(message)
                # print("Выход")
                # bot.register_next_step_handler(message, main_menu)
                step = 0
                task_id = 0
                task_words = []
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Ты сделал верно {answer_true} из {answer_true + answer_false} заданий. Что-то ещё?',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            else:
                conn = sqlite3.connect('tasks.db')
                cur = conn.cursor()
                #print(task_id)
                sqlite_select_query = f"""SELECT words from Tasks where (user_id = {message.chat.id} and task_id = {task_id})"""
                cur.execute(sqlite_select_query)
                # cur.execute(f"SELECT words * FROM Tasks * WHERE user_id = {message.chat.id}")
                list_of_words = cur.fetchall()
                sqlite_select_query = f"""SELECT answers from Tasks where (user_id = {message.chat.id} and task_id = {task_id})"""
                cur.execute(sqlite_select_query)
                list_of_answers = cur.fetchall()
                cur.close()
                conn.close()
                for i in range(len(list_of_words)):
                    s1 = str(list_of_words[i])
                    s1 = s1.replace('(', '')
                    s1 = s1.replace(')', '')
                    s1 = s1.replace("'", '')
                    s1 = s1.replace(',', '')
                    s2 = str(list_of_answers[i])
                    s2 = s2.replace('(', '')
                    s2 = s2.replace(')', '')
                    s2 = s2.replace("'", '')
                    s2 = s2.replace(',', '')
                    task_words.append([s1, s2])
                    #print(s1)
                    #print(s2)
                #print(task_words)
                task_words = task_words + tasks_new_common[task_id - 9]
                random.shuffle(task_words)
                markup = types.ReplyKeyboardMarkup()
                btn_stop = types.KeyboardButton('Стоп')
                markup.row(btn_stop)
                if (len(task_words) == 0):
                    bot.send_message(message.chat.id, "Список пуст")
                    step = 0
                    task_id = 0
                    markup = types.ReplyKeyboardMarkup()
                    btn1 = types.KeyboardButton('Тренировка')
                    btn2 = types.KeyboardButton('Моя статистика')
                    btn3 = types.KeyboardButton('Добавить слово')
                    markup.row(btn1, btn2, btn3)
                    bot.send_message(message.chat.id, "Что-то ещё?",
                                     reply_markup=markup)
                    bot.register_next_step_handler(message, on_click)
                else:
                    bot.send_message(message.chat.id, "Напиши букву, которая должна стоять на месте пропуска\nПр_рогатива -> е")
                    bot.send_message(message.chat.id, task_words[step][0], reply_markup=markup)
                    step += 1
                    bot.register_next_step_handler(message, training)
        elif (step > 0):
            if (message.text.lower() == "стоп" or message.text.strip() == "Стоп"):
                # main_menu(message)
                # print("Выход")
                # bot.register_next_step_handler(message, main_menu)
                step = 0
                task_id = 0
                task_words = []
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('Тренировка')
                btn2 = types.KeyboardButton('Моя статистика')
                btn3 = types.KeyboardButton('Добавить слово')
                markup.row(btn1, btn2, btn3)
                bot.send_message(message.chat.id,
                                 f'Ты сделал верно {answer_true} из {answer_true + answer_false} заданий. Что-то ещё?',
                                 reply_markup=markup)
                answer_true = 0
                answer_false = 0
                bot.register_next_step_handler(message, on_click)
            elif (message.text.strip().lower() == task_words[step - 1][1].lower()):
                #print(message.text.strip().lower())
                #print(task_words[step - 1][1].lower())
                #print("-----------------")
                bot.send_message(message.chat.id, "Верно!")
                answer_true += 1
                conn = sqlite3.connect('stats.db')
                cur = conn.cursor()
                sqlite_select_query = f"""UPDATE Stats SET rights = rights + 1 where user_id = {message.chat.id}"""
                cur.execute(sqlite_select_query)
                conn.commit()
                cur.close()
                conn.close()
                if (step >= len(task_words)):
                    step = 0
                    markup = types.ReplyKeyboardMarkup()
                    btn1 = types.KeyboardButton('Тренировка')
                    btn2 = types.KeyboardButton('Моя статистика')
                    btn3 = types.KeyboardButton('Добавить слово')
                    markup.row(btn1, btn2, btn3)
                    bot.send_message(message.chat.id,
                                     f'Слова закончились. Ты молодец!\n Ты сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                     reply_markup=markup)
                    answer_true = 0
                    answer_false = 0
                    task_words = []
                    bot.register_next_step_handler(message, on_click)
                else:
                    bot.send_message(message.chat.id, task_words[step][0])
                    step += 1
                    # print('yep')
                    bot.register_next_step_handler(message, training)
            else:
                # answer = req_gptshka(task_4[step-1][1])
                # answer = subject_selection(message.text)
                # bot.send_message(message.chat.id, f'Неверно! \nПравильный ответ: {task_4[step-1][1]} \nПопробуй запомнить так: {answer}')
                #print(message.text.strip()[1:-1:], task_words[step - 1][1][1:-1:])
                bot.send_message(message.chat.id,
                                 f'Неверно! \nПравильный ответ: {task_words[step - 1][1]}')
                answer_false += 1
                conn = sqlite3.connect('stats.db')
                cur = conn.cursor()
                sqlite_select_query = f"""UPDATE Stats SET wrongs = wrongs + 1 where user_id = {message.chat.id}"""
                cur.execute(sqlite_select_query)
                conn.commit()
                cur.close()
                conn.close()
                if (step >= len(task_words)):
                    step = 0
                    markup = types.ReplyKeyboardMarkup()
                    btn1 = types.KeyboardButton('Тренировка')
                    btn2 = types.KeyboardButton('Моя статистика')
                    btn3 = types.KeyboardButton('Добавить слово')
                    markup.row(btn1, btn2, btn3)
                    bot.send_message(message.chat.id,
                                     f'Слова закончились. Ты молодец!\nТы сделал верно {answer_true} из {answer_true + answer_false} заданий.',
                                     reply_markup=markup)
                    answer_true = 0
                    answer_false = 0
                    task_words = []
                    bot.register_next_step_handler(message, on_click)
                else:
                    bot.send_message(message.chat.id, task_words[step][0])
                    step += 1
                    # print("no")
                    bot.register_next_step_handler(message, training)
    except Exception as exp:
        print("ERROR training", exp)
    '''

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(Start.mode)
    await message.answer(f"Привет, {message.from_user.first_name}!\nЗдесь ты можешь попрактиковаться в орфографии для ЕГЭ.\nДля управления используй встроенную или обычную клавиатуру", reply_markup=keyboard.start_kb)
    conn = sqlite3.connect('stats.db')
    cur = conn.cursor()
    cur.execute(f'SELECT COUNT (*) from Stats where user_id = {message.chat.id}')
    tmp = str(cur.fetchall()[0])
    tmp = tmp.replace('(', '')
    tmp = tmp.replace(')', '')
    tmp = tmp.replace("'", '')
    tmp = tmp.replace(',', '')
    # print(tmp)
    cnt = int(tmp)
    if (cnt == 0):
        cur.execute('INSERT INTO Stats (user_id, rights, wrongs) VALUES (?, ?, ?)',
                    (message.chat.id, 0, 0))
    conn.commit()
    cur.close()
    conn.close()

@router.message(Start.mode)
async def start_mode(message: Message, state: FSMContext):
    await state.update_data(mode=message.text)
    if (message.text.lower() == 'моя статистика'):
        data = await state.get_data()
        await state.clear()
        await state.set_state(Start.mode)
        await stats(message)
    else:
        await state.set_state(Start.task)
        markup = keyboard.training_kb
        await message.answer(
            f'Каким заданием хочешь заняться?',
            reply_markup=markup
        )

@router.message(Start.task)
async def start_mode(message: Message, state: FSMContext):
    if (message.text.isdigit()):
        await state.update_data(task=message.text)
    else:
        await message.answer(
            f'Укажи номер задания',
        )


#@router.message(F.text.lower() == "добавить слово")
#async def stats(message: Message):
#    await message.answer(
#        "добавить слово.",
#        reply_markup=keyboard.training_kb
#    )