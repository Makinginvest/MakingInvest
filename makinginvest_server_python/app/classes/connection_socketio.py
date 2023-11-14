import datetime
from typing import Any, List


class ConnectionManagerSockerIo:
    def __init__(self):
        self.is_background_task_running_crypto = False
        self.prices_crypto = []

        self.is_background_task_running_forex = False
        self.prices_forex = []

        self.is_background_task_running_stocks = False
        self.prices_stocks = []

        self.is_background_task_running_market_analysis = False
        self.dt_market_analysis_updated = None
        self.market_analysis = None

        self.is_background_task_running_symbols_tracker = False
        self.dt_symbols_tracker_updated = None
        self.symbols_tracker = None

        self.is_background_task_running_news_aggr = False
        self.dt_news_aggr_updated = None
        self.news_aggr = None

        self.is_background_task_running_signal_aggr_open = False
        self.dt_signal_aggr_open_updated = None
        self.signal_aggr_open = []

        # ------------------------------- CRYPTO PRICES ------------------------------ #

    def set_is_background_task_running_crypto(self, value: bool):
        self.is_background_task_running_crypto = value

    def set_prices_crypto(self, prices_crypto: List):
        self.prices_crypto = prices_crypto

        # ------------------------------- FOREX PRICES ------------------------------- #

    def set_is_background_task_running_forex(self, value: bool):
        self.is_background_task_running_forex = value

    def set_prices_forex(self, prices_forex: List):
        self.prices_forex = prices_forex

        # ------------------------------- STOCK PRICES ------------------------------- #

    def set_is_background_task_running_stocks(self, value: bool):
        self.is_background_task_running_stocks = value

    def set_prices_stocks(self, prices_stocks: List):
        self.prices_stocks = prices_stocks

        # ------------------------------ MARKET ANALYSIS ------------------------------ #

    def set_is_background_task_running_market_analysis(self, value: bool):
        self.is_background_task_running_market_analysis = value

    def set_dt_market_analysis_updated(self, market_analysis_last_updated_datetime: datetime.datetime):
        self.dt_market_analysis_updated = market_analysis_last_updated_datetime

    def set_market_analysis(self, market_analysis: Any):
        self.market_analysis = market_analysis

        # ------------------------------ SYMBOLS TRACKER ------------------------------ #

    def set_is_background_task_running_symbols_tracker(self, value: bool):
        self.is_background_task_running_symbols_tracker = value

    def set_dt_symbols_tracker_updated(self, symbols_tracker_last_updated_datetime: datetime.datetime):
        self.dt_symbols_tracker_updated = symbols_tracker_last_updated_datetime

    def set_symbols_tracker(self, symbols_tracker: Any):
        self.symbols_tracker = symbols_tracker

        # ----------------------------------- NEWS ----------------------------------- #

    def set_is_background_task_running_news_aggr(self, value: bool):
        self.is_background_task_running_news_aggr = value

    def set_dt_news_aggr_updated(self, news_aggr_last_updated_datetime: datetime.datetime):
        self.dt_news_aggr_updated = news_aggr_last_updated_datetime

    def set_news_aggr(self, news_aggr: Any):
        self.news_aggr = news_aggr

        # ------------------------------- OPEN SIGNALS ------------------------------- #

    def set_is_background_task_running_signal_aggr_open(self, value: bool):
        self.is_background_task_running_signal_aggr_open = value

    def set_signal_aggr_open(self, signal_aggr_open: List):
        self.signal_aggr_open = signal_aggr_open

    def set_dt_signal_aggr_open_updated(self, signal_aggr_open_last_updated_datetime: datetime.datetime):
        self.dt_signal_aggr_open_updated = signal_aggr_open_last_updated_datetime
