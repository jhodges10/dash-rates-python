import requests
import os
import logging
# from decimal import *

def get_dash_poloniex():
    url = os.environ.get('poloniexDashUrl')
    response = requests.get(url)
    if response.status_code == 200:
        poloniex_trades = response.json()
        total = float()
        amount = float()

        for count, trade in enumerate(poloniex_trades):
            count += 1
            total += float(trade['total'])
            amount += float(trade['amount'])
        average = total/amount
        print(average)
        return average
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    get_dash_poloniex()
