import requests
import os
import logging
from redis import Redis
import json
# from decimal import *

redis_conn = Redis('localhost', 6379)

def get_dash_poloniex(url):
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
        redis_conn.set('poloniex.get_dash_poloniex', json.dumps(average))
        return average
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    get_dash_poloniex()
