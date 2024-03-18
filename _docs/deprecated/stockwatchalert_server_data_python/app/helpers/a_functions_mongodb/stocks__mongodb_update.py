import asyncio
from datetime import date, timedelta
import datetime
import time
import numpy as np

import pandas as pd
from _log_config.app_logger import app_logger
from app.helpers.a_functions.resample_df import get_resample_df

from app.helpers.a_functions_mongodb._mongodb import update_mongodb_data_by_symbol
from app.helpers.a_functions_mongodb.stocks__functions import get_ftm_stock_ohlcv_data, get_stock_symbols


def get_dates_from_to_array_day(lookback_days=15):
    today = date.today()
    from_date = today - timedelta(days=lookback_days)
    last = date(today.year, today.month, today.day)
    return pd.date_range(from_date, last, freq="D")


def get_date_range_start_end_limit(start_date=None, end_date=None, lookback_days=30, chunk=5):
    start_date = datetime.datetime.utcnow() if start_date is None else start_date
    end_date = start_date - timedelta(days=lookback_days) if end_date is None else end_date
    current_date = start_date
    date_range = [current_date]

    while current_date >= end_date:
        current_date -= timedelta(days=chunk)
        date_range.append(current_date)

    return date_range


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_all(symbol, interval="15min", lookback_days=30) -> pd.DataFrame:
    try:
        date_range = get_date_range_start_end_limit(chunk=5, lookback_days=lookback_days)

        df = pd.DataFrame()
        for date in date_range:
            _data = await get_ftm_stock_ohlcv_data(symbol=symbol, interval=interval, from_date=date - timedelta(days=6), to_date=date)
            df = df.append(_data)
            df.sort_index(inplace=True)
        df = df[~df.index.duplicated(keep="last")]

        df["timeframe"] = "15m"
        df["symbol"] = symbol

        df = get_resample_df(df, "15m")
        df_30m = get_resample_df(df, "30m")
        df_1h = get_resample_df(df, "1h")
        df_2h = get_resample_df(df, "2h")
        df_4h = get_resample_df(df, "4h")
        df_1d = get_resample_df(df, "1d")

        df = df.dropna(subset=["close"])
        df_30m = df_30m.dropna(subset=["close"])
        df_1h = df_1h.dropna(subset=["close"])
        df_2h = df_2h.dropna(subset=["close"])
        df_4h = df_4h.dropna(subset=["close"])
        df_1d = df_1d.dropna(subset=["close"])

        # datetime now in utc
        datenow_15 = get_now_floor("15min")
        datenow_30 = get_now_floor("30min")
        datenow_1h = get_now_floor("1h")
        datenow_2h = get_now_floor("2h")
        datenow_4h = get_now_floor("4h")

        df = df[df["dateTimeUtc"] < datenow_15]
        df_30m = df_30m[df_30m["dateTimeUtc"] < datenow_30]
        df_1h = df_1h[df_1h["dateTimeUtc"] < datenow_1h]
        df_2h = df_2h[df_2h["dateTimeUtc"] < datenow_2h]
        df_4h = df_4h[df_4h["dateTimeUtc"] < datenow_4h]
        df_1d = df_1d.dropna(subset=["close"])

        tasks = [
            update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalStocks", timeframe="15m"),
            update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalStocks", timeframe="30m"),
            update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalStocks", timeframe="1h"),
            update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalStocks", timeframe="2h"),
            update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalStocks", timeframe="4h"),
        ]
        await asyncio.gather(*tasks)

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


