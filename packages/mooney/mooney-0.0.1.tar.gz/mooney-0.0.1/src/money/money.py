from src.money.currency import Currency


class Money:
    currency: Currency
    whole: int
    decimal: int
    _amount: int

    def __init__(self, currency: Currency, whole: int, decimal: int):
        self.currency = currency
        self.whole = whole
        self.decimal = decimal
        self._amount = self.whole * (10 ** self.currency.decimal_length) + self.decimal

    def to_string(self):
        amount = f"{self._amount}"
        return f"{amount[:-self.currency.decimal_length]}.{amount[-self.currency.decimal_length:]}"
