import asyncio

from aiogram.dispatcher import FSMContext

from keyboards.default.buttons_menu import main_keyboard
from loader import dp

coeff = {
    "rub-kzt": 5.26,
    "kzt-rub": 0.19,
    "rub-uah": 0.4672,
    "uah-rub": 2.14,
    "kzt-uah": 0.0868,
    "uah-kzt": 11.51,
    "uah-uah": 1,
    "rub-rub": 1,
    "kzt-kzt": 1,
}
min_currency = {
    "rub": 1000,
    "usd": 8,
    "kzt": 3000,
    "uah": 500,
    "byn": 20,
    "tjs": 70,
    "azn": 10,
    "uzs": 50000,
}


async def auto_finish_state(id, state: FSMContext):
    await asyncio.sleep(5)
    current_state = await state.get_state()
    if current_state is not None:
        await dp.bot.send_message(id, "Из-за длительного бездействия вы были перенаправлены в главное меню.",
                                  reply_markup=main_keyboard)
        await state.finish()
