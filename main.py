from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '5995636478:AAEcb2JUzOcrbSxqXAbmeFd9bVXttfReaus'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Buttons menu
menu = InlineKeyboardMarkup(row_width=1)
menu_well = InlineKeyboardButton(text='Курсы валют')
menu.add(menu_well)
курс

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['info'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler(commands=['well'])
async def process_well_command(message: types.Message):
    await message.reply("Курсы", reply_markup=menu)


if __name__ == '__main__':
    executor.start_polling(dp)
