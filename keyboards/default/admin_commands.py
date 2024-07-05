from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_4 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Показать кол-во пользователей!")
        ],
        [
            KeyboardButton(text="Показать полный список пользователей!")
        ],
        [
            KeyboardButton(text="Показать уведомления пользователей!")
        ],
        [
            KeyboardButton(text="Заблокировать пользователя!")
        ],
        [
            KeyboardButton(text="Разблокировать пользователя!")
        ],
        [
            KeyboardButton(text="Отправить пользователям сообщение!")
        ],
        [
            KeyboardButton(text="Посмотреть все технические ошибки!")
        ],
        [
            KeyboardButton(text="Удалить выполненные тех. ошибки!")
        ],
        [
            KeyboardButton(text="Посмотреть все отзывы!")
        ],
        [
            KeyboardButton(text="Отчистить БД от отзывов!")
        ],
        [
            KeyboardButton(text="Количество олимпиад в Базе Данных!")
        ],
        
    ],
    resize_keyboard=True  # размер кнопки(не огромный)
)