async def stocks_update_all_mongodb_historical_all(interval="15min", lookback_days=30):
    start = time.time()
    symbols = get_stock_symbols(path="_datasets/data/_data_symbols_stock_options_sp500.csv")
    symbols = [s.replace("/", "") for s in symbols]
    # symbols = symbols[:50]
    # symbols = ["PYPL"]

    for i in range(0, len(symbols), 5):
        symbols_batch = symbols[i : i + 5]
        asyncio.sleep(7)
        await asyncio.gather(*[update_ohlcv_data_mongodb_all(symbol, interval=interval, lookback_days=lookback_days) for symbol in symbols_batch])

    stat = f"stocks_update_all_mongodb_historical_all_5m_15m: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_recent(symbol, interval="15min") -> pd.DataFrame:
    try:
        df = await get_ftm_stock_ohlcv_data(symbol=symbol, interval=interval)

        if df is None or df.empty:
            return None

        df["timeframe"] = "15m"
        df["symbol"] = symbol

        df_30m = get_resample_df(df, "30m")
        df_1h = get_resample_df(df, "1h")
        df_2h = get_resample_df(df, "2h")
        df_4h = get_resample_df(df, "4h")

        df = df.dropna(subset=["close"])
        df_30m = df_30m.dropna(subset=["close"])
        df_1h = df_1h.dropna(subset=["close"])
        df_2h = df_2h.dropna(subset=["close"])
        df_4h = df_4h.dropna(subset=["close"])

        # datetime now in utc
        datenow_15 = get_now_floor("15min")
        datenow_30 = get_now_floor("30min")
        datenow_1h = get_now_floor("1h")
        datenow_2h = get_now_floor("2h")
        datenow_4h = get_now_floor("4h")

        df = df[df["dateTimeUtc"] < datenow_15]
        df_30m = df_30m[df_30m["dateTimeUtc"] < datenow_30]
        df_1h = df_1h[df_1h["dateTimeUtc"] < datenow_1h]
        df_2h = df_2h[df_2h["dateTimeUtc"] < datenow_2h]
        df_4h = df_4h[df_4h["dateTimeUtc"] < datenow_4h]

        tasks = [
            update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalStocks", timeframe="15m"),
            update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalStocks", timeframe="30m"),
            update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalStocks", timeframe="1h"),
            update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalStocks", timeframe="2h"),
            update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalStocks", timeframe="4h"),
        ]

        await asyncio.gather(*tasks)

        close = df["close"].iloc[-1] if len(df) > 0 else 0
        close_15min_ago = df["close"].iloc[-2] if len(df) > 1 else 0
        close_30min_ago = df["close"].iloc[-3] if len(df) > 2 else 0
        close_1hr_ago = df["close"].iloc[-4] if len(df) > 3 else 0
        close_4hr_ago = df["close"].iloc[-16] if len(df) > 15 else 0
        close_24hr_ago = df["close"].iloc[-96] if len(df) > 95 else 0

        close_15min_ago_pct = (close - close_15min_ago) / close_15min_ago if close_15min_ago != 0 else 0
        close_30min_ago_pct = (close - close_30min_ago) / close_30min_ago if close_30min_ago != 0 else 0
        close_1hr_ago_pct = (close - close_1hr_ago) / close_1hr_ago if close_1hr_ago != 0 else 0
        close_4hr_ago_pct = (close - close_4hr_ago) / close_4hr_ago if close_4hr_ago != 0 else 0
        close_24hr_ago_pct = (close - close_24hr_ago) / close_24hr_ago if close_24hr_ago != 0 else 0

        # round to 2 decimal places
        close_15min_ago_pct = round(close_15min_ago_pct, 2)
        close_30min_ago_pct = round(close_30min_ago_pct, 2)
        close_1hr_ago_pct = round(close_1hr_ago_pct, 2)
        close_4hr_ago_pct = round(close_4hr_ago_pct, 2)
        close_24hr_ago_pct = round(close_24hr_ago_pct, 2)

        df_close = pd.DataFrame(
            {
                "s": [symbol],
                "c": [close],
                "c15m": [close_15min_ago],
                "c30m": [close_30min_ago],
                "c1h": [close_1hr_ago],
                "c4h": [close_4hr_ago],
                "c24h": [close_24hr_ago],
                "c15m_pct": [close_15min_ago_pct],
                "c30m_pct": [close_30min_ago_pct],
                "c1h_pct": [close_1hr_ago_pct],
                "c4h_pct": [close_4hr_ago_pct],
                "c24h_pct": [close_24hr_ago_pct],
            }
        )

        return df_close

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


async def stocks_update_all_mongodb_historical_recent(interval="15min", start_index=0, end_index=-1):
    start = time.time()
    symbols = get_stock_symbols()
    symbols = [s.replace("/", "") for s in symbols]
    df_close = pd.DataFrame()
    symbols = symbols[start_index:end_index]

    for i in range(0, len(symbols), 15):
        symbols_batch = symbols[i : i + 15]
        val = await asyncio.gather(*[update_ohlcv_data_mongodb_recent(symbol, interval=interval) for symbol in symbols_batch])
        df_close = df_close.append(val)

    stat = f"stocks_update_all_mongodb_historical_recent: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"


def get_now_floor(period="15min"):
    now = datetime.datetime.utcnow()
    now_15 = now - datetime.timedelta(minutes=now.minute % 15, seconds=now.second, microseconds=now.microsecond)
    now_15 = np.datetime64(now_15)
    now_15 = pd.to_datetime(now_15, utc=True)

    now_30 = now - datetime.timedelta(minutes=now.minute % 30, seconds=now.second, microseconds=now.microsecond)
    now_30 = np.datetime64(now_30)
    now_30 = pd.to_datetime(now_30, utc=True)

    # floor to 1 hour
    now_1hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_1hr = np.datetime64(now_1hr)
    now_1hr = pd.to_datetime(now_1hr, utc=True)

    now_2hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_2hr = now_2hr - datetime.timedelta(hours=now_2hr.hour % 2)
    now_2hr = np.datetime64(now_2hr)
    now_2hr = pd.to_datetime(now_2hr, utc=True)

    now_4hr = now - datetime.timedelta(minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    now_4hr = now_4hr - datetime.timedelta(hours=now_4hr.hour % 4)
    now_4hr = np.datetime64(now_4hr)
    now_4hr = pd.to_datetime(now_4hr, utc=True)

    if period == "15min":
        return now_15
    elif period == "30min":
        return now_30
    elif period == "1h":
        return now_1hr
    elif period == "2h":
        return now_2hr
    elif period == "4h":
        return now_4hr
    else:
        return None
