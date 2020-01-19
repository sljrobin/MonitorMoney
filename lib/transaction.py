#!/usr/bin/env python3
import json
from colorama import Fore, Style
from datetime import datetime
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from lib import preferences


class Transaction(object):
    def create(self):
        """Create a new transaction
        """
        # Creating strings for printing
        str_date = '"{}":['
        str_input = Style.BRIGHT + '> ' + \
            Fore.BLUE + '{} ' + \
            Style.DIM + '({})' + Style.RESET_ALL + \
            Style.BRIGHT + Fore.BLUE + ': ' + Style.RESET_ALL
        str_separator = Style.DIM + '-' * 80 + Style.RESET_ALL
        str_transaction = ' ' * 2 + \
                          '{{"type":"{}", "amount":{}, "category":"{}", "subcategory":"{}", "description":"{}"}}'

        # Getting the categories
        prefs = preferences.Preferences()
        prefs.show_categories()
        print(str_separator)

        # Getting transaction details from user
        now = datetime.now().strftime('%Y-%m-%d')
        transaction = {
            'date': input(str_input.format('Date', now)) or now,
            'type': input(str_input.format('Type', 'debit')).lower() or 'debit',
            'amount': input(str_input.format('Amount', 0.0)) or 0.0,
            'category': input(str_input.format('Category', 'groceries')).lower() or 'groceries',
            'subcategory': input(str_input.format('Subcategory', '')).lower() or '',
            'description': input(str_input.format('Description', 'Sainsbury\'s')) or 'Sainsbury\'s'}

        # Printing transaction: JSON
        print(str_separator)
        json_object = json.loads(str_transaction.format(transaction['type'],
                                                        transaction['amount'],
                                                        transaction['category'],
                                                        transaction['subcategory'],
                                                        transaction['description']))
        json_str = json.dumps(json_object, sort_keys=False)
        print(highlight(json_str, JsonLexer(), TerminalFormatter()), end='')
        # Printing transaction: RAW
        print(str_separator)
        raw = str_date.format(transaction['date']) + '\n' + \
            str_transaction.format(transaction['type'],
                                   transaction['amount'],
                                   transaction['category'],
                                   transaction['subcategory'],
                                   transaction['description']) + '\n' + \
            ']'
        print(raw)
