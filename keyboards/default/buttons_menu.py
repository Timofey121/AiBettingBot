from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Start"),
            KeyboardButton(text="Stop"),
        ],
        [
            KeyboardButton(text="Личный кабинет 💻"),
            KeyboardButton(text="Установить валюту💱"),
        ],
        [
            KeyboardButton(text="📲Пополнение"),
            KeyboardButton(text="Вывод♻️"),
        ],
        [
            KeyboardButton(text="Support🧑‍💻"),
        ],
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
