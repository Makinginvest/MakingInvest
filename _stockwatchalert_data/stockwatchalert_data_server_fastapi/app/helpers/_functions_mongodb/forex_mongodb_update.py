import asyncio
import datetime
import time
from datetime import date, timedelta

import pandas as pd
from _project.log_config.app_logger import app_logger
from app.helpers._functions.get_now_floor import get_now_floor
from app.helpers._functions.get_resample_df import get_resample_df
from app.helpers._functions_mongodb.forex_functions import get_forex_symbols_oanda, get_onada_forex_ohlcv_data
from app.helpers._functions_mongodb._mongodb import update_mongodb_data_by_symbol


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
async def update_ohlcv_data_mongodb_all(symbol, granularity="M5", timeframe="5m") -> pd.DataFrame:
    try:
        date_range = get_date_range_start_end_limit(chunk=10, lookback_days=370 * 1)

        if timeframe == "5m":
            date_range = get_date_range_start_end_limit(chunk=10, lookback_days=30 * 1)

        df = pd.DataFrame()
        for date in date_range:
            _data = await get_onada_forex_ohlcv_data(symbol=symbol, granularity=granularity, to_date=date, from_date=date - timedelta(days=11))
            df = df.append(_data)
            df.sort_index(inplace=True)
        df = df[~df.index.duplicated(keep="last")]

        df["timeframe"] = timeframe
        df["symbol"] = symbol
        df["symbol"] = df["symbol"].str.replace("_", "")

        df = df[df["dateTimeUtc"] > pd.Timestamp(datetime.datetime(2022, 1, 1), tz="UTC")]

        if timeframe == "5m":
            tasks = [
                update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalForex", timeframe="5m"),
            ]

        if timeframe == "15m":
            df_15m = get_resample_df(df, timeframe="15m")
            df_30m = get_resample_df(df, timeframe="30m")
            df_1h = get_resample_df(df, timeframe="1h")
            df_2h = get_resample_df(df, timeframe="2h")
            df_4h = get_resample_df(df, timeframe="4h")

            # delete row where close is NaN
            df_15m = df_15m.dropna(subset=["close"])
            df_30m = df_30m.dropna(subset=["close"])
            df_1h = df_1h.dropna(subset=["close"])
            df_2h = df_2h.dropna(subset=["close"])
            df_4h = df_4h.dropna(subset=["close"])

            tasks = [
                update_mongodb_data_by_symbol(df_15m.to_dict("records"), baseCollection="historicalForex", timeframe="15m"),
                update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalForex", timeframe="30m"),
                update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalForex", timeframe="1h"),
                update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalForex", timeframe="2h"),
                update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalForex", timeframe="4h"),
            ]

        if timeframe == "1d":
            tasks = [update_mongodb_data_by_symbol(df.to_dict("records"), baseCollection="historicalForex", timeframe="1d")]

        await asyncio.gather(*tasks)

    except Exception as e:
        print("Error:update_ohlcv_data_mongodb_all", e)
        return None


async def forex_update_all_mongodb_historical_all(granularity="M5", timeframe="5m"):
    start = time.time()
    symbols = get_forex_symbols_oanda(path="_project/datasets/data/_data_symbols_forex_oanda.csv")
    symbols = [s.replace("/", "_") for s in symbols]
    # symbols = symbols[:5]
    # symbols = ["EUR_CZK"]

    for i in range(0, len(symbols), 4):
        symbols_batch = symbols[i : i + 4]
        asyncio.sleep(3)
        await asyncio.gather(*[update_ohlcv_data_mongodb_all(symbol, granularity=granularity, timeframe=timeframe) for symbol in symbols_batch])

    stat = f"forex_update_all_mongodb_historical_recent_5m: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"


# --------------------------------  RECENT ------------------------------- #
async def update_ohlcv_data_mongodb_recent(symbol, granularity="M5", timeframe="5m", upload_limit=20) -> pd.DataFrame:
    try:
        df = await get_onada_forex_ohlcv_data(symbol=symbol, granularity=granularity)
        df["timeframe"] = timeframe
        df["symbol"] = symbol
        df["symbol"] = df["symbol"].str.replace("_", "")
        df_for_resameple = df.copy()

        if df is None or df.empty:
            return None

        date_floor = get_now_floor(timeframe)
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
                _tf = tf if tf != "30m" else "30min"
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


async def forex_update_all_mongodb_historical_recent(granularity="M5", timeframe="5m"):
    start = time.time()
    symbols = get_forex_symbols_oanda(path="_project/datasets/data/_data_symbols_forex_oanda.csv")
    symbols = [s.replace("/", "_") for s in symbols]
    # symbols = symbols[:1]

    all_dfs = []

    for i in range(0, len(symbols), 25):
        symbols_batch = symbols[i : i + 25]
        batches = await asyncio.gather(*[update_ohlcv_data_mongodb_recent(symbol, granularity=granularity, timeframe=timeframe) for symbol in symbols_batch])
        for batch in batches:
            if batch:
                all_dfs.extend(batch)

    # Combine all valid dataframes
    if not all_dfs:
        return "No data to update."

    all_dfs_combined = pd.concat(all_dfs, ignore_index=True)
    all_dfs_combined = all_dfs_combined.dropna(subset=["close"])

    grouped = all_dfs_combined.groupby("timeframe")
    for _timeframe, group in grouped:
        await update_mongodb_data_by_symbol(group.to_dict("records"), baseCollection="historicalForex", timeframe=_timeframe)

    stat = f"forex_update_all_mongodb_historical_recent_{timeframe}: {(time.time() - start) / 60:.2f} minutes"
    app_logger().info(stat)
    return "done"
