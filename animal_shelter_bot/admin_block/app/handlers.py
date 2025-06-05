import json
import re
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router
from animal_shelter_bot.states import AdminStates, UserStates
from aiogram.types import Message
from animal_shelter_bot.registration.app.db import get_user_by_phone, add_new_user, get_user_by_id, update_user_role, get_all_admins, search_users
from animal_shelter_bot.user_block.app import keyboards as kb
from animal_shelter_bot.registration.app import keyboards as kbb
from animal_shelter_bot.registration.app.utils import normalize_phone
from animal_shelter_bot.user_block.app.handlers import (KEYBOARDS, create_inline_markup,
                                                        save_inline_menus, add_or_update_handler, load_handlers,
                                                        register_handlers, INLINE_MENUS_FILE, HANDLERS_FILE,
                                                        save_handlers, load_inline_menus,
                                                        button_handlers, inline_menus)

admin_router = Router()





# Обработчики для администратора

@admin_router.message(Command("add_button"), AdminStates.admin_active)
async def cmd_add_button(message: Message, state: FSMContext):
    """Начинает процесс добавления новой кнопки"""
    await message.answer("Введите текст кнопки:")
    await state.set_state(AdminStates.waiting_for_button_text)


@admin_router.message(AdminStates.waiting_for_button_text)
async def process_button_text(message: Message, state: FSMContext):
    """Обрабатывает текст кнопки"""
    button_text = message.text
    await state.update_data(button_text=button_text)
    await message.answer("Теперь введите текст ответа:\n\n" +
                        "Примечание: Чтобы добавить inline-меню со ссылками, " +
                        "добавьте тег [[INLINE_MENU:имя_меню]] в текст ответа.")
    await state.set_state(AdminStates.waiting_for_response_text)


@admin_router.message(AdminStates.waiting_for_response_text)
async def process_response_text(message: Message, state: FSMContext):
    """Обрабатывает текст ответа"""
    response_text = message.text
    await state.update_data(response_text=response_text)

    # Проверяем, есть ли в ответе тег inline-меню
    inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', response_text)
    if inline_menu_tag:
        menu_name = inline_menu_tag.group(1)
        await state.update_data(inline_menu_name=menu_name)

        # Проверяем, существует ли такое меню
        if menu_name in inline_menus:
            await message.answer(
                f"Найдено существующее меню '{menu_name}' с кнопками:\n\n" +
                "\n".join([f"{i+1}. {btn[0]} -> {btn[1]}" for i, btn in enumerate(inline_menus[menu_name])]) +
                "\n\nВыберите действие:\n" +
                "1. Использовать существующее меню\n"
            )
            await state.set_state(AdminStates.waiting_for_inline_menu_action)
        else:
            await message.answer(
                f"Меню '{menu_name}' не найдено. Создаем новое.\n\n" +
                "Введите кнопки для меню в формате:\n" +
                "Текст кнопки 1|https://ссылка1.com\n" +
                "Текст кнопки 2|https://ссылка2.com\n\n" +
                "Каждая кнопка на новой строке, разделите текст и ссылку символом '|'"
            )
            await state.set_state(AdminStates.waiting_for_inline_menu_buttons)
    else:
        # Если нет тега inline-меню, продолжаем стандартный процесс
        # Убедимся, что клавиатуры загружены
        if not kb.reply_keyboards:
            kb.load_reply_keyboards()

        # Формируем список доступных клавиатур
        keyboard_options = "Выберите тип клавиатуры:\n\n"
        for i, name in enumerate(KEYBOARDS.keys(), 1):
            keyboard_options += f"0. {name}\n"
        for i, name in enumerate(kb.reply_keyboards.keys(), 1):
            keyboard_options += f"{i} {name}\n"

        keyboard_options += "\nВведите название клавиатуры (например, 'none'):"

        await message.answer(keyboard_options)
        await state.set_state(AdminStates.waiting_for_markup_type)


@admin_router.message(AdminStates.waiting_for_inline_menu_action)
async def process_inline_menu_action(message: Message, state: FSMContext):
    """Обрабатывает выбор действия для существующего inline-меню"""
    action = message.text.strip()
    data = await state.get_data()
    menu_name = data["inline_menu_name"]

    if action == "1":
        # Использовать существующее меню
        await message.answer(f"Будет использовано существующее меню '{menu_name}'.")

        # Продолжаем стандартный процесс добавления кнопки
        keyboard_options = "Выберите тип клавиатуры для основного сообщения:\n\n"
        for i, name in enumerate(KEYBOARDS.keys(), 1):
            keyboard_options += f"0. {name}\n"
        for i, name in enumerate(kb.reply_keyboards.keys(), 1):
            keyboard_options += f"{i} {name}\n"

        keyboard_options += "\nВведите название клавиатуры (например, 'none'):"

        await message.answer(keyboard_options)
        await state.set_state(AdminStates.waiting_for_markup_type)
    else:
        await message.answer("Пожалуйста, выберите 1 или 2")


@admin_router.message(AdminStates.waiting_for_inline_menu_buttons)
async def process_inline_menu_buttons(message: Message, state: FSMContext):
    """Обрабатывает ввод кнопок для inline-меню"""
    buttons_text = message.text
    data = await state.get_data()
    menu_name = data["inline_menu_name"]

    # Парсим кнопки
    buttons = []
    for line in buttons_text.strip().split("\n"):
        if "|" in line:
            text, url = line.split("|", 1)
            text = text.strip()
            url = url.strip()
            if text and url:
                buttons.append([text, url])

    if not buttons:
        await message.answer(
            "Не удалось распознать кнопки. Попробуйте еще раз в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com"
        )
        return

    # Сохраняем меню
    inline_menus[menu_name] = buttons
    save_inline_menus()

    await message.answer(
        f"Меню '{menu_name}' с {len(buttons)} кнопками успешно создано.\n\n" +
        "Теперь выберите тип клавиатуры для основного сообщения:"
    )

    # Формируем список доступных клавиатур
    keyboard_options = "Выберите тип клавиатуры для основного сообщения:\n\n"
    for i, name in enumerate(KEYBOARDS.keys(), 1):
        keyboard_options += f"0. {name}\n"
    for i, name in enumerate(kb.reply_keyboards.keys(), 1):
        keyboard_options += f"{i} {name}\n"

    keyboard_options += "\nВведите название клавиатуры (например, 'none'):"

    await message.answer(keyboard_options)
    await state.set_state(AdminStates.waiting_for_markup_type)


