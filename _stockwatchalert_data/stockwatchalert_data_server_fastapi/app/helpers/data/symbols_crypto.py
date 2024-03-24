import io
import os
import zipfile
from datetime import date, timedelta
from pandas import Timestamp

import aiohttp
import pandas as pd
import requests

from app._database_data.db_connect_data import database_mongodb_data
from app.helpers._functions_mongodb.crypto_functions import get_USDT_symbols_by_value
from app.helpers._functions_mongodb.crypto_mongodb_update import crypto_update_all_mongodb_historical_recent


async def update_all_symbols_mongodb_aggr():
    try:
        symbols_crypto = await update_symbols_crypto_mongodb_aggr()
        symbols_crypto_futures = await update_symbols_crypto_futures_mongodb_aggr()
        symbols_forex = await update_symbols_forex_mongodb_aggr()
        symbols_stocks = await update_symbols_stocks_mongodb_aggr()

        return {"crypto": symbols_crypto, "cryptoFutures": symbols_crypto_futures, "forex": symbols_forex, "stocks": symbols_stocks}

    except Exception as e:
        print(e)
        return {}


async def update_symbols_crypto_mongodb_aggr():
    try:
        symbols = await generate_binance_usdt_busd_csv()
        # keep only symbol columns
        symbols = symbols[["symbol"]]
        collection = database_mongodb_data["symbols"]

        await collection.update_one({"type": "crypto"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def update_symbols_crypto_futures_mongodb_aggr():
    try:
        symbols = await generate_binance_usdt_busd_futures_csv()
        # keep only symbol columns
        symbols = symbols[["symbol"]]
        collection = database_mongodb_data["symbols"]

        await collection.update_one({"type": "cryptoFutures"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def update_symbols_forex_mongodb_aggr():
    try:
        symbols = pd.read_csv("_project/datasets/data/_data_symbols_forex_oanda_main.csv")
        symbols = symbols[["symbol"]]
        symbols["symbol"] = symbols["symbol"].apply(lambda x: x.replace("/", ""))

        collection = database_mongodb_data["symbols"]

        await collection.update_one({"type": "forex"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def update_symbols_stocks_mongodb_aggr():
    try:
        await fetch_stocks_to_csv()
        symbols = pd.read_csv("_project/datasets/data/_data_symbols_stock_us_market.csv")
        collection = database_mongodb_data["symbols"]
        await collection.update_one({"type": "stocks"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def generate_binance_usdt_busd_csv():
    url = "https://api.binance.com/api/v3/ticker/price"

    async with aiohttp.ClientSession() as session:
        data = []
        async with session.get(url) as response:
            for symbol_info in await response.json():
                data.append({"s": symbol_info["symbol"]})

            data = [symbol for symbol in data if symbol["s"].endswith("USDT") or symbol["s"].endswith("BUSD")]
            new_data = []
            for symbol in data:
                if symbol["s"].endswith("USDT"):
                    new_data.append(symbol)

            symbols_only = [symbol["s"].replace("USDT", "") for symbol in new_data]

            for symbol in data:
                if symbol["s"].endswith("BUSD"):
                    if symbol["s"].replace("BUSD", "") not in symbols_only:
                        new_data.append(symbol)

            # remove BULLUSDT and BEARUSDT and DOWNUSDT and UPUSDT if sigbal contains them
            new_data = [symbol for symbol in new_data if "BULLUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BEARUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "DOWNUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "UPUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BUSD" not in symbol["s"]]

            symbols_to_delete = await get_symbols_crypto_binance_delete()
            new_data = [symbol for symbol in new_data if symbol["s"] not in symbols_to_delete]

            new_data = pd.DataFrame(new_data)
            new_data.rename(columns={"s": "symbol"}, inplace=True)
            new_data.to_csv("_project/datasets/data/_data_symbols_crypto_usdt_busd.csv", index=False)

            df_all = await crypto_update_all_mongodb_historical_recent(timeframe="15m", path="_project/datasets/data/_data_symbols_crypto_usdt_busd.csv")
            df_all = df_all.sort_values(by=["dateTimeUtc", "symbol"], ascending=False)
            df_all = df_all.drop_duplicates(subset=["symbol"], keep="first")
            df_all = df_all[df_all["dateTimeUtc"] > Timestamp.now() - pd.Timedelta(days=1)]
            columns = ["symbol", "close", "dateTimeUtc", "dateTimeEst"]

            df_all = df_all[columns]
            df_all.to_csv("_project/datasets/data/_data_symbols_crypto_usdt_busd.csv", index=False)

            return df_all


async def generate_binance_usdt_busd_futures_csv():
    # Using the Binance futures endpoint
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    async with aiohttp.ClientSession() as session:
        data = []
        async with session.get(url) as response:
            for symbol_info in await response.json():
                data.append({"s": symbol_info["symbol"]})

            data = [symbol for symbol in data if symbol["s"].endswith("USDT") or symbol["s"].endswith("BUSD")]
            new_data = []
            for symbol in data:
                if symbol["s"].endswith("USDT"):
                    new_data.append(symbol)

            symbols_only = [symbol["s"].replace("USDT", "") for symbol in new_data]

            for symbol in data:
                if symbol["s"].endswith("BUSD"):
                    if symbol["s"].replace("BUSD", "") not in symbols_only:
                        new_data.append(symbol)

            # remove BULLUSDT and BEARUSDT and DOWNUSDT and UPUSDT if symbol contains them
            new_data = [symbol for symbol in new_data if "BULLUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BEARUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "DOWNUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "UPUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BUSD" not in symbol["s"]]

            symbols_to_delete = await get_symbols_crypto_binance_delete()
            new_data = [symbol for symbol in new_data if symbol["s"] not in symbols_to_delete]

            new_data = pd.DataFrame(new_data)
            new_data.rename(columns={"s": "symbol"}, inplace=True)
            new_data.to_csv("_project/datasets/data/_data_symbols_crypto_usdt_busd_futures.csv", index=False)

            df_all = await crypto_update_all_mongodb_historical_recent(timeframe="15m", path="_project/datasets/data/_data_symbols_crypto_usdt_busd_futures.csv")

            df_all = df_all.sort_values(by=["dateTimeUtc", "symbol"], ascending=False)
            df_all = df_all.drop_duplicates(subset=["symbol"], keep="first")
            df_all = df_all[df_all["dateTimeUtc"] > Timestamp.now() - pd.Timedelta(days=1)]
            columns = ["symbol", "close", "dateTimeUtc", "dateTimeEst"]

            df_all = df_all[columns]
            df_all.to_csv("_project/datasets/data/_data_symbols_crypto_usdt_busd_futures.csv", index=False)

            return df_all


async def get_binance_data_daily_symbol_value():
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    symbols = await get_USDT_symbols_by_value("_project/datasets/data/_data_symbols_crypto_usdt_busd.csv")
    symbols = [s.replace("/", "") for s in symbols]
    # symbols = symbols[:10]
    file_paths = []

    try:
        async with aiohttp.ClientSession() as session:
            for i in range(0, len(symbols), 5):
                symbol_batch = symbols[i : i + 5]
                for s in symbol_batch:
                    url = f"https://data.binance.vision/data/spot/daily/klines/{s}/1d/{s}-1d-{yesterday}.zip"
                    try:
                        async with session.get(url) as resp:
                            r = await resp.read()
                            z = zipfile.ZipFile(io.BytesIO(r))
                            z.extractall("_project/datasets/binance/_temp/binance_raw")
                            file_paths.append(f"_project/datasets/binance/_temp/binance_raw/{s}-1d-{yesterday}.csv")
                    except Exception as e:
                        pass
            await session.close()

        df = pd.DataFrame()
        for f in file_paths:
            symbol_name = f.split("/")[-1].split(".")[0].split("-")[0]
            new_df = pd.read_csv(f, header=None)
            columns = ["time", "open", "high", "low", "close", "volume", "1", "2", "3", "4", "5", "6"]
            new_df.columns = columns
            new_df.drop(new_df.columns[6:], axis=1, inplace=True)
            new_df["symbol"] = symbol_name

            df = pd.concat([df, new_df], ignore_index=True)
        df["value"] = df["volume"] * df["close"]
        df = df[["symbol", "close", "volume", "value"]]
        df = df.sort_values(by=["value"], ascending=False)
        df.to_csv("_project/datasets/data/_data_symbols_crypto_usdt_busd.csv", index=False)

        for f in file_paths:
            os.remove(f)
        # return [symbol, value] as json

        df = df[["symbol", "value"]]
        return df.to_dict("records")

    except Exception as e:
        raise e


async def get_symbols_crypto_binance_delete():
    symbols = pd.read_csv("_project/datasets/data/_data_symbols_crypto_delete.csv")
    symbols = symbols["symbol"].tolist()

    symbols = [s.replace("/", "") for s in symbols]
    return symbols


async def fetch_stocks_to_csv():
    """
    Fetch stock list from the Alpaca API, filter for stocks under $100, and write to a CSV file.

    Parameters:
    - api_url: URL of the Alpaca API endpoint to fetch stock data.
    - headers: Headers required for authentication with the Alpaca API.
    - csv_filename: The name of the CSV file to write to.
    """
    api_url = "https://paper-api.alpaca.markets/v2/assets?status=active&exchange=NYSE%2CNASDAQ&attributes="
    headers = {"APCA-API-KEY-ID": "PKP54IQSJ4CAPG89OJ70", "APCA-API-SECRET-KEY": "WyaK46LT5OL7pFm6o5ScJelU6nGhAdPExJqtkujo", "accept": "application/json"}
    csv_filename = "_project/datasets/data/_data_symbols_stock_us_market.csv"

    # Fetch the data
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Convert JSON response to pandas DataFrame
        df = pd.DataFrame(response.json())
        # Filter for stocks from NASDAQ, NYSE, AMEX, and CBOE exchanges
        keep_exchanges = ["NASDAQ", "NYSE", "AMEX", "CBOE"]
        df = df[df["exchange"].isin(keep_exchanges)]

        # Filter for assets of type "stock"
        # df = df[df["asset_class"] == "us_equity"]
        df = df[df["tradable"] == True]
        # remove where symbol containers "."
        # print(df["symbol"])
        df = df[~df["symbol"].str.contains(".", regex=False)]
        df = df[~df["symbol"].str.contains("-", regex=False)]
        df = df[~df["name"].str.contains("ETF", regex=False)]
        df = df[~df["name"].str.contains("%", regex=False)]

        columns = ["exchange", "symbol", "name", "status", "tradable"]

        # Write to CSV
        df[columns].to_csv(csv_filename, index=False)

        print("Successfully fetched data from alpaca API.")
    else:
        print("Failed to fetch data")


# Alpaca API endpoint

# Fetch stock data and write to CSV
