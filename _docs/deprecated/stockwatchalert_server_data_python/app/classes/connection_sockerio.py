import datetime
from typing import List


class ConnectionManagerSockerIo:
    def __init__(self):

        self.is_background_task_running_crypto = False
        self.is_background_task_running_forex = False
        self.is_background_task_running_stocks = False
        self.is_background_task_running_signal_aggr_open = False

        self.prices_crypto = []
        self.prices_forex = []
        self.prices_stocks = []
        self.signal_aggr_open = []
        self.signal_aggr_open_last_updated_datetime = None

    def set_is_background_task_running_crypto(self, value: bool):
        self.is_background_task_running_crypto = value

    def set_is_background_task_running_forex(self, value: bool):
        self.is_background_task_running_forex = value

    def set_is_background_task_running_stocks(self, value: bool):
        self.is_background_task_running_stocks = value

    def set_is_background_task_running_signal_aggr_open(self, value: bool):
        self.is_background_task_running_signal_aggr_open = value

    def set_prices_crypto(self, prices_crypto: List):
        self.prices_crypto = prices_crypto

    def set_prices_forex(self, prices_forex: List):
        self.prices_forex = prices_forex

    def set_prices_stocks(self, prices_stocks: List):
        self.prices_stocks = prices_stocks

    def set_signal_aggr_open(self, signal_aggr_open: List):
        self.signal_aggr_open = signal_aggr_open

    def set_signal_aggr_open_last_updated_datetime(self, signal_aggr_open_last_updated_datetime: datetime):
        self.signal_aggr_open_last_updated_datetime = signal_aggr_open_last_updated_datetime
