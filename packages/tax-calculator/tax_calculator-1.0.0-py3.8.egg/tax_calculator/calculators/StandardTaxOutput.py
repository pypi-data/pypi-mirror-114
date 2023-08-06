from datetime import datetime

from arrow import arrow

from tax_calculator.AbstractTaxOutput import AbstractTaxOutput
from tax_calculator.IMoney import IMoney


class StandardTaxOutput(AbstractTaxOutput):

    def __init__(self, created_at: arrow, tax_to_pay: IMoney, ricavi: IMoney, **kwargs):
        super().__init__(created_at, tax_to_pay, ricavi, **kwargs)