import asyncio
from datetime import date, timedelta
import datetime
import time

import pandas as pd
from _project.log_config.app_logger import app_logger
from app.helpers._functions.get_now_floor import get_now_floor
from app.helpers._functions.get_resample_df import get_resample_df

from app.helpers._functions_mongodb._mongodb import update_mongodb_data_by_symbol
from app.helpers._functions_mongodb.stocks__functions import get_alpaca_stock_ohlcv_data, get_ftm_stock_ohlcv_data_daily, get_ftm_stock_ohlcv_data_intraday, get_stock_symbols


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

    # reverse the list
    date_range = date_range[::-1]
    return date_range


# --------------------------------  All ------------------------------- #
async def update_ohlcv_data_mongodb_all(symbol, interval="15min", lookback_days=30) -> pd.DataFrame:
    print("update_ohlcv_data_mongodb_all", symbol, interval, lookback_days)
    try:
        date_range_15m = get_date_range_start_end_limit(chunk=90, lookback_days=lookback_days)
        date_range_4h = get_date_range_start_end_limit(chunk=200, lookback_days=lookback_days)
        date_range_1d = get_date_range_start_end_limit(chunk=500, lookback_days=lookback_days)

        df = pd.DataFrame()
        for date in date_range_15m:
            _data = await get_alpaca_stock_ohlcv_data(symbol=symbol, timeframe=interval, start_date=date, end_date=date + timedelta(days=95))
            df = df.append(_data)
            df.sort_index(inplace=True)
        df["timeframe"] = "15m"
        df["symbol"] = symbol
        df = df[~df.index.duplicated(keep="last")]

        df_4h = pd.DataFrame()
        for date in date_range_4h:
            _data = await get_alpaca_stock_ohlcv_data(symbol=symbol, timeframe="4hour", start_date=date, end_date=date + timedelta(days=210))
            df_4h = df_4h.append(_data)
            df_4h.sort_index(inplace=True)
        df_4h["timeframe"] = "4h"
        df_4h["symbol"] = symbol
        df_4h = df_4h[~df_4h.index.duplicated(keep="last")]

        df_1d = pd.DataFrame()
        for date in date_range_1d:
            _data = await get_alpaca_stock_ohlcv_data(symbol=symbol, timeframe="1day", start_date=date, end_date=date + timedelta(days=550))
            df_1d = df_1d.append(_data)
            df_1d.sort_index(inplace=True)
        df_1d["timeframe"] = "1d"
        df_1d["symbol"] = symbol
        df_1d = df_1d[~df_1d.index.duplicated(keep="last")]

        df = get_resample_df(df, "15m")
        df_30m = get_resample_df(df, "30m")
        df_1h = get_resample_df(df, "1h")
        df_2h = get_resample_df(df, "2h")
        df_4h = get_resample_df(df_4h, "4h")
        df_12h = get_resample_df(df_4h, "12h")
        # df_1d = get_resample_df(df_1d, "1d")

        df = df.dropna(subset=["close"])
        df_30m = df_30m.dropna(subset=["close"])
        df_1h = df_1h.dropna(subset=["close"])
        df_2h = df_2h.dropna(subset=["close"])
        df_4h = df_4h.dropna(subset=["close"])
        df_12h = df_12h.dropna(subset=["close"])
        df_1d = df_1d.dropna(subset=["close"])

        # datetime now in utc
        datenow_15 = get_now_floor("15min")
        datenow_30 = get_now_floor("30min")
        datenow_1h = get_now_floor("1h")
        datenow_2h = get_now_floor("2h")
        datenow_4h = get_now_floor("4h")
        datenow_12h = get_now_floor("12h")
        datenow_1d = get_now_floor("1d")

        df = df[df["dateTimeUtc"] < datenow_15]
        df_30m = df_30m[df_30m["dateTimeUtc"] < datenow_30]
        df_1h = df_1h[df_1h["dateTimeUtc"] < datenow_1h]
        df_2h = df_2h[df_2h["dateTimeUtc"] < datenow_2h]
        df_4h = df_4h[df_4h["dateTimeUtc"] < datenow_4h]
        df_12h = df_12h[df_12h["dateTimeUtc"] < datenow_12h]
        df_1d = df_1d.dropna(subset=["close"])

        tasks = [
            update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalStocks", timeframe="15m"),
            update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalStocks", timeframe="30m"),
            update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalStocks", timeframe="1h"),
            update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalStocks", timeframe="2h"),
            update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalStocks", timeframe="4h"),
            update_mongodb_data_by_symbol(df_12h.to_dict("records"), baseCollection="historicalStocks", timeframe="12h"),
            update_mongodb_data_by_symbol(df_1d.to_dict("records"), baseCollection="historicalStocks", timeframe="1d"),
        ]
        await asyncio.gather(*tasks)

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


