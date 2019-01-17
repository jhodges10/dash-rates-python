import requests
import os
import logging

def get_bitcoin_average_dash_btc():
    url = os.environ.get('dash2btcUrl')
    response = requests.get(url)
    if response.status_code == 200:
        dash_avg_value = response.json()['last']
        print(dash_avg_value)
        return dash_avg_value
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    get_bitcoin_average_dash_btc()
