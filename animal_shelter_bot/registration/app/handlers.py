"""Модуль с описанием хэндлеров для регистрации"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from animal_shelter_bot.registration.app import keyboards as kb
from animal_shelter_bot.user_block.app import keyboards as ukb
from animal_shelter_bot.states import Registration, UserStates, AdminStates
from animal_shelter_bot.registration.app.utils import check_number, validate_name, validate_email, validate_age, validate_city_name
from animal_shelter_bot.registration.const import RegistrationButtons, RegistrationMessages
from animal_shelter_bot.registration.app.db import get_user_by_phone, add_new_user, get_user_by_id


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
    if not check_number(message.text):
        await message.answer(RegistrationMessages.FAILED_LOGIN)
        return

    await state.update_data(contact_number=message.text)
    user = await get_user_by_phone(message.text)  # ищем по номеру

    if user:

        if str(user['user_id']) != str(message.from_user.id):
            await message.answer("Этот номер телефона уже зарегистрирован другим пользователем.")
            await message.answer(RegistrationMessages.TYPE_NUMBER)
            return


        # Пользователь найден
        role = user['role']
        #await message.answer(f"{RegistrationMessages.SUCCESS_LOGIN} {message.text}")
        #await state.clear()

        if role == 'admin':
            await state.set_state(AdminStates.admin_active)
            await message.answer("Вы вошли как админ. Для вывода команд напишите /help_admin")
        else:
            await state.set_state(UserStates.user_active)
            await message.answer(
                f'{RegistrationMessages.SUCCESS_LOGIN} {user['number']}',
                reply_markup=kb.get_main_menu()
            )

    else:
        # Новый пользователь — начать регистрацию
        await state.set_state(Registration.waiting_name)
        await message.answer(RegistrationMessages.ASK_NAME)




@registration_router.message(Registration.waiting_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not validate_name(name):
        await message.answer(RegistrationMessages.INVALID_NAME)
        return

    await state.update_data(name=name)
    await state.set_state(Registration.waiting_surname)
    await message.answer(RegistrationMessages.ASK_SURNAME)


@registration_router.message(Registration.waiting_surname)
async def process_surname(message: Message, state: FSMContext):
    surname = message.text.strip()

    if not validate_name(surname):
        await message.answer(RegistrationMessages.INVALID_SURNAME)
        return

    await state.update_data(surname=surname)
    await state.set_state(Registration.waiting_email)
    await message.answer(RegistrationMessages.ASK_EMAIL)


@registration_router.message(Registration.waiting_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()

    if not validate_email(email):
        await message.answer(RegistrationMessages.INVALID_EMAIL)
        return

    await state.update_data(email=email)
    await state.set_state(Registration.waiting_age)
    await message.answer(RegistrationMessages.ASK_AGE)


@registration_router.message(Registration.waiting_age)
async def process_age(message: Message, state: FSMContext):
    age = message.text.strip()

    if not validate_age(age):
        await message.answer(RegistrationMessages.INVALID_AGE)
        return

    await state.update_data(age=int(age))
    await state.set_state(Registration.waiting_city)
    await message.answer(RegistrationMessages.ASK_CITY)


@registration_router.message(Registration.waiting_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    if not validate_city_name(city):
        await message.answer(RegistrationMessages.INVALID_CITY)
        return

    await state.update_data(city=city)

    data = await state.get_data()
    user_id = str(message.from_user.id)

    # Проверка: есть ли пользователь с этим user_id
    existing_user_by_id = await get_user_by_id(user_id)
    if existing_user_by_id:
        await message.answer("Вы уже зарегистрированы в системе с другим номером, пожалуйста, используйте его для входа.")
        await message.answer(RegistrationMessages.GREETING, reply_markup=kb.contact_keyboard)
        return



    # Добавляем await перед вызовом асинхронной функции
    await add_new_user(
        user_id=user_id,
        name=data['name'],
        surname=data['surname'],
        number=data['contact_number'],
        email=data['email'],
        age=data['age'],
        city=data['city'],
        role='user'
    )

    await message.answer("Город принят, сохраняю...")
    await state.set_state(UserStates.user_active)

    await message.answer(
        RegistrationMessages.REG_COMPLETE,
        reply_markup=kb.get_main_menu()

    )
@registration_router.message()
async def handle_any_message(message: Message, state: FSMContext) -> None:
    """Обработчик любого сообщения от незарегистрированного пользователя"""
    # Проверяем текущее состояние пользователя
    current_state = await state.get_state()

    # Если у пользователя нет состояния или он не в процессе регистрации
    if not current_state:
        # Начинаем процесс регистрации
        await message.answer(RegistrationMessages.GREETING, reply_markup=kb.contact_keyboard)