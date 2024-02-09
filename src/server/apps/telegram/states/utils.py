import phonenumbers
from phonenumbers import NumberParseException


class PhoneNumberNotValid(Exception):
    """Переопределение ошибки ввода номера телефона."""


def validate_phone_number(phone_number: str):
    """Функция валидации веденного номера телефона."""
    try:
        parse_number = phonenumbers.parse(phone_number, 'RU')
    except NumberParseException:
        raise PhoneNumberNotValid

    if not phonenumbers.is_valid_number(parse_number):
        raise PhoneNumberNotValid

    return phone_number