@admin_router.message(AdminStates.waiting_for_markup_type)
async def process_markup_type(message: Message, state: FSMContext):
    """Обрабатывает тип клавиатуры и создает кнопку"""
    markup_name = message.text.strip()
    data = await state.get_data()

    # Проверяем, есть ли такая клавиатура или это специальное значение "none"
    if markup_name != "none" and markup_name not in kb.reply_keyboards:
        keyboard_list = "\n".join([f"- {name}" for name in kb.reply_keyboards.keys()])

        await message.answer(
            f"❌ Клавиатура '{markup_name}' не найдена. Доступные клавиатуры:\n\n"
            f"{keyboard_list}\n\n"
            "Или введите 'none' для отсутствия клавиатуры."
        )
        return

    if markup_name == "none":
        markup_name = None

    data = await state.get_data()
    button_text = data["button_text"]
    response_text = data["response_text"]

    # Добавляем/обновляем обработчик
    success = await add_or_update_handler(button_text, response_text, markup_name)

    if success:
        if button_text in button_handlers:
            action = "обновлена"
        else:
            action = "добавлена"

        # Проверяем, есть ли inline-меню в ответе
        inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', response_text)
        if inline_menu_tag:
            menu_name = inline_menu_tag.group(1)
            if menu_name in inline_menus:
                await state.set_state(AdminStates.admin_active)
                await message.answer(
                    f"Кнопка '{button_text}' успешно {action}!\n" +
                    f"Она будет использовать inline-меню '{menu_name}' с {len(inline_menus[menu_name])} кнопками."
                )
            else:
                await state.set_state(AdminStates.admin_active)
                await message.answer(
                    f"Кнопка '{button_text}' успешно {action}, но меню '{menu_name}' не найдено.\n" +
                    "Используйте команду /add_inline_menu, чтобы создать это меню."
                )
        else:
            await state.set_state(AdminStates.admin_active)
            await message.answer(f"Кнопка '{button_text}' успешно {action}!")
    else:
        await state.set_state(AdminStates.admin_active)
        await message.answer("Ошибка при добавлении/обновлении кнопки")

    await state.set_state(AdminStates.admin_active)


# Новые команды для управления inline-меню

@admin_router.message(Command("reload_all"), AdminStates.admin_active)
async def cmd_reload_all(message: Message):
    """Перезагружает все данные из JSON-файлов"""
    try:
        # Перезагружаем обработчики кнопок
        button_handlers.clear()

        # Перезагружаем reply-клавиатуры в модуле kb
        # Очищаем клавиатуры в модуле
        kb.reply_keyboards.clear()  # Очищаем, но не переопределяем!
        kb.load_reply_keyboards()  # Загружаем заново

        # Перезагружаем inline-меню
        inline_menus.clear()  # Очищаем словарь
        load_inline_menus()  # Загружаем данные

        # Загружаем обработчики (после загрузки клавиатур)
        load_handlers()

        # Регистрируем обновленные обработчики
        register_handlers()

        await message.answer(
            f"✅ Все данные успешно перезагружены!\n"
            f"- Загружено {len(button_handlers)} обработчиков\n"
            f"- Загружено {len(kb.reply_keyboards)} reply-клавиатур\n"
            f"- Загружено {len(inline_menus)} inline-меню"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при перезагрузке данных: {e}")


@admin_router.message(Command("add_inline_menu"), AdminStates.admin_active)
async def cmd_add_inline_menu(message: Message, state: FSMContext):
    """Начинает процесс добавления нового inline-меню"""
    await message.answer("Введите имя для нового inline-меню (без пробелов):")
    await state.set_state(AdminStates.waiting_for_inline_menu_name)


@admin_router.message(AdminStates.waiting_for_inline_menu_name)
async def process_inline_menu_name(message: Message, state: FSMContext):
    """Обрабатывает имя нового inline-меню"""
    menu_name = message.text.strip()

    # Проверяем корректность имени
    if " " in menu_name:
        await message.answer("Имя меню не должно содержать пробелов. Попробуйте еще раз:")
        return

    # Проверяем, существует ли уже такое меню
    if menu_name in inline_menus:
        await message.answer(
            f"Меню с именем '{menu_name}' уже существует. Выберите действие:\n" +
            "1. Перезаписать существующее меню\n" +
            "2. Выбрать другое имя"
        )
        await state.update_data(menu_name=menu_name)
        await state.set_state(AdminStates.waiting_for_menu_overwrite_confirm)
    else:
        await state.update_data(menu_name=menu_name)
        await message.answer(
            f"Создаем новое меню '{menu_name}'.\n\n" +
            "Введите кнопки для меню в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com\n\n" +
            "Каждая кнопка на новой строке, разделите текст и ссылку символом '|'"
        )
        await state.set_state(AdminStates.waiting_for_new_inline_menu_buttons)


@admin_router.message(AdminStates.waiting_for_menu_overwrite_confirm)
async def process_menu_overwrite_confirm(message: Message, state: FSMContext):
    """Обрабатывает подтверждение перезаписи меню"""
    action = message.text.strip()
    data = await state.get_data()
    menu_name = data["menu_name"]

    if action == "1":
        # Перезаписать существующее меню
        await message.answer(
            f"Перезаписываем меню '{menu_name}'.\n\n" +
            "Введите кнопки для меню в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com\n\n" +
            "Каждая кнопка на новой строке, разделите текст и ссылку символом '|'"
        )
        await state.set_state(AdminStates.waiting_for_new_inline_menu_buttons)
    elif action == "2":
        # Выбрать другое имя
        await message.answer("Введите новое имя для меню (без пробелов):")
        await state.set_state(AdminStates.waiting_for_inline_menu_name)
    else:
        await message.answer("Пожалуйста, выберите 1 или 2")


@admin_router.message(AdminStates.waiting_for_new_inline_menu_buttons)
async def process_new_inline_menu_buttons(message: Message, state: FSMContext):
    """Обрабатывает ввод кнопок для нового inline-меню"""
    buttons_text = message.text
    data = await state.get_data()
    menu_name = data["menu_name"]

    # Парсим кнопки
    buttons = []
    for line in buttons_text.strip().split("\n"):
        if "|" in line:
            text, url = line.split("|", 1)
            text = text.strip()
            url = url.strip()
            if text and url:
                buttons.append([text, url])

    if not buttons:
        await message.answer(
            "Не удалось распознать кнопки. Попробуйте еще раз в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com"
        )
        return

    # Сохраняем меню
    inline_menus[menu_name] = buttons
    save_inline_menus()

    # Показываем пример использования
    await message.answer(
        f"Меню '{menu_name}' с {len(buttons)} кнопками успешно создано.\n\n" +
        f"Чтобы использовать это меню, добавьте тег [[INLINE_MENU:{menu_name}]] " +
        "в текст ответа при создании или редактировании кнопки."
    )

    # Создаем и показываем пример меню
    inline_markup = create_inline_markup(menu_name)
    await message.answer(
        f"Вот как будет выглядеть меню '{menu_name}':",
        reply_markup=inline_markup
    )

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("list_inline_menus"), AdminStates.admin_active)
async def cmd_list_inline_menus(message: Message):
    """Выводит список всех inline-меню"""
    if not inline_menus:
        await message.answer("Список inline-меню пуст")
        return

    # Сортируем меню по имени
    sorted_menus = sorted(inline_menus.items())

    # Формируем сообщение со списком меню
    response = "📋 СПИСОК ВСЕХ INLINE-МЕНЮ:\n\n"

    for i, (menu_name, buttons) in enumerate(sorted_menus, 1):
        response += f"{i}. '{menu_name}' ({len(buttons)} кнопок):\n"
        for j, (text, url) in enumerate(buttons, 1):
            response += f"   {j}. {text} -> {url}\n"
        response += "\n"

        # Если список слишком длинный, разбиваем на части
        if i % 5 == 0 and i < len(sorted_menus):
            await message.answer(response)
            response = "📋 ПРОДОЛЖЕНИЕ СПИСКА INLINE-МЕНЮ:\n\n"

    if response.strip() != "📋 ПРОДОЛЖЕНИЕ СПИСКА INLINE-МЕНЮ:":
        await message.answer(response)


