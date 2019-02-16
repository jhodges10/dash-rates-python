import requests
import os
import logging
from redis import Redis
import json

if os.getenv('REDIS_URL'):
    redis_conn = Redis.from_url(os.getenv('REDIS_URL'), decode_responses=True)
else:
    redis_conn = Redis()


def get_btc_to_ves(url):
    response = requests.get(url)
    if response.status_code == 200:
        btc_to_ves_val = response.json()['VES']
        print(btc_to_ves_val)
        redis_conn.set('cryptocompare.get_btc_to_ves', json.dumps(btc_to_ves_val))
        return True
    else:
        logging.error(response.content())
        return None

def get_average_price(url):
    response = requests.get(url)
    if response.status_code == 200:
        dash_average_val = response.json()['RAW']['PRICE']
        print(dash_average_val)
        redis_conn.set('cryptocompare.get_average_price', json.dumps(dash_average_val))
        return dash_average_val
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    # get_btc_to_ves()
    get_average_price()
