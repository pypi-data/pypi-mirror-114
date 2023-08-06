#! /usr/bin/env python

import json
import sys

import argparse

from tax_calculator import version
from tax_calculator.IMoney import Euro, IMoney
from tax_calculator.ITaxCalculator import ITaxCalculator
from tax_calculator.ITaxContext import ITaxContext
from tax_calculator.calculators.CodiceAteco import CodiceAteco
from tax_calculator.calculators.RegimeForfettarioTaxCalculator import RegimeForfettarioTaxCalculator
from tax_calculator.calculators.RegimeForfettarioTaxContext import RegimeForfettarioTaxContext

import logging

from tax_calculator.encoders.encoders import MultiplexerEncoder

LOG = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(prog="TaxCalculator", description="""
    Allows you to compute taxes (italy)
    """, epilog=f"Version {version.VERSION}")

    parser.add_argument("--country", type=str, default="IT",
                        help="""country where to compute taxes. Defaults to italy""")

    subparsers = parser.add_subparsers()
    forfettario = subparsers.add_parser('compute-forfettario')

    forfettario.add_argument("--ricavi", type=str, required=True, help="""
        How much money do you have actually enjoyed?
        se una fattura non è stata ancora riscossa, non inserirla!
    """)
    forfettario.add_argument("--contributi_previdenziali_anno_scorso", type=str, default=0.0, help="""Number of euro you have paid the last year for INPS""")
    forfettario.add_argument("--ateco", type=str, default="62.02.00", help="""Your codice ateco""")
    forfettario.add_argument("--aliquota_imposta_sostitutiva", type=float, default=0.05, help="""Percentage of imposta sostitutiva (e.g. 0.05). By default is the forfettario agevolato""")
    forfettario.add_argument("--contributi_previdenziali", type=float, default=0.2572,
                             help="""Percentage of tax you nee dto pay to the contributi previdenziali (e.g. 0.25). By default
                             they are the ones from the INPS""")
    forfettario.set_defaults(func=forfettario_handler)

    return parser.parse_args(args)


def forfettario_handler(args):
    tax_calculator = RegimeForfettarioTaxCalculator()
    tax_context = RegimeForfettarioTaxContext()

    tax_context.ricavi_money = IMoney.parse(args.ricavi)
    tax_context.contributi_previdenziali_anno_scorso_money = IMoney.parse(args.contributi_previdenziali_anno_scorso)
    tax_context.contributi_previdenziali_percentage = args.contributi_previdenziali  # gestione separata INPS: 0.2572
    tax_context.aliquota_imposta_sostitutiva_percentage = args.aliquota_imposta_sostitutiva  # aliquota iva agevolata: 0.05
    tax_context.codice_ateco = CodiceAteco.parse(args.ateco)  # 62.02.00

    tax_output = tax_calculator.calculate(tax_context)
    summary = tax_calculator.get_summary(tax_context, tax_output)
    print(json.dumps(summary, indent=4, ensure_ascii=False, sort_keys=True, cls=MultiplexerEncoder))

    # useful for testing
    return summary


# console entry point
def main():
    _main(sys.argv[1:])


def _main(args):
    logging.basicConfig(level="INFO", format="%(asctime)s %(funcName)s@%(lineno)d - %(levelname)s - %(message)s")

    options = parse_args(args)
    result = options.func(options)
    # useful for testing
    return result


if __name__ == "__main__":
    _main(sys.argv[1:])

