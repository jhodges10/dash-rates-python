#!flask/bin/python
import os
import logging
import json
from flask import Flask, jsonify, make_response
from flask_restplus import Api, Resource
from pathlib import Path  # python3 only
from dotenv import load_dotenv
from redis import Redis
from providers.cryptocompare import get_average_price
from providers.poloniex import get_dash_poloniex
from providers.bitcoinaverage import get_bitcoin_average_dash_btc
from storage_interface import start_data_manager

app = Flask(__name__)
api = Api(app=app, doc="/docs")
ns_conf = api.namespace('', description='Rates')
try:
    if os.getenv('REDIS_URL'):
        r = Redis.from_url(os.getenv('REDIS_URL'), decode_responses=True)
    else:
        r = Redis(decode_responses=True)
    print("Connection Made")

except Exception as e:
    print(e)

def setup():
    # Environment variable is set on Heroku
    if os.getenv("ENVIRONMENT") == "PRODUCTION": 
        print("Found production environment, no need to load .env file... Continuing.")
        pass
    # Load .env file into os environment 
    else:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=False)


@ns_conf.route("/<rate>")
class Rates(Resource):
    def get(self, rate):
        """
        Returns the rates for queried currencies
        """
        print(rate)
        payload = r.get('cryptocompare.get_average_price')
        print(payload)
        return json.dumps(payload)


@ns_conf.route("/avg")
class Avg(Resource):
    def get(self):
        """
        Returns the average price of Dash
        """
        payload = r.get('cryptocompare.get_average_price')
        print(payload)
        return payload


@ns_conf.route("/btcaverage")
class BTCAverage(Resource):
    def get(self):
        """
        This is the average DASH price across Binance, Kraken, Poloniex, and Bitfinex
        """
        payload = r.get('bitcoinaverage.get_bitcoin_average_dash_btc')
        print(payload)
        return payload


@ns_conf.route("/poloniex")
class Polo(Resource):
    def get(self):
        """
        This is an average of the price paid for the last 200 trades on Poloniex

        """
        payload = r.get('poloniex.get_dash_poloniex')
        print(payload)
        return payload

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    setup() # Initialize .envs/ ENV variables
    port_number = os.getenv("PORT", 5000)
    debug = os.getenv('DEBUG', False)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    
    start_data_manager()
    app.run(host='0.0.0.0', port=port_number, debug=debug)
