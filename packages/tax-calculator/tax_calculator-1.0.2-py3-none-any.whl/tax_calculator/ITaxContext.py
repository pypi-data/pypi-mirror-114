import abc
from typing import Dict

import stringcase
from datetime import datetime

from arrow import arrow, Arrow

from tax_calculator.IMoney import IMoney


class ITaxContext(abc.ABC):

    @abc.abstractmethod
    def time_to_consider(self) -> Arrow:
        pass

    def get_help_of(self, name: str) -> str:
        return getattr(self, f"help_{stringcase.snakecase(name)}")()

    def get_tax_variables(self) -> Dict[str, any]:
        return self.__dict__

    def check(self):
        for key in self.__dict__:
            if self.__dict__[key] is None:
                raise ValueError(f"required value \"{key}\" is set to None!")
            value = self.__dict__[key]
            if key.endswith("percentage"):
                if not isinstance(value, float):
                    raise TypeError(f"required float, got {type(value)}")
                if not (0 <= value <= 1):
                    raise ValueError(f"required percentage, got {value}")
            elif key.endswith("money"):
                if issubclass(type(value), IMoney):
                    continue
                if type(value) in [float, int]:
                    continue
                raise TypeError(f"required number, got {type(value)}")
            else:
                # no additional check is required
                pass


class StandardTaxContext(ITaxContext):

    def __init__(self):
        self._time_to_consider = Arrow.utcnow()

    def time_to_consider(self) -> Arrow:
        return self._time_to_consider

    def help_time_to_consider(self) -> str:
        return """
        The timestamp when the tax calculation shoud be focus.
        E.g., we would like to want to compute at the 31st of May 2021, regardless 
        of the fact that now it is that time. 
        """
