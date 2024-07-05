from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from utils.db_api.PostgreSQL import subscriber_exists, get_trans, update_balance, delete_trans, select_all_rev, get_lk, \
    update_rev_balance, add_stop


@dp.message_handler(text="Stop")
async def StartAi1(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        if len(list(await get_trans(str(message.from_user.id)))) == 0:
            await message.answer("К сожалению, у вас пока что нет сделок")
        else:
            await message.answer("""
Уведомление 🟢
Дождитесь пока ставка пройдет и AI автоматически закончит работу📲
""")
            await add_stop(message.from_user.id, 'yes')
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")