async def stocks_update_all_mongodb_historical_all(interval="15min", lookback_days=365):
    start = time.time()
    symbols = get_stock_symbols(path="_project/datasets/data/_data_symbols_stock_options_sp500.csv")
    symbols = [s.replace("/", "") for s in symbols]
    symbols = symbols[:250]
    # symbols = ["PYPL"]

    for i in range(0, len(symbols), 5):
        symbols_batch = symbols[i : i + 5]
        asyncio.sleep(5)
        await asyncio.gather(*[update_ohlcv_data_mongodb_all(symbol, interval=interval, lookback_days=lookback_days) for symbol in symbols_batch])

    stat = f"stocks_update_all_mongodb_historical_all_5m_15m: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_recent(symbol, interval="15min", timeframe="15m", upload_limit=10) -> pd.DataFrame:
    try:
        df = pd.DataFrame()
        if timeframe == "1d":
            df = await get_ftm_stock_ohlcv_data_daily(symbol=symbol, interval=interval)
        else:
            df = await get_ftm_stock_ohlcv_data_intraday(symbol=symbol, interval=interval)

        if df is None or df.empty:
            return None

        df["timeframe"] = timeframe
        df["symbol"] = symbol
        df_for_resameple = df.copy()

        date_floor = get_now_floor(interval)
        df = df[df["dateTimeUtc"] <= date_floor]
        df = df.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)

        if timeframe == "1d":
            df["dateTimeUtc"] = df["dateTimeUtc"].dt.floor("1d")
        dfs = [df]

        if timeframe == "15m":
            resamples_timeframes = ["30m", "1h", "2h", "4h"]
            for tf in resamples_timeframes:
                _tf = tf if tf != "30m" else "30min"
                df_resample = get_resample_df(df_for_resameple, tf)
                df_resample = df_resample.dropna(subset=["close"])
                date_floor = get_now_floor(_tf)
                df_resample = df_resample[df_resample["dateTimeUtc"] <= date_floor]
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)
                dfs.append(df_resample)

        if timeframe == "1h":
            resamples_timeframes = ["2h", "4h"]
            for tf in resamples_timeframes:
                df_resample = get_resample_df(df_for_resameple, tf)
                df_resample = df_resample.dropna(subset=["close"])
                date_floor = get_now_floor(_tf)
                df_resample = df_resample[df_resample["dateTimeUtc"] <= date_floor]
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)
                dfs.append(df_resample)

        return dfs

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


async def stocks_update_all_mongodb_historical_recent(interval="15min", start_index=0, end_index=-1, timeframe="15m"):
    start = time.time()
    symbols = get_stock_symbols()
    symbols = [s.replace("/", "") for s in symbols]
    symbols = symbols[start_index:end_index]
    # symbols = symbols[:2]

    all_dfs = []

    for i in range(0, len(symbols), 25):
        symbols_batch = symbols[i : i + 25]
        batches = await asyncio.gather(*[update_ohlcv_data_mongodb_recent(symbol, interval=interval, timeframe=timeframe) for symbol in symbols_batch])
        for batch in batches:
            if batch:
                all_dfs.extend(batch)

    # Combine all valid dataframes
    if not all_dfs:
        return "No data to update."

    all_dfs_combined = pd.concat(all_dfs, ignore_index=True)
    # write to csv

    grouped = all_dfs_combined.groupby("timeframe")
    for timeframe, group in grouped:
        await update_mongodb_data_by_symbol(group.to_dict("records"), baseCollection="historicalStocks", timeframe=timeframe)

    stat = f"stocks_update_all_mongodb_historical_recent_{timeframe}: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"
