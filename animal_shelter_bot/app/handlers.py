"""Модуль где будут хранится все хэндлеры"""

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery #Проще импортировать нужные типы так, чтобы не писать постоянно types.
from aiogram import Router, F
import app.keyboards as kb #Содержит клавиатуры


h_router = Router() #По сути, объект исполняющий роль Диспетчера в данном файле
@h_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Обработчик команды /start.

    Args:
        message: Объект входящего сообщения от пользователя

    Пример ответа:
        "Привет! Я бот."
    """
    greeting = "Привет! Я бот."
    await message.answer(greeting, reply_markup=kb.main_menu)
    #logger.info("Новый пользователь: {}", message.from_user.id) потом)


@h_router.message(F.text == 'Посмотреть GitHub проекта')
async def git_hub_link_handler(message: Message):
    """Орбраточик запроса ссылки на Git для демонстрации работы меню"""
    await message.answer('Вы можете ознакомится с гитхабом проекта по ссылке ниже', reply_markup=kb.inline_example)


@h_router.message(F.text == 'О нас')
async def about_us_handler(message: Message):
    """Обработик кнопки 'о нас' вызывает соответствующее inline меню"""
    await message.answer('Что именно вы бы хотели узнать о нас?', reply_markup=kb.inline_about_us)


@h_router.callback_query(F.data == 'back_about_us')
async def back_about_us_handler(callback: CallbackQuery):
    """Обработик кнопки 'назад' в inline меню 'о нас' возвращает меню в старотовое состояние"""
    await callback.answer()
    await callback.message.edit_text('Что именно вы бы хотели узнать о нас?', reply_markup=kb.inline_about_us)


@h_router.callback_query(F.data == 'our_principles')
async def our_principles_handler(callback: CallbackQuery):
    """Обработик кнопки 'наши принципы' в inline меню 'о нас' выводит текст"""
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


@h_router.callback_query(F.data == 'our_address')
async def our_address_handler(callback: CallbackQuery):
    """Обработик кнопки 'наш адрес' в inline меню 'о нас' выводит текст"""
    await callback.answer()
    await callback.message.edit_text('г.Санкт Петербург\n'
                                    'м.Кировский Завод\n'
                                    'Автовская 31 лит И.', reply_markup=kb.inline_back_about_us)


@h_router.callback_query(F.data == 'opening_hours')
async def opening_hours_handler(callback: CallbackQuery):
    """Обработик кнопки 'часы работы' в inline меню 'о нас' выводит текст"""
    await callback.answer()
    await callback.message.edit_text('Ежедневно с 10.00-22.00', reply_markup=kb.inline_back_about_us)
