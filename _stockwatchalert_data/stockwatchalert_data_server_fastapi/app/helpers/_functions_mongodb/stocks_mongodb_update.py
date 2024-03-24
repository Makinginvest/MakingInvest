import asyncio
import chunk
from datetime import date, timedelta
import datetime
import time
import timeit
from typing import List

import pandas as pd
from _project.log_config.app_logger import app_logger
from app.helpers._functions.get_resample_df import get_resample_df
from more_itertools import chunked

from app.helpers._functions_mongodb._mongodb import update_mongodb_data_by_symbol
from app.helpers._functions_mongodb.stocks_functions import (
    get_stock_ohlcv_data_alpaca_http_multi,
    get_stock_ohlcv_data_alpaca_http_single,
    get_stock_symbols,
)


# --------------------------------  All ------------------------------- #
async def update_ohlcv_data_mongodb_all(symbol: str, timeframe="15m", lookback_days=380) -> List[pd.DataFrame]:
    try:
        end_date = datetime.datetime.utcnow()
        start_date = end_date - timedelta(days=lookback_days)

        # Fetch 15-min data
        if timeframe == "15m":
            df = pd.DataFrame()
            df_15m = await get_stock_ohlcv_data_alpaca_http_single(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
            if df_15m is None or df_15m.empty:
                return None
            df_15m = df_15m.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            df_15m = df_15m.sort_values(by="dateTimeUtc", ascending=False)
            df = pd.concat([df, df_15m])

            # we need to resample based on group of symbols and timeframe
            resamples_timeframes = ["30m"]
            for tf in resamples_timeframes:
                df_resample = get_resample_df(df_15m, tf)
                df_resample = df_resample.dropna(subset=["close"])
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False)
                df = pd.concat([df, df_resample])

        # Fetch 1h data
        if timeframe == "1h":
            df = pd.DataFrame()
            df_1h = await get_stock_ohlcv_data_alpaca_http_single(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
            if df_1h is None or df_1h.empty:
                return None
            df_1h = df_1h.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            df_1h = df_1h.sort_values(by="dateTimeUtc", ascending=False)
            df = pd.concat([df, df_1h])

            # we need to resample based on group of symbols and timeframe
            resamples_timeframes = ["2h", "4h"]
            for tf in resamples_timeframes:
                df_resample = get_resample_df(df_1h, tf)
                df_resample = df_resample.dropna(subset=["close"])
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False)
                df = pd.concat([df, df_resample])

        # Fetch 1d data
        if timeframe == "1d":
            df = pd.DataFrame()
            df_1d = await get_stock_ohlcv_data_alpaca_http_single(symbol=symbol, timeframe=timeframe, start_date=start_date, end_date=end_date)
            if df_1d is None or df_1d.empty:
                return None
            df_1d = df_1d.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            df_1d = df_1d.sort_values(by="dateTimeUtc", ascending=False)
            df = pd.concat([df, df_1d])
            # print(df.head(20))

        return df

    except Exception as e:
        print("Error:update_ohlcv_data_mongodb_all", e)
        return None


