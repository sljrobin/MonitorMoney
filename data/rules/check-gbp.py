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


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def get_rate():
    """Get the GBP rate
    """
    cmd_rate = 'curl -s -k "https://www.x-rates.com/calculator/?from=GBP&to=EUR&amount=1"' + \
        '| grep "ccOutputRslt" | tail -c +33 | head -c 5'
    rate = os.popen(cmd_rate).read()
    return rate


def main():
    """Convert the savings in the appropriate currency
    """
    # Checking internet
    internet_on()
    # Getting rate and savings
    rate = get_rate()
    # Converting values to float
    rate = float(rate)
    # Creating string for formatting
    str_error = Fore.RED + '' + Style.RESET_ALL

    # Checking an argument is provided
    if len(sys.argv) > 1:
        # Converting to float
        try:
            alert = float(sys.argv[1])
            # If current rate is >= to set rate, showing notification
            if rate >= alert:
                notify("MoniMoney", "Set rate: {}\nCurrent rate: {}".format(sys.argv[1], rate))
        except:
            print(str_error.format("Error while converting provided rate."))
    else:
        print(str_error.format("An argument is required (e.g. 1.20)."))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperation interrupted')
        sys.exit(0)
