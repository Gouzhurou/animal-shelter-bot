"""Модуль со вспомогательными функциями"""

import re

def check_number(number) -> bool:
    """Проверяет, соответствует ли номер телефона требованиям"""
    if len(number) == 11 and number[0] == '8' and number.isdigit():
        return True
    if len(number) == 12 and number[:2] == '+7' and number[2:].isdigit():
        return True
    return False

def validate_name(text: str) -> bool:
    """Проверяет, что имя/фамилия содержит  буквы (включая ёЁ) и дефисы, но не разрешаем дефисы в начале/конце, имеет длину не менее 2 символов"""
    return (re.fullmatch(r'^[а-яА-ЯёЁa-zA-Z]+(?:-[а-яА-ЯёЁa-zA-Z]+)*$', text)
            and len(text) >= 2)

def validate_city_name(text: str) -> bool:
    """Проверяет название города (допускает дефисы, пробелы, точки)"""
    # Разрешаем: буквы, пробелы, дефисы, точки, апострофы
    # Запрещаем специальные символы и цифры
    return (re.fullmatch(r'^[а-яА-ЯёЁa-zA-Z\s\-\.\']+$', text)
            and len(text) >= 2
            and len(text) <= 100)


def validate_email(email: str) -> bool:
    """Проверяет email по стандартному шаблону"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.fullmatch(pattern, email) is not None


def validate_age(age: str) -> bool:
    """Проверяет, что возраст - число от 1 до 120"""
    return age.isdigit() and 1 <= int(age) <= 120

def normalize_phone(phone: str) -> str:
    """Приводит номер телефона к виду 7921XXXXXXX (без +, чтобы было универсальнее)"""
    digits = re.sub(r'\D', '', phone)

    if digits.startswith('8'):
        digits = '7' + digits[1:]  # заменяем 8 на 7
    elif digits.startswith('7') and len(digits) == 11:
        pass  # норм
    elif digits.startswith('9') and len(digits) == 10:
        digits = '7' + digits  # добавляем 7

    return digits