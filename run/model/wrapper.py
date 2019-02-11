#!/usr/bin/env python3

import json
import requests


class Markit:

    def __init__(self):
        self.domain_name = 'http://dev.markitondemand.com/Api/v2'
        self.lookup_path = '/Lookup/json?input='
        self.quote_path = '/Quote/json?symbol='
        self.quote2 = 'https://api.iextrading.com/1.0/stock/{}/quote'

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    # TODO 3
    def __iter__(self):
        pass

    # TODO 0
    def lookup(self, company_name):
        # print(self.domain_name+self.lookup_path+company_name)
        res = json.loads(
            requests.get(
                self.domain_name
                + self.lookup_path
                + company_name
            ).text
        )
        try:
            if len(res) > 1:
                return [(i['Symbol'], i['Name']) for i in res]
            return res[0]['Symbol']
        except IndexError:
            return False

    # TODO 1
    def quote(self, ticker_symbol):
        #print(self.domain_name+self.quote_path + ticker_symbol)
        res = json.loads(
            requests.get(self.domain_name +
                         self.quote_path + ticker_symbol).text
        )
        try:
            return res['LastPrice']
        except KeyError:
            return False

    def quote_price2(self, ticker_symbol):
        result = requests.get(self.quote2.format(ticker_symbol))
        try:
            return result.json()['latestPrice']
        except KeyError:
            return False