async def stocks_update_all_mongodb_historical_all(timeframe="15min", lookback_days=365, recursive_tries=3, recursive_symbols=[]) -> None:
    start = time.time()

    # Get stock symbols based on the timeframe
    symbols = get_stock_symbols(path="_project/datasets/data/_data_symbols_stock_us_market.csv")
    symbols = recursive_symbols if recursive_symbols else symbols
    print(len(symbols))
    symbols = [s.replace("/", "") for s in symbols]
    symbols = [s for s in symbols if "-" not in s]  # Remove symbols with a "-"
    symbols = list(set(symbols))  # remove deplicates
    symbols = sorted(symbols, key=lambda x: x, reverse=False)
    symbols = symbols[3000:]
    # print(symbols)

    all_dfs = pd.DataFrame()

    chunk_symbols = 100 if timeframe != "1d" else 100

    for symbols_batch in chunked(symbols, chunk_symbols):
        start_time = timeit.default_timer()
        tasks = []
        for symbol in symbols_batch:
            tasks.append(asyncio.ensure_future(update_ohlcv_data_mongodb_all(symbol=symbol, timeframe=timeframe, lookback_days=lookback_days)))
        batch_results = await asyncio.gather(*tasks)
        for result in batch_results:
            if isinstance(result, pd.DataFrame) and not result.empty:
                all_dfs = pd.concat([all_dfs, result])
        end_time = timeit.default_timer()
        duration = end_time - start_time
        print(f"{len(symbols_batch)} symbols updated in {duration} seconds.")
        await asyncio.sleep(30 - duration) if duration < 30 and timeframe != "1d" else None

    if all_dfs.empty:
        print("No data to update.")
        return "No data to update."

    # Combine all valid dataframes
    all_dfs_combined = all_dfs
    # drop duplicated on symbol and dateTimeUtc
    all_dfs_combined = all_dfs_combined.drop_duplicates(subset=["symbol", "dateTimeUtc", "timeframe"], keep="first")
    # all_dfs_combined.to_csv(f"_project/datasets/data/_data_historical_stocks_{timeframe}.csv", index=False)
    # print unique symbols
    symbols_unique = all_dfs_combined["symbol"].unique()
    symbols_no_data = list(set(symbols) - set(symbols_unique))
    print(f"Symbols with no data: {len(symbols_no_data)}")
    # Group by timeframe and update MongoDB data for each group
    grouped = all_dfs_combined.groupby("timeframe")
    for _timeframe, group in grouped:
        # write to csv
        await update_mongodb_data_by_symbol(group.to_dict("records"), baseCollection="historicalStocks", timeframe=_timeframe, use_replace_one=False)

    # Log the execution time
    execution_time = (time.time() - start) / 60
    stat = f"stocks_update_all_mongodb_historical_all_{timeframe}: {execution_time:.2f} minutes"
    app_logger().info(stat)

    # do recursive_calls if needed
    if recursive_tries > 0 and len(symbols_no_data) > 0:
        # write to csv symbols_no_data
        symbols_no_data_df = pd.DataFrame(symbols_no_data, columns=["symbol"])
        # symbols_no_data_df.to_csv(f"_project/datasets/data/_data_symbols_stock_us_market_{timeframe}_no_data.csv", index=False)

        await stocks_update_all_mongodb_historical_all(
            timeframe=timeframe, lookback_days=lookback_days, recursive_tries=recursive_tries - 1, recursive_symbols=symbols_no_data
        )

    return "done"


# --------------------------------  RECENT ------------------------------- #
async def stocks_update_all_mongodb_historical_recent(start_index=0, end_index=-1, timeframe="15m", recursive_tries=1, recursive_symbols=[]):
    start = time.time()
    symbols = get_stock_symbols(path="_project/datasets/data/_data_symbols_stock_us_market.csv")
    symbols = recursive_symbols if recursive_symbols else symbols
    print(len(symbols))
    symbols = [s.replace("/", "") for s in symbols]
    symbols = [s for s in symbols if "-" not in s]  # Remove symbols with a "-"
    symbols = list(set(symbols))  # remove deplicates

    symbols = symbols[start_index:end_index]
    all_dfs = []

    for symbols_batch in chunked(symbols, 200):
        tasks = []
        batches = chunked(symbols_batch, 10)
        for batch in batches:
            tasks.append(asyncio.ensure_future(update_ohlcv_data_mongodb_recent(symbols=batch, timeframe=timeframe)))
        batch_results = await asyncio.gather(*tasks)
        for result in batch_results:
            if result:
                all_dfs.extend(result)

    # Check if there is data to update
    if not all_dfs:
        return "No data to update."

    # Combine all valid dataframes
    all_dfs_combined = pd.concat(all_dfs, ignore_index=True)
    # all_dfs_combined.to_csv(f"_project/datasets/data/_data_historical_stocks_{timeframe}.csv", index=False)
    # print unique symbols
    symbols_unique = all_dfs_combined["symbol"].unique()
    symbols_no_data = list(set(symbols) - set(symbols_unique))
    print(f"Symbols with no data: {len(symbols_no_data)}")

    # Group by timeframe and update MongoDB data for each group
    grouped = all_dfs_combined.groupby("timeframe")
    for _timeframe, group in grouped:
        # write to csv
        await update_mongodb_data_by_symbol(group.to_dict("records"), baseCollection="historicalStocks", timeframe=_timeframe)

    # Log the execution time
    execution_time = (time.time() - start) / 60
    stat = f"stocks_update_all_mongodb_historical_recent_{timeframe}: {execution_time:.2f} minutes"
    app_logger().info(stat)

    # do recursive_calls if needed
    if recursive_tries > 0 and len(symbols_no_data) > 0:
        print("recursive_tries", recursive_tries)
        # write to csv symbols_no_data
        symbols_no_data_df = pd.DataFrame(symbols_no_data, columns=["symbol"])
        # symbols_no_data_df.to_csv(f"_project/datasets/data/_data_symbols_stock_us_market_{timeframe}_no_data.csv", index=False)

        await stocks_update_all_mongodb_historical_recent(timeframe=timeframe, recursive_tries=recursive_tries - 1, recursive_symbols=symbols_no_data)

    return "done"


