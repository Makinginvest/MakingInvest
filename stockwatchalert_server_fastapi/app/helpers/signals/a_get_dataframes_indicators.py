import numpy as np
import pandas as pd
import pandas as pd
import time
from functools import wraps
from app.helpers._functions.get_symbols_local_v1 import get_symbols_by_value_v1
from app.helpers._mongodb.a_mongodb_data import get_mongodb_data_historical

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


async def get_symbols_local_by_market_v1(market: str = "crypto"):
    path = ""
    if market == "crypto":
        path = "_project/data/symbols/_data_symbols_crypto_usdt_busd_futures.csv"
    if market == "stocks":
        path = "_project/data/symbols/_data_symbols_stock_us_market.csv"
    if market == "forex":
        path = "_project/data/symbols/_data_symbols_forex_oanda_main.csv"

    data = await get_symbols_by_value_v1(path)
    return data


async def get_symbol_data_mongodb_by_market_v1(symbol, timeframe, data_length, dt_start, dt_end, hist_coll_name="historicalCrypto"):
    _df = await get_mongodb_data_historical(symbol, hist_coll_name=hist_coll_name, timeframe=timeframe, limit=data_length, dt_start=dt_start, dt_end=dt_end)
    return _df


def timeit(func):
    """
    A decorator that times the execution duration of the decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Capture the start time
        result = func(*args, **kwargs)  # Execute the decorated function
        end_time = time.time()  # Capture the end time
        duration = end_time - start_time  # Calculate the duration
        print(f"{func.__name__} took {duration:.4f} seconds to complete.")
        return result

    return wrapper


def get_market_rank(dataframe: pd.DataFrame, timeframe="4h", rank: int = 10, rolling_lookback=96, min_close=None, max_close=None) -> pd.DataFrame:
    _dataframe = dataframe.copy()

    _dataframe["hlc3"] = (_dataframe["high"] + _dataframe["low"] + _dataframe["close"]) / 3
    _dataframe["ohlc4"] = (_dataframe["open"] + _dataframe["high"] + _dataframe["low"] + _dataframe["close"]) / 4
    _dataframe["oc_pct"] = np.abs(_dataframe["close"] - _dataframe["open"]) / _dataframe["open"]
    # _dataframe["volume"] = _dataframe["volume"] * _dataframe["close"] * _dataframe["hlc3"]
    _dataframe["volume"] = _dataframe["volume"] * _dataframe["close"] * _dataframe["ohlc4"]
    # _dataframe["volume"] = _dataframe["volume"] * _dataframe["oc_pct"]

    # Calculate rolling volume
    _dataframe["volume_rolling"] = _dataframe.groupby("symbol")["volume"].rolling(rolling_lookback).sum().reset_index(level=0, drop=True)

    # If min_close and max_close are specified, filter out rows where 'close' is outside the specified range
    if min_close is not None and max_close is not None:
        _dataframe = _dataframe[(_dataframe["close"] >= min_close) & (_dataframe["close"] <= max_close)]

    # Calculate volume rank
    _dataframe["volume_rank"] = _dataframe.groupby("dateTimeUtc")["volume_rolling"].rank(ascending=False, method="first")

    # Identify top rank based on the specified rank threshold
    _dataframe["is_top_rank"] = _dataframe["volume_rank"] <= rank

    # Ensure no duplicate indices before merging
    _dataframe = _dataframe.drop_duplicates(subset=["symbol", "dateTimeUtc"])

    # Define the columns to be retained
    columns = ["dateTimeUtc", "symbol", "volume_rank", "is_top_rank", "volume_rolling"]
    _dataframe = _dataframe[columns]

    # Merge the original dataframe with the calculated rankings
    dataframe = pd.merge(dataframe, _dataframe, on=["symbol", "dateTimeUtc"], how="left")

    return dataframe


def get_trade_duration(duration) -> str:
    days = duration.days
    seconds = duration.seconds

    # Calculate hours and minutes from seconds
    hours = seconds // 3600  # Convert seconds to hours
    minutes = (seconds % 3600) // 60  # Convert remainder to minutes

    # Format the duration as a string
    days_str = "d" if days <= 1 else "d"
    duration_str: str = f"{days}{days_str} {hours}h {minutes}m"
    return duration_str


def get_trades_duration_from_seconds(duration: int) -> str:
    try:
        days = duration // (24 * 3600)
        duration %= 24 * 3600
        hours = duration // 3600
        duration %= 3600
        minutes = duration // 60

        # no decimals
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)

        # Format the duration as a string
        days_str = "d" if days <= 1 else "d"
        duration_str = f"{days}{days_str} {hours}h {minutes}m"
        return duration_str

    except Exception as e:
        return None


def get_dates_months(start: datetime, end: datetime):
    dates_months = []

    # Ensure start is a datetime object (this step is redundant if inputs are guaranteed to be datetime objects)
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ValueError("start and end must be datetime.datetime objects")

    # Adjust the start_date to the first day of the start month
    start_month = start.replace(day=1)

    # Adjust the end_date to the last day of the end month
    temp_end_month = end + relativedelta(months=1)
    end_month_adjusted = temp_end_month.replace(day=1) - timedelta(days=1)

    while start_month <= end_month_adjusted:
        # The end of the month is the day before the start of the next month
        end_month = start_month + relativedelta(months=+1) - timedelta(days=1)

        # Append the dictionary to the list, ensuring the types match the input types
        dates_months.append({"start": start_month, "end": end_month})

        # Move to the first day of the next month
        start_month += relativedelta(months=+1)

    return dates_months
