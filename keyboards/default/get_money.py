from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_money = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад в меню")
        ],
        [
            KeyboardButton(text="Карты (RU,UK,KZ,EU)")
        ],
        [
            KeyboardButton(text="Qiwi"),
            KeyboardButton(text="YooMoney")
        ],
        [
            KeyboardButton(text=" Perfect money")
        ],
        [
            KeyboardButton(text="BTC")
        ],
    ],
    resize_keyboard=True
)
