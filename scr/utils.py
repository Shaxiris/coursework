import json
from class_payment.payment import Payment
from datetime import datetime
from typing import Iterator
import os


def get_path_to_file(name_file: str, *dirs: str) -> str:
    """
    Возвращает абсолютный путь к файлу с платёжными операциями,
    вне зависимости от места запуска скрипта.

    :param name_file: название файла с операциями
    :param dirs: папка или папки, в которых расположен файл с операциями,
    если смотреть путь от корневой папки проекта
    """
    path_current_file = os.path.abspath(__file__)
    root_dir_path = os.path.dirname(os.path.dirname(path_current_file))
    path_to_file = os.path.join(root_dir_path, *dirs, name_file)
    return path_to_file


def get_payments(path: str, parameters: set) -> Iterator[dict]:
    """
    Функция фильтрует и сортирует по дате в обратном порядке
    релевантные для нас значения из списка словарей с информацией
    о платежах.

    :param path: путь к JSON-файлу, содержащему список словарей
    :param parameters: обязательные характеристики платежа

    :return: итератор на основе отсортированного списка словарей платежа
    """
    with open(path, "rt", encoding="utf-8") as json_file:
        payments = json.load(json_file)

    successful_payments = [pay for pay in payments if check_payment(pay, parameters)]
    successful_payments.sort(reverse=True, key=reformat_date)

    latest_payments = iter(successful_payments)

    return latest_payments


def check_payment(pay: dict, parameters: set) -> bool:
    """
    Функция проверяет, соответствует ли платёж требованиям.

    Проверки:
    был ли платёж успешным ("state": "executed");
    содержит ли информация о платеже все необходимые характеристики;
    является ли дата платежа корректной

    :param pay: словарь, содержащий информацию о платеже
    :param parameters: обязательные характеристики платежа
    """
    state = pay.get("state")
    if not state:
        return False
    if state.lower() != "executed":
        return False
    elif not parameters.issubset(set(pay.keys())):
        return False
    elif not all(pay.values()):
        return False
    elif not check_date(pay.get("date")):
        return False

    return True


def check_date(date: str) -> bool:
    """
    Проверяет корректность формата даты и
    её соответствие принятой форме записи
    """
    if type(date) is not str:
        return False
    if len(date.split("T")) != 2:
        return False

    try:
        datetime.fromisoformat(date.replace("T", " "))
    except ValueError:
        return False

    return True


def reformat_date(pay: dict) -> datetime:
    """
    Функция для корректной сортировки значений по дате.
    Приводит строку к формату datetime, если строка соответствует
    принятому формату записи

    Обязательно должна идти после фильтрации значений
    на соответствие требуемому формату
    """
    date_pay = pay.get("date").replace("T", " ")
    date = datetime.fromisoformat(date_pay)

    return date


def create_payment(pay: dict) -> Payment:
    """
    Создает и возвращает объект класса Payment, установив атрибуты
    в соответствии с подходящими ключами передаваемого словаря.
    """
    payment = Payment()
    payment.id_pay = pay.get("id")
    payment.state_pay = pay.get("state")
    payment.date_pay = pay.get("date")
    payment.operation_amount_pay = pay.get("operationAmount")
    payment.description_pay = pay.get("description")
    payment.from_pay = pay.get("from")
    payment.to_pay = pay.get("to")

    return payment


def show_payment(pay: Payment) -> None:
    """
    Выводит информацию о платеже на экран в требуемом виде
    """
    date = pay.date_pay
    date_format = date.strftime("%d.%m.%Y")
    red_date, white_date = date_format.rsplit('.', 1)
    description = pay.description_pay
    pay_from = pay.from_pay
    pay_to = pay.to_pay
    operation_amount = pay.operation_amount_pay

    print(f"\033[31m{red_date}\033[0m.{white_date} {description}")
    if pay_from:
        print(f"{pay_from[0]} \033[34m{hide(pay_from[1])} "
              f"\033[0m-\033[33m>\033[0m", end=" ")
    print(f"{pay_to[0]} \033[34m{hide(pay_to[1])}")
    print(f"\033[31m{operation_amount[0]}\033[0m {operation_amount[1]}")
    print()


def hide(number: str) -> str:
    """
    Скрывает определённую часть номера карты или счёта символом "*"
    """
    card_digits = 16
    bank_account_digits = 20
    if type(number) is str:
        if len(number) == card_digits:
            hide_start = 6
            hide_end = 12
            hidden_simbols = hide_end - hide_start
            number_hide = number[:hide_start] + "*" * hidden_simbols + number[hide_end:]
            number_sep = [number_hide[i:i+4] for i in range(0, len(number), 4)]

            return " ".join(number_sep)

        elif len(number) == bank_account_digits:
            return number.replace(number[:-4], "**")