from aiogram import types  # подключение модуля для работы с сообщениями

from keyboards.default.buttons_menu import main_keyboard
from loader import dp  # подключение Dispatcher, подключенного к Telegram боту


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    text = (
        "Неизвестная команда, воспользуйтесь меню",
    )

    await message.answer("\n".join(text), reply_markup=main_keyboard)  # вывод текст - ответ на команду
