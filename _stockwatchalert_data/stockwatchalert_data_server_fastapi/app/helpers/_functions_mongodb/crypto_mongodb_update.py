import asyncio
import datetime
import io
from operator import le
import os
import re
import time
import zipfile
from datetime import date, timedelta
import warnings

import aiohttp
import ccxt.async_support as ccxt
import pandas as pd
from _project.log_config.app_logger import app_logger
from app.helpers._functions.get_resample_df import get_resample_df


from app.helpers._functions_mongodb.crypto_functions import get_USDT_symbols_by_value
from app.helpers._functions_mongodb._mongodb import update_mongodb_data_by_symbol


pd.options.display.float_format = "{:.8f}".format
warnings.filterwarnings("ignore")


def get_dates_from_to_array_day(lookback_days=15):
    today = date.today()
    from_date = today - timedelta(days=lookback_days)
    last = date(today.year, today.month, today.day)
    return pd.date_range(from_date, last, freq="D")


def get_dates_from_to_array_months(lookback_months=1):
    today = date.today()
    from_date = today - timedelta(days=lookback_months * 30)
    last = date(today.year, today.month, today.day)
    return pd.date_range(from_date, last, freq="M")


# ---------------------------  MONTHLY GET DATA -------------------------- #
async def get_binance_data_monthly_zip(session, symbol=None, interval=None, year=None, month=None):
    try:
        url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{year}-{month}.zip"
        async with session.get(url) as resp:
            r = await resp.read()
            z = zipfile.ZipFile(io.BytesIO(r))
            z.extractall("_project/datasets/binance/_temp/binance_raw")
            return f"_project/datasets/binance/_temp/binance_raw/{symbol}-{interval}-{year}-{month}.csv"
    except Exception as e:
        return None


async def get_binance_data_monthly_by_symbol(symbol, timeframe, lookback_months=1):
    file_list = []
    lookback_dates_months = get_dates_from_to_array_months(lookback_months)

    try:
        async with aiohttp.ClientSession() as session:
            for date in lookback_dates_months:
                url = asyncio.ensure_future(get_binance_data_monthly_zip(session, symbol, timeframe, date.year, date.strftime("%m")))
                file_list.append(asyncio.ensure_future(url))

            file_list = await asyncio.gather(*file_list)
            file_list = [x for x in file_list if x is not None]

            df = pd.DataFrame()
            for f in file_list:
                new_df = pd.read_csv(f, header=None)
                columns = ["time", "open", "high", "low", "close", "volume", "1", "2", "3", "4", "5", "6"]
                new_df.columns = columns
                new_df.drop(new_df.columns[6:], axis=1, inplace=True)
                df = pd.concat([df, new_df], ignore_index=True)

            df.insert(1, "symbol", symbol)
            df["time"] = pd.to_datetime(df["time"], unit="ms")
            df.sort_values(by=["time"], inplace=True)

            if not os.path.exists(f"_project.datasets/_binance/{timeframe}"):
                os.makedirs(f"_project.datasets/_binance/{timeframe}")

            df.to_csv(f"_project.datasets/_binance/{timeframe}/{symbol}-{timeframe}.csv", index=False)

            for f in file_list:
                os.remove(f)

    except Exception as e:
        print(e)

    return "done"


# ----------------------------  DAILY GET DATA --------------------------- #
async def get_binance_data_daily_zip(session, symbol=None, interval=None, year=None, month=None, day=None):
    try:
        url = f"https://data.binance.vision/data/spot/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{year}-{month}-{day}.zip"
        async with session.get(url) as resp:
            r = await resp.read()
            z = zipfile.ZipFile(io.BytesIO(r))
            z.extractall("_project/datasets/binance/_temp/binance_raw")

            return f"_project/datasets/binance/_temp/binance_raw/{symbol}-{interval}-{year}-{month}-{day}.csv"
    except Exception as e:
        return None


