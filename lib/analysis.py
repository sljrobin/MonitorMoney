#!/usr/bin/env python3
from colorama import Fore, Style
from datetime import date
from lib import currency
from lib import preferences
from lib import statement


class Analysis(object):
    def __init__(self, stat, start=date.min, end=date.max):
        """Initialize an analysis object
        * Set the minimum and maximum dates
        * Get statement data

        :param str stat: Path of the statement
        :param date start: Starting date for when counting transactions
        :param date end: Ending date until when counting transactions
        """
        # Setting the dates
        self.date_start = start
        self.date_end = end

        # Getting statement data
        stat = statement.Statement(stat, start, end)
        self.statement_data = stat.get_data()

        # Getting currency symbol
        cur = currency.Currency()
        self.symbol = cur.get_symbol(self.statement_data)

    def __get_totals(self):
        """Calculate credits, debits, with and without taxes, and savings of a statement

        :return: dict totals: credits, debits and savings
        """
        # Creating a directory to sort all transactions by categories
        prefs = preferences.Preferences()
        categories = prefs.get_categories()
        categorised = {}
        for category in categories:
            categorised[category] = {'credits': 0, 'debits': 0}

        # Creating dictionaries to summarize all credits, debits, with and without taxes, and calculate savings
        gross = {'credits': 0, 'debits': 0}
        net = {'credits': 0, 'debits': 0, 'savings': 0}

        # Creating a dictionary with all transactions
        all_transactions = self.statement_data['transactions']

        # Creating a variable for taxes only
        taxes = 0

        # Adding transactions to 'categorised' and 'summary' and isolating Taxes amount
        for transaction_date, transactions in all_transactions.items():
            if self.date_start <= transaction_date <= self.date_end:
                for transaction in transactions:
                    if transaction['category'] in categorised.keys():
                        if transaction['type'] == 'credit':
                            gross['credits'] += transaction['amount']
                            categorised[transaction['category']]['credits'] += transaction['amount']
                        elif transaction['type'] == 'debit':
                            gross['debits'] += transaction['amount']
                            categorised[transaction['category']]['debits'] += transaction['amount']
                            # Isolating Taxes
                            if transaction['subcategory'] == 'taxes':
                                taxes += transaction['amount']

        # Calculating totals without taxes
        net['credits'] = gross['credits'] - taxes
        net['debits'] = gross['debits'] - taxes
        net['savings'] = net['credits'] - net['debits']

        # Creating a dictionary containing totals
        totals = {
            'gross': gross,
            'net': net,
            'categories': categorised
        }
        return totals

    def show_totals(self):
        """Show credits, debits and savings of a statement
        Show a summary and the totals without taxes sorted by categories
        """
        # Getting totals
        totals = self.__get_totals()
        # Getting percentage of savings
        percentage = totals['net']['savings'] / totals['net']['credits']

        # Creating strings for printing
        str_arrow = Style.DIM + '  {}  ' + Style.RESET_ALL
        str_header = Style.BRIGHT + '> {}: ' + Style.RESET_ALL
        str_subheader = '{}: '
        str_separator = Style.DIM + ' ' * 2 + '-' * 44 + Style.RESET_ALL
        str_transactions = str_arrow + str_subheader + \
            Fore.GREEN + '{:,.2f}{}' + Style.RESET_ALL + \
            Style.DIM + ' / ' + Style.RESET_ALL + \
            Fore.RED + '{:,.2f}{}' + Style.RESET_ALL
        str_savings = str_arrow + str_subheader + \
                      Fore.YELLOW + '{:+,.2f}{}' + Style.RESET_ALL
        str_category = str_arrow + \
            Fore.BLUE + '{}' + \
            Fore.GREEN + '{: >10,.2f}{}' + \
            Fore.RED + '\t{: >10,.2f}{}' + Style.RESET_ALL
        str_totals = '{}' + \
            Fore.GREEN + '{: >10,.2f}{}' + \
            Fore.RED + '\t{: >10,.2f}{}' + Style.RESET_ALL
        str_percentage = '(' + Fore.YELLOW + '{:.2%}' + Style.RESET_ALL + ')'

        # Printing totals: Credits, Debits, including with Taxes, and Savings
        print(str_header.format('Summary'))
        print(str_transactions.format('\u2b91', 'Gross',
                                      totals['gross']['credits'], self.symbol,
                                      totals['gross']['debits'], self.symbol))
        print(str_transactions.format('\u2b91', 'Net',
                                      totals['net']['credits'], self.symbol,
                                      totals['net']['debits'], self.symbol))
        print(str_savings.format('\u2b91', 'Savings',
                                 totals['net']['savings'], self.symbol), end=' '),
        print(str_percentage.format(percentage))

        # Printing totals: Categories
        print()
        print(str_header.format('Analysis'))
        for category in totals['categories']:
            # Printing category only if transactions have been made in this category
            if totals['categories'][category]['credits'] != 0 or totals['categories'][category]['debits'] != 0:
                print(str_category.format('\u2b91',
                                          category.title().ljust(14, ' '),
                                          totals['categories'][category]['credits'], self.symbol,
                                          totals['categories'][category]['debits'], self.symbol))
        # Printing totals: Categories totals but not including Taxes
        print(str_separator)
        print(str_totals.format(''.ljust(19),
                                totals['net']['credits'], self.symbol,
                                totals['net']['debits'], self.symbol))
