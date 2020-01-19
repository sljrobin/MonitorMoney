#!/usr/bin/env python3
from colorama import Fore, Style
import os
import urllib.request
import sys


def internet_on():
    """Check the Internet connection
    """
    try:
        urllib.request.urlopen('https://www.google.com/', timeout=30)
    except:
        print("No Internet connection")
        sys.exit(1)


def get_rate():
    """Get the GBP rate
    """
    cmd_rate = 'curl -s -k "https://www.x-rates.com/calculator/?from=GBP&to=EUR&amount=1"' + \
        '| grep "ccOutputRslt" | tail -c +33 | head -c 5'
    rate = os.popen(cmd_rate).read()
    return rate


def get_savings():
    """Get the last savings
    """
    cmd_savings = 'make -C /Users/sljrobin/Documents/Projects/MoniMoney/ last | grep "Savings"'
    savings = os.popen(cmd_savings).read()
    savings = savings[28:-24].replace(',', '')
    return savings


def main():
    """Convert the savings in the appropriate currency
    """
    # Checking internet
    internet_on()
    # Getting rate and savings
    rate = get_rate()
    savings = get_savings()
    # Converting values to float
    rate = float(rate)
    savings = float(savings)
    # Converting savings
    savings_converted = savings * rate

    # Creating strings for printing
    str_arrow = Style.DIM + '  \u2b91  ' + Style.RESET_ALL
    str_rate = str_arrow + \
        Fore.BLUE + '{:,.2f}€' + Style.RESET_ALL + \
        Fore.WHITE + ' \u2192 ' + Style.RESET_ALL + \
        Fore.BLUE + '{:,.5f}£' + Style.RESET_ALL
    str_savings = str_arrow + \
        Fore.YELLOW + '{:,.2f}£' + Style.RESET_ALL + \
        Fore.WHITE + ' \u2192 ' + Style.RESET_ALL + \
        Fore.YELLOW + '{:,.2f}€' + Style.RESET_ALL
    str_separator = Style.DIM + ' ' * 2 + '-' * 44 + Style.RESET_ALL

    # Printing converted savings
    print(str_separator)
    print(str_savings.format(savings, savings_converted))
    print(str_rate.format(1.00, rate))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperation interrupted')
        sys.exit(0)
