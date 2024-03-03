import datetime
import aiohttp
import pandas as pd
import ccxt.async_support as ccxt

exchange = ccxt.binance({"rateLimit": 0, "enableRateLimit": False})

import os
from dotenv import load_dotenv

load_dotenv()


def get_stock_symbols(path="_datasets/data/_data_symbols_stock_options_sp500.csv"):
    symbols_df = pd.read_csv(path)
    symbols = symbols_df["symbol"].str.replace("/", "")
    symbols = symbols.tolist()

    return symbols


async def get_ftm_stock_ohlcv_data(symbol=None, interval="15min", to_date=None, from_date=None):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    to_date = datetime.datetime.utcnow() if to_date is None else to_date
    to_date = to_date.replace(minute=to_date.minute - to_date.minute % 5, second=0, microsecond=0)
    from_date = datetime.datetime.utcnow() - datetime.timedelta(1) if from_date is None else from_date
    from_date = from_date.replace(minute=from_date.minute - from_date.minute % 5, second=0, microsecond=0)

    #  format to yyyy-mm-dd
    to_date = to_date.strftime("%Y-%m-%d")
    from_date = from_date.strftime("%Y-%m-%d")

    # from=2020-03-02&to=2020-04-02
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
