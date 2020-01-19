#!/usr/bin/env python3
from datetime import date, datetime
import argparse
import sys
from lib import analysis
from lib import preferences
from lib import statement
from lib import transaction


def main():
    # Creating a preferences object
    prefs = preferences.Preferences()

    # Defining arguments
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('action', type=str, default='analysis',
                        help='Perform analysis, show a statement, generate Makefile rule, or create a new transaction.')
    parser.add_argument('--rule', type=str, help='Year and month used to create a new Makefile rule (e.g. 2019-dec)')
    parser.add_argument('--start', type=str, default='2016-01-01', help='Start date')
    parser.add_argument('--end', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date')
    parser.add_argument('--statement', type=str, help='Path of the statement to use')
    parser.add_argument('--all', action='store_true', default=False, help='Take all statements or not')
    args = parser.parse_args()

    # Casting dates
    date_start = datetime.strptime(args.start, "%Y-%m-%d")
    date_end = datetime.strptime(args.end, "%Y-%m-%d")

    # Action: generate a new rule for Makefile
    if args.action == 'generate':
        date_rule = datetime.strptime(args.rule, "%Y-%b")
        prefs.generate_makefile_rule(date_rule.year, date_rule.month)

    # Action: create a new transaction
    elif args.action == 'create':
        trans = transaction.Transaction()
        trans.create()

    # Action: show a statement
    elif args.action == 'statement':
        # Selection: all statements
        if args.all:
            # Showing dates
            prefs.show_dates(args.start, args.end)
            # Getting all statement paths
            statements = prefs.get_statements()
            # For each statement found, showing account details and transactions
            for statement_file in statements:
                stat = statement.Statement(statement_file,
                                                date(date_start.year, date_start.month, date_start.day),
                                                date(date_end.year, date_end.month, date_end.day))
                stat.show_account()
                stat.show_transactions()
        # Selection: one statement
        else:
            # Defining statement
            stat = statement.Statement(args.statement,
                                            date(date_start.year, date_start.month, date_start.day),
                                            date(date_end.year, date_end.month, date_end.day))
            # Showing dates, account details and transactions
            prefs.show_dates(args.start, args.end)
            stat.show_account()
            stat.show_transactions()

    # Action: show an analysis
    elif args.action == 'analysis':
        # Selection: all statements
        if args.all:
            # Showing dates
            prefs.show_dates(args.start, args.end)
            # Getting all statement paths
            statements = prefs.get_statements()
            # For each statement found, showing account details and analysis
            for statement_file in statements:
                stat = statement.Statement(statement_file,
                                                date(date_start.year, date_start.month, date_start.day),
                                                date(date_end.year, date_end.month, date_end.day))
                analy = analysis.Analysis(statement_file,
                                             date(date_start.year, date_start.month, date_start.day),
                                             date(date_end.year, date_end.month, date_end.day))
                stat.show_account()
                analy.show_totals()
        # Selection: one statement
        else:
            # Defining statement and analysis
            stat = statement.Statement(args.statement,
                                            date(date_start.year, date_start.month, date_start.day),
                                            date(date_end.year, date_end.month, date_end.day))
            analy = analysis.Analysis(args.statement,
                                         date(date_start.year, date_start.month, date_start.day),
                                         date(date_end.year, date_end.month, date_end.day))
            # Showing dates, account details and analysis
            prefs.show_dates(args.start, args.end)
            stat.show_account()
            analy.show_totals()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperation interrupted')
        sys.exit(0)
