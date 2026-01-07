import re


def validate_date_format(date_str):
    """Проверка формата дд.мм.гггг и года 2026."""
    pattern = r'^\d{2}\.\d{2}\.2026$'
    return bool(re.match(pattern, date_str))


def validate_amount(amount_str):
    """Проверка, что введено положительное число."""
    try:
        val = float(amount_str)
        return val >= 0
    except ValueError:
        return False


def validate_not_empty(text_str):
    """Проверка, что строка не пустая."""
    return bool(text_str.strip())
