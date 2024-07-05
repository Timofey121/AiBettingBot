import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, get_lk


@dp.message_handler(text="Личный кабинет 💻")
async def StartAi1(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        info = list(await get_lk(message.from_user.id))[0]
        await message.answer(f"""
Личный кабинет 
Ваш ID : {message.from_user.id}
Баланс : {info[1]}
Прибыль от AI : {info[4]}
Сделок совершенно: {info[2]}
Revshare balance : {int(info[5])}
Ваш revshare link: {info[3]}
Получай 8% с доходов приведенных друзей♻️
""")
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! Для уточнения причины напишите @Timofey1566")
