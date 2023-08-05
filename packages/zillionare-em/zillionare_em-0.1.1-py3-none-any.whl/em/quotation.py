from typing import Any


class Quotation(object):
    def __init__(self, **kwargs):
        self.name = None
        self.code = None
        self.fivequote = {}

        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        return f"{self.name}<{self.code}>@{self.current_price}"

    def __repr__(self) -> str:
        return f"{super().__repr__()}[{str(self)}]"

    def __getattribute__(self, name: str) -> Any:
        if name in ["topprice", "bottomprice"]:
            return float(object.__getattribute__(self, name))
        else:
            return object.__getattribute__(self, name)

    @property
    def prev_close_price(self):
        return float(self.fivequote.get("yesClosePrice", 0))

    @property
    def open_price(self):
        return float(self.fivequote.get("openPrice", 0))

    @property
    def current_price(self):
        return float(self.fivequote.get("currentPrice", 0))
