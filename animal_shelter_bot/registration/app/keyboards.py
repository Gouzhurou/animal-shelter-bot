"""Модуль с описанием клавиатур для регистрации"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from animal_shelter_bot.registration.const import RegistrationButtons
from animal_shelter_bot.user_block.app import keyboards as ukb

# Клавиатура с контактами
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=RegistrationButtons.GET_NUMBER)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def get_main_menu():
    """Возвращает главное меню из модуля user_block"""
    # Если клавиатуры еще не загружены, загружаем их
    if not ukb.reply_keyboards:
        ukb.load_reply_keyboards()

    return ukb.create_reply_markup("main_menu_first_page")