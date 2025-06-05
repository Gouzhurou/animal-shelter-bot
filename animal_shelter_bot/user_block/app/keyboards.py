"""Модуль с описанием клавиатур пользователя"""

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from animal_shelter_bot.user_block.const import UserButtons, UserLinks
import json
import os


#Стандартная Reply клавиатура (выпадающая снизу)
#Тут можно будет описать общие блоки и после выбора инлайнить конкретные запросы из ТЗ

# Добавляем константу для пути к файлу с reply-клавиатурами
REPLY_KEYBOARDS_FILE = "data/reply_keyboards.json"

# Словарь для хранения загруженных reply-клавиатур
reply_keyboards = {}


def create_reply_markup(keyboard_name):
    """Создает объект ReplyKeyboardMarkup из структуры клавиатуры по имени"""
    if keyboard_name == "none" or keyboard_name not in reply_keyboards:
        return None

    keyboard_structure = reply_keyboards[keyboard_name]
    keyboard = []

    for row in keyboard_structure:
        keyboard_row = []
        for button_text in row:
            keyboard_row.append(KeyboardButton(text=button_text))
        keyboard.append(keyboard_row)

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню"
    )


def load_reply_keyboards():
    """Загружает структуры reply-клавиатур из JSON-файла"""
    global reply_keyboards

    # Проверяем существование файла
    if os.path.exists(REPLY_KEYBOARDS_FILE):
        try:
            with open(REPLY_KEYBOARDS_FILE, 'r', encoding='utf-8') as f:
                reply_keyboards = json.load(f)
            print(f"Загружено {len(reply_keyboards)} reply-клавиатур из файла")
        except Exception as e:
            print(f"Ошибка при загрузке reply-клавиатур: {e}")


def save_reply_keyboards():
    """Сохраняет структуры reply-клавиатур в JSON-файл"""
    try:
        with open(REPLY_KEYBOARDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reply_keyboards, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(reply_keyboards)} reply-клавиатур в файл")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении reply-клавиатур: {e}")
        return False



"""main_menu_first_page = ReplyKeyboardMarkup(keyboard=[
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

test_menu_first_page = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="test")]
])


inline_help_animals = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=UserButtons.VIEW_HELP_ANIMALS, url=UserLinks.LINK_HELP_ANIMALS)]
])

inline_urgent_help = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=UserButtons.VIEW_URGENT_HELP, url=UserLinks.LINK_URGENT_HELP)]
])"""
