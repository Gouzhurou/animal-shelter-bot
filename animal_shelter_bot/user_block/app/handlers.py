"""Модуль с описанием хэндлеров пользователя"""

from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
from animal_shelter_bot.user_block.app import keyboards as kb
from animal_shelter_bot.user_block.const import UserButtons, UserMessages
from animal_shelter_bot.states import UserStates


user_router = Router()


@user_router.message(Command("start"), UserStates.user_active)
async def start_handler(message: Message) -> None:
    """Обработчик команды /start.

    Args:
        message: Объект входящего сообщения от пользователя

    Пример ответа:
        "Привет! Я бот."
    """
    greeting = "Привет! Я бот."
    await message.answer(greeting, reply_markup=kb.main_menu_first_page)


@user_router.message(F.text == UserButtons.VIEW_ABOUT_US, UserStates.user_active)
async def about_us_handler(message: Message):
    """Обработчик кнопки 'о нас'"""
    await message.answer(UserMessages.ABOUT_US)


@user_router.message(F.text == UserButtons.VIEW_ADDRESS, UserStates.user_active)
async def address_handler(message: Message):
    """Обработчик кнопки 'наш адрес'"""
    await message.answer(UserMessages.ADDRESS)
