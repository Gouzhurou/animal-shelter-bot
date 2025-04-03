"""Модуль со вспомогательными функциями"""


def check_number(number) -> bool:
    """Проверяет, соответствует ли номер телефона требованиям"""
    if len(number) == 11 and number[0] == '8' and number.isdigit():
        return True
    if len(number) == 12 and number[:2] == '+7' and number[2:].isdigit():
        return True
    return False