@admin_router.message(Command("remove_inline_menu"), AdminStates.admin_active)
async def cmd_remove_inline_menu(message: Message, state: FSMContext):
    """Начинает процесс удаления inline-меню"""
    if not inline_menus:
        await message.answer("Список inline-меню пуст")
        return

    # Формируем список меню
    menus_list = "Выберите меню для удаления (введите имя):\n\n"
    for i, menu_name in enumerate(sorted(inline_menus.keys()), 1):
        menus_list += f"{i}. {menu_name} ({len(inline_menus[menu_name])} кнопок)\n"

    await message.answer(menus_list)
    await state.set_state(AdminStates.waiting_for_menu_to_remove)


@admin_router.message(AdminStates.waiting_for_menu_to_remove)
async def process_menu_to_remove(message: Message, state: FSMContext):
    """Обрабатывает удаление inline-меню"""
    menu_name = message.text.strip()

    if menu_name in inline_menus:
        # Удаляем меню
        del inline_menus[menu_name]
        save_inline_menus()

        # Проверяем, используется ли это меню в ответах
        used_in = []
        for button, (response, _) in button_handlers.items():
            if f"[[INLINE_MENU:{menu_name}]]" in response:
                used_in.append(button)

        if used_in:
            await message.answer(
                f"Меню '{menu_name}' успешно удалено, но оно используется в следующих кнопках:\n" +
                "\n".join([f"- {button}" for button in used_in]) +
                "\n\nПожалуйста, обновите эти кнопки."
            )
        else:
            await message.answer(f"Меню '{menu_name}' успешно удалено")
    else:
        await message.answer(f"Меню '{menu_name}' не найдено")

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("edit_inline_menu"),AdminStates.admin_active)
async def cmd_edit_inline_menu(message: Message, state: FSMContext):
    """Начинает процесс редактирования inline-меню"""
    if not inline_menus:
        await message.answer("Список inline-меню пуст")
        return

    # Формируем список меню
    menus_list = "Выберите меню для редактирования (введите имя):\n\n"
    for i, menu_name in enumerate(sorted(inline_menus.keys()), 1):
        menus_list += f"{i}. {menu_name} ({len(inline_menus[menu_name])} кнопок)\n"

    await message.answer(menus_list)
    await state.set_state(AdminStates.waiting_for_menu_to_edit)


@admin_router.message(AdminStates.waiting_for_menu_to_edit)
async def process_menu_to_edit(message: Message, state: FSMContext):
    """Обрабатывает выбор меню для редактирования"""
    menu_name = message.text.strip()

    if menu_name not in inline_menus:
        await message.answer(f"Меню '{menu_name}' не найдено")
        await state.set_state(AdminStates.admin_active)
        return

    # Сохраняем имя меню
    await state.update_data(menu_name=menu_name)

    # Формируем текущие кнопки
    buttons_text = "\n".join([f"{text}|{url}" for text, url in inline_menus[menu_name]])

    await message.answer(
        f"Редактирование меню '{menu_name}'.\n\n" +
        "Текущие кнопки:\n" +
        buttons_text +
        "\n\nВведите новые кнопки в том же формате:\n" +
        "Текст кнопки 1|https://ссылка1.com\n" +
        "Текст кнопки 2|https://ссылка2.com\n\n" +
        "Или отправьте '+', чтобы оставить текущие кнопки"
    )

    await state.set_state(AdminStates.waiting_for_edited_menu_buttons)


