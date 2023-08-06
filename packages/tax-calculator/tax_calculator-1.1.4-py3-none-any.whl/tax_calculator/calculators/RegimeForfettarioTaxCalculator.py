import html
import re
import urllib

import arrow as arrow
import requests
from soupsieve import select

from tax_calculator.AbstractTaxOutput import AbstractTaxOutput
from tax_calculator.IMoney import IMoney, Euro
from tax_calculator.ITaxCalculator import ITaxCalculator
from tax_calculator.calculators.CodiceAteco import CodiceAteco
from tax_calculator.calculators.RegimeForfettarioTaxContext import RegimeForfettarioTaxContext
from tax_calculator.calculators.StandardTaxOutput import StandardTaxOutput
from tax_calculator.generics import TTAXCONTEXT, TTAXOUTPUT, Json

import logging


LOG = logging.getLogger(__name__)


class RegimeForfettarioTaxCalculator(ITaxCalculator[RegimeForfettarioTaxContext, StandardTaxOutput]):
    """
    :see https://flextax.it/regime-forfettario-tassazione/:
    """

    def get_coefficiente_di_reddittivita(self, ateco: CodiceAteco) -> float:
        """
        get the cofficient di redditività
        :param ateco: ateco code to consider
        :return: percentage of coefficiente redivitia (between 0 and 1)
        """
        page = self._parse_html(url=f"https://www.codiceateco.it/categoria?q={ateco}")
        value = str(page.select(".ateco-result .row .huge")[3].text)
        value = value.strip("\n\t ")
        if value.endswith("%"):
            value = value[:-1]
            value = float(value)
            return value/100.
        raise ValueError(f"Cannot detectcoefficiente di redditività!")

    def get_maximum_allow_threshold(self, ateco: CodiceAteco) -> "IMoney":
        page = self._parse_html(url=f"https://www.codiceateco.it/categoria?q={ateco}")
        value = str(page.select(".ateco-result .row .huge")[1].text)
        value = value.strip("\n\t ")
        if value.endswith("€"):
            value = value[:-1]
            value = float(value)
            return Euro(value)
        raise ValueError(f"Cannot detect maximum allowed threshold!")

    def calculate(self, context: RegimeForfettarioTaxContext) -> AbstractTaxOutput:
        super().calculate(context)

        coefficiente_di_redditivita = self.get_coefficiente_di_reddittivita(context.codice_ateco)
        percentuale_tasse_dovute = 1.0 - coefficiente_di_redditivita
        spese_forfettarie = context.ricavi_money * percentuale_tasse_dovute

        # il coefficiente di reddività viene applicato ai ricavi incassati in un anno
        # se emetti fattuea ma il cliente non ti paga, tale somma non dovrà essere considerata nei ricavi
        ricavi_effettuati = context.ricavi_money

        reddito_imponibile_lordo = ricavi_effettuati * coefficiente_di_redditivita
        reddito_imponibile_netto = reddito_imponibile_lordo - context.contributi_previdenziali_anno_scorso_money

        contributi_gestione_inps = reddito_imponibile_lordo * context.contributi_previdenziali_percentage
        applicazione_aliquota_imposta_sostitutiva = reddito_imponibile_netto * context.aliquota_imposta_sostitutiva_percentage

        return StandardTaxOutput(
            created_at=arrow.utcnow(),
            tax_to_pay=applicazione_aliquota_imposta_sostitutiva + contributi_gestione_inps,
            ricavi=context.ricavi_money,
            **{k:v for k, v in locals().items() if k not in "self"}
        )

    def get_summary(self, input: RegimeForfettarioTaxContext, output: StandardTaxOutput) -> Json:
        result = super().get_summary(input, output)

        result["specific"] = {}
        result["specific"]["ricavi lordi"] = output.ricavi
        result["specific"]["ricavi netti"] = output.ricavi_netti
        result["specific"]["tasse annuali da pagare"] = output.tax_to_pay
        result["specific"]["rapporto tasse su ricavi"] = f"{output.tax_over_ricavi_ratio * 100.0:2f}%"

        return result






