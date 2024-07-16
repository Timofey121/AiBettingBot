import hashlib
import string
from datetime import datetime, timedelta
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink
import os, shutil

from data.config import SkyPayToken
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.currency import currency
from keyboards.default.done import done
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_trans, update_balance, delete_trans, select_all_rev, get_lk, \
    update_rev_balance, add_stop, add_summ, get_payment, update_only_balance, delete_payment, get_currency, \
    add_currency, update_currency

coeff = {
    "rub-kzt": 5.26,
    "kzt-rub": 0.19,
    "rub-uah": 0.4672,
    "uah-rub": 2.14,
    "kzt-uah": 0.0868,
    "uah-kzt": 11.51,
    "uah-uah": 1,
    "rub-rub": 1,
    "kzt-kzt": 1,
}


@dp.message_handler(text="Установить валюту♻️")
async def GetMoney(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        if len(list(await get_currency(message.from_user.id))) == 0:
            await add_currency(message.from_user.id, "rub")
        await message.answer("Выберите подходящую Вам валюту", reply_markup=currency)
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")


@dp.message_handler(text="🇷🇺Рубли")
async def GetMoneyCard(message: types.Message):
    balance = list(await get_lk(message.from_user.id))[0][1]
    curr = list(await get_currency(message.from_user.id))[0][1]
    await update_only_balance(message.from_user.id, int(coeff[f"{curr}-rub"] * int(balance)))
    await message.answer(f"Валюта обновлена на 🇷🇺Рубли", reply_markup=main_keyboard)
    await update_currency(message.from_user.id, "rub")


# @dp.message_handler(text="🇺🇿Uz сум")
# async def GetMoneyCard(message: types.Message):
#     await message.answer(f"Валюта обновлена на 🇺🇿Uz сум", reply_markup=main_keyboard)
#     await update_currency(message.from_user.id, "uzs")


@dp.message_handler(text="🇰🇿Kz тенге")
async def GetMoneyCard(message: types.Message):
    balance = list(await get_lk(message.from_user.id))[0][1]
    curr = list(await get_currency(message.from_user.id))[0][1]
    await update_only_balance(message.from_user.id, int(coeff[f"{curr}-kzt"] * int(balance)))
    await message.answer(f"Валюта обновлена на 🇰🇿Kz тенге", reply_markup=main_keyboard)
    await update_currency(message.from_user.id, "kzt")


@dp.message_handler(text="🇺🇦Uk гривна")
async def GetMoneyCard(message: types.Message):
    balance = list(await get_lk(message.from_user.id))[0][1]
    curr = list(await get_currency(message.from_user.id))[0][1]
    await update_only_balance(message.from_user.id, int(coeff[f"{curr}-uah"] * int(balance)))
    await message.answer(f"Валюта обновлена на 🇺🇦Uk гривна", reply_markup=main_keyboard)
    await update_currency(message.from_user.id, "uah")

# @dp.message_handler(text="🇧🇾Bel рубль")
# async def GetMoneyCard(message: types.Message):
#     await message.answer(f"Валюта обновлена на 🇧🇾Bel рубль", reply_markup=main_keyboard)
#     await update_currency(message.from_user.id, "byn")


# @dp.message_handler(text="🇹🇯Tj Самони")
# async def GetMoneyCard(message: types.Message):
#     await message.answer(f"Валюта обновлена на 🇹🇯Tj Самони", reply_markup=main_keyboard)
#     await update_currency(message.from_user.id, "tjs")