@admin_router.message(AdminStates.waiting_for_edited_menu_buttons)
async def process_edited_menu_buttons(message: Message, state: FSMContext):
    """Обрабатывает редактирование кнопок меню"""
    buttons_text = message.text.strip()
    data = await state.get_data()
    menu_name = data["menu_name"]

    if buttons_text == "+":
        await message.answer(f"Меню '{menu_name}' оставлено без изменений")
        await state.set_state(AdminStates.admin_active)
        return

    # Парсим кнопки
    buttons = []
    for line in buttons_text.split("\n"):
        if "|" in line:
            text, url = line.split("|", 1)
            text = text.strip()
            url = url.strip()
            if text and url:
                buttons.append([text, url])

    if not buttons:
        await message.answer(
            "Не удалось распознать кнопки. Попробуйте еще раз в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com\n\n" +
            "Или отправьте '+', чтобы оставить текущие кнопки"
        )
        return

    # Обновляем меню
    inline_menus[menu_name] = buttons
    save_inline_menus()

    # Показываем обновленное меню
    inline_markup = create_inline_markup(menu_name)
    await message.answer(
        f"Меню '{menu_name}' успешно обновлено. Теперь в нем {len(buttons)} кнопок.\n" +
        "Вот как оно выглядит:",
        reply_markup=inline_markup
    )

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("list_buttons"), AdminStates.admin_active)
async def cmd_list_buttons(message: Message):
    """Выводит список всех доступных кнопок"""
    if not button_handlers:
        await message.answer("Список кнопок пуст")
        return

    # Сначала загрузим информацию из JSON для сравнения
    try:
        with open(HANDLERS_FILE, 'r', encoding='utf-8') as f:
            raw_handlers = json.load(f)
    except Exception:
        raw_handlers = {}

    # Сортируем кнопки по алфавиту
    sorted_buttons = sorted(button_handlers.items())

    # Формируем сообщение со списком кнопок
    response = "📋 СПИСОК ВСЕХ КНОПОК:\n\n"

    for i, (button, (text, markup)) in enumerate(sorted_buttons, 1):
        # Получаем название клавиатуры из JSON-файла
        markup_name = "none"
        if button in raw_handlers:
            _, json_markup_name = raw_handlers[button]
            markup_name = json_markup_name

        # Проверяем, использует ли кнопка inline-меню
        inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', text)
        inline_menu_info = ""
        if inline_menu_tag:
            menu_name = inline_menu_tag.group(1)
            if menu_name in inline_menus:
                inline_menu_info = f", Inline-меню: {menu_name} ({len(inline_menus[menu_name])} кнопок)"
            else:
                inline_menu_info = f", Inline-меню: {menu_name} (не найдено)"

        # Добавляем информацию о кнопке
        response += f"{i}. '{button}'\n"
        response += f"   Ответ: {text[:50]}{'...' if len(text) > 50 else ''}\n"
        response += f"   Клавиатура: {markup_name}{inline_menu_info}\n\n"

        # Если список слишком длинный, разбиваем на части
        if i % 15 == 0 and i < len(sorted_buttons):
            await message.answer(response)
            response = "📋 ПРОДОЛЖЕНИЕ СПИСКА КНОПОК:\n\n"

    if response.strip() != "📋 ПРОДОЛЖЕНИЕ СПИСКА КНОПОК:":
        await message.answer(response)


@admin_router.message(Command("edit_button"),AdminStates.admin_active)
async def cmd_edit_button(message: Message, state: FSMContext):
    """Начинает процесс редактирования кнопки"""
    await message.answer("Введите текст кнопки для редактирования:")
    await state.set_state(AdminStates.waiting_for_button_to_edit)


@admin_router.message(AdminStates.waiting_for_button_to_edit)
async def process_button_to_edit(message: Message, state: FSMContext):
    """Обрабатывает выбор кнопки для редактирования"""
    button_text = message.text

    if button_text not in button_handlers:
        await message.answer(f"Кнопка '{button_text}' не найдена")
        await state.set_state(AdminStates.admin_active)
        return

    # Сохраняем текст кнопки и получаем текущие данные
    current_response, current_markup = button_handlers[button_text]

    # Определяем тип клавиатуры напрямую из JSON
    current_markup_name = "none"  # значение по умолчанию
    try:
        with open(HANDLERS_FILE, 'r', encoding='utf-8') as f:
            handlers_data = json.load(f)

        # Если кнопка есть в JSON, берем имя клавиатуры напрямую
        if button_text in handlers_data:
            # Формат в JSON: [response_text, markup_name]
            _, stored_markup_name = handlers_data[button_text]
            current_markup_name = stored_markup_name  # берем имя из JSON
    except Exception as e:
        print(f"Ошибка при чтении JSON для определения клавиатуры: {e}")

    # Проверяем, использует ли кнопка inline-меню
    inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', current_response)
    inline_menu_info = ""
    if inline_menu_tag:
        menu_name = inline_menu_tag.group(1)
        if menu_name in inline_menus:
            inline_menu_info = f"\nКнопка использует inline-меню: {menu_name}"
        else:
            inline_menu_info = f"\nКнопка ссылается на несуществующее inline-меню: {menu_name}"

    await state.update_data(
        button_text=button_text,
        current_response=current_response,
        current_markup_name=current_markup_name
    )

    # Показываем текущий ответ
    await message.answer(
        f"Текущий ответ для кнопки '{button_text}':\n\n"
        f"{current_response}\n\n"
        f"Клавиатура: {current_markup_name}{inline_menu_info}\n\n"
        f"Введите новый текст ответа или отправьте '+', чтобы оставить текущий:\n\n"
        f"Примечание: Чтобы добавить inline-меню со ссылками, "
        f"добавьте тег [[INLINE_MENU:имя_меню]] в текст ответа."
    )

    await state.set_state(AdminStates.waiting_for_new_response)


@admin_router.message(AdminStates.waiting_for_new_response)
async def process_new_response(message: Message, state: FSMContext):
    """Обрабатывает новый текст ответа"""
    new_response = message.text
    data = await state.get_data()

    # Если пользователь хочет оставить текущий текст
    if new_response == "+":
        new_response = data["current_response"]

    await state.update_data(new_response=new_response)

    # Проверяем, есть ли в новом ответе тег inline-меню
    inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', new_response)
    if inline_menu_tag:
        menu_name = inline_menu_tag.group(1)
        await state.update_data(inline_menu_name=menu_name)

        # Проверяем, существует ли такое меню
        if menu_name not in inline_menus:
            await message.answer(
                f"⚠️ Внимание: Меню '{menu_name}' не найдено.\n\n"
                "Выберите действие:\n"
                "1. Продолжить с несуществующим меню (вы сможете создать его позже)\n"
                "2. Создать это меню сейчас"
            )
            await state.set_state(AdminStates.waiting_for_missing_menu_action)
            return

    # Формируем список доступных клавиатур
    keyboard_options = (
        f"Текущая клавиатура: {data['current_markup_name']}\n\n"
        "Выберите новый тип клавиатуры или отправьте '+', чтобы оставить текущую:\n\n"
    )

    # Убедимся, что клавиатуры загружены
    if not kb.reply_keyboards:
        kb.load_reply_keyboards()

    for i, name in enumerate(KEYBOARDS.keys(), 1):
        keyboard_options += f"0. {name}\n"
    for i, name in enumerate(kb.reply_keyboards.keys(), 1):
        keyboard_options += f"{i}. {name}\n"

    await message.answer(keyboard_options)
    await state.set_state(AdminStates.waiting_for_new_markup)


