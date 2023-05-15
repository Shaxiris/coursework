from datetime import datetime


class Payment:
    """Информация о платеже"""

    AMOUNT_DIGITS = [16, 20]    # корректное количество цифр в номере банковской карты и счёта

    def __init__(self) -> None:
        self.__id_pay = None
        self.__state_pay = None
        self.__date_pay = None
        self.__operation_amount_pay = None
        self.__description_pay = None
        self.__from_pay = None
        self.__to_pay = None

    def __str__(self) -> str:
        return f"Payment {self.__id_pay}, more detailed information is closed."

    def __repr__(self) -> str:
        return f"Payment(" \
            f"id_pay={self.__id_pay}," \
            f"state_pay=\"{self.__state_pay}\"," \
            f"date_pay=\"{self.__date_pay}\"," \
            f"operation_amount_pay={self.__operation_amount_pay}," \
            f"description_pay=\"{self.__description_pay}\"," \
            f"from_pay=\"{self.__from_pay}\"," \
            f"to_pay=\"{self.__to_pay}\")"

    @property
    def id_pay(self) -> int:
        return self.__id_pay

    @id_pay.setter
    def id_pay(self, id_pay: int) -> None:
        """
        Устанавливает id платежа.

        Проверка: является ли целым числом
        """
        if type(id_pay) is int:
            self.__id_pay = id_pay

    @property
    def state_pay(self) -> str:
        return self.__state_pay

    @state_pay.setter
    def state_pay(self, state_pay: str) -> None:
        """
        Устанавливает состояние платежа.

        Проверка: соответствует ли состояние платежа
        одному из двух возможных вариантов
        """
        if type(state_pay) is str:
            if state_pay.lower() in ("executed", "canceled"):
                self.__state_pay = state_pay.upper()

    @property
    def date_pay(self) -> datetime:
        return self.__date_pay

    @date_pay.setter
    def date_pay(self, date: str) -> None:
        """
        Устанавливает дату платежа в формате datatime.

        Проверка: является ли дата корректной
        """
        if type(date) is str:
            for_date = " ".join(date.split("T"))

            try:
                self.__date_pay = datetime.fromisoformat(for_date)
            except ValueError:
                self.__date_pay = None

    @property
    def operation_amount_pay(self) -> tuple:
        return self.__operation_amount_pay

    @operation_amount_pay.setter
    def operation_amount_pay(self, operation_amount: dict) -> None:
        """
        Устанавливает сумму и валюту платежа в формате кортежа.

        Проверки:
        существуют ли значения суммы и валюты платежа;
        является ли формат валюты платежа строкой;
        корректна ли сумма платежа
        """
        if type(operation_amount) is dict:
            amount = operation_amount.get('amount')
            currency = operation_amount.get('currency')
            currency_name = currency.get('name') if currency else None

            if amount and currency_name:
                if self.__check_amount(amount) and type(currency_name) is str:
                    amount_format_float = f"{float(amount):.2f}"
                    self.__operation_amount_pay = (amount_format_float, currency_name)

    @staticmethod
    def __check_amount(amount: str) -> bool:
        """
        Проверяет корректность суммы платежа через попытку
        приведения формата к типу float
        """
        if type(amount) is bool:
            return False
        try:
            float(amount)
        except ValueError:
            return False

        return True

    @property
    def description_pay(self) -> str:
        return self.__description_pay

    @description_pay.setter
    def description_pay(self, description_pay: str) -> None:
        """
        Устанавливает назначение/описание платежа.

        Проверка: является ли описание платежа строкой
        """
        if type(description_pay) is str:
            self.__description_pay = description_pay

    @property
    def from_pay(self) -> tuple:
        return self.__from_pay

    @from_pay.setter
    def from_pay(self, from_pay: str) -> None:
        """
        Устанавливает либо тип банковской карты и её номер,
        либо банковский счёт и его номер в формате кортежа,
        поле отправителя.

        Проверки:
        является ли эта информация строкой;
        корректен ли номер карты/счёта
        """
        if type(from_pay) is str:
            card_sep = from_pay.rsplit(" ", 1)
            if len(card_sep) == 2:
                card, number = card_sep
                if self.__check_card(card, number):
                    self.__from_pay = (card, number)

    def __check_card(self, card: str, number: str) -> bool:
        """
        Проверяет, состоит ли номер карты/счёта только из цифр и
        соответствует ли количество цифр в номере обязательному для карты/счёта
        """
        if not number.isdigit():
            return False
        elif len(number) not in self.AMOUNT_DIGITS:
            return False
        elif card.lower() == "счет" and len(number) != self.AMOUNT_DIGITS[-1]:
            return False

        return True

    @property
    def to_pay(self) -> tuple:
        return self.__to_pay

    @to_pay.setter
    def to_pay(self, to_pay: str) -> None:
        """
        Устанавливает либо тип банковской карты и её номер,
        либо банковский счёт и его номер в формате кортежа,
        поле получателя.

        Проверки:
        является ли эта информация строкой;
        корректен ли номер карты/счёта
        """
        if type(to_pay) is str:
            card_sep = to_pay.rsplit(" ", 1)
            if len(card_sep) == 2:
                card, number = card_sep
                if self.__check_card(card, number):
                    self.__to_pay = (card, number)