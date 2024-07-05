from datetime import datetime, timedelta
import random

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hunderline, hlink

from keyboards.default.buttons_menu import main_keyboard
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_lk, add_trans, update_balance, select_all_trans, \
    delete_trans, select_all_rev, update_rev_balance, select_all_stop, delete_stop, get_ct, update_ct, delete_ct, \
    select_all_getmoney, delete_get, get_payment, update_only_balance, delete_payment, get_all_payment

token = "ae83897f7ad94aaeb0e31330932d6c7c"


async def check(dp):
    AllInfo = list(await select_all_trans())
    for itm in AllInfo:
        info = list(await get_lk(itm[0]))[0]
        now = datetime.now()
        end = datetime.strptime(f"{itm[-2]}", "%Y-%m-%d %H:%M")
        if end <= now:
            if int(itm[-1]) == 2:
                rev_people = list(await select_all_rev(itm[0]))
                for id in rev_people:
                    info1 = list(await get_lk(id[0]))[0]
                    await update_rev_balance(id[0], int(int(info1[1]) + int(itm[2]) * 0.08),
                                             int(int(info1[-1]) + int(itm[2]) * 0.08))
                await update_balance(itm[0], str(int(itm[1]) + int(itm[2])), str(int(info[4]) + int(itm[2])),
                                     str(int(info[2]) + 1))
                await delete_trans(itm[0])
                await update_ct(itm[0], int(list(await get_ct(itm[0]))[0][1]) + 1)
                await dp.bot.send_message(itm[0], f"""
АI ставка выиграла ✅
Прибыль: {itm[2]} 
Сделок совершенно: {str(list(await get_ct(itm[0]))[0][1])}
Баланс: {str(int(itm[1]) + int(itm[2]))}
AI анализирует матчи ♻️
Бот оповестит вас когда AI сделает ставку🔘
Нажмите Stop если хотите вывести средства ☑️
""")
                stop = list(await select_all_stop(itm[0]))
                if len(stop) == 0:
                    time = random.randint(3, 8)
                    info = list(await get_lk(itm[0]))[0]
                    profit = int(random.randint(65, 92) / 100 * int(info[1]))
                    end = datetime.now() + timedelta(minutes=int(time))
                    await add_trans(itm[0], info[1], profit, end.strftime("%Y-%m-%d %H:%M"), '1')
                    await update_balance(itm[0], 0, info[-2], info[2])
                    await dp.bot.send_message(itm[0], f"""
AI начал анализ матчей ♻️
Бот оповестит вас когда AI сделает первую ставку🔘
""")
                else:
                    info = list(await get_lk(itm[0]))[0]
                    await delete_ct(itm[0])
                    await dp.bot.send_message(itm[0], f"""
AI остановлен ⚙️
Сделок сделано : {str(list(await get_ct(itm[0]))[0][1])}
Всего сделок сделано : {info[2]}
Прибыль: {info[4]} 
Баланс {info[1]}
Средства готовы к выводу 🟢
Также можете нажать Start и AI продолжит делать ставки ♻️
""")
                    await delete_stop(itm[0])
            else:
                time = random.randint(3, 8)
                profit = int(random.randint(65, 92) / 100 * int(itm[1]))
                end = datetime.now() + timedelta(minutes=int(time))
                await delete_trans(itm[0])
                await add_trans(itm[0], itm[1], profit, end.strftime("%Y-%m-%d %H:%M"), '2')
                await dp.bot.send_message(itm[0], f"""
AI сделал ставку 🟢
Ожидаемая прибыль : {profit}
Сумма ставки : {itm[1]}
Бот оповестит о окончании ставки 🤖
""")

    AllGet = list(await select_all_getmoney())
    for itm in AllGet:
        now = datetime.now()
        end = datetime.strptime(f"{itm[1]}", "%Y-%m-%d %H:%M")
        if end <= now:
            await dp.bot.send_message(itm[0], f"""
🗣Букмекирская контора заблокировала счёт обнаружив работа AI бота и заморозила вывод ❗️
🗣Приносим извинения за предоставленные неудобства , AI уже перенесен на другую БК 🟢
🗣Мы дадим вам бонус 100% на следующие пополнение и бот не возьмёт 20% комиссию за работу на следующий вывод ✅
""")
            await delete_get(itm[0])

    AllPayment = list(await get_all_payment())
    for itm in AllPayment:
        tg_id = itm[0]
        id, summ = list(await get_payment(tg_id))[0][1], list(await get_payment(tg_id))[0][2]
        url = f"https://papi.skycrypto.net/rest/v2/purchases/{str(id)}"
        response = requests.get(url, headers={'Authorization': f'Token {token}'})
        if response.json()["status"] == 1:
            info = list(await get_lk(tg_id))[0]
            balance = info[1]
            await update_only_balance(tg_id, int(balance) + int(summ))
            await delete_payment(tg_id)