"""Модуль с описанием состояний"""

from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    """Класс с состояниями регистрации"""
    waiting_number = State()


class UserStates(StatesGroup):
    """Класс с состояниями пользователя"""
    user_active = State()


class AdminStates(StatesGroup):
    """Класс с состояниями администратора"""
    admin_active = State()
