"""Модуль с описанием хэндлеров пользователя"""

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
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


@user_router.message(F.text == 'Посмотреть GitHub проекта')
async def git_hub_link_handler(message: Message):
    """Обработчик запроса ссылки на Git для демонстрации работы меню"""
    await message.answer('Вы можете ознакомится с гитхабом проекта по ссылке ниже',
                         reply_markup=kb.inline_example)


@user_router.message(F.text == UserButtons.VIEW_ABOUT_US, UserStates.user_active)
async def about_us_handler(message: Message):
    """Обработчик кнопки 'о нас'"""
    await message.answer(UserMessages.ABOUT_US)


@user_router.message(F.text == UserButtons.VIEW_ADDRESS, UserStates.user_active)
async def address_handler(message: Message):
    """Обработчик кнопки 'наш адрес'"""
    await message.answer(UserMessages.ADDRESS)


@user_router.callback_query(F.data == 'back_about_us')
async def back_about_us_handler(callback: CallbackQuery):
    """Обработчик кнопки 'назад' в inline меню 'о нас'"""
    await callback.answer()
    await callback.message.edit_text('Что именно вы бы хотели узнать о нас?',
                                     reply_markup=kb.inline_about_us)


@user_router.callback_query(F.data == 'our_principles')
async def our_principles_handler(callback: CallbackQuery):
    """Обработчик кнопки 'наши принципы' в inline меню 'о нас'"""
    await callback.answer()
    await callback.message.edit_text('Мы негосударственная организация, поэтому сами находим '
                                    'деньги на работу наших проектов:'
                                    'собираем пожертвования, ищем спонсоров, '
                                    'гранты, субсидии.'
                                    '\nВсю свою работу мы осуществляем на '
                                    'территории собственного приюта для животных.'
                                    'Мы оказываем помощь травмированным и больным '
                                    'бездомным животным, проводим льготные '
                                    'массовые стерилизации и вакцинации, ищем новые '
                                    'семьи для наших подопечных, проводим '
                                    'уроки доброты. Помогаем другим приютам и '
                                    'кураторам.'
                                    '\nНа попечении более 900 животных'
                                    '\nСтроим Центр Помощи Животным.'
                                    '\nПридерживаемся принципов 5 свобод животных.',
                                     reply_markup=kb.inline_back_about_us)


@user_router.callback_query(F.data == 'our_address')
async def our_address_handler(callback: CallbackQuery):
    """Обработчик кнопки 'наш адрес' в inline меню 'о нас' """
    await callback.answer()
    await callback.message.edit_text('г.Санкт Петербург\n'
                                    'м.Кировский Завод\n'
                                    'Автовская 31 лит И.', reply_markup=kb.inline_back_about_us)


@user_router.callback_query(F.data == 'opening_hours')
async def opening_hours_handler(callback: CallbackQuery):
    """Обработчик кнопки 'часы работы' в inline меню 'о нас' """
    await callback.answer()
    await callback.message.edit_text('Ежедневно с 10.00-22.00',
                                     reply_markup=kb.inline_back_about_us)
