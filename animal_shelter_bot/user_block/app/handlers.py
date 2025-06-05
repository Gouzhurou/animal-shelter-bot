import json
import os
import re
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from functools import partial
from animal_shelter_bot.user_block.app import keyboards as kb
from animal_shelter_bot.user_block.const import UserButtons, UserMessages, UserLinks
from animal_shelter_bot.states import UserStates, AdminStates
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from animal_shelter_bot.registration.app.db import get_user_by_phone, add_new_user, get_user_by_id
user_router = Router()

# Загрузка переменных окружения
load_dotenv()

# Получаем список ID администраторов из переменных окружения
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))

# Путь к файлу для хранения обработчиков
HANDLERS_FILE = "data/handlers.json"
# Путь к файлу для хранения inline-меню
INLINE_MENUS_FILE = "data/inline_menus.json"

# Убедимся, что директории существуют
os.makedirs(os.path.dirname(HANDLERS_FILE), exist_ok=True)

# Словарь для хранения всех обработчиков
button_handlers = {}
# Словарь для хранения всех inline-меню
inline_menus = {}

# Словарь доступных клавиатур
KEYBOARDS = {
    "none": None,
}


# Функция-помощник для создания простых обработчиков текстовых сообщений
async def simple_text_handler(message: Message, response_text: str, markup=None):
    """Обработчик для отправки простого текстового ответа"""
    # Проверяем, содержит ли текст ответа специальный тег для inline-меню
    inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', response_text)

    if inline_menu_tag:
        # Извлекаем имя меню
        menu_name = inline_menu_tag.group(1)
        # Удаляем тег из ответа
        clean_response = response_text.replace(inline_menu_tag.group(0), "")

        # Проверяем, существует ли такое меню
        if menu_name in inline_menus:
            # Создаем inline-клавиатуру
            inline_markup = create_inline_markup(menu_name)
            await message.answer(clean_response, reply_markup=inline_markup)
        else:
            # Если меню не найдено, отправляем ответ без клавиатуры
            await message.answer(f"{clean_response}\n\n⚠️ Ошибка: меню '{menu_name}' не найдено")
    else:
        # Отправляем обычный ответ
        await message.answer(response_text, reply_markup=markup)


