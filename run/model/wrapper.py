#!/usr/bin/env python3

import json
import requests

class Markit:

    def __init__(self):
        self.domain_name = 'http://dev.markitondemand.com/Api/v2'
        self.lookup_path = '/Lookup/json?input='
        self.quote_path  = '/Quote/json?symbol='

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    # TODO 3
    def __iter__(self):
        pass

    # TODO 0
    def lookup(self, company_name):
        #print(self.domain_name+self.lookup_path+company_name)
        res = json.loads(
                requests.get(
                    self.domain_name
                    +self.lookup_path
                    +company_name
                ).text
            )
        try:
            if len(res) > 1:
                return [i['Name'] for i in res]
            return res[0]['Symbol']
        except IndexError:
            return False

    # TODO 1
    def quote(self, ticker_symbol):
        #print(self.domain_name+self.quote_path + ticker_symbol)
        res = json.loads(
                requests.get(self.domain_name + self.quote_path + ticker_symbol).text
            )
        try:
            return res['LastPrice']
        except KeyError:
            return False