async def get_binance_data_daily_by_symbol(symbol, timeframe="15m", lookback_days=15):
    file_list = []
    lookback_dates_days = get_dates_from_to_array_day(lookback_days)
    async with aiohttp.ClientSession() as session:
        for date in lookback_dates_days:
            url = get_binance_data_daily_zip(session, symbol, timeframe, date.year, date.strftime("%m"), date.strftime("%d"))
            file_list.append(asyncio.ensure_future(url))

        file_list = await asyncio.gather(*file_list)
        await session.close()

        file_list = [x for x in file_list if x is not None]

        if len(file_list) == 0:
            return None

        df = pd.DataFrame()
        for f in file_list:
            new_df = pd.read_csv(f, header=None)
            columns = ["time", "open", "high", "low", "close", "volume", "1", "2", "3", "4", "5", "6"]
            new_df.columns = columns
            new_df.drop(new_df.columns[6:], axis=1, inplace=True)
            df = pd.concat([df, new_df], ignore_index=True)

        df["time"] = pd.to_datetime(df["time"], unit="ms")
        if os.path.exists(f"_project.datasets/_binance/{timeframe}/{symbol}-{timeframe}.csv"):
            df_existing = pd.read_csv(f"_project.datasets/_binance/{timeframe}/{symbol}-{timeframe}.csv")
            df_existing["time"] = pd.to_datetime(df_existing["time"])
            df = pd.concat([df_existing, df], ignore_index=True)
            df.sort_values(by=["time"], inplace=True)
            df.drop_duplicates(subset=["time"], keep="last", inplace=True)

        df.sort_values(by=["time"], inplace=True)

        df["dateTimeUtc"] = df["time"]
        df["dateTimeEst"] = df["dateTimeUtc"] - pd.Timedelta(hours=5)
        df["symbol"] = symbol
        df["timeframe"] = timeframe

        if not os.path.exists(f"_project.datasets/_binance/{timeframe}"):
            os.makedirs(f"_project.datasets/_binance/{timeframe}")

        df.to_csv(f"_project.datasets/_binance/{timeframe}/{symbol}-{timeframe}.csv", index=False)
        os.remove(f"_project.datasets/_binance/{timeframe}/{symbol}-{timeframe}.csv")

        for f in file_list:
            os.remove(f)

        # Keep data from Janauary 1st 2022
        df = df[df["dateTimeUtc"] >= pd.to_datetime(datetime.date(2022, 1, 1))]

        df.set_index("time", inplace=True)

        if timeframe == "15m":
            df_15m = df
            df_30m = get_resample_df(df, "30m")
            df_1h = get_resample_df(df, "1h")
            df_2h = get_resample_df(df, "2h")
            df_3h = get_resample_df(df, "3h")
            df_4h = get_resample_df(df, "4h")
            df_6h = get_resample_df(df, "6h")
            df_8h = get_resample_df(df, "8h")
            df_12h = get_resample_df(df, "12h")
            df_1d = get_resample_df(df, "1d")

            tasks = [
                update_mongodb_data_by_symbol(df_15m.to_dict("records"), baseCollection="historicalCrypto", timeframe="15m"),
                update_mongodb_data_by_symbol(df_30m.to_dict("records"), baseCollection="historicalCrypto", timeframe="30m"),
                update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalCrypto", timeframe="1h"),
                update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalCrypto", timeframe="2h"),
                update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalCrypto", timeframe="4h"),
                update_mongodb_data_by_symbol(df_6h.to_dict("records"), baseCollection="historicalCrypto", timeframe="6h"),
                update_mongodb_data_by_symbol(df_8h.to_dict("records"), baseCollection="historicalCrypto", timeframe="8h"),
                update_mongodb_data_by_symbol(df_12h.to_dict("records"), baseCollection="historicalCrypto", timeframe="12h"),
                update_mongodb_data_by_symbol(df_1d.to_dict("records"), baseCollection="historicalCrypto", timeframe="1d"),
            ]
            await asyncio.gather(*tasks)

        if timeframe == "1h":
            df_1h = df
            df_2h = get_resample_df(df, "2h")
            df_4h = get_resample_df(df, "4h")
            df_6h = get_resample_df(df, "6h")
            df_8h = get_resample_df(df, "8h")
            df_12h = get_resample_df(df, "12h")
            df_1d = get_resample_df(df, "1d")

            tasks = [
                update_mongodb_data_by_symbol(df_1h.to_dict("records"), baseCollection="historicalCrypto", timeframe="1h"),
                update_mongodb_data_by_symbol(df_2h.to_dict("records"), baseCollection="historicalCrypto", timeframe="2h"),
                update_mongodb_data_by_symbol(df_4h.to_dict("records"), baseCollection="historicalCrypto", timeframe="4h"),
                update_mongodb_data_by_symbol(df_6h.to_dict("records"), baseCollection="historicalCrypto", timeframe="6h"),
                update_mongodb_data_by_symbol(df_8h.to_dict("records"), baseCollection="historicalCrypto", timeframe="8h"),
                update_mongodb_data_by_symbol(df_12h.to_dict("records"), baseCollection="historicalCrypto", timeframe="12h"),
                update_mongodb_data_by_symbol(df_1d.to_dict("records"), baseCollection="historicalCrypto", timeframe="1d"),
            ]

            await asyncio.gather(*tasks)

        return "done"


