import time
from config import BOT_TOKEN

import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time as tm
import asyncio
from db import Database
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '5995636478:AAEcb2JUzOcrbSxqXAbmeFd9bVXttfReaus'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
buttons_list = []

BlockdUserList = dict()
num, maxx, block = 6, 60, 600


async def userIsBlockd(user_id):
    try:
        user = BlockdUserList[user_id]
        user["messages"] += 1
    except:
        BlockdUserList[user_id] = {"next_time": int(time.time()) + maxx, "messages": 1, "blocked": 0}
        user = BlockdUserList[user_id]
    if user["blocked"] >= int(time.time()):
        return True
    else:
        if user["next_time"] >= int(time.time()):
            if user["messages"] >= num:
                BlockdUserList[user_id]["blocked"] = time.time() + block
                return True
        else:
            BlockdUserList[user_id]["messages"] = 1
            BlockdUserList[user_id]["next_time"] = int(time.time()) + maxx
    return False


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):  # начало работы бота
    if await userIsBlockd(message.from_user.id):
        await message.reply("Блокировка за флуд!")
        return
    kb = [
        [types.KeyboardButton(text='Курсы валют'), ],
        [types.KeyboardButton(text='Информация')],
        [types.KeyboardButton(text='Добавить'), types.KeyboardButton(text='Удалить')],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    data = Database()
    data.add_currencies(message.from_user.id, [14, 15, 19, 23, 43])
    data.connection(message.from_user.id, message.text)
    await message.reply("Привет!\nНапиши мне и я расскажу тебе про все валюты!", reply_markup=keyboard)


@dp.message_handler(text='Информация')
async def process_help_command(message: types.Message):
    if await userIsBlockd(message.from_user.id):
        await message.reply("Блокировка за флуд!")
        return
    await message.reply("Это бот для конвертации валюты и точка\n По всем вопросам писать @missoceane7")
    data = Database()
    data.connection(message.from_user.id, message.text)


@dp.message_handler(lambda message: message.text == 'Удалить')
async def process_remove(message: types.Message):
    # Функция удаления (чистит конкретные данные в базе данных)
    if await userIsBlockd(message.from_user.id):
        await message.reply("Блокировка за флуд!")
        return
    keyboard = types.InlineKeyboardMarkup()
    data = Database()
    global buttons_list
    buttons_list = data.check_currencies(message.from_user.id)
    for element in buttons_list:
        keyboard.add(types.InlineKeyboardButton(text=element, callback_data=element))
    await message.answer("Курсы валют для удаления:", reply_markup=keyboard)
    data.connection(message.from_user.id, message.text)


@dp.message_handler(lambda message: message.text == 'Добавить')
async def process_add(message: types.Message):
    # Функция добавления новых валют
    if await userIsBlockd(message.from_user.id):
        await message.reply("Блокировка за флуд!")
        return
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    data = Database()
    global buttons_list
    buttons_list = data.all_currencies()
    for element in buttons_list:
        keyboard.add(types.InlineKeyboardButton(text=element[0], callback_data=element[0]))
    await message.answer("Курсы валют для добавления:", reply_markup=keyboard)
    data.connection(message.from_user.id, message.text)


@dp.message_handler(lambda message: message.text == 'Курсы валют')
async def process_course(message: types.Message):
    # Вывод выбранных пользователем валют
    if await userIsBlockd(message.from_user.id):
        await message.reply("Блокировка за флуд!")
        return
    keyboard = types.InlineKeyboardMarkup()
    data = Database()
    global buttons_list
    buttons_list = data.check_currencies(message.from_user.id)
    for element in buttons_list:
        keyboard.add(types.InlineKeyboardButton(text=element, callback_data=element))
    await message.answer("Курсы валют:", reply_markup=keyboard)
    data.connection(message.from_user.id, message.text)


@dp.callback_query_handler()
async def process_answer(callback: types.CallbackQuery):
    # Обработка всех inline-кнопок
    data = Database()
    if callback.message.text == "Курсы валют:":
        list_values = await main()
        meaning = list_values['Valute'][(data.correct_currencies(callback.data)[0])]['Value']
        await callback.message.answer(f'Курс {callback.data}: {meaning} ₽')
    elif callback.message.text == "Курсы валют для удаления:":
        await callback.message.reply(data.correct_currencies(callback.data, callback.from_user.id, 'delete'))
    elif callback.message.text == "Курсы валют для добавления:":
        await callback.message.reply(data.correct_currencies(callback.data, callback.from_user.id, 'add'))


async def main():
    # API для работы с курсами cbr(Центральный банк России)
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
            resp = await response.json(content_type=None)
            return resp


if __name__ == '__main__':
    executor.start_polling(dp)
