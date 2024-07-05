from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

done = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Проверить оплату")
        ],
        [
            KeyboardButton(text="Отмена платежа")
        ],
    ],
    resize_keyboard=True
)
