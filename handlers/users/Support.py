# -*- coding: utf8 -*-

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default.buttons_menu import main_keyboard
from keyboards.default.back_to_menu import buttons_menu
from loader import dp
from states import Test
from utils.db_api.PostgreSQL import subscriber_exists, get_trans


@dp.message_handler(text="Support🧑‍💻", state=None)
async def technical_support(message: types.Message):
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
            if message.from_user.username is None:
                await message.answer(f"Привет, к сожалению, мы не сможем ответить Вам, т.к. у Вас нет имени пользователя!"
                                     f"Укажите пожалуйста его в настройках, чтобы мы смогли с Вами связаться!")
                photo = open('handlers/users/img.png', 'rb')
                await message.answer_photo(photo, reply_markup=main_keyboard)
            else:
                await message.answer("Привет, расскажи в чем проблема? Мы ответим Вам, как только закончим"
                                     " с предыдущем вопросом!", reply_markup=buttons_menu)
                await Test.Q_for_tech_support.set()
    else:
        await message.answer(f"К сожалению, Вы ЗАБЛОКИРОВАНЫ!")


@dp.message_handler(state=Test.Q_for_tech_support)
async def technical_support_1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "⬅️ Назад в меню":
        await message.answer('Вы вернулись в меню', reply_markup=main_keyboard)
        await state.finish()
    else:
        await message.answer("Ваша проблема принята. Мы свяжемся с Вами в ближайшее время.", reply_markup=main_keyboard)
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin,
                                          f"Сообщение о технической поддержки для админов:\n"
                                          f"Full_name = {message.from_user.full_name}\n"
                                          f"is_bot = {'Не бот!' if message.from_user.is_bot is False else 'Бот!'}\n"
                                          f"User_name = @{'Нет значения' if message.from_user.username is None else message.from_user.username}\n"
                                          f"id = {message.from_user.id}\n"
                                          f"Language = {message.from_user.language_code}\n\n"
                                          f"Его просьба:\n"
                                          f"{answer}")
            except Exception as err:
                pass
        await state.finish()
