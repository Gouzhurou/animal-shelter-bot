from aiogram import Router, F
from aiogram.types import Message, Contact, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from animal_shelter_bot.const.messages import Messages
from animal_shelter_bot.const.buttons import Buttons
from animal_shelter_bot import db
from animal_shelter_bot.utils import validate_name, validate_age, validate_email, validate_city, validate_phone
from animal_shelter_bot.user_block import show_user_menu
from animal_shelter_bot.admin_block import show_admin_menu

router = Router()

class Registration(StatesGroup):
    name = State()
    surname = State()
    email = State()
    age = State()
    city = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=Buttons.send_phone, request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "📱 Для входа отправьте номер телефона в формате +7XXXXXXXXXX или нажмите кнопку ниже:",
        reply_markup=kb
    )

@router.message(F.contact)
async def contact_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await process_phone_number(phone, message, state)

@router.message(F.text.regexp(r'^\+7\d{10}$'))
async def manual_phone_input(message: Message, state: FSMContext):
    phone = message.text
    await process_phone_number(phone, message, state)

async def process_phone_number(phone: str, message: Message, state: FSMContext):
    if not validate_phone(phone):
        return await message.answer("❌ Неверный формат номера. Используйте +7XXXXXXXXXX.")

    role = db.check_user(phone)
    if role == "admin":
        await show_admin_menu(message)
    elif role == "user":
        await show_user_menu(message)
    else:
        await state.update_data(phone=phone)
        await message.answer(Messages.ask_name, reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.name)

@router.message(Registration.name)
async def name_handler(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer(Messages.invalid_name)
    await state.update_data(name=message.text)
    await message.answer(Messages.ask_surname)
    await state.set_state(Registration.surname)

@router.message(Registration.surname)
async def surname_handler(message: Message, state: FSMContext):
    if not validate_name(message.text):
        return await message.answer(Messages.invalid_surname)
    await state.update_data(surname=message.text)
    await message.answer(Messages.ask_email)
    await state.set_state(Registration.email)

@router.message(Registration.email)
async def email_handler(message: Message, state: FSMContext):
    if not validate_email(message.text):
        return await message.answer(Messages.invalid_email)
    await state.update_data(email=message.text)
    await message.answer(Messages.ask_age)
    await state.set_state(Registration.age)

@router.message(Registration.age)
async def age_handler(message: Message, state: FSMContext):
    if not validate_age(message.text):
        return await message.answer(Messages.invalid_age)
    await state.update_data(age=message.text)
    await message.answer(Messages.ask_city)
    await state.set_state(Registration.city)

@router.message(Registration.city)
async def city_handler(message: Message, state: FSMContext):
    if not validate_city(message.text):
        return await message.answer(Messages.invalid_city)

    await state.update_data(city=message.text)
    data = await state.get_data()
    db.register_user(data)

    await message.answer(Messages.registration_complete)
    await show_user_menu(message)
    await state.clear()

def setup_registration_handlers(dp):
    dp.include_router(router)
