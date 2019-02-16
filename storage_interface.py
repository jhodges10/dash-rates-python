import sys, os
from providers import bitcoinaverage, poloniex, cryptocompare
from pathlib import Path  # python3 only
from dotenv import load_dotenv
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

def setup():
    # Environment variable is set on Heroku
    if os.getenv("ENVIRONMENT") == "PRODUCTION": 
        print("Found production environment, no need to load .env file... Continuing.")
        pass
    # Load .env file into os environment 
    else:
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path, verbose=False)

    return True

def refresh_data():
    setup()
    try:
        bitcoinaverage.get_bitcoin_average_dash_btc(os.environ.get('dash2btcUrl'))
    except:
        print("Failed to update bitcoin average pricing")

    try:
        poloniex.get_dash_poloniex(os.environ.get('poloniexDashUrl'))
    except:
        print("Failed to update poloniex pricing")

    try:
        cryptocompare.get_average_price(os.environ.get('averageUrl'))
        cryptocompare.get_btc_to_ves(os.environ.get('vesUrl'))
    except:
        print("Failed to update cryptocompare pricing")
        
    return True

def start_data_manager():
    print("Starting BG Workers")
    print("Intitializing Redis Queue")
    redis_conn = Redis('localhost', 6379)
    print("Connection Made")

    try:
        scheduler = Scheduler(connection=redis_conn)
    except:
        print("No Redis connection possible, exiting...")
        sys.exit(1)

    scheduler.schedule(
        scheduled_time=datetime.utcnow(),      # Time for first execution, in UTC timezone
        func=refresh_data,                     # Function to be queued
        interval=30,                            # Time before the function is called again, in seconds
    )

if __name__ == "__main__":
    start_data_manager()
