import io
import os
import aiohttp
import pandas as pd
from app._database.db_connect_data import database_mongodb_data

import zipfile
from datetime import date, timedelta

from app.helpers._functions.get_symbols_local_v1 import get_symbols_by_value_v1


async def update_all_symbols_from_data_db_mongodb_aggr():
    try:
        collection = database_mongodb_data["symbols"]

        # Retrieve documents from MongoDB
        symbols_crypto = await collection.find_one({"type": "crypto"})
        symbols_crypto_futures = await collection.find_one({"type": "cryptoFutures"})
        symbols_forex = await collection.find_one({"type": "forex"})
        symbols_stocks = await collection.find_one({"type": "stocks"})

        # Remove the "_id" field from each document
        symbols_crypto.pop("_id", None)
        symbols_crypto_futures.pop("_id", None)
        symbols_forex.pop("_id", None)
        symbols_stocks.pop("_id", None)

        # Convert dictionary objects to pandas DataFrames
        df_crypto = pd.DataFrame(symbols_crypto["data"])
        df_crypto_futures = pd.DataFrame(symbols_crypto_futures["data"])
        df_forex = pd.DataFrame(symbols_forex["data"])
        df_stocks = pd.DataFrame(symbols_stocks["data"])

        # Save DataFrames to CSV files
        df_crypto.to_csv("_project/data/symbols/_data_symbols_crypto_usdt_busd.csv", index=False)
        df_crypto_futures.to_csv("_project/data/symbols/_data_symbols_crypto_usdt_busd_futures.csv", index=False)
        df_forex.to_csv("_project/data/symbols/_data_symbols_forex_oanda_main.csv", index=False)
        df_stocks.to_csv("_project/data/symbols/_data_symbols_stock_us_market.csv", index=False)

        return {
            "crypto": df_crypto,
            "forex": df_forex,
            "stocks": df_stocks,
        }

    except Exception as e:
        print(e)
        return {}


async def update_all_symbols_mongodb_aggr():
    try:
        symbols_crypto = await update_symbols_crypto_mongodb_aggr()
        symbols_forex = await update_symbols_forex_mongodb_aggr()
        symbols_stocks = await update_symbols_stocks_mongodb_aggr()

        return {
            "crypto": symbols_crypto,
            "forex": symbols_forex,
            "stocks": symbols_stocks,
        }

    except Exception as e:
        print(e)
        return {}


