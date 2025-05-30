from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from animal_shelter_bot.const.buttons import UserButtons

def get_user_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UserButtons.view_pets)],
            [KeyboardButton(text=UserButtons.my_requests)],
            [KeyboardButton(text=UserButtons.help)],
        ],
        resize_keyboard=True
    )

async def show_user_menu(message):
    await message.answer("👤 Главное меню пользователя:", reply_markup=get_user_menu())