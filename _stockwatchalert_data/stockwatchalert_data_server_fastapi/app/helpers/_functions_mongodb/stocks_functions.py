import asyncio
from datetime import datetime, timedelta
from typing import List
import aiohttp
import pandas as pd
import os
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.timeframe import TimeFrameUnit


api_key = os.getenv("ALPACA_API_KEY_ID")
api_secret = os.getenv("ALPACA_API_SECRET_KEY")
client = StockHistoricalDataClient(api_key, api_secret, raw_data=True)


import os
from dotenv import load_dotenv

load_dotenv()


def get_stock_symbols(path="_project/datasets/data/_data_symbols_stock_us_market.csv"):
    symbols_df = pd.read_csv(path)
    # convert symbol column to string
    symbols_df["symbol"] = symbols_df["symbol"].astype(str)

    symbols = symbols_df["symbol"].str.replace("/", "")
    symbols = symbols.tolist()

    return symbols


async def get_fmp_stock_ohlcv_data_intraday(symbol=None, timeframe="15min", end_date=None, start_date=None):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    end_date = datetime.utcnow() if end_date is None else end_date
    end_date = end_date.replace(minute=end_date.minute - end_date.minute % 5, second=0, microsecond=0)
    start_date = datetime.utcnow() - timedelta(5) if start_date is None else start_date
    start_date = start_date.replace(minute=start_date.minute - start_date.minute % 5, second=0, microsecond=0)

    #  format to yyyy-mm-dd
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    url = f"https://financialmodelingprep.com/api/v3/historical-chart/{timeframe}/{symbol}?apikey={api_key}&from={start_date}&to={end_date}"
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


async def get_fmp_stock_ohlcv_data_daily(symbol=None, end_date=None, start_date=None):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    end_date = datetime.utcnow() if end_date is None else end_date
    end_date = end_date.replace(minute=end_date.minute - end_date.minute % 5, second=0, microsecond=0)
    start_date = datetime.utcnow() - timedelta(365 * 5) if start_date is None else start_date
    start_date = start_date.replace(minute=start_date.minute - start_date.minute % 5, second=0, microsecond=0)

    #  format to yyyy-mm-dd
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}&from={start_date}&to={end_date}"
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


async def get_stock_ohlcv_data_alpaca_http_single(symbol: str = "", timeframe: str = "15min", start_date: datetime = None, end_date: datetime = None, limit: int = 10000):
    start_date = datetime.utcnow() - timedelta(2) if start_date is None else start_date
    end_date = datetime.utcnow() if end_date is None else end_date

    if timeframe == "1d":
        _timeframe = "1day"
    if timeframe == "1h":
        _timeframe = "1hour"
    if timeframe == "15m":
        _timeframe = "15min"
    if timeframe == "5m":
        _timeframe = "5min"

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    page_token = ""

    # print(f"symbol: {symbol}, timeframe: {timeframe}, start_date: {start_date}, end_date: {end_date}, limit: {limit}")

    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY_ID"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_API_SECRET_KEY"),
    }

    try:
        async with aiohttp.ClientSession() as session:
            df = pd.DataFrame()
            while True:
                url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?&feed=sip&timeframe={_timeframe}&start={start_date}&end={end_date}&limit={limit}&adjustment=all&page_token={page_token}"
                # print(url)
                async with session.get(url, headers=headers) as response:
                    data = await response.json()

                    # Check if 'bars' key exists and is not None
                    if not data or "bars" not in data:
                        break

                    bars = data["bars"]
                    _data = {
                        "open": [x["o"] for x in bars],
                        "high": [x["h"] for x in bars],
                        "low": [x["l"] for x in bars],
                        "close": [x["c"] for x in bars],
                        "volume": [x["v"] for x in bars],
                        "time": [x["t"] for x in bars],
                    }
                    _df = pd.DataFrame(_data)
                    _df["time"] = pd.to_datetime(_df["time"])
                    _df["timeframe"] = timeframe
                    _df["symbol"] = symbol
                    _df.insert(0, "dateTimeUtc", _df["time"])
                    _df.insert(1, "dateTimeEst", _df["time"] - pd.Timedelta(hours=5))
                    _df = _df.set_index("time")
                    _df = _df.sort_index()
                    df = pd.concat([df, _df])

                    page_token = data.get("next_page_token")
                    if not page_token:
                        # print("no more pages")
                        # print(data)
                        break

            return df

    except Exception as e:
        print(f"error: get_alpaca_stock_ohlcv_data {symbol}", e)
        return None