async def update_symbols_crypto_mongodb_aggr():
    try:
        symbols = await generate_binance_usdt_busd_csv()

        collection = database_mongodb_data["symbolsAggr"]

        await collection.update_one({"type": "crypto"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def update_symbols_forex_mongodb_aggr():
    try:
        symbols = pd.read_csv("_project/data/symbols/_data_symbols_forex_oanda_main.csv")
        symbols = symbols[["symbol"]]
        symbols["symbol"] = symbols["symbol"].apply(lambda x: x.replace("/", ""))

        collection = database_mongodb_data["symbolsAggr"]

        await collection.update_one({"type": "forex"}, {"$set": {"data": symbols.to_dict("records")}}, upsert=True)

        return symbols.to_dict("records")

    except Exception as e:
        print(e)
        return []


async def update_symbols_stocks_mongodb_aggr():
    try:
        symbols = pd.read_csv("_project/data/symbols/_data_symbols_stock_options_sp500.csv")
        collection = database_mongodb_data["symbolsAggr"]
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

            symbols_only = [
                symbol["s"].replace(
                    "USDT",
                    "",
                )
                for symbol in new_data
            ]

            for symbol in data:
                if symbol["s"].endswith("BUSD"):
                    if (
                        symbol["s"].replace(
                            "BUSD",
                            "",
                        )
                        not in symbols_only
                    ):
                        new_data.append(symbol)

            # remove BULLUSDT and BEARUSDT and DOWNUSDT and UPUSDT if sigbal contains them
            new_data = [symbol for symbol in new_data if "BULLUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BEARUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "DOWNUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "UPUSDT" not in symbol["s"]]

            symbols_to_delete = await get_symbols_crypto_binance_delete()
            new_data = [symbol for symbol in new_data if symbol["s"] not in symbols_to_delete]

            new_data = pd.DataFrame(new_data)
            new_data.rename(
                columns={"s": "symbol"},
                inplace=True,
            )
            new_data.to_csv(
                "_project/data/symbols/_data_symbols_crypto_usdt_busd.csv",
                index=False,
            )

            return new_data


async def get_binance_data_daily_spot_symbol_value(path="_project/data/symbols/_data_symbols_crypto_usdt_busd.csv"):
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    symbols = await get_symbols_by_value_v1(path)
    symbols = [s.replace("/", "") for s in symbols]
    # symbols = symbols[:10]
    file_paths = []

    try:
        async with aiohttp.ClientSession() as session:
            for i in range(
                0,
                len(symbols),
                5,
            ):
                symbol_batch = symbols[i : i + 5]
                for s in symbol_batch:
                    url = f"https://data.binance.vision/data/spot/daily/klines/{s}/1d/{s}-1d-{yesterday}.zip"
                    try:
                        async with session.get(url) as resp:
                            r = await resp.read()
                            z = zipfile.ZipFile(io.BytesIO(r))
                            z.extractall("_project/datasets/_temp/binance_raw")
                            file_paths.append(f"_project/datasets/_temp/binance_raw/{s}-1d-{yesterday}.csv")
                    except Exception as e:
                        pass
            await session.close()

        df = pd.DataFrame()
        for f in file_paths:
            symbol_name = f.split("/")[-1].split(".")[0].split("-")[0]
            new_df = pd.read_csv(
                f,
                header=None,
            )
            columns = [
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
            ]
            new_df.columns = columns
            new_df.drop(
                new_df.columns[6:],
                axis=1,
                inplace=True,
            )
            new_df["symbol"] = symbol_name

            df = pd.concat(
                [
                    df,
                    new_df,
                ],
                ignore_index=True,
            )

        df["value"] = df["volume"] * df["close"]
        df = df[
            [
                "symbol",
                "close",
                "volume",
                "value",
            ]
        ]
        df = df.sort_values(by=["value"], ascending=False)
        df.to_csv("_project/data/symbols/_data_symbols_crypto_usdt_busd.csv", index=False)

        for f in file_paths:
            os.remove(f)
        # return [symbol, value] as json

        df = df[
            [
                "symbol",
                "value",
            ]
        ]
        return df.to_dict("records")

    except Exception as e:
        raise e


async def generate_binance_future_usdt_busd_csv():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    async with aiohttp.ClientSession() as session:
        data = []
        async with session.get(url) as response:
            for symbol_info in (await response.json())["symbols"]:
                data.append({"s": symbol_info["symbol"]})

            data = [symbol for symbol in data if symbol["s"].endswith("USDT") or symbol["s"].endswith("BUSD")]
            new_data = []
            for symbol in data:
                if symbol["s"].endswith("USDT"):
                    new_data.append(symbol)

            symbols_only = [
                symbol["s"].replace(
                    "USDT",
                    "",
                )
                for symbol in new_data
            ]

            for symbol in data:
                if symbol["s"].endswith("BUSD"):
                    if (
                        symbol["s"].replace(
                            "BUSD",
                            "",
                        )
                        not in symbols_only
                    ):
                        new_data.append(symbol)

            # remove BULLUSDT and BEARUSDT and DOWNUSDT and UPUSDT if sigbal contains them
            new_data = [symbol for symbol in new_data if "BULLUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "BEARUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "DOWNUSDT" not in symbol["s"]]
            new_data = [symbol for symbol in new_data if "UPUSDT" not in symbol["s"]]

            symbols_to_delete = await get_symbols_crypto_binance_delete()
            new_data = [symbol for symbol in new_data if symbol["s"] not in symbols_to_delete]

            new_data = pd.DataFrame(new_data)
            new_data.rename(
                columns={"s": "symbol"},
                inplace=True,
            )
            new_data.to_csv(
                "_project/data/symbols/_data_symbols_crypto_usdt_busd_futures.csv",
                index=False,
            )

            return new_data


async def get_binance_data_daily_futures_symbol_value(path="_project/data/symbols/_data_symbols_crypto_usdt_busd_futures.csv"):
    yesterday = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    symbols = await get_symbols_by_value_v1(path)
    symbols = [s.replace("/", "") for s in symbols]
    # symbols = symbols[:10]
    file_paths = []

    try:
        async with aiohttp.ClientSession() as session:
            for i in range(
                0,
                len(symbols),
                5,
            ):
                symbol_batch = symbols[i : i + 5]
                for s in symbol_batch:
                    url = f"https://data.binance.vision/data/futures/um/daily/klines/{s}/1d/{s}-1d-{yesterday}.zip"

                    try:
                        async with session.get(url) as resp:
                            r = await resp.read()
                            z = zipfile.ZipFile(io.BytesIO(r))
                            z.extractall("_project/datasets/_temp/binance_raw")
                            file_paths.append(f"_project/datasets/_temp/binance_raw/{s}-1d-{yesterday}.csv")
                    except Exception as e:
                        print(
                            s,
                            e,
                            url,
                        )
            await session.close()

        df = pd.DataFrame()
        for f in file_paths:
            symbol_name = f.split("/")[-1].split(".")[0].split("-")[0]
            new_df = pd.read_csv(
                f,
                skiprows=1,
                header=None,
            )  # skipping the first row
            columns = [
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
            ]
            new_df.columns = columns
            new_df.drop(
                new_df.columns[6:],
                axis=1,
                inplace=True,
            )
            new_df["symbol"] = symbol_name

            df = pd.concat(
                [
                    df,
                    new_df,
                ],
                ignore_index=True,
            )

        # drop na
        df = df.dropna()
        # convert volumne and close to float
        df["volume"] = df["volume"].astype(float)
        df["close"] = df["close"].astype(float)
        df["value"] = df["volume"] * df["close"]
        df = df[
            [
                "symbol",
                "close",
                "volume",
                "value",
            ]
        ]
        df = df.sort_values(by=["value"], ascending=False)
        df.to_csv(path, index=False)

        for f in file_paths:
            os.remove(f)

        df = df[
            [
                "symbol",
                "value",
            ]
        ]
        return df.to_dict("records")

    except Exception as e:
        raise e


async def get_symbols_crypto_binance_delete():
    symbols = pd.read_csv("_project/data/symbols/_data_symbols_crypto_delete.csv")
    symbols = symbols["symbol"].tolist()

    symbols = [s.replace("/", "") for s in symbols]
    return symbols
