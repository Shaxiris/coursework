import scr.utils as u
import pytest
from datetime import datetime
from class_payment.payment import Payment


@pytest.fixture
def parameters():
    return {"id", "date", "state", "operationAmount", "description", "to"}


@pytest.fixture
def correct_dict():
    return {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }


@pytest.fixture
def data_list():
    return [
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {
                "amount": "79931.03",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215"
        },
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {
                "amount": "40701.91",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472"
        },
        {
            "id": 863064926,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "operationAmount": {
                "amount": "41096.24",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }
    ]


def test_get_path_to_file_correct():
    assert u.get_path_to_file("operations.json", "sources") == "/home/ksu/PycharmProjects/3_course_Coursework/sources" \
                                                               "/operations.json"


def test_get_path_to_file_incorrect():
    with pytest.raises(TypeError):
        u.get_path_to_file(2, 4)

    with pytest.raises(TypeError):
        u.get_path_to_file(True, None)


def test_get_payments_correct(parameters):
    path = "/home/ksu/PycharmProjects/3_course_Coursework/sources/operations.json"
    payments = u.get_payments(path, parameters)
    assert next(payments) == {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }


def test_get_payments_incorrect(parameters):
    path = "/home/ksu/PycharmProjects/3_course_Coursework/operations.json"
    with pytest.raises(FileNotFoundError):
        u.get_payments(path, parameters)

    path = "ksu/sources/operations.json"
    with pytest.raises(FileNotFoundError):
        u.get_payments(path, parameters)


def test_check_payment_correct(correct_dict, parameters):
    assert u.check_payment(correct_dict, parameters) is True


def test_check_payment_incorrect(parameters):
    incorrect_dict = {
        "id": 863064926,
        "state": "",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    assert u.check_payment(incorrect_dict, parameters) is False

    incorrect_dict = {
        "id": 863064926,
        "state": "CANCELED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    assert u.check_payment(incorrect_dict, parameters) is False

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "to": "Счет 90424923579946435907"
    }
    assert u.check_payment(incorrect_dict, parameters) is False

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-32T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    assert u.check_payment(incorrect_dict, parameters) is False

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": None,
        "to": "Счет 90424923579946435907"
    }
    assert u.check_payment(incorrect_dict, parameters) is False


def test_check_date_correct():
    assert u.check_date("2018-10-14T08:21:33.419441") is True


def test_check_date_incorrect():
    assert u.check_date("2018-10-1408:21:33.419441") is False

    assert u.check_date("2018-10-14T28:21:33.419441") is False

    assert u.check_date("2018-10-14") is False

    assert u.check_date("2018-09-31T08:21:33.419441") is False

    assert u.check_date("2013-02-29T08:21:33.419441") is False

    assert u.check_date(2013) is False


def test_reformat_date_correct(correct_dict):
    assert u.reformat_date(correct_dict) == datetime(2019, 12, 8, 22, 46, 21, 935582)


def test_reformat_date_incorrect():
    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-32T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    with pytest.raises(ValueError):
        u.reformat_date(incorrect_dict)

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-3122:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    with pytest.raises(ValueError):
        u.reformat_date(incorrect_dict)

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-32T",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    with pytest.raises(ValueError):
        u.reformat_date(incorrect_dict)

    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": (2019, 12, 32),
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    with pytest.raises(AttributeError):
        u.reformat_date(incorrect_dict)


def test_create_payment_correct(correct_dict):
    pay = u.create_payment(correct_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_empty():
    with pytest.raises(TypeError):
        u.create_payment()


def test_create_payment_none():
    with pytest.raises(AttributeError):
        u.create_payment(None)


def test_create_payment_lack_id():
    incorrect_dict = {
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay is None
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_lack_state():
    incorrect_dict = {
        "id": 863064926,
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay is None
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_lack_date():
    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay is None
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_lack_amount():
    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "description": "Открытие вклада",
        "to": "Счет 90424923579946435907"
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay is None
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_lack_description():
    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "to": "Счет 90424923579946435907"
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay is None
    assert pay.to_pay == ("Счет", "90424923579946435907")


def test_create_payment_lack_to():
    incorrect_dict = {
        "id": 863064926,
        "state": "EXECUTED",
        "date": "2019-12-08T22:46:21.935582",
        "operationAmount": {
            "amount": "41096.24",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Открытие вклада",
    }
    pay = u.create_payment(incorrect_dict)
    assert type(pay) == Payment
    assert pay.id_pay == 863064926
    assert pay.state_pay == "EXECUTED"
    assert pay.date_pay == datetime(2019, 12, 8, 22, 46, 21, 935582)
    assert pay.operation_amount_pay == ("41096.24", "USD")
    assert pay.description_pay == "Открытие вклада"
    assert pay.to_pay is None


def test_show_payment_correct(correct_dict):
    pay = u.create_payment(correct_dict)
    assert u.show_payment(pay) == print(f"""
\033[31m{"08.12"}\033[0m.{"2019"} {"Открытие вклада"}
{"Счет"} \033[34m{"**5907"}
\033[31m{"41096.24"}\033[0m {"USD"}"

""")


def test_show_payment_correct_with_from():
    correct_dict = {
        "id": 716496732,
        "state": "EXECUTED",
        "date": "2018-04-04T17:33:34.701093",
        "operationAmount": {
            "amount": "40701.91",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Visa Gold 5999414228426353",
        "to": "Счет 72731966109147704472"
    }
    pay = u.create_payment(correct_dict)
    assert u.show_payment(pay) == print(f"""
\033[31m{"04.04"}\033[0m.{"2018"} {"Перевод организации"}
{"Visa Gold"} \033[34m{"5999 **** **42 6353"} \033[0m-\033[33m>\033[0m" {"Счет"} \033[34m{"**4472"}
\033[31m{"40701.91"}\033[0m {"USD"}"

""")


def test_show_payment_incorrect():
    incorrect_dict = {
        "id": 716496732,
        "state": "EXECUTED",
        "date": "2018-04-04T17:33:34.701093",
        "currency": {
            "name": "USD",
            "code": "USD"
        },
        "description": "Перевод организации",
        "from": "Visa Gold 5999414228426353",
        "to": "Счет 72731966109147704472"
    }
    pay = u.create_payment(incorrect_dict)
    with pytest.raises(TypeError):
        assert u.show_payment(pay)

    incorrect_dict = {
        "id": 716496732,
        "state": "EXECUTED",
        "date": "",
        "currency": {
            "name": "USD",
            "code": "USD"
        },
        "description": "Перевод организации",
        "from": "Visa Gold 5999414228426353",
        "to": "Счет 72731966109147704472"
    }
    pay = u.create_payment(incorrect_dict)
    with pytest.raises(AttributeError):
        assert u.show_payment(pay)


def test_hide_correct():
    assert u.hide("72731966109147704472") == "**4472"

    assert u.hide("5999414228426353") == "5999 41** **** 6353"


def test_hide_incorrect():
    assert u.hide(72731966109147704470) is None

    assert u.hide("7277044720") is None

    assert u.hide("727319661091477044720") is None

    assert u.hide("599941422842353") is None