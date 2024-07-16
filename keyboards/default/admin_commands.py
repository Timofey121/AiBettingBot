from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_4 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад в меню")
        ],
        [
            KeyboardButton(text="Показать информацию о пользователях!"),
            KeyboardButton(text="Показать кол-во пользователей!")
        ],
        [
            KeyboardButton(text="Отправить пользователям сообщение!")
        ],
        [
            KeyboardButton(text="Заблокировать пользователя!"),
            KeyboardButton(text="Разблокировать пользователя!")
        ],
        [
            KeyboardButton(text="Изменить баланс пользователю!")
        ],

    ],
    resize_keyboard=True
)
