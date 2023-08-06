import abc
import math
from typing import Union


class IMoney(abc.ABC):

    def __init__(self, value: float = 0.0):
        self._value = value

    @classmethod
    def parse(cls, val: Union[str, float]) -> "IMoney":
        """

        :param val: something like "5.3€".
        :return:
        """
        if isinstance(val, float):
            return Euro(val)

        val = val.strip()
        try:
            # pure numeric strings re interpreted as euros
            return Euro(float(val))
        except ValueError:
            for money in MONEYS:
                if val[-1] == money.symbol():
                    return money(float(val[:-1]))
            else:
                raise ValueError(f"Cannot decide which money this represents")


    @classmethod
    @abc.abstractmethod
    def symbol(cls) -> str:
        pass

    @property
    def value(self) -> float:
        return self._value

    @abc.abstractmethod
    def one_euro_equals_to(self) -> float:
        pass

    def _to_eur(self) -> float:
        return (1.0 * self.value) / self.one_euro_equals_to()

    def _from_eur(self, value: float) -> float:
        return 1.0 * value * self.one_euro_equals_to()

    def to(self, money_class: type) -> "IMoney":
        money_instance = money_class()
        return money_class(value=money_instance._from_eur(self._to_eur()))

    def __float__(self):
        return float(self._value)

    def __int__(self):
        return int(self._value)

    def __iadd__(self, other):
        if isinstance(other, IMoney):
            self._value += other.to(type(self))._value
        else:
            self._value += float(other)
        return self

    def __add__(self, other):
        result = type(self)(self._value)
        result += other
        return result

    def __isub__(self, other):
        if isinstance(other, IMoney):
            self._value -= other.to(type(self))._value
        else:
            self._value -= float(other)
        return self

    def __sub__(self, other):
        result = type(self)(self._value)
        result -= other
        return result

    def __imul__(self, other):
        if isinstance(other, IMoney):
            self._value *= other.to(type(self))._value
        else:
            self._value *= float(other)
        return self

    def __mul__(self, other):
        result = type(self)(self._value)
        result *= other
        return result

    def __itruediv__(self, other):
        if isinstance(other, IMoney):
            self._value /= other.to(type(self))._value
        else:
            self._value /= float(other)
        return self

    def __truediv__(self, other):
        result = type(self)(self._value)
        result /= other
        return result

    def __lt__(self, other) -> bool:
        if isinstance(other, IMoney):
            return self._value < other.to(type(self))._value
        else:
            return self._value < float(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, IMoney):
            return self._value > other.to(type(self))._value
        else:
            return self._value > float(other)

    def __le__(self, other) -> bool:
        if isinstance(other, IMoney):
            return self._value <= other.to(type(self))._value
        else:
            return self._value <= float(other)

    def __ge__(self, other) -> bool:
        if isinstance(other, IMoney):
            return self._value >= other.to(type(self))._value
        else:
            return self._value >= float(other)

    def __eq__(self, other) -> bool:
        if isinstance(other, IMoney):
            return math.isclose(self._value, other.to(type(self))._value, rel_tol=1e-3)
        else:
            return math.isclose(self._value, float(other), rel_tol=1e-3)

    def __ne__(self, other) -> bool:
        if isinstance(other, IMoney):
            return not math.isclose(self._value, other.to(type(self))._value, rel_tol=1e-3)
        else:
            return not math.isclose(self._value, float(other), rel_tol=1e-3)

    def __str__(self):
        return f"{self._value:.2f}{type(self).symbol()}"

    def __repr__(self):
        return f"{self._value:.5f}{type(self).symbol()}"

    def __format__(self, format_spec):
        return format(self._value, format_spec)


class Euro(IMoney):

    @classmethod
    def symbol(cls) -> str:
        return "€"

    def one_euro_equals_to(self) -> float:
        return 1.0

    def _to_eur(self) -> float:
        return self.value

    def _from_eur(self, value: float) -> float:
        return value


class Dollar(IMoney):

    @classmethod
    def symbol(cls) -> str:
        return "$"

    def one_euro_equals_to(self) -> float:
        return 1.18


MONEYS = [
    Euro,
    Dollar
]