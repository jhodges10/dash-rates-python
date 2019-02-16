# This is Dash Rates Python3

## Installation

1. Start by installing all requirements with `pip3 install requirements.txt`
2. To start the application to run locally, make sure you start the infrastructure with `make infra`.
3. Start a worker with `rq worker`
4. Start the scheduler with `rqscheduler`
5. Start the web process with `python3 index.py`