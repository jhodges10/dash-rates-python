import requests
import os
import logging
from redis import Redis
import json

redis_conn = Redis('localhost', 6379)

def get_bitcoin_average_dash_btc(url):
    response = requests.get(url)
    if response.status_code == 200:
        dash_avg_value = response.json()['last']
        print(dash_avg_value)
        redis_conn.set('bitcoinaverage.get_bitcoin_average_dash_btc', json.dumps(dash_avg_value))
        return dash_avg_value
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    get_bitcoin_average_dash_btc()
