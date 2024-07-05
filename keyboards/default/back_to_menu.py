from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад в меню"),
        ],
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
