#! /usr/bin/env python

import json
import sys

import argparse

from tax_calculator import version
from tax_calculator.IMoney import Euro
from tax_calculator.ITaxCalculator import ITaxCalculator
from tax_calculator.ITaxContext import ITaxContext
from tax_calculator.calculators.CodiceAteco import CodiceAteco
from tax_calculator.calculators.RegimeForfettarioTaxCalculator import RegimeForfettarioTaxCalculator
from tax_calculator.calculators.RegimeForfettarioTaxContext import RegimeForfettarioTaxContext

import logging


LOG = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(prog="TaxCalculator", description="""
    Allows you to compute taxes (italy)
    """, epilog=f"Version {version.VERSION}")

    parser.add_argument("--country", type=str, default="IT",
                        help="""country where to compute taxes. Defaults to italy""")

    subparsers = parser.add_subparsers()
    forfettario = subparsers.add_parser('compute-forfettario')

    forfettario.add_argument("--ricavi", type=float, required=True, help="""
        How much money do you have actually enjoyed?
        se una fattura non è stata ancora riscossa, non inserirla!
    """)
    forfettario.add_argument("--contributi_previdenziali_anno_scorso", type=float, default=0.0, help="""Number of euro you have paid the last year for INPS""")
    forfettario.add_argument("--ateco", type=str, default="62.02.00", help="""Your codice ateco""")
    forfettario.add_argument("--aliquota_imposta_sostitutiva", type=float, default=0.05, help="""Percentage of imposta sostitutiva (e.g. 0.05)""")
    forfettario.add_argument("--contributi_previdenziali", type=float, default=0.2572,
                             help="""Percentage of tax you nee dto pay to the contributi previdenziali (e.g. 0.25)""")
    forfettario.set_defaults(func=forfettario)

    return parser.parse_args(args)


def forfettario(args):
    tax_calculator = RegimeForfettarioTaxCalculator()
    tax_context = RegimeForfettarioTaxContext()

    tax_context.ricavi_money = Euro(args.ricavi)
    tax_context.contributi_previdenziali_anno_scorso_money = Euro(args.contributi_previdenziali_anno_scorso)
    tax_context.contributi_previdenziali_percentage = args.contributi_previdenziali  # gestione separata INPS: 0.2572
    tax_context.aliquota_imposta_sostitutiva_percentage = args.aliquota_imposta_sostitutiva  # aliquota iva agevolata: 0.05
    tax_context.codice_ateco = CodiceAteco.parse(args.ateco)  # 62.02.00

    tax_output = tax_calculator.calculate(tax_context)
    summary = tax_calculator.get_summary(tax_context, tax_output)
    LOG.info(json.dumps(summary, indent=4, sort_keys=True))


def main(args):
    options = parse_args(args)
    options.func(args)
    print(f"DONE!")


if __name__ == "__main__":
    main(sys.argv[1:])

