import hashlib
import string
from datetime import datetime, timedelta
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.back_to_menu import buttons_menu
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.done import done
from keyboards.default.get_money import get_money
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_trans, update_balance, delete_trans, select_all_rev, get_lk, \
    update_rev_balance, add_stop, update_only_balance, add_get_money


@dp.message_handler(text="Вывод♻️")
async def GetMoney(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        if len(list(await get_trans(str(message.from_user.id)))) != 0:
            await message.answer(f"""
Бот в работе ❗️
🗣 Дождитесь окончания ставок и нажмите stop.
Только после этого вы сможете пользоваться остальными разделами :
Личный кабинет 
Вывод 
Support""")
        else:
            balance = list(await get_lk(message.from_user.id))[0][1]
            if int(balance) == 0:
                await message.answer(f"""
📲Вывод невозможен 
Баланс: 0
🗣Пополните баланс .""")
            else:
                await message.answer("""
Заказ выплаты 📲
Выберите удобный способ ⤵️
""", reply_markup=get_money)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")


@dp.message_handler(text="Карты (RU,UK,KZ,EU)")
async def GetMoneyCard(message: types.Message):
    await message.answer("Напишите номер Карты ⤵️", reply_markup=buttons_menu)
    await Test.Q_for_get_money.set()


@dp.message_handler(text="Qiwi")
async def GetMoneyQiwi(message: types.Message):
    await message.answer("Напишите номер Qiwi ⤵️", reply_markup=buttons_menu)
    await Test.Q_for_get_money.set()


@dp.message_handler(text="YooMoney")
async def GetMoneyYooMoney(message: types.Message):
    await message.answer("Напишите номер YooMoney ⤵️", reply_markup=buttons_menu)
    await Test.Q_for_get_money.set()


@dp.message_handler(text="Perfect money")
async def GetMoneyPerfect(message: types.Message):
    await message.answer("Напишите номер Perfect money ⤵️", reply_markup=buttons_menu)
    await Test.Q_for_get_money.set()


@dp.message_handler(text="BTC")
async def GetMoneyBTC(message: types.Message):
    await message.answer("Напишите номер BTC ⤵️", reply_markup=buttons_menu)
    await Test.Q_for_get_money.set()


@dp.message_handler(text="⬅️ Назад в меню")
async def GetMoneyBTC(message: types.Message):
    await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)


@dp.message_handler(state=Test.Q_for_get_money)
async def GetMoney1(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад в меню":
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            if len(message.text) != 16:
                await message.answer("Некорретный номер карты", reply_markup=main_keyboard)
                await state.finish()
            else:
                t = int(message.text)
                info = list(await get_lk(message.from_user.id))[0]
                await message.answer(f"""
Введите сумму вывода ♻️
Баланс : {info[1]}""")
                await Test.Q_for_get_money2.set()
        except:
            await message.answer("Некорретный номер карты", reply_markup=main_keyboard)
            await state.finish()


@dp.message_handler(state=Test.Q_for_get_money2)
async def GetMoney2(message: types.Message, state: FSMContext):
    info = list(await get_lk(message.from_user.id))[0]
    try:
        await update_only_balance(message.from_user.id, int(info[1]) - int(message.text))
        time = 15
        end = datetime.now() + timedelta(minutes=int(time))
        await add_get_money(message.from_user.id, end.strftime("%Y-%m-%d %H:%M"))
        await message.answer("""
Вывод создан 🟢
Обработка платежа от 
1 - 10 минут ♻️
В зависимости от загруженности системы ❗️""", reply_markup=main_keyboard)
    except:
        await message.answer("Введена некорректная сумма. Повтори запрос позже", reply_markup=main_keyboard)
    await state.finish()

