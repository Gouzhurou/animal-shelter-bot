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

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_bot() -> Tuple[Bot, Dispatcher]:
    """Инициализирует и возвращает экземпляры бота и диспетчера.
    
    Returns:
        Tuple[Bot, Dispatcher]: Кортеж с объектами бота и диспетчера
    
    Raises:
        ValueError: Если токен бота не найден в .env файле
    """
    load_dotenv()

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        error_msg = "Токен бота не найден в .env файле!"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Бот успешно инициализирован")
    return Bot(token=telegram_token), Dispatcher()


bot, dp = setup_bot()


@dp.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    """Обработчик команды /start.
    
    Args:
        message: Объект входящего сообщения от пользователя
    
    Пример ответа:
        "Привет! Я бот."
    """
    greeting = "Привет! Я бот."
    await message.answer(greeting)
    logger.info("Новый пользователь: {}", message.from_user.id)


async def main() -> None:
    """Основная асинхронная функция для запуска бота."""
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("Ошибка в работе бота: {}", e)
    finally:
        logger.info("Бот остановлен")


if __name__ == "__main__":
    # Для Windows-систем
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