@admin_router.message(AdminStates.waiting_for_missing_menu_action)
async def process_missing_menu_action(message: Message, state: FSMContext):
    """Обрабатывает действие для отсутствующего меню"""
    action = message.text.strip()
    data = await state.get_data()
    menu_name = data["inline_menu_name"]

    if action == "1":
        # Продолжить с несуществующим меню
        await message.answer(
            f"Продолжаем с несуществующим меню '{menu_name}'.\n"
            "Вы сможете создать его позже с помощью команды /add_inline_menu."
        )

        # Формируем список доступных клавиатур
        keyboard_options = (
            f"Текущая клавиатура: {data['current_markup_name']}\n\n"
            "Выберите новый тип клавиатуры или отправьте '+', чтобы оставить текущую:\n\n"
        )

        for i, name in enumerate(KEYBOARDS.keys(), 1):
            keyboard_options += f"0. {name}\n"
        for i, name in enumerate(kb.reply_keyboards.keys(), 1):
            keyboard_options += f"{i}. {name}\n"

        await message.answer(keyboard_options)
        await state.set_state(AdminStates.waiting_for_new_markup)
    elif action == "2":
        # Создать меню сейчас
        await message.answer(
            f"Создаем новое меню '{menu_name}'.\n\n" +
            "Введите кнопки для меню в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com\n\n" +
            "Каждая кнопка на новой строке, разделите текст и ссылку символом '|'"
        )
        await state.set_state(AdminStates.waiting_for_new_menu_buttons)
    else:
        await message.answer("Пожалуйста, выберите 1 или 2")


@admin_router.message(AdminStates.waiting_for_new_menu_buttons)
async def process_new_menu_buttons_during_edit(message: Message, state: FSMContext):
    """Обрабатывает ввод кнопок для нового меню во время редактирования кнопки"""
    buttons_text = message.text
    data = await state.get_data()
    menu_name = data["inline_menu_name"]

    # Парсим кнопки
    buttons = []
    for line in buttons_text.strip().split("\n"):
        if "|" in line:
            text, url = line.split("|", 1)
            text = text.strip()
            url = url.strip()
            if text and url:
                buttons.append([text, url])

    if not buttons:
        await message.answer(
            "Не удалось распознать кнопки. Попробуйте еще раз в формате:\n" +
            "Текст кнопки 1|https://ссылка1.com\n" +
            "Текст кнопки 2|https://ссылка2.com"
        )
        return

    # Сохраняем меню
    inline_menus[menu_name] = buttons
    save_inline_menus()

    await message.answer(
        f"Меню '{menu_name}' с {len(buttons)} кнопками успешно создано.\n\n" +
        "Теперь выберите тип клавиатуры для основного сообщения:"
    )

    # Формируем список доступных клавиатур
    keyboard_options = (
        f"Текущая клавиатура: {data['current_markup_name']}\n\n"
        "Выберите новый тип клавиатуры или отправьте '+', чтобы оставить текущую:\n\n"
    )

    for i, name in enumerate(KEYBOARDS.keys(), 1):
        keyboard_options += f"0. {name}\n"
    for i, name in enumerate(kb.reply_keyboards.keys(), 1):
        keyboard_options += f"{i}. {name}\n"

    await message.answer(keyboard_options)
    await state.set_state(AdminStates.waiting_for_new_markup)


@admin_router.message(AdminStates.waiting_for_new_markup)
async def process_new_markup(message: Message, state: FSMContext):
    """Обрабатывает новый тип клавиатуры и обновляет кнопку"""
    new_markup = message.text.lower()
    data = await state.get_data()

    # Если пользователь хочет оставить текущую клавиатуру
    if new_markup == "+":
        new_markup = data["current_markup_name"]

    # Проверяем, есть ли такая клавиатура
    if new_markup not in KEYBOARDS and new_markup not in kb.reply_keyboards and new_markup != "none":
        await message.answer(f"Клавиатура '{new_markup}' не найдена. Пожалуйста, выберите из списка.")
        return

    if new_markup == "none":
        new_markup = None

    button_text = data["button_text"]
    new_response = data["new_response"]

    # Обновляем обработчик
    success = await add_or_update_handler(button_text, new_response, new_markup)

    if success:
        # Проверяем, есть ли inline-меню в ответе
        inline_menu_tag = re.search(r'\[\[INLINE_MENU:(.+?)]]', new_response)
        if inline_menu_tag:
            menu_name = inline_menu_tag.group(1)
            if menu_name in inline_menus:
                await message.answer(
                    f"Кнопка '{button_text}' успешно обновлена!\n" +
                    f"Она будет использовать inline-меню '{menu_name}' с {len(inline_menus[menu_name])} кнопками."
                )
            else:
                await message.answer(
                    f"Кнопка '{button_text}' успешно обновлена, но меню '{menu_name}' не найдено.\n" +
                    "Используйте команду /add_inline_menu, чтобы создать это меню."
                )
        else:
            await message.answer(f"Кнопка '{button_text}' успешно обновлена!")
    else:
        await message.answer("Ошибка при обновлении кнопки")

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("remove_button"), AdminStates.admin_active)
async def cmd_remove_button(message: Message, state: FSMContext):
    """Начинает процесс удаления кнопки"""
    await message.answer("Введите текст кнопки для удаления:")
    await state.set_state(AdminStates.waiting_for_button_to_remove)


