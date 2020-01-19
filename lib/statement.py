#!/usr/bin/env python3
import json
from colorama import Fore, Style
from datetime import date, datetime
from lib import currency
from lib import preferences


class Statement(object):
    def __init__(self, statement, start=date.min, end=date.max):
        """Initialize a statement object
        * Set the minimum and maximum dates
        * Load JSON data and convert it to a Python dictionary
        * Get the currency symbol

        :param str statement: Path of the statement
        :param date start: Starting date for when counting transactions
        :param date end: Ending date until when counting transactions
        """
        # Setting the dates
        self.date_start = start
        self.date_end = end

        # Loading JSON data
        with open(statement, 'r') as statement_file:
            data_json = json.load(statement_file)
        # Creating a dictionary of all transactions with 'datetime.date' keys instead of strings
        transactions = {}
        for key in data_json['transactions']:
            key_casted = datetime.strptime(key, '%Y-%m-%d')
            transactions[date(key_casted.year, key_casted.month, key_casted.day)] = data_json['transactions'][key]
        # Creating final dictionary with all statement information
        self.statement_data = {
            'account': data_json['account'],
            'transactions': transactions
        }

        # Getting currency symbol
        cur = currency.Currency()
        self.symbol = cur.get_symbol(self.statement_data)

    def get_data(self):
        """Get statement data

        :return: dict statement_data: statement data
        """
        return self.statement_data

    def load(self, statement):
        """Load a statement

        :param str statement: Path of the statement
        :return: dict statement_data: All statement data
        """
        # Loading JSON data
        with open(statement, 'r') as statement_file:
            data_json = json.load(statement_file)

        # Creating a dictionary of all transactions with 'datetime.date' keys instead of strings
        transactions = {}
        for key in data_json['transactions']:
            key_casted = datetime.strptime(key, '%Y-%m-%d')
            transactions[date(key_casted.year, key_casted.month, key_casted.day)] = data_json['transactions'][key]

        # Creating final dictionary with all statement information
        statement_data = {
            'account': data_json['account'],
            'transactions': transactions
        }
        return statement_data

    def show_account(self):
        """Show account details of a statement
        """
        # Creating strings for printing
        str_arrow = Style.DIM + '  {}  ' + Style.RESET_ALL
        str_header = Style.BRIGHT + '{}: ' + Style.RESET_ALL
        str_subheader = '{}: '
        str_name_bank = str_arrow + str_subheader + Fore.BLUE + '{}' + Style.RESET_ALL + \
            Style.DIM + ' / ' + Style.RESET_ALL + \
            str_subheader + Fore.BLUE + '{}' + Style.RESET_ALL + \
            ' (' + Fore.BLUE + '{}' + Style.RESET_ALL + ')' + Style.RESET_ALL
        str_currency = str_arrow + str_subheader + \
            Fore.BLUE + '{}' + Style.RESET_ALL + ' (' + Fore.BLUE + '{}' + Style.RESET_ALL + ')' + Style.RESET_ALL

        # Printing account details
        print()
        print('-' * 80)
        print(str_header.format('Account'))
        print(str_name_bank.format('\u2b91',
                                   'Name', self.statement_data['account']['name'],
                                   'Bank', self.statement_data['account']['bank'],
                                   self.statement_data['account']['country']))
        print(str_currency.format('\u2b91', 'Currency', self.statement_data['account']['currency'], self.symbol))
        print(Style.DIM + '-' * 80 + Style.RESET_ALL)

    def show_transactions(self):
        """Show transactions of a statement
        """
        # Creating a directory with all transactions
        all_transactions = self.statement_data['transactions']

        # Creating a directory to sort all transactions by categories
        prefs = preferences.Preferences()
        categories = prefs.get_categories()
        categorised = {}
        for category in categories:
            categorised[category] = []

        # Adding transactions to 'categorised'
        for transaction_date, transactions in all_transactions.items():
            if self.date_start <= transaction_date <= self.date_end:
                for transaction in transactions:
                    if transaction['category'] in categorised.keys():
                        transaction_categorised = {
                            'type': transaction['type'],
                            'date': transaction_date.strftime('%Y/%m/%d'),
                            'amount': transaction['amount'],
                            'subcategory': transaction['subcategory'],
                            'description': transaction['description']
                        }
                        categorised[transaction['category']].append(transaction_categorised)

        # Creating strings for printing
        str_category = Style.BRIGHT + '{}' + Style.RESET_ALL
        str_pipe = Style.DIM + ' | ' + Style.RESET_ALL
        str_transaction_credit = Style.DIM + '  {}  ' + Style.RESET_ALL + \
             Fore.GREEN + '{} ' + Style.RESET_ALL + \
             Fore.BLUE + '{}' + Style.RESET_ALL + str_pipe + \
             Fore.WHITE + '{}' + Style.RESET_ALL + str_pipe + \
             Fore.GREEN + '{:,.2f}{}' + Style.RESET_ALL + str_pipe + \
             '{}' + Style.RESET_ALL
        str_transaction_credit_nosub = Style.DIM + '  {}  ' + Style.RESET_ALL + \
             Fore.GREEN + '{} ' + Style.RESET_ALL + \
             Fore.BLUE + '{}' + Style.RESET_ALL + str_pipe + \
             Fore.GREEN + '{:,.2f}{}' + Style.RESET_ALL + str_pipe + \
             '{}' + Style.RESET_ALL
        str_transaction_debit = Style.DIM + '  {}  ' + Style.RESET_ALL + \
              Fore.RED + '{} ' + Style.RESET_ALL + \
              Fore.BLUE + '{}' + Style.RESET_ALL + str_pipe + \
              Fore.WHITE + '{}' + Style.RESET_ALL + str_pipe + \
              Fore.RED + '{:,.2f}{}' + Style.RESET_ALL + str_pipe + \
              '{}' + Style.RESET_ALL
        str_transaction_debit_nosub = Style.DIM + '  {}  ' + Style.RESET_ALL + \
              Fore.RED + '{} ' + Style.RESET_ALL + \
              Fore.BLUE + '{}' + Style.RESET_ALL + str_pipe + \
              Fore.RED + '{:,.2f}{}' + Style.RESET_ALL + str_pipe + \
              '{}' + Style.RESET_ALL
        # Printing transactions
        for category, transactions in categorised.items():
            # Removing categories with no transactions
            if transactions:
                print(str_category.format(category.title()))
                for transaction in transactions:
                    # Credits
                    if transaction['type'] == 'credit':
                        # Without subcategory
                        if not transaction['subcategory']:
                            print(str_transaction_credit_nosub.format('\u2b91', '+', transaction['date'],
                                                                      transaction['amount'], self.symbol,
                                                                      transaction['description']))
                        # With subcategory
                        else:
                            print(str_transaction_credit.format('\u2b91', '+', transaction['date'],
                                                                      transaction['subcategory'].title(),
                                                                      transaction['amount'], self.symbol,
                                                                      transaction['description']))
                    # Debits
                    elif transaction['type'] == 'debit':
                        # Without subcategory
                        if not transaction['subcategory']:
                            print(str_transaction_debit_nosub.format('\u2b91', '-', transaction['date'],
                                                                     transaction['amount'], self.symbol,
                                                                     transaction['description']))
                        # With subcategory
                        else:
                            print(str_transaction_debit.format('\u2b91', '-', transaction['date'],
                                                               transaction['subcategory'].title(),
                                                               transaction['amount'], self.symbol,
                                                               transaction['description']))
