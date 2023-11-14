import asyncio
import datetime
from sqlite3 import Timestamp
import time
from datetime import date, timedelta

import pandas as pd
from _log_config.app_logger import app_logger
from app.helpers.a_functions.resample_df import get_resample_df
from app.helpers.a_functions_mongodb.forex__functions import get_forex_symbols_oanda, get_onada_forex_ohlcv_data
from app.helpers.a_functions_mongodb._mongodb import update_mongodb_data_by_symbol


def get_dates_from_to_array_day(lookback_days=15):
    today = date.today()
    from_date = today - timedelta(days=lookback_days)
    last = date(today.year, today.month, today.day)
    return pd.date_range(from_date, last, freq="D")


def get_date_range_start_end_limit(start_date=None, end_date=None, lookback=30, chunk=5):
    start_date = datetime.datetime.utcnow() if start_date is None else start_date
    end_date = start_date - timedelta(days=lookback) if end_date is None else end_date
    current_date = start_date
    date_range = [current_date]

    while current_date >= end_date:
        current_date -= timedelta(days=chunk)
        date_range.append(current_date)

    return date_range


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_all(symbol, granularity="M5") -> pd.DataFrame:
    try:
        date_range = get_date_range_start_end_limit(chunk=10, lookback=30 * 15)

        df = pd.DataFrame()
        for date in date_range:
            _data = await get_onada_forex_ohlcv_data(symbol=symbol, granularity=granularity, to_date=date, from_date=date - timedelta(days=11))
            df = df.append(_data)
            df.sort_index(inplace=True)
        df = df[~df.index.duplicated(keep="last")]

        df["timeframe"] = "5m"
        df["symbol"] = symbol
        df["symbol"] = df["symbol"].str.replace("_", "")
        df = df.replace({pd.NaT: None})
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

        df["dateTimeUtc"] = pd.to_datetime(df["dateTimeUtc"])
        df["dateTimeEst"] = pd.to_datetime(df["dateTimeEst"])
        # convert dtype=datetime64[ns]  to datetime.datetime
        df["dateTimeUtc"] = df["dateTimeUtc"].dt.tz_localize(None)
        df["dateTimeEst"] = df["dateTimeEst"].dt.tz_localize(None)

        df = df[df["dateTimeUtc"] > datetime.datetime(2022, 1, 1)]

        df_15m = get_resample_df(df, timeframe="15m")
        df_30m = get_resample_df(df, timeframe="30m")
        df_45m = get_resample_df(df, timeframe="45m")
        df_1h = get_resample_df(df, timeframe="1h")
        df_2h = get_resample_df(df, timeframe="2h")
        df_4h = get_resample_df(df, timeframe="4h")
        df_6h = get_resample_df(df, timeframe="6h")
        df_12h = get_resample_df(df, timeframe="12h")

        # delete row where close is NaN
        df_15m = df_15m.dropna(subset=["close"])
        df_30m = df_30m.dropna(subset=["close"])
        df_45m = df_45m.dropna(subset=["close"])
        df_1h = df_1h.dropna(subset=["close"])
        df_2h = df_2h.dropna(subset=["close"])
        df_4h = df_4h.dropna(subset=["close"])
        df_6h = df_6h.dropna(subset=["close"])
        df_12h = df_12h.dropna(subset=["close"])

        # keep only last 30 days of data for 5 mins
        v = (datetime.datetime.now() - datetime.timedelta(days=30 * 6)).date()
        v = pd.to_datetime(v, utc=True)
        df = df[df.index.date >= v]

        tasks = [
            update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalForex", timeframe="5m"),
            update_mongodb_data_by_symbol(df_15m.to_dict("records"), baseCollection="historicalForex", timeframe="15m"),
            update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalForex", timeframe="30m"),
            update_mongodb_data_by_symbol(df_45m.to_dict("records"), baseCollection="historicalForex", timeframe="45m"),
            update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalForex", timeframe="1h"),
            update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalForex", timeframe="2h"),
            update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalForex", timeframe="4h"),
            update_mongodb_data_by_symbol(df_6h.to_dict("records"), baseCollection="historicalForex", timeframe="6h"),
            update_mongodb_data_by_symbol(df_12h.to_dict("records"), baseCollection="historicalForex", timeframe="12h"),
        ]

        if granularity == "M15":
            tasks = tasks[1:]

        await asyncio.gather(*tasks)

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


