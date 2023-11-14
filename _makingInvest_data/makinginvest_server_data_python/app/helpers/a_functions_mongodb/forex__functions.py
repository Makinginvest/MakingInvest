import datetime
import aiohttp
import pandas as pd
import ccxt.async_support as ccxt

exchange = ccxt.binance({"rateLimit": 0, "enableRateLimit": False})

import os
from dotenv import load_dotenv

load_dotenv()


def get_forex_symbols_oanda(path="data/_data_symbols_forex_oanda.csv"):
    symbols_df = pd.read_csv(path)
    symbols = symbols_df["symbol"].str.replace("/", "_")
    symbols = symbols.tolist()

    return symbols


#
async def get_onada_forex_ohlcv_data(symbol=None, granularity="M5", from_date=None, to_date=None):
    api_key = os.getenv("OANDA_APIKEY")

    to_date = datetime.datetime.utcnow() if to_date is None else to_date
    to_date = to_date.replace(minute=to_date.minute - to_date.minute % 5, second=0, microsecond=0)
    from_date = datetime.datetime.utcnow() - datetime.timedelta(3) if from_date is None else from_date
    from_date = from_date.replace(minute=from_date.minute - from_date.minute % 5, second=0, microsecond=0)

    to_date = to_date.strftime("%Y-%m-%dT%H:%M:%S") + ".000000000Z"
    from_date = from_date.strftime("%Y-%m-%dT%H:%M:%S") + ".000000000Z"

    url = f"https://api-fxtrade.oanda.com/v3/instruments/{symbol}/candles?price=M&from={from_date}&to={to_date}&granularity={granularity}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Authorization": f"Bearer {api_key}"}) as response:
                data = await response.json()

                if "candles" not in data:
                    print(data)
                    return None

                data = data["candles"]
                # print(data)
                data = {
                    "open": [x["mid"]["o"] for x in data],
                    "high": [x["mid"]["h"] for x in data],
                    "low": [x["mid"]["l"] for x in data],
                    "close": [x["mid"]["c"] for x in data],
                    "volume": [x["volume"] for x in data],
                    "time": [x["time"] for x in data],
                }
                df = pd.DataFrame(data)
                # remove utc timezone
                df["time"] = df["time"].str.replace("Z", "")
                df["time"] = pd.to_datetime(df["time"])
                df.insert(0, "dateTimeUtc", df["time"])
                df.insert(1, "dateTimeEst", df["time"] - pd.Timedelta(hours=5)),
                df = df.set_index("time")
                df = df.sort_index()

                return df
    except Exception as e:
        print(f"Error pulling data oanda: {symbol}", e)
        return None
