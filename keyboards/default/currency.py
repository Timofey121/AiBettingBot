from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


currency = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇷🇺Рубли"),
            # KeyboardButton(text="🇺🇿Uz сум"),
        ],
        [
            KeyboardButton(text="🇰🇿Kz тенге"),
            KeyboardButton(text="🇺🇦Uk гривна"),
        ],
        # [
        #     KeyboardButton(text="🇧🇾Bel рубль"),
        #     KeyboardButton(text="🇹🇯Tj Самони"),
        # ],
    ],
    resize_keyboard=True
)
