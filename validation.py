import re

def validate_email(email):
    """
    Проверяет, что адрес электронной почты имеет правильный формат.

    :param email: Адрес электронной почты.
    :return: True, если формат корректен, False в противном случае.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_phone(phone_number):
    """
    Проверяет, что номер телефона содержит только цифры.

    :param phone_number: Номер телефона.
    :return: True, если номер корректен, False в противном случае.
    """
    return phone_number.isdigit()