@admin_router.message(AdminStates.waiting_for_button_to_remove)
async def process_button_to_remove(message: Message, state: FSMContext):
    """Обрабатывает удаление кнопки"""
    button_text = message.text

    if button_text not in button_handlers:
        await message.answer(f"Кнопка '{button_text}' не найдена")
        await state.set_state(AdminStates.admin_active)
        return

    # Удаляем из словаря
    del button_handlers[button_text]

    # Перерегистрируем все обработчики
    register_handlers()

    # Сохраняем изменения
    success = save_handlers()

    if success:
        await message.answer(f"Кнопка '{button_text}' успешно удалена")
    else:
        await message.answer("Ошибка при удалении кнопки")

    await state.set_state(AdminStates.admin_active)



@admin_router.message(Command("help_admin"), AdminStates.admin_active)
async def cmd_help_admin(message: Message):
    """Выводит справку по админским командам"""
    help_text = (
        "📋 Список команд администратора:\n\n"

        "Управление кнопками:\n"
        "/add_button - Добавить новую кнопку\n"
        "/edit_button - Редактировать существующую кнопку\n"
        "/remove_button - Удалить кнопку\n"
        "/list_buttons - Показать список всех кнопок\n\n"

        "Управление inline-меню:\n"
        "/add_inline_menu - Добавить новое inline-меню\n"
        "/edit_inline_menu - Редактировать существующее inline-меню\n"
        "/remove_inline_menu - Удалить inline-меню\n"
        "/list_inline_menus - Показать список всех inline-меню\n\n"

        "Управление reply-клавиатурами:\n"
        "/add_reply_keyboard - Добавить новую reply-клавиатуру\n"
        "/edit_reply_keyboard - Редактировать существующую reply-клавиатуру\n"
        "/remove_reply_keyboard - Удалить reply-клавиатуру\n"
        "/list_reply_keyboards - Показать список всех reply-клавиатур\n\n"

        "Общие команды:\n"
        "/reload_all - Перезагрузить все данные из JSON-файлов\n"
        "/help_admin - Показать эту справку\n\n"

        "Команды смены на юзера и обратно:\n"
        "/admin_switch - Переход в режим обычного пользователя\n"
        "/admin_flex - Возврат к режиму админа\n\n"

        "Команды удаления и добавления администратора:\n"
        "/admin_add - Добавление нового администратора\n"
        "/admin_remove - Удаление прав администратора\n"
         "/admin_list - Вывести список администраторов"
    )

    await message.answer(help_text)

#---------------------------------------------------------------


@admin_router.message(Command("list_reply_keyboards"), AdminStates.admin_active)
async def cmd_list_reply_keyboards(message: Message):
    """Выводит список всех reply-клавиатур"""
    if not kb.reply_keyboards:
        await message.answer("❌ Нет зарегистрированных reply-клавиатур.")
        return

    response = "📋 Список доступных reply-клавиатур:\n\n"
    for keyboard_name, keyboard_structure in kb.reply_keyboards.items():
        response += f"📌 **{keyboard_name}**\n"
        for row in keyboard_structure:
            response += f"- {' | '.join(row)}\n"
        response += "\n"

    await message.answer(response)


@admin_router.message(Command("add_reply_keyboard"), AdminStates.admin_active)
async def cmd_add_reply_keyboard(message: Message, state: FSMContext):
    """Начинает процесс добавления новой reply-клавиатуры"""
    await message.answer("Введите имя для новой reply-клавиатуры (без пробелов):")
    await state.set_state(AdminStates.waiting_for_reply_keyboard_name)


@admin_router.message(AdminStates.waiting_for_reply_keyboard_name)
async def process_reply_keyboard_name(message: Message, state: FSMContext):
    """Обрабатывает имя новой reply-клавиатуры"""
    keyboard_name = message.text.strip()

    if ' ' in keyboard_name:
        await message.answer("❌ Имя клавиатуры не должно содержать пробелов. Введите другое имя:")
        return

    await state.update_data(reply_keyboard_name=keyboard_name)

    if keyboard_name in kb.reply_keyboards:
        await message.answer(
            f"⚠️ Клавиатура с именем '{keyboard_name}' уже существует. Хотите перезаписать?\n1. Да\n2. Нет")
        await state.set_state(AdminStates.waiting_for_reply_keyboard_overwrite)
    else:
        await message.answer(
            "Введите структуру клавиатуры в формате:\n"
            "Кнопка1, Кнопка2, Кнопка3\n"
            "Кнопка4, Кнопка5\n"
            "...\n\n"
            "Каждая строка - это ряд кнопок, разделенных запятыми. Каждая строка начинается с новой строки."
        )
        await state.set_state(AdminStates.waiting_for_reply_keyboard_structure)


@admin_router.message(AdminStates.waiting_for_reply_keyboard_overwrite)
async def process_reply_keyboard_overwrite(message: Message, state: FSMContext):
    """Обрабатывает решение о перезаписи существующей reply-клавиатуры"""
    choice = message.text.strip()

    if choice == "1" or choice.lower() == "да":
        await message.answer(
            "Введите структуру клавиатуры в формате:\n"
            "Кнопка1, Кнопка2, Кнопка3\n"
            "Кнопка4, Кнопка5\n"
            "...\n\n"
            "Каждая строка - это ряд кнопок, разделенных запятыми. Каждая строка начинается с новой строки."
        )
        await state.set_state(AdminStates.waiting_for_reply_keyboard_structure)
    else:
        await message.answer("❌ Операция отменена.")
        await state.set_state(AdminStates.admin_active)


