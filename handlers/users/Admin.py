from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from data.config import ADMINS, CREATOR
from keyboards.default.admin_commands import keyboard_4
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.back_to_menu import buttons_menu
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import select_all_users, count_users, subscriber_exists, select_blocked_users, \
    update_blocked_users, get_lk, update_only_balance


@dp.message_handler(Command("admin"))
async def notification(message: types.Message):
    if str(message.from_user.id) in ADMINS or str(message.from_user.id) in CREATOR:
        await message.answer('Выберите нужную команду (cм.ниже).', reply_markup=keyboard_4)
        await Test.Q_for_admin_1.set()
    else:
        text = ("Неизвестная команда, воспользуйтесь меню",
                )
        await message.answer("\n".join(text), reply_markup=main_keyboard)


@dp.message_handler(state=Test.Q_for_admin_1)
async def answer(message: types.Message, state: FSMContext):
    try:
        if message.text == "Показать информацию о пользователях!":
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                balance = list(await get_lk(dat[i][1]))[0][1]
                if len(str("\n".join(c[t]))) + len(
                        str(f"Пользователь {dat[i][2]} (ID = {dat[i][1]}) -> Баланс = {balance}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][2]} (ID = {dat[i][1]}) -> Баланс = {balance}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Показать кол-во пользователей!":
            await message.answer(f"Привет админ! В боте - {list(await count_users())[0][0]} пользователей!",
                                 reply_markup=main_keyboard)
            await state.finish()

        elif message.text == "Заблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_all_users())
            await message.answer(f"Полный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=buttons_menu)
            await Test.Q_for_admin_2.set()

        elif message.text == "Разблокировать пользователя!":
            await message.answer(f"Введите id пользователя, которого хотите заблокировать",
                                 reply_markup=ReplyKeyboardRemove())
            dat = list(await select_blocked_users())
            c = [[]]
            t = 0
            if len(dat) == 0:
                await message.answer(f'Заблокированных пользователей нет!', reply_markup=main_keyboard)
                await state.finish()
            else:
                await message.answer(f"Полный список заблокированных пользователей:")
                for i in range(len(dat)):
                    if len(str("\n".join(c[t]))) + len(str(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")) > 4096:
                        t += 1
                        c.append([])
                    c[t].append(f"Пользователь {dat[i][2]} -> ID = {dat[i][1]}")
                for i in range(len(c)):
                    await message.answer("\n".join(c[i]), reply_markup=buttons_menu)
                await Test.Q_for_admin_3.set()

        elif message.text == "Отправить пользователям сообщение!":
            await message.answer(f"Введите сообщение для пользователей!", reply_markup=buttons_menu)
            await Test.Q_for_admin_4.set()

        elif message.text == "Изменить баланс пользователю!":
            dat = list(await select_all_users())
            await message.answer(
                f"Введите ID пользователя, котрому хотите изменить баланс\nПолный список пользователей:")
            c = [[]]
            t = 0
            for i in range(len(dat)):
                balance = list(await get_lk(dat[i][1]))[0][1]
                if len(str("\n".join(c[t]))) + len(
                        str(f"Пользователь {dat[i][2]} (ID = {dat[i][1]}) -> Баланс = {balance}")) > 4096:
                    t += 1
                    c.append([])
                c[t].append(f"Пользователь {dat[i][2]} (ID = {dat[i][1]}) -> Баланс = {balance}")
            for i in range(len(c)):
                await message.answer("\n".join(c[i]), reply_markup=buttons_menu)
            await Test.Q_for_admin_5.set()

    except Exception as ex:
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_5)
async def block2(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        await state.update_data(TgId=message.text)
        await message.answer(f"Введите новый баланс пользователя!", reply_markup=buttons_menu)
        await Test.Q_for_admin_6.set()


@dp.message_handler(state=Test.Q_for_admin_6)
async def block2(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        data = await state.get_data()
        TgId = data.get("TgId")
        NewBalance = message.text
        await update_only_balance(TgId, NewBalance)
        await message.answer(f"Баланс пользователя с Id = {TgId} изменен на {NewBalance}", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_2)
async def block2(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            await update_blocked_users(message.text, 1)
            await message.answer(
                f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - ЗАБЛОКИРОВАН",
                reply_markup=main_keyboard)
        except Exception as ex:
            print(ex)
            await message.answer("Такого пользователя не существует!", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_3)
async def block3(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        try:
            await update_blocked_users(message.text, 0)
            await message.answer(
                f"Пользователь {list(await subscriber_exists(message.text))[0][1]} -> ID = {message.text} - РАЗБЛОКИРОВАН",
                reply_markup=main_keyboard)
        except:
            await message.answer("Такого пользователя не существует!", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(state=Test.Q_for_admin_4)
async def block4(message: types.Message, state: FSMContext):
    if message.text == '⬅️ Назад в меню':
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        dat = list(await select_all_users())
        for i in range(len(dat)):
            try:
                await dp.bot.send_message(f'{dat[i][1]}', message.text)
            except:
                pass
        await state.finish()
