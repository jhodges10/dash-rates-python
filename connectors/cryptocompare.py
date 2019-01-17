import requests
import os
import logging

def get_btc_to_ves():
    url = os.environ.get('vesUrl')
    response = requests.get(url)
    if response.status_code == 200:
        btc_to_ves_val = response.json()['VES']
        print(btc_to_ves_val)
        return True
    else:
        logging.error(response.content())
        return None

def get_average_price():
    url = os.environ.get('averageUrl')
    response = requests.get(url)
    if response.status_code == 200:
        dash_average_val = response.json()['RAW']['PRICE']
        print(dash_average_val)
        return dash_average_val
    else:
        logging.error(response.content())
        return None

if __name__ == "__main__":
    # get_btc_to_ves()
    get_average_price()
