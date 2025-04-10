"""Модуль где будут хранится клавиатуры"""

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


"""Стандартная Reply клавиатура (выпадающая снизу) 
Тут можно будет описать общие блоки и после выбора инлайнить конкретные запросы из ТЗ"""
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть GitHub проекта'), KeyboardButton(text='О нас')],
    [KeyboardButton(text='test3'), KeyboardButton(text='test4')]
],
    resize_keyboard=True, # Можно выбрать только 2 размера кнопок, это маленькие, если поставить False будут большие
    input_field_placeholder="*Пока тут ничего нет)*") # что будет написанно вместо "Введите сообщение"


"""Пример InLine Клавиатуры со ссылками"""
inline_example = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Git', url='https://github.com/Gouzhurou/animal-shelter-bot')]
])


inline_about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наш Адрес', callback_data='our_address')],
    [InlineKeyboardButton(text='Часы Работы', callback_data='opening_hours'), InlineKeyboardButton(text='наши принципы', callback_data='our_principles')]
])

inline_back_about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_about_us')]
])
