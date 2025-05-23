"""
Модуль main для телеграм-бота приюта животных.

Основные функции:
- Инициализация бота с конфигурацией из .env
- Обработка команды /start
- Запуск long-polling
"""

import os
import asyncio
import logging
from typing import Tuple
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


GREETING_MESSAGE = "Привет! Я бот."
TOKEN_ERROR_MSG = "Токен бота не найден в .env файле!"
BOT_INIT_SUCCESS_MSG = "Бот успешно инициализирован"
BOT_START_MSG = "Запуск бота..."
BOT_STOP_MSG = "Бот остановлен"

START_BOT_CALLBACK = "start_bot"

START_BUTTON_TEXT = "Начать"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_bot() -> Tuple[Bot, Dispatcher]:
    """
    Настройка и инициализация бота.
    
    Returns:
        Tuple[Bot, Dispatcher]: Инициализированные экземпляры бота и диспетчера.
        
    Raises:
        ValueError: Если токен бота не найден в .env файле.
    """
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        logger.error(TOKEN_ERROR_MSG)
        raise ValueError(TOKEN_ERROR_MSG)

    logger.info(BOT_INIT_SUCCESS_MSG)
    return Bot(token=telegram_token), Dispatcher()


def get_start_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт и возвращает инлайн-клавиатуру для стартового сообщения бота.
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой для начала работы с ботом.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=START_BUTTON_TEXT, callback_data=START_BOT_CALLBACK)]
    ])
    return keyboard


bot, dp = setup_bot()


@dp.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    """
    Обработчик команды /start. Отправляет приветственное сообщение пользователю.
    
    Args:
        message (types.Message): Сообщение пользователя.
    """
    await message.answer(GREETING_MESSAGE, reply_markup=get_start_keyboard())
    logger.info(f"Новый пользователь: {message.from_user.id}")


@dp.callback_query(lambda c: c.data == START_BOT_CALLBACK)
async def on_start_button(callback: types.CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Начать".
    
    Args:
        callback (types.CallbackQuery): Данные обратного вызова.
    """
    await callback.answer()
    await callback.message.answer("Вы нажали кнопку Начать!")
    logger.info(f"Пользователь {callback.from_user.id} нажал кнопку Начать")


async def main() -> None:
    """Основная асинхронная функция для запуска бота."""
    try:
        logger.info(BOT_START_MSG)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка в работе бота: {e}")
    finally:
        logger.info(BOT_STOP_MSG)


if __name__ == "__main__":
    # Для Windows-систем
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
