#!/usr/bin/env python3
from colorama import Fore, Style
from datetime import datetime
import json
import math
import os
import re

PREFERENCES = './data/preferences/preferences.json'


class Preferences(object):
    def __init__(self):
        """Load preferences file
        """
        # Loading preferences and selecting main path
        with open(PREFERENCES, 'r') as preferences_files:
            self.preferences_data = json.load(preferences_files)

    def generate_makefile_rule(self, year, month):
        """Generate a makefile rule

        :param: date year: year used to create the rule
        :param: date month: month used to create the rule
        """
        # Selecting makefile
        makefile = self.preferences_data['makefile']

        # Creating a temporary datetime object to handle conversion
        tmp_date = datetime(year, month, 1)
        tmp_year = str(tmp_date.year)
        tmp_month = tmp_date.strftime('%B').lower()

        # Selecting the appropriate keys in the preferences
        try:
            rule_entry = makefile[tmp_year][tmp_month]
            rule_dates = {
                'start': rule_entry['start'],
                'end': rule_entry['end']
            }
        except KeyError as e:
            print('Error: the key {} is not present in the preferences'.format(e))

        # Casting month abbreviation and defining preferred account
        tmp_month = tmp_date.strftime('%b').lower()
        preferred_account = '--statement=$(GB_ACCOUNT)'

        # Creating strings for formatting
        str_rule = '{}-{}_{}:\n\t$(call {},{},{},{})'

        # Generating rule: Comment
        print('# {}: {}'.format(tmp_year, tmp_month.title()))
        # Generating rule: Analysis
        print(str_rule.format(tmp_year, tmp_month, 'analysis',
                              'analysis', rule_dates['start'], rule_dates['end'], preferred_account))
        print(str_rule.format(tmp_year, tmp_month, 'analysis-all',
                              'analysis', rule_dates['start'], rule_dates['end'], '--all'))
        # Generating rule: Statement
        print(str_rule.format(tmp_year, tmp_month, 'statement',
                              'statement', rule_dates['start'], rule_dates['end'], preferred_account))
        print(str_rule.format(tmp_year, tmp_month, 'statement-all',
                              'statement', rule_dates['start'], rule_dates['end'], '--all'))

    def get_categories(self):
        """Get categories defined in the preferences

        :return: list categories: categories
        """
        # Selecting categories
        categories = self.preferences_data['categories']
        return categories

    def get_statements(self):
        """Get all paths of all statements

        :return: list statements: a list containing all statements with full paths
        """
        # Selecting statements
        main_path = self.preferences_data['statements']

        # Creating a regex to select only files with .json extension
        regex = re.compile(r'\.(json)$')

        # Creating a list containing all statements paths
        statements = []
        for path, dnames, fnames in os.walk(main_path):
            statements.extend([os.path.join(path, x) for x in fnames if regex.search(x)])
        return statements

    def show_categories(self):
        """Show categories and subcategories defined in the preferences
        """
        # Getting categories
        categories = self.get_categories()

        # Creating strings for printing
        str_category = '> ' + Style.BRIGHT + Fore.BLUE + '{}' + Style.RESET_ALL
        str_subcategory = ' >> ' + Fore.BLUE + '{}' + Style.RESET_ALL

        # Printing categories
        print("Available categories:")
        for category in categories:
            print(str_category.format(category.title()))
            for subcategory in categories[category]:
                print(str_subcategory.format(subcategory.title()))

    def show_dates(self, date_start, date_end):
        """Show dates and date interval with number of days, all defined in arguments

        :param str date_start: Starting date for when counting transactions
        :param str date_end: Ending date until when counting transactions
        """
        # Computing deltas
        now = datetime.now()
        delta = datetime.strptime(date_end, '%Y-%m-%d') - datetime.strptime(date_start, '%Y-%m-%d')
        delta_start = now - datetime.strptime(date_start, '%Y-%m-%d')
        delta_end = datetime.strptime(date_end, '%Y-%m-%d') - now

        # Changing dates format
        start = datetime.strptime(date_start, '%Y-%m-%d').strftime('%A, %d %B %Y')
        end = datetime.strptime(date_end, '%Y-%m-%d').strftime('%A, %d %B %Y')

        # Creating strings for printing
        str_arrow = Style.DIM + '  {}  ' + Style.RESET_ALL
        str_header = Style.BRIGHT + '{}: ' + Style.RESET_ALL
        str_date = str_arrow + str_header + Fore.BLUE + '{}' + Style.RESET_ALL
        str_deltas = ' (' + Fore.BLUE + '-{}' + Style.RESET_ALL +\
                     '/' + Fore.BLUE + '+{} ~{}w' + Style.RESET_ALL + ')' + Style.RESET_ALL

        # Printing dates
        print(str_header.format('Dates'))
        # Printing month in case delta is small
        if delta.days <= 33:
            print(str_date.format('\u2b91', 'Month', datetime.strptime(date_end, '%Y-%m-%d').strftime('%B %Y')))
        print(str_date.format('\u2b91', 'Start', start))
        print(str_date.format('\u2b91', 'End', end))
        print(str_date.format('\u2b91', 'Days', delta.days), end='')
        # Printing deltas only for current month
        if datetime.strptime(date_start, '%Y-%m-%d') <= now <= datetime.strptime(date_end, '%Y-%m-%d'):
            print(str_deltas.format(delta_start.days, delta_end.days, math.ceil(delta_end.days/7.0)))
