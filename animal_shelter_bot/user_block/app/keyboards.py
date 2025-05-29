"""Модуль с описанием клавиатур пользователя"""

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from animal_shelter_bot.user_block.const import UserButtons


#Стандартная Reply клавиатура (выпадающая снизу)
#Тут можно будет описать общие блоки и после выбора инлайнить конкретные запросы из ТЗ

main_menu_first_page = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=UserButtons.VIEW_ABOUT_US), KeyboardButton(text=UserButtons.VIEW_ADDRESS),
     KeyboardButton(text=UserButtons.VIEW_OPENING_HOURS)],
    [KeyboardButton(text=UserButtons.VIEW_VISIT_SHELTER),
     KeyboardButton(text=UserButtons.VIEW_HELP_ANIMALS),
     KeyboardButton(text=UserButtons.VIEW_WHAT_SHELTER_NEEDS)],
    [KeyboardButton(text=UserButtons.VIEW_BECOME_A_VOLUNTEER),
     KeyboardButton(text=UserButtons.VIEW_URGENT_HELP),
     KeyboardButton(text=UserButtons.VIEW_NEXT_PAGE_BUTTON)]
],
    resize_keyboard=True,  # Можно выбрать только 2 размера кнопок, это маленькие
    input_field_placeholder="Выберите пункт меню")  # что будет написанно вместо Введите сообщение
