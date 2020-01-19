#!/usr/bin/env python3
import currency


class Currency(object):
    def get_symbol(self, statement):
        """Convert a currency abbreviation to a symbol (e.g. 'GBP' to '£')

        :param dict statement: Statement data
        :return: str symbol: The currency symbol
        """
        symbol = currency.symbol(statement['account']['currency'])
        return symbol
