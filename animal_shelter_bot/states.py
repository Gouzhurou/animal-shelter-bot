"""Модуль с описанием состояний"""

from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    """Класс с состояниями регистрации"""
    waiting_number = State()
    waiting_name = State()
    waiting_surname = State()
    waiting_email = State()
    waiting_age = State()
    waiting_city = State()

class UserStates(StatesGroup):
    """Класс с состояниями пользователя"""
    user_active = State()




class AdminStates(StatesGroup):
    """Класс с состояниями администратора"""
    admin_active = State()
    waiting_for_button_text = State()
    waiting_for_response_text = State()
    waiting_for_inline_menu_action = State()
    waiting_for_inline_menu_buttons = State()
    waiting_for_markup_type = State()
    waiting_for_inline_menu_name = State()
    waiting_for_menu_overwrite_confirm = State()
    waiting_for_new_inline_menu_buttons = State()
    waiting_for_menu_to_remove = State()
    waiting_for_menu_to_edit = State()
    waiting_for_edited_menu_buttons = State()
    waiting_for_button_to_edit = State()
    waiting_for_edited_button_text = State()
    waiting_for_button_to_remove = State()
    waiting_for_new_response = State()
    waiting_for_missing_menu_action = State()
    waiting_for_new_markup = State()
    waiting_for_new_menu_buttons = State()
    waiting_for_reset_confirmation = State()
    waiting_for_reply_keyboard_name = State()
    waiting_for_reply_keyboard_overwrite = State()
    waiting_for_reply_keyboard_structure = State()
    waiting_for_reply_keyboard_to_edit = State()
    waiting_for_edited_reply_keyboard_structure = State()
    waiting_for_reply_keyboard_to_remove = State()
    waiting_for_reply_keyboard_remove_confirmation = State()
    waiting_for_user_test_confirmation = State()
    waiting_admin_phone = State()
    admin_remove= State()