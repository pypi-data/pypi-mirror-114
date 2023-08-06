import abc
from typing import Generic
from urllib.parse import urlunparse

import requests

from tax_calculator.AbstractTaxOutput import AbstractTaxOutput
from tax_calculator.ITaxContext import ITaxContext
from tax_calculator.generics import TTAXCONTEXT, TTAXOUTPUT, Json

from bs4 import BeautifulSoup


class ITaxCalculator(Generic[TTAXCONTEXT, TTAXOUTPUT], abc.ABC):

    @abc.abstractmethod
    def calculate(self, context: TTAXCONTEXT) -> TTAXOUTPUT:
        pass

    def get_summary(self, input: TTAXCONTEXT, output: TTAXOUTPUT) -> Json:
        """
        Compute a json-like object representing the output of the tax calculation.
        The default method just put into the json all he variables in both input and output
        :param input: context fed to calculate method
        :param output: output of calculate method
        :return: json
        """
        result = dict()

        result["calculator"] = type(self).__name__
        result["input"] = {}
        for k, v in input.get_tax_variables().items():
            result["input"][k] = v
        result["output"] = {}
        for k, v in input.get_tax_variables().items():
            result["output"][k] = v
        return result

    def parse_html(self, url: str = None, scheme: str = None, hostname: str = None, port: int = None, path: str = None, params: str = None, query: str = None, fragment: str = None) -> "BeautifulSoup":
        """
        parse an html page
        :param url: url of the html page to fetch. we will use get method.
        :param scheme: uri scheme (e.g., http). ignored if url is none
        :param hostname: uri hostname (e.g., www.google.com). ignored if url is none
        :param port: uri port (e.g., 80). ignored if url is none
        :param path: uri path (e.g., /foo/bar.html). ignored if url is none
        :param params: uri params (e.g., http). ignored if url is none
        :param query: uri query (e.g., http). ignored if url is none
        :param fragment: uri fragment (e.g., http). ignored if url is none
        :return: parsed html code
        """
        if url is None:
            url = urlunparse(scheme=scheme, netloc=f"{hostname}:{port}", path=path, params=params, query=query, fragment=fragment)

        value = requests.get(url)
        return BeautifulSoup(value.text)
