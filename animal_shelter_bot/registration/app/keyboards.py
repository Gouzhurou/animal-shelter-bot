"""Модуль с описанием клавиатур для регистрации"""

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from animal_shelter_bot.registration.const import RegistrationButtons

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=RegistrationButtons.GET_NUMBER)]],
    resize_keyboard=True,
    one_time_keyboard=True)