async def update_ohlcv_data_mongodb_recent(symbols, timeframe="15m", upload_limit=1) -> pd.DataFrame:
    try:

        # Fetch 15-min data
        if timeframe == "15m":
            dfs = []
            df_15m = pd.DataFrame()
            df_15m = await get_stock_ohlcv_data_alpaca_http_multi(symbols=symbols, timeframe=timeframe, limit=10000)
            if df_15m is None or df_15m.empty:
                return None
            df_15m = df_15m.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            _df_15m = df_15m.copy()
            _df_15m = _df_15m.sort_values(by="dateTimeUtc", ascending=False)
            _df_15m = _df_15m.groupby("symbol").head(upload_limit)
            dfs = [_df_15m]

            resamples_timeframes = ["30m"]
            grouped = df_15m.groupby("symbol")
            for tf in resamples_timeframes:
                for symbol, group in grouped:
                    _tf = tf if tf != "30m" else "30min"
                    df_resample = get_resample_df(group, tf)
                    df_resample = df_resample.dropna(subset=["close"])
                    df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False)
                    df_resample = df_resample.head(upload_limit)
                    dfs.append(df_resample)

        # Fetch 1-hour data
        if timeframe == "1h":
            dfs = []
            df_1h = pd.DataFrame()
            df_1h = await get_stock_ohlcv_data_alpaca_http_multi(symbols=symbols, timeframe=timeframe, limit=10000)
            if df_1h is None or df_1h.empty:
                return None
            df_1h = df_1h.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            _df_1h = df_1h.copy()
            _df_1h = _df_1h.sort_values(by="dateTimeUtc", ascending=False)
            _df_1h = _df_1h.groupby("symbol").head(upload_limit)
            dfs = [_df_1h]

            resamples_timeframes = ["2h", "4h"]
            grouped = df_1h.groupby("symbol")
            for tf in resamples_timeframes:
                for symbol, group in grouped:
                    df_resample = get_resample_df(group, tf)
                    df_resample = df_resample.dropna(subset=["close"])
                    df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False)
                    df_resample = df_resample.head(upload_limit)
                    dfs.append(df_resample)

        # Fetch 1-day data
        if timeframe == "1d":
            dfs = []
            df_1d = pd.DataFrame()
            df_1d = await get_stock_ohlcv_data_alpaca_http_multi(symbols=symbols, timeframe=timeframe, limit=10000)
            if df_1d is None or df_1d.empty:
                return None
            df_1d = df_1d.drop_duplicates(subset=["symbol", "dateTimeUtc"], keep="first")
            _df_1d = df_1d.copy()
            _df_1d = _df_1d.sort_values(by="dateTimeUtc", ascending=False)
            _df_1d = _df_1d.groupby("symbol").head(upload_limit)
            dfs = [_df_1d]

        return dfs

    except Exception as e:
        print("Error:update_mongodb_data_by_symbol", e)
        return None


# --------------------------------- FUNTIONS --------------------------------- #
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
