from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_buttons_choose = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вывести все!", callback_data="Информация-Вывести-все")
        ],
        [
            InlineKeyboardButton(text="Вывести олимпиады, входящие в РСОШ!", callback_data="Информация-Вывести-РСОШ")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="⬅️ Назад в меню")
        ]
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
