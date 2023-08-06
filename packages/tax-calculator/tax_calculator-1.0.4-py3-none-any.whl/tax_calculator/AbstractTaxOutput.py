import abc
from datetime import datetime
from typing import Dict

from arrow import arrow

from tax_calculator.IMoney import IMoney, Euro


class AbstractTaxOutput(abc.ABC):

    def __init__(self, created_at: arrow, tax_to_pay: IMoney, ricavi: IMoney, **kwargs):
        self.created_at = created_at
        self.tax_to_pay = tax_to_pay
        self.ricavi = ricavi
        for k, v in kwargs.items():
            if k.startswith("_"):
                continue
            if k in "self":
                continue
            self.__dict__[k] = v

    @property
    def ricavi_netti(self) -> IMoney:
        return self.ricavi - self.tax_to_pay

    @property
    def tax_over_ricavi_ratio(self) -> float:
        """

        :return: ration [0,1] between tax to pay and total ricavi.
        """
        return (self.tax_to_pay.to(Euro) * 1.0) / self.ricavi.to(Euro)

    def get_tax_variables(self) -> Dict[str, any]:
        return self.__dict__