async def get_stock_ohlcv_data_alpaca_http_multi(symbols: List = [], timeframe: str = "15min", start_date: datetime = None, end_date: datetime = None, limit: int = 10000):
    start_date = datetime.utcnow() - timedelta(2) if start_date is None else start_date
    end_date = datetime.utcnow() if end_date is None else end_date

    if timeframe == "1d":
        _timeframe = "1day"
    if timeframe == "1h":
        _timeframe = "1hour"
    if timeframe == "15m":
        _timeframe = "15min"
    if timeframe == "5m":
        _timeframe = "5min"

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    symbols_str = ",".join(symbols)

    url = f"https://data.alpaca.markets/v2/stocks/bars?symbols={symbols_str}&feed=sip&timeframe={_timeframe}&start={start_date}&end={end_date}&adjustment=all&limit={limit}"
    # print(url)

    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY_ID"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_API_SECRET_KEY"),
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                # Check if 'bars' key exists and is not None
                if not data or "bars" not in data:
                    return pd.DataFrame()

                df_list = []
                for symbol, bars in data["bars"].items():
                    # print(symbol, len(bars))
                    data = {
                        "open": [x["o"] for x in bars],
                        "high": [x["h"] for x in bars],
                        "low": [x["l"] for x in bars],
                        "close": [x["c"] for x in bars],
                        "volume": [x["v"] for x in bars],
                        "time": [x["t"] for x in bars],
                    }
                    df = pd.DataFrame(data)
                    df["time"] = pd.to_datetime(df["time"])
                    df["timeframe"] = timeframe
                    df["symbol"] = symbol
                    df.insert(0, "dateTimeUtc", df["time"])
                    df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5))
                    df = df.set_index("time")
                    df = df.sort_index()
                    df_list.append(df)

                if df_list:
                    df_final = pd.concat(df_list)
                    return df_final
                else:
                    return pd.DataFrame()

    except Exception as e:
        print(f"error: get_alpaca_stock_ohlcv_data {symbols}", e)
        return None


async def get_stock_ohlcv_data_alpaca(symbols=[], timeframe="15Min", start_date=None, end_date=None, limit=10000):
    start_date = datetime.utcnow() - timedelta(1) if start_date is None else start_date
    end_date = datetime.utcnow() if end_date is None else end_date

    if timeframe == "1d":
        _timeframe = TimeFrame(1, TimeFrameUnit.Day)
    if timeframe == "4h":
        _timeframe = TimeFrame(4, TimeFrameUnit.Hour)
    if timeframe == "1h":
        _timeframe = TimeFrame(1, TimeFrameUnit.Hour)
    if timeframe == "15m":
        _timeframe = TimeFrame(15, TimeFrameUnit.Minute)
    if timeframe == "5m":
        _timeframe = TimeFrame(5, TimeFrameUnit.Minute)

    try:
        # Assuming 'client' is an instance of the Alpaca API client that has been defined elsewhere
        request_params = StockBarsRequest(symbol_or_symbols=symbols, timeframe=_timeframe, start=start_date, end=end_date, limit=limit)
        loop = asyncio.get_running_loop()
        bars_data = await loop.run_in_executor(None, lambda: client.get_stock_bars(request_params))

        if not bars_data:
            return pd.DataFrame()

        df_list = []
        for symbol, bars in bars_data.items():  # Assuming bars_data is iterable and yields (symbol, bars) pairs
            data = {
                "open": [x["o"] for x in bars],
                "high": [x["h"] for x in bars],
                "low": [x["l"] for x in bars],
                "close": [x["c"] for x in bars],
                "volume": [x["v"] for x in bars],
                "time": [x["t"] for x in bars],
            }
            df = pd.DataFrame(data)
            df["time"] = pd.to_datetime(df["time"])
            df["timeframe"] = timeframe
            df["symbol"] = symbol
            df.insert(0, "dateTimeUtc", df["time"])
            df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5))
            df = df.set_index("time")
            df = df.sort_index()
            df_list.append(df)

        if df_list:
            df_final = pd.concat(df_list)
            return df_final
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"error: get_alpaca_stock_ohlcv_data {symbols}", e)
        return None


async def get_stock_bars(symbols, _timeframe, start_date, end_date, limit):
    request_params = StockBarsRequest(symbol_or_symbols=symbols, timeframe=_timeframe, start=start_date, end=end_date, limit=limit)

    # Use asyncio.to_thread() to run the blocking call in a separate thread
    stock_bars = await asyncio.to_thread(request_params.get)

    return stock_bars