@admin_router.message(AdminStates.waiting_for_reply_keyboard_structure)
async def process_reply_keyboard_structure(message: Message, state: FSMContext):
    """Обрабатывает структуру новой reply-клавиатуры"""
    structure_text = message.text.strip()
    data = await state.get_data()
    keyboard_name = data["reply_keyboard_name"]

    try:
        # Парсим структуру клавиатуры
        keyboard_structure = []
        for line in structure_text.split('\n'):
            if line.strip():
                row = [button.strip() for button in line.split(',')]
                keyboard_structure.append(row)

        # Сохраняем клавиатуру
        kb.reply_keyboards[keyboard_name] = keyboard_structure
        kb.save_reply_keyboards()

        # Выводим информацию о созданной клавиатуре
        response = f"✅ Reply-клавиатура '{keyboard_name}' успешно создана:\n\n"
        for row in keyboard_structure:
            response += f"- {' | '.join(row)}\n"

        await message.answer(response)
    except Exception as e:
        await message.answer(f"❌ Ошибка при создании клавиатуры: {str(e)}")

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("edit_reply_keyboard"), AdminStates.admin_active)
async def cmd_edit_reply_keyboard(message: Message, state: FSMContext):
    """Начинает процесс редактирования reply-клавиатуры"""
    if not kb.reply_keyboards:
        await message.answer("❌ Нет зарегистрированных reply-клавиатур для редактирования.")
        return

    keyboard_list = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(kb.reply_keyboards.keys())])
    await message.answer(f"Выберите клавиатуру для редактирования (введите номер):\n{keyboard_list}")
    await state.set_state(AdminStates.waiting_for_reply_keyboard_to_edit)


@admin_router.message(AdminStates.waiting_for_reply_keyboard_to_edit)
async def process_reply_keyboard_to_edit(message: Message, state: FSMContext):
    """Обрабатывает выбор reply-клавиатуры для редактирования"""
    try:
        index = int(message.text.strip()) - 1
        keyboard_names = list(kb.reply_keyboards.keys())

        if 0 <= index < len(keyboard_names):
            keyboard_name = keyboard_names[index]
            keyboard_structure = kb.reply_keyboards[keyboard_name]

            # Формируем текущую структуру для отображения
            structure_text = ""
            for row in keyboard_structure:
                structure_text += f"{', '.join(row)}\n"

            await state.update_data(reply_keyboard_to_edit=keyboard_name)
            await message.answer(
                f"Редактирование клавиатуры '{keyboard_name}'.\n\n"
                f"Текущая структура:\n{structure_text}\n\n"
                "Введите новую структуру в формате:\n"
                "Кнопка1, Кнопка2, Кнопка3\n"
                "Кнопка4, Кнопка5\n"
                "...\n\n"
                "Каждая строка - это ряд кнопок, разделенных запятыми. Каждая строка начинается с новой строки."
            )
            await state.set_state(AdminStates.waiting_for_edited_reply_keyboard_structure)
        else:
            await message.answer("❌ Неверный номер. Попробуйте снова.")
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число.")


@admin_router.message(AdminStates.waiting_for_edited_reply_keyboard_structure)
async def process_edited_reply_keyboard_structure(message: Message, state: FSMContext):
    """Обрабатывает новую структуру редактируемой reply-клавиатуры"""
    structure_text = message.text.strip()
    data = await state.get_data()
    keyboard_name = data["reply_keyboard_to_edit"]

    try:
        # Парсим новую структуру клавиатуры
        keyboard_structure = []
        for line in structure_text.split('\n'):
            if line.strip():
                row = [button.strip() for button in line.split(',')]
                keyboard_structure.append(row)

        # Обновляем клавиатуру
        kb.reply_keyboards[keyboard_name] = keyboard_structure
        kb.save_reply_keyboards()

        # Выводим информацию об обновленной клавиатуре
        response = f"✅ Reply-клавиатура '{keyboard_name}' успешно обновлена:\n\n"
        for row in keyboard_structure:
            response += f"- {' | '.join(row)}\n"

        await message.answer(response)
    except Exception as e:
        await message.answer(f"❌ Ошибка при обновлении клавиатуры: {str(e)}")

    await state.set_state(AdminStates.admin_active)


@admin_router.message(Command("remove_reply_keyboard"),AdminStates.admin_active)
async def cmd_remove_reply_keyboard(message: Message, state: FSMContext):
    """Начинает процесс удаления reply-клавиатуры"""
    if not kb.reply_keyboards:
        await message.answer("❌ Нет зарегистрированных reply-клавиатур для удаления.")
        return

    keyboard_list = "\n".join([f"{i + 1}. {name}" for i, name in enumerate(kb.reply_keyboards.keys())])
    await message.answer(f"Выберите клавиатуру для удаления (введите номер):\n{keyboard_list}")
    await state.set_state(AdminStates.waiting_for_reply_keyboard_to_remove)


@admin_router.message(AdminStates.waiting_for_reply_keyboard_to_remove)
async def process_reply_keyboard_to_remove(message: Message, state: FSMContext):
    """Обрабатывает выбор reply-клавиатуры для удаления"""
    try:
        index = int(message.text.strip()) - 1
        keyboard_names = list(kb.reply_keyboards.keys())

        if 0 <= index < len(keyboard_names):
            keyboard_name = keyboard_names[index]

            # Проверяем, используется ли клавиатура в обработчиках
            is_used = False
            for _, (_, markup_name) in button_handlers.items():
                if isinstance(markup_name, str) and markup_name == keyboard_name:
                    is_used = True
                    break

            if is_used:
                await message.answer(
                    f"⚠️ Клавиатура '{keyboard_name}' используется в обработчиках кнопок. "
                    "Вы уверены, что хотите удалить её? Это может привести к ошибкам.\n"
                    "1. Да, удалить\n"
                    "2. Нет, отменить"
                )
                await state.update_data(reply_keyboard_to_remove=keyboard_name)
                await state.set_state(AdminStates.waiting_for_reply_keyboard_remove_confirmation)
            else:
                # Удаляем клавиатуру
                del kb.reply_keyboards[keyboard_name]
                kb.save_reply_keyboards()
                await message.answer(f"✅ Reply-клавиатура '{keyboard_name}' успешно удалена.")
                await state.set_state(AdminStates.admin_active)
        else:
            await message.answer("❌ Неверный номер. Попробуйте снова.")
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число.")


@admin_router.message(AdminStates.waiting_for_reply_keyboard_remove_confirmation)
async def process_reply_keyboard_remove_confirmation(message: Message, state: FSMContext):
    """Обрабатывает подтверждение удаления используемой reply-клавиатуры"""
    choice = message.text.strip()
    data = await state.get_data()
    keyboard_name = data["reply_keyboard_to_remove"]

    if choice == "1" or choice.lower() == "да, удалить":
        # Удаляем клавиатуру
        del kb.reply_keyboards[keyboard_name]
        kb.save_reply_keyboards()
        await message.answer(
            f"✅ Reply-клавиатура '{keyboard_name}' успешно удалена. Обратите внимание, что обработчики, использующие эту клавиатуру, могут работать некорректно.")
    else:
        await message.answer("❌ Операция отменена.")

    await state.set_state(AdminStates.admin_active)

