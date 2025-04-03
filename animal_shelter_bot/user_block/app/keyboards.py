"""Модуль с описанием клавиатур пользователя"""

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
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


"""Пример InLine Клавиатуры со ссылками"""
inline_example = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Git', url='https://github.com/Gouzhurou/animal-shelter-bot')]
])


inline_about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наш Адрес', callback_data='our_address')],
    [InlineKeyboardButton(text='Часы Работы', callback_data='opening_hours'),
     InlineKeyboardButton(text='наши принципы', callback_data='our_principles')]
])

inline_back_about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_about_us')]
])
