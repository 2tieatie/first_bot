from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from gino import Gino
from data import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from openpyxl import load_workbook
import os


wb = load_workbook(filename='расписание.xlsx')

ws = wb['123']

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

value = 0

# Змінні для гри життя
ON = 255
OFF = 0
vals = [ON, OFF]

cht_game_id = 0

# Список юзерів з правами адміна
admins_id = [
    720207278
]

db = Gino()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

scheduler = AsyncIOScheduler()

scheduler.start()

load_dotenv()

amount_of_users_in_group = 207

# Кнопки у меню з іграми
game_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton('Гра кістки', callback_data='dice'),
     InlineKeyboardButton('Гра дартс', callback_data='dart')],
    [InlineKeyboardButton('Гра баскетбол', callback_data='basketball'),
     InlineKeyboardButton('Гра футбол', callback_data='football')],
    [InlineKeyboardButton('Гра слоти', callback_data='slots'),
     InlineKeyboardButton('Гра боулінг', callback_data='bowling')],
    [InlineKeyboardButton('Головне меню', callback_data='back_to_menu')]])

# Кнопки у головному меню
main_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton('Переглянути команди', callback_data='h_help'),
     InlineKeyboardButton('Надіслати серце', callback_data='s_heart')],
    [InlineKeyboardButton('Зіграти у гру', callback_data='play_game'),
     InlineKeyboardButton('Гра житя', callback_data='g_life')]])

# Кнопки у меня серця
heart_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton('Cерце любові', callback_data='heart'),
     InlineKeyboardButton('Розбите серце', callback_data='heartbroken')],
    [InlineKeyboardButton('Головне меню', callback_data='back_to_menu')]])