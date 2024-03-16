import datetime
import time
import aiohttp
import pandas as pd
import ccxt.async_support as ccxt

import os
from dotenv import load_dotenv

load_dotenv()


def get_stock_symbols(path="_project/datasets/data/_data_symbols_stock_options_sp500.csv"):
    symbols_df = pd.read_csv(path)
    # convert symbol column to string
    symbols_df["symbol"] = symbols_df["symbol"].astype(str)

    symbols = symbols_df["symbol"].str.replace("/", "")
    symbols = symbols.tolist()

    return symbols


async def get_ftm_stock_ohlcv_data_intraday(symbol=None, interval="15min", to_date=None, from_date=None):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    to_date = datetime.datetime.utcnow() if to_date is None else to_date
    to_date = to_date.replace(minute=to_date.minute - to_date.minute % 5, second=0, microsecond=0)
    from_date = datetime.datetime.utcnow() - datetime.timedelta(5) if from_date is None else from_date
    from_date = from_date.replace(minute=from_date.minute - from_date.minute % 5, second=0, microsecond=0)

    #  format to yyyy-mm-dd
    to_date = to_date.strftime("%Y-%m-%d")
    from_date = from_date.strftime("%Y-%m-%d")

    url = f"https://financialmodelingprep.com/api/v3/historical-chart/{interval}/{symbol}?apikey={api_key}&from={from_date}&to={to_date}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if data is None:
                    return pd.DataFrame()

                data = {
                    "open": [x["open"] for x in data],
                    "high": [x["high"] for x in data],
                    "low": [x["low"] for x in data],
                    "close": [x["close"] for x in data],
                    "volume": [x["volume"] for x in data],
                    "time": [x["date"] for x in data],
                }
                df = pd.DataFrame(data)
                # time zone is new york convert to utc
                df["time"] = pd.to_datetime(df["time"])
                df["time"] = df["time"].dt.tz_localize("America/New_York")
                df["time"] = df["time"].dt.tz_convert("UTC")

                df["time"] = pd.to_datetime(df["time"])
                df.insert(0, "dateTimeUtc", df["time"])
                df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5)),
                df = df.set_index("time")
                df = df.sort_index()
                # df = df.between_time("13:30", "19:55")

                return df
    except Exception as e:
        print(f"error: {symbol}", e)
        return None


async def get_ftm_stock_ohlcv_data_daily(symbol=None, interval="15min", to_date=None, from_date=None):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    to_date = datetime.datetime.utcnow() if to_date is None else to_date
    to_date = to_date.replace(minute=to_date.minute - to_date.minute % 5, second=0, microsecond=0)
    from_date = datetime.datetime.utcnow() - datetime.timedelta(20) if from_date is None else from_date
    from_date = from_date.replace(minute=from_date.minute - from_date.minute % 5, second=0, microsecond=0)

    #  format to yyyy-mm-dd
    to_date = to_date.strftime("%Y-%m-%d")
    from_date = from_date.strftime("%Y-%m-%d")

    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}&from={from_date}&to={to_date}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if data is None:
                    return pd.DataFrame()

                data = {
                    "open": [x["open"] for x in data["historical"]],
                    "high": [x["high"] for x in data["historical"]],
                    "low": [x["low"] for x in data["historical"]],
                    "close": [x["close"] for x in data["historical"]],
                    "volume": [x["volume"] for x in data["historical"]],
                    "time": [x["date"] for x in data["historical"]],
                }

                df = pd.DataFrame(data)
                # time zone is new york convert to utc
                df["time"] = pd.to_datetime(df["time"])
                df["time"] = df["time"].dt.tz_localize("America/New_York")
                df["time"] = df["time"].dt.tz_convert("UTC")

                df["time"] = pd.to_datetime(df["time"])
                df.insert(0, "dateTimeUtc", df["time"])
                df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5)),
                df = df.set_index("time")
                df = df.sort_index()

                return df
    except Exception as e:
        print(f"error get_ftm_stock_ohlcv_data_daily: {symbol}", e)
        return None


async def get_alpaca_stock_ohlcv_data(symbol=None, timeframe="15min", start_date=None, end_date=None, limit=10000):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(1) if start_date is None else start_date
    end_date = datetime.datetime.utcnow() if end_date is None else end_date

    # print(f"start_date: {start_date}, end_date: {end_date}")
    #  format to yyyy-mm-dd
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?feed=sip&timeframe={timeframe}&start={start_date}&end={end_date}&limit={limit}"

    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY_ID"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_API_SECRET_KEY"),
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                # Check if 'bars' key exists and is not None
                if not data or "bars" not in data or data["bars"] is None:
                    return pd.DataFrame()

                data = {
                    "open": [x["o"] for x in data["bars"]],
                    "high": [x["h"] for x in data["bars"]],
                    "low": [x["l"] for x in data["bars"]],
                    "close": [x["c"] for x in data["bars"]],
                    "volume": [x["v"] for x in data["bars"]],
                    "time": [x["t"] for x in data["bars"]],
                }
                df = pd.DataFrame(data)
                df["time"] = pd.to_datetime(df["time"])
                df.insert(0, "dateTimeUtc", df["time"])
                df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5)),
                df = df.set_index("time")
                df = df.sort_index()
                return df

    except Exception as e:
        print(f"error: get_alpaca_stock_ohlcv_data {symbol}", e)
        return None