async def forex_update_all_mongodb_historical_all(resolution="M5"):
    start = time.time()
    symbols = get_forex_symbols_oanda(path="_datasets/data/_data_symbols_forex_oanda.csv")
    symbols = [s.replace("/", "_") for s in symbols]
    # symbols = symbols[25:]
    # symbols = ["EUR_CZK"]

    for i in range(0, len(symbols), 4):
        symbols_batch = symbols[i : i + 4]
        asyncio.sleep(3)
        await asyncio.gather(*[update_ohlcv_data_mongodb_all(symbol, granularity=resolution) for symbol in symbols_batch])

    stat = f"forex_update_all_mongodb_historical_recent_5m: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_recent(symbol, granularity="M5") -> pd.DataFrame:
    try:
        df = await get_onada_forex_ohlcv_data(symbol=symbol, granularity=granularity)
        df["timeframe"] = "5m"
        df["symbol"] = symbol
        df["symbol"] = df["symbol"].str.replace("_", "")

        df = df.replace({pd.NaT: None})
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

        # conver to datetime
        df["dateTimeUtc"] = pd.to_datetime(df["dateTimeUtc"])
        df["dateTimeEst"] = pd.to_datetime(df["dateTimeEst"])

        df_15m = get_resample_df(df, timeframe="15m")
        df_30m = get_resample_df(df, timeframe="30m")
        df_45m = get_resample_df(df, timeframe="45m")
        df_1h = get_resample_df(df, timeframe="1h")
        df_2h = get_resample_df(df, timeframe="2h")
        df_4h = get_resample_df(df, timeframe="4h")

        # delete row where close is NaN
        df_15m = df_15m.dropna(subset=["close"])
        df_30m = df_30m.dropna(subset=["close"])
        df_45m = df_45m.dropna(subset=["close"])
        df_1h = df_1h.dropna(subset=["close"])
        df_2h = df_2h.dropna(subset=["close"])
        df_4h = df_4h.dropna(subset=["close"])

        tasks = [
            update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalForex", timeframe="5m"),
            update_mongodb_data_by_symbol(df_15m.to_dict("records"), baseCollection="historicalForex", timeframe="15m"),
            update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalForex", timeframe="30m"),
            update_mongodb_data_by_symbol(df_45m.to_dict("records"), baseCollection="historicalForex", timeframe="45m"),
            update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalForex", timeframe="1h"),
            update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalForex", timeframe="2h"),
            update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalForex", timeframe="4h"),
        ]

        if granularity == "M15":
            tasks = tasks[1:]

        await asyncio.gather(*tasks)

        close = df_15m["close"].iloc[-1] if len(df_15m) > 0 else 0
        close_15min_ago = df_15m["close"].iloc[-2] if len(df_15m) > 1 else 0
        close_30min_ago = df_15m["close"].iloc[-3] if len(df_15m) > 2 else 0
        close_1hr_ago = df_15m["close"].iloc[-4] if len(df_15m) > 3 else 0
        close_4hr_ago = df_15m["close"].iloc[-16] if len(df_15m) > 15 else 0
        close_24hr_ago = df_15m["close"].iloc[-96] if len(df_15m) > 95 else 0

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
                "s": [symbol.replace("_", "")],
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


async def forex_update_all_mongodb_historical_recent(resolution="M5"):
    start = time.time()
    symbols = get_forex_symbols_oanda(path="_datasets/data/_data_symbols_forex_oanda.csv")
    symbols = [s.replace("/", "_") for s in symbols]
    df_close = pd.DataFrame()
    # symbols = symbols[:1]

    for i in range(0, len(symbols), 50):
        symbols_batch = symbols[i : i + 50]
        val = await asyncio.gather(*[update_ohlcv_data_mongodb_recent(symbol, granularity=resolution) for symbol in symbols_batch])
        df_close = df_close.append(val)

    stat = f"forex_update_all_mongodb_historical_recent_5m: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"
