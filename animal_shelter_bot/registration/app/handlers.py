"""Модуль с описанием хэндлеров для регистрации"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from animal_shelter_bot.registration.app import keyboards as kb
from animal_shelter_bot.user_block.app import keyboards as ukb
from animal_shelter_bot.states import Registration, UserStates
from animal_shelter_bot.registration.app.utils import check_number
from animal_shelter_bot.registration.const import RegistrationButtons, RegistrationMessages


registration_router = Router()


@registration_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Обработчик команды /start при первом использовании"""
    await message.answer(RegistrationMessages.GREETING, reply_markup=kb.contact_keyboard)


@registration_router.message(F.text == RegistrationButtons.GET_NUMBER)
async def get_number_handler(message: Message, state: FSMContext) -> None:
    """Обработчик кнопки 'Предоставить номер'"""
    await state.set_state(Registration.waiting_number)
    await message.answer(RegistrationMessages.TYPE_NUMBER)


@registration_router.message(Registration.waiting_number)
async def get_contact_number(message: Message, state: FSMContext) -> None:
    """Обработчик номера телефона"""
    if check_number(message.text):
        await state.update_data(contact_number=message.text)
        await state.set_state(UserStates.user_active)
        data = await state.get_data()  # TODO: сравнить полученные данные с бд
        await message.answer(f'{RegistrationMessages.SUCCESS_LOGIN} {data['contact_number']}',
                                 reply_markup=ukb.main_menu_first_page)
    else:
        await message.answer(RegistrationMessages.FAILED_LOGIN)
