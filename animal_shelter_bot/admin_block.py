from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from animal_shelter_bot.const.messages import Messages
from animal_shelter_bot.const.buttons import AdminButtons
from animal_shelter_bot.utils import validate_phone
from animal_shelter_bot import db

router = Router()

class AdminAction(StatesGroup):
    add_admin_phone = State()
    remove_admin_phone = State()

def get_admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=AdminButtons.manage_admins)],
            [KeyboardButton(text=AdminButtons.upload_content)],
            [KeyboardButton(text=AdminButtons.get_report)],
        ],
        resize_keyboard=True
    )

def get_manage_admins_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=AdminButtons.add_admin), KeyboardButton(text=AdminButtons.remove_admin)],
            [KeyboardButton(text=AdminButtons.back_to_admin_menu)],
        ],
        resize_keyboard=True
    )

async def show_admin_menu(message: Message):
    await message.answer("🛠 Главное меню администратора:", reply_markup=get_admin_menu())

@router.message(F.text == AdminButtons.manage_admins)
async def manage_admins(message: Message):
    await message.answer("Что вы хотите сделать?", reply_markup=get_manage_admins_menu())

@router.message(F.text == AdminButtons.add_admin)
async def ask_add_admin_phone(message: Message, state: FSMContext):
    await message.answer(Messages.ask_phone_for_add)
    await state.set_state(AdminAction.add_admin_phone)

@router.message(AdminAction.add_admin_phone)
async def process_add_admin_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not validate_phone(phone):
        return await message.answer(Messages.invalid_phone)

    if not db.user_exists(phone):
        return await message.answer(Messages.user_not_found)

    db.set_role(phone, "admin")
    await message.answer(Messages.admin_added, reply_markup=get_manage_admins_menu())
    await state.clear()

@router.message(AdminAction.remove_admin_phone)
async def process_remove_admin_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    
    # Проверка формата номера
    if not validate_phone(phone):
        return await message.answer(Messages.invalid_phone)
    
    # Проверка, что пользователь существует
    if not db.user_exists(phone):
        return await message.answer(Messages.user_not_found)
    
    # Получаем номер текущего админа
    current_admin_phone = message.contact.phone_number if hasattr(message, 'contact') else None
    
    # Запрет на удаление самого себя
    if phone == current_admin_phone:
        return await message.answer("❌ Вы не можете снять права с самого себя!")
    
    # Снимаем права
    db.set_role(phone, "user")
    await message.answer(Messages.admin_removed, reply_markup=get_manage_admins_menu())
    await state.clear()

@router.message(F.text == AdminButtons.upload_content)
async def upload_content_placeholder(message: Message):
    await message.answer("📤 Функция загрузки контента пока не реализована.")

@router.message(F.text == AdminButtons.get_report)
async def get_report_placeholder(message: Message):
    await message.answer("📊 Отчет пока недоступен.")

@router.message(F.text == AdminButtons.back_to_admin_menu)
async def back_to_admin_menu(message: Message):
    await show_admin_menu(message)

def setup_admin_handlers(dp):
    dp.include_router(router)