# Функция для создания inline-клавиатуры из хранилища
def create_inline_markup(menu_name):
    """Создает inline-клавиатуру по имени из хранилища"""
    if menu_name not in inline_menus:
        return None

    # Получаем кнопки для данного меню
    buttons = inline_menus[menu_name]

    # Создаем клавиатуру
    inline_keyboard = []
    row = []

    for button in buttons:
        text, url = button
        row.append(InlineKeyboardButton(text=text, url=url))

        # Добавляем не более 2 кнопок в строку
        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    # Добавляем оставшиеся кнопки
    if row:
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# Функция для сохранения обработчиков в файл
def save_handlers():
    """Сохраняет все обработчики в JSON-файл"""
    # Преобразуем обработчики в формат для сохранения
    handlers_to_save = {}
    for button, (response_text, markup) in button_handlers.items():
        # Находим имя клавиатуры
        markup_name = "none"
        for name, kb_obj in KEYBOARDS.items():
            if markup == kb_obj:
                markup_name = name
                break

        # Если клавиатура не найдена в KEYBOARDS и это объект ReplyKeyboardMarkup,
        # пытаемся найти её среди клавиатур, загруженных из JSON
        if markup_name == "none" and markup is not None and hasattr(markup, 'keyboard'):
            # Преобразуем объект клавиатуры в структуру для сравнения
            markup_structure = []
            for row in markup.keyboard:
                row_buttons = []
                for button_obj in row:
                    row_buttons.append(button_obj.text)
                markup_structure.append(row_buttons)

            # Ищем соответствие в reply_keyboards
            for name, structure in kb.reply_keyboards.items():
                if markup_structure == structure:
                    markup_name = name
                    break

        # Используем список, так как он соответствует формату в JSON файле
        handlers_to_save[button] = [response_text, markup_name]

    # Сохраняем в файл
    try:
        with open(HANDLERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(handlers_to_save, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении обработчиков: {e}")
        return False


# Функция для сохранения inline-меню в файл
def save_inline_menus():
    """Сохраняет все inline-меню в JSON-файл"""
    try:
        with open(INLINE_MENUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(inline_menus, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении inline-меню: {e}")
        return False


# Функция для загрузки обработчиков из файла
def load_handlers():
    """Загружает обработчики из JSON-файла или создает стандартные, если файл не существует"""
    global button_handlers

    if not kb.reply_keyboards:
        kb.load_reply_keyboards()
        print("Загружены клавиатуры из JSON")

    # Проверяем существование файла
    if os.path.exists(HANDLERS_FILE):
        try:
            with open(HANDLERS_FILE, 'r', encoding='utf-8') as f:
                saved_handlers = json.load(f)

            # Очищаем текущие обработчики
            button_handlers.clear()

            # Преобразуем строковые представления клавиатур в объекты
            for button, values in saved_handlers.items():
                # Учитываем, что значения в JSON хранятся как список [response_text, markup_name]
                response_text, markup_name = values

                # Определяем маркап по имени
                markup = None

                # Если "none", то клавиатура не нужна
                if markup_name == "none":
                    pass
                # Пробуем сначала найти в KEYBOARDS
                elif markup_name in KEYBOARDS:
                    markup = KEYBOARDS[markup_name]
                    print(f"Клавиатура '{markup_name}' найдена в KEYBOARDS")
                # Затем пробуем создать из reply_keyboards
                elif markup_name in kb.reply_keyboards:
                    markup = kb.create_reply_markup(markup_name)
                    print(f"Клавиатура '{markup_name}' создана из reply_keyboards")
                else:
                    print(f"Клавиатура '{markup_name}' не найдена нигде! Установлено None")

                # Сохраняем обработчик с текстом и объектом клавиатуры
                button_handlers[button] = (response_text, markup)

            print(f"Загружено {len(button_handlers)} обработчиков из файла")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке обработчиков: {e}")
            return False
    else:
        # Если файл не существует, создаем стандартные обработчики
        print(f"Файл {HANDLERS_FILE} не найден")
        return True

# Функция для загрузки inline-меню из файла
def load_inline_menus():
    """Загружает inline-меню из JSON-файла"""
    global inline_menus

    # Проверяем существование файла
    if os.path.exists(INLINE_MENUS_FILE):
        try:
            with open(INLINE_MENUS_FILE, 'r', encoding='utf-8') as f:
                loaded_menus = json.load(f)
                inline_menus.clear()  # Очищаем текущие меню
                inline_menus.update(loaded_menus)  # Обновляем словарь новыми данными
            print(f"Загружено {len(inline_menus)} inline-меню из файла")
        except Exception as e:
            print(f"Ошибка при загрузке inline-меню: {e}")
            inline_menus.clear()
    else:
        # Если файл не существует, создаем пустой словарь
        inline_menus.clear()
        # Сохраняем пустой словарь в файл
        save_inline_menus()



# Функция для регистрации всех обработчиков
def register_handlers():
    """Регистрирует все обработчики из словаря button_handlers"""
    # Сначала очищаем все обработчики
    user_router.message.handlers = [h for h in user_router.message.handlers
                                  if not hasattr(h.callback, '_is_dynamic_handler')]

    # Регистрируем обработчики из словаря
    for button_text, (response_text, markup) in button_handlers.items():
        handler = partial(simple_text_handler, response_text=response_text, markup=markup)
        handler.__doc__ = f"""Обработчик кнопки '{button_text}'"""
        handler._is_dynamic_handler = True

        # Регистрируем обработчик
        user_router.message(F.text == button_text, UserStates.user_active)(handler)

    print(f"Зарегистрировано {len(button_handlers)} обработчиков")


# Функция для добавления или обновления обработчика
async def add_or_update_handler(button_text: str, response_text: str, markup_name: str = None):
    """Добавляет новый обработчик или обновляет существующий"""
    if not kb.reply_keyboards:
        kb.load_reply_keyboards()

    # Определяем маркап по имени
    markup = KEYBOARDS.get(markup_name)

    # Проверяем, не является ли markup_name именем клавиатуры из reply_keyboards
    if markup_name in kb.reply_keyboards:
        # Создаем объект клавиатуры из JSON
        markup = kb.create_reply_markup(markup_name)
    else:
        # Пробуем получить из стандартных клавиатур
        markup = KEYBOARDS.get(markup_name)

    # Печатаем отладочную информацию
    print(f"Устанавливаем клавиатуру: {markup_name}, объект: {markup}")

    # Добавляем в словарь
    button_handlers[button_text] = (response_text, markup)

    # Создаем и регистрируем обработчик
    handler = partial(simple_text_handler, response_text=response_text, markup=markup)
    handler.__doc__ = f"""Обработчик кнопки '{button_text}'"""
    handler._is_dynamic_handler = True

    # Регистрируем обработчик
    user_router.message(F.text == button_text, UserStates.user_active)(handler)

    # Сохраняем изменения
    success = save_handlers()

    return success