@admin_router.message(AdminStates.waiting_for_user_test_confirmation)
async def process_user_test_confirmation(message: Message, state: FSMContext):
    """Позволяет администратору протестировать функциональность обычного юзера"""
    choice = message.text.strip().lower()

    if choice == "1":
        await message.answer(
            "Вы вошли в режим тестирования как пользователь.\n"
            "Все действия, которые вы совершите далее, будут выполняться в контексте обычного пользователя.\n\n"
            "Чтобы выйти из этого режима и вернуться в админ-панель, введите /admin_flex.",
            reply_markup=kbb.get_main_menu()
        )
        # Устанавливаем состояние как будто это обычный пользователь
        await state.set_state(UserStates.user_active)
    else:
        await message.answer("Тестирование отменено.")
        await state.set_state(AdminStates.admin_active)

@admin_router.message(F.text == "/admin_switch")
async def ask_for_test_confirmation(message: Message, state: FSMContext):
    """Спрашивает у админа подтверждение на вход в режим тестирования"""


    # 1. Получаем информацию о пользователе из БД
    user_data = await get_user_by_id(str(message.from_user.id))

    if not user_data or user_data.get('role') != 'admin':
        await state.set_state(UserStates.user_active)
        return

    current_state = await state.get_state()

    if current_state == UserStates.user_active.state:
        await message.answer("Вы уже находитесь в режиме пользователя. Для возврата используйте /admin_flex.")
        await state.set_state(UserStates.user_active)
        return

    await message.answer(
        "Вы уверены, что хотите перейти в режим пользователя для тестирования?(напишите 1 или 2)\n\n"
        "1. Да\n"
        "2. Нет, отмена"
    )
    await state.set_state(AdminStates.waiting_for_user_test_confirmation)



@admin_router.message(F.text == "/admin_flex")
async def return_to_admin_mode(message: Message, state: FSMContext):
    user_data = await get_user_by_id(str(message.from_user.id))

    if not user_data or user_data.get('role') != 'admin':
        await state.set_state(UserStates.user_active)
        return

    current_state = await state.get_state()
    if current_state != UserStates.user_active.state:
        await message.answer("Вы не в режиме пользователя.")
        return

    await state.set_state(AdminStates.admin_active)
    await message.answer("Вы вернулись в админ-панель.")







# для добавления админа
@admin_router.message(F.text == "/admin_add")
async def add_admin(message: Message, state: FSMContext):
    user_data = await get_user_by_id(str(message.from_user.id))

    if not user_data or user_data.get('role') != 'admin':
        await state.set_state(UserStates.user_active)
        return

    current_state = await state.get_state()
    if current_state == UserStates.user_active.state:
        await state.set_state(UserStates.user_active)
        return

    await message.answer(
        "Введите номер телефона пользователя, которого хотите наделить правами администратора"
    )
    await state.set_state(AdminStates.waiting_admin_phone)

# Хэндлер ввода номера телефона
@admin_router.message(AdminStates.waiting_admin_phone)
async def process_admin_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    user = await get_user_by_phone(phone)

    if not user:
        await message.answer(f"Пользователь с номером {phone} не найден")
        await state.set_state(AdminStates.admin_active)
        return

    if user['role'] == 'admin':
        await message.answer(f"Пользователь {phone} уже администратор")
        await state.set_state(AdminStates.admin_active)
        return

    await update_user_role(phone, 'admin')
    await message.answer(
        f"Пользователь {user['name']} {user['surname']} ({phone}) теперь администратор"
    )
    await state.set_state(AdminStates.admin_active)

#  для удаления админа
# Команда для удаления администратора
@admin_router.message(F.text == "/admin_remove")
async def remove_admin(message: Message, state: FSMContext):
    user_data = await get_user_by_id(str(message.from_user.id))

    if not user_data or user_data.get('role') != 'admin':
        await state.set_state(UserStates.user_active)
        return

    current_state = await state.get_state()
    if current_state == UserStates.user_active.state:
        await state.set_state(UserStates.user_active)
        return

    """Запрос номера телефона для снятия прав администратора"""
    await message.answer(
        "Введите номер телефона пользователя, у которого нужно забрать права администратора"
    )
    await state.set_state(AdminStates.admin_remove)

# Обработка номера телефона для удаления прав администратора
@admin_router.message(AdminStates.admin_remove)
async def process_remove_admin(message: Message, state: FSMContext):
    phone = message.text.strip()
    user = await get_user_by_phone(phone)

    if not user:
        await message.answer(f"Пользователь с номером {phone} не найден")
        return

    if user['role'] != 'admin':
        await message.answer(f"Пользователь {phone} не является администратором")
        return

    await update_user_role(phone, 'user')
    await message.answer(
        f"Пользователь {user['name']} {user['surname']} ({phone}) больше не администратор"
    )
    await state.set_state(AdminStates.admin_active)

#  для списка админов
@admin_router.message(F.text == "/admin_list")
async def list_admins(message: Message, state: FSMContext):

    user_data = await get_user_by_id(str(message.from_user.id))

    if not user_data or user_data.get('role') != 'admin':
        await state.set_state(UserStates.user_active)
        return

    current_state = await state.get_state()
    if current_state == UserStates.user_active.state:
        await state.set_state(UserStates.user_active)
        return

    """Показать всех администраторов"""
    admins = await get_all_admins()

    if not admins:
        await message.answer(" Нет зарегистрированных администраторов")
        await state.set_state(AdminStates.admin_active)
        return

        # Форматируем список администраторов
    admin_list = "📋 Список администраторов:\n\n" + "\n".join(
        f"{i + 1}. {admin['name']} {admin['surname']} "
        f"(тел: {admin['number']}, ID: {admin['user_id']})"
        for i, admin in enumerate(admins))

    await message.answer(admin_list)
    await state.set_state(AdminStates.admin_active)


# Инициализация при импорте модуля
load_handlers()
load_inline_menus()
register_handlers()
