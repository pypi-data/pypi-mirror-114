import abc


class IMoney(abc.ABC):

    def __init__(self, value: float = 0.0):
        self._value = value

    @abc.abstractmethod
    def symbol(self) -> str:
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

    def __str__(self):
        return f"{self._value:.2f}{self.symbol()}"


class Euro(IMoney):
    def symbol(self) -> str:
        return "€"

    def one_euro_equals_to(self) -> float:
        return 1.0

    def _to_eur(self) -> float:
        return self.value

    def _from_eur(self, value: float) -> float:
        return value


class Dollar(IMoney):
    def symbol(self) -> str:
        return "$"

    def one_euro_equals_to(self) -> float:
        return 1.18