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
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_bot() -> Tuple[Bot, Dispatcher]:
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not telegram_token:
        error_msg = "Токен бота не найден в .env файле!"
        logger.error(error_msg)
        raise ValueError(error_msg)
    logger.info("Бот успешно инициализирован")
    return Bot(token=telegram_token), Dispatcher()

bot, dp = setup_bot()

# --- Inline keyboard ----
def get_start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Запустить",
            callback_data="start_bot"
        )
    )
    return kb.as_markup()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """
    При /start — отправляет приветствие и inline-кнопку "Запустить"
    """
    text = "Привет. Меня зовут Фуражкин и я готов вам помочь."
    await message.answer(
        text,
        reply_markup=get_start_keyboard()
    )
    logger.info(f"Показано приветствие пользователю {message.from_user.id}")

@dp.callback_query(lambda c: c.data == "start_bot")
async def on_start_btn(callback: types.CallbackQuery):
    """
    Обработка нажатия inline-кнопки "Запустить"
    """
    await callback.answer("Бот запущен! Чем могу помочь?", show_alert=True)
    logger.info(f"Пользователь нажал 'Запустить': {callback.from_user.id}")


async def main() -> None:
    """Основная асинхронная функция для запуска бота."""
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("Ошибка в работе бота: %s", e)
    finally:
        logger.info("Бот остановлен")

if __name__ == "__main__":
    # Для Windows-систем
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
