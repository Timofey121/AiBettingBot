import random
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_lk, add_trans, update_balance, add_ct


@dp.message_handler(text="Start")
async def StartAi1(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        time = random.randint(5, 10)
        info = list(await get_lk(message.from_user.id))[0]
        if int(info[1]) <= 0:
            await message.answer(f"🗣Для начала работы необходимо пополнить баланс🔘")
        else:
            profit = int(random.randint(50, 80) / 100 * int(info[1]))
            end = datetime.now() + timedelta(minutes=int(time))
            await add_trans(message.from_user.id, info[1], profit, end.strftime("%Y-%m-%d %H:%M"), '1')
            await update_balance(message.from_user.id, 0, info[-2], info[2])
            await message.answer(f"""
AI начал анализ матчей ♻️
Бот оповестит вас когда AI сделает первую ставку🔘
""")
            await add_ct(message.from_user.id)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ! ")