async def get_binance_data_monthly_all_symbol(timeframe="15m", lookback_months=1, symbols=None):
    for i in range(0, len(symbols), 5):
        try:
            symbols_batch = symbols[i : i + 5]
            await asyncio.gather(*[get_binance_data_monthly_by_symbol(symbol, timeframe, lookback_months=lookback_months) for symbol in symbols_batch])
        except Exception as e:
            print(f"Error get_binance_data_monthly_all_symbol", e)

    return symbols


async def get_binance_data_daily_all_symbol(timeframe="15m", lookback_days=15, symbols=None):
    for i in range(0, len(symbols), 5):
        try:
            symbols_batch = symbols[i : i + 5]
            await asyncio.gather(*[get_binance_data_daily_by_symbol(s, timeframe=timeframe, lookback_days=lookback_days) for s in symbols_batch])
        except Exception as e:
            print(f"Error get_binance_data_daily_by_symbol", e)

    return symbols


async def crypto_update_all_mongodb_historical_all(timeframe="15m", lookback_days=15, lookback_months=1, pull_monthly=True):
    try:
        start = time.time()
        symbols = await get_USDT_symbols_by_value("_project/datasets/data/_data_symbols_crypto_usdt_busd.csv")
        symbols = [s.replace("/", "") for s in symbols]
        symbols = symbols[:]

        if pull_monthly:
            await get_binance_data_monthly_all_symbol(timeframe=timeframe, lookback_months=lookback_months, symbols=symbols)

        await get_binance_data_daily_all_symbol(timeframe=timeframe, lookback_days=lookback_days, symbols=symbols)
        stat = f"crypto_update_all_mongodb_historical_all: {(time.time() - start) / 60:.2f} minutes"
        app_logger().info(stat)

    except Exception as e:
        print(f"Error", e)

    return "done"


# ----------------------------  RECENT UPDATE ---------------------------- #
async def update_ohlcv_data_mongodb_recent(symbol, timeframe="15m", limit=500, exchange=None) -> pd.DataFrame:
    try:
        upload_limit = 10
        df = await exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(df, columns=["time", "open", "high", "low", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["timeframe"] = timeframe
        df["symbol"] = symbol
        df.insert(0, "dateTimeUtc", df["time"])
        df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5)),
        df.set_index("time", inplace=True)
        df_for_resameple = df.copy()

        df = df.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)
        dfs = [df]

        if timeframe == "15m":
            resamples_timeframes = ["30m"]
            for tf in resamples_timeframes:
                df_resample = get_resample_df(df_for_resameple, tf)
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)
                dfs.append(df_resample)

        if timeframe == "1h":
            resamples_timeframes = ["2h", "4h", "6h", "8h", "12h", "1d"]
            for tf in resamples_timeframes:
                df_resample = get_resample_df(df_for_resameple, tf)
                df_resample = df_resample.sort_values(by="dateTimeUtc", ascending=False).head(upload_limit)
                dfs.append(df_resample)

        return dfs

    except Exception as e:
        print("Error:crypto_update_all_mongodb_historical_recent", e)
        return None


async def crypto_update_all_mongodb_historical_recent(timeframe="15m", limit=200, path="_project/datasets/data/_data_symbols_crypto_usdt_busd.csv"):
    try:
        exchange = ccxt.binance({"rateLimit": 2400, "enableRateLimit": False})
        start = time.time()
        symbols = await get_USDT_symbols_by_value(path)
        symbols = [s.replace("/", "") for s in symbols]

        all_dfs = []

        for i in range(0, len(symbols), 50):
            symbols_batch = symbols[i : i + 50]
            batches = await asyncio.gather(*[update_ohlcv_data_mongodb_recent(symbol, timeframe=timeframe, limit=limit, exchange=exchange) for symbol in symbols_batch])
            for batch in batches:
                if batch:
                    all_dfs.extend(batch)

        if not all_dfs:
            return "No data to update."

        all_dfs_combined = pd.concat(all_dfs, ignore_index=True)

        grouped = all_dfs_combined.groupby("timeframe")
        for _timeframe, group in grouped:
            await update_mongodb_data_by_symbol(group.to_dict("records"), baseCollection="historicalCrypto", timeframe=_timeframe)

        await exchange.close()

        stat = f"crypto_update_all_mongodb_historical_recent_{timeframe}: {(time.time() - start) / 60:.2f} minutes"
        app_logger().info(stat)
        return all_dfs_combined

    except Exception as e:
        print("Error:crypto_update_all_mongodb_historical_recent", e)
        return []
