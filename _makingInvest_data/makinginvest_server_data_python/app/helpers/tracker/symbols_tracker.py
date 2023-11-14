import asyncio
import datetime
from fastapi import HTTPException

import pandas as pd
from app.helpers.a_functions_mongodb.a_mongodb_data import get_mongodb_data_historical
from app.helpers.a_functions.crypto__functions import get_USDT_symbols_by_value
from app.a_database_data.db_connect_data import database_mongodb_data
from app.a_database_data.db_connect_data import database_mongodb_data


async def update_symbol_tracker_all():
    try:
        crypto = await get_symbols_trackers_crypto()
        stocks = await get_symbols_trackers_stocks()
        forex = await get_symbols_trackers_forex()

        data = {
            "crypto": crypto.to_dict("records"),
            "stocks": stocks.to_dict("records"),
            "forex": forex.to_dict("records"),
            "name": "symbolsTracker",
            "lastUpdatedDateTime": datetime.datetime.utcnow(),
            "dtUpdated": datetime.datetime.utcnow(),
        }

        collection = database_mongodb_data["symbolsTracker"]
        await collection.update_one({"name": "symbolsTracker"}, {"$set": {**data}}, upsert=True)

        return data

    except Exception as e:
        print(e)
        return None


async def get_symbol_tracker_all():
    try:
        collection = database_mongodb_data["symbolsTracker"]
        data = await collection.find_one({"name": "symbolsTracker"})

        if data:
            data.pop("_id")
            return data

        HTTPException(400, detail="No data found")

    except Exception as e:
        print(e)
        raise HTTPException(400, detail=e)


async def get_symbols_trackers_stocks():
    try:
        # get symbols
        symbols = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_stock_options_sp500.csv")
        symbols = symbols[:200]

        df = pd.DataFrame()

        # run in chunk of 8
        for i in range(0, len(symbols), 8):
            symbols_chunks = symbols[i : i + 8]
            tasks = [get_symbol_tracker(symbol, "historicalStocks", "stocks") for symbol in symbols_chunks]
            res = await asyncio.gather(*tasks)

            for d in res:
                df = df.append(d, ignore_index=True)

        return df

    except Exception as e:
        print(e)
        return None


async def get_symbols_trackers_forex():
    try:
        # get symbols
        symbols = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_forex_oanda_main.csv")
        symbols = symbols[:200]
        # symbols = ["EURUSD"]

        df = pd.DataFrame()

        # get symbols trackers
        # run in chunk of 8
        for i in range(0, len(symbols), 8):
            symbols_chunks = symbols[i : i + 8]
            tasks = [get_symbol_tracker(symbol, "historicalForex", "forex") for symbol in symbols_chunks]
            res = await asyncio.gather(*tasks)

            for d in res:
                df = df.append(d, ignore_index=True)

        return df

    except Exception as e:
        print(e)
        return None


async def get_symbols_trackers_crypto():
    try:
        # get symbols
        symbols = await get_USDT_symbols_by_value("_datasets/data/_data_symbols_crypto_usdt_busd.csv")
        df = pd.DataFrame()

        # run in chunk of 8
        for i in range(0, len(symbols), 8):
            symbols_chunks = symbols[i : i + 8]
            tasks = [get_symbol_tracker(symbol, "historicalCrypto", "crypto") for symbol in symbols_chunks]
            res = await asyncio.gather(*tasks)

            for d in res:
                df = df.append(d, ignore_index=True)
        return df

    except Exception as e:
        print(e)
        return None


async def get_symbol_tracker(symbol: str, collection: str, market: str = "crypto"):
    try:
        # get symbol tracker
        start_date = datetime.datetime.now() - datetime.timedelta(days=10)
        df = await get_mongodb_data_historical(symbol, histCollection=collection, timeframe="1h", datetime_start=start_date)

        if df is None:
            return pd.DataFrame()

        val_1hr_ago = df["close"].iloc[-2] if len(df) > 1 else None
        val_2hr_ago = df["close"].iloc[-3] if len(df) > 2 else None
        val_4hr_ago = df["close"].iloc[-5] if len(df) > 4 else None
        val_8hr_ago = df["close"].iloc[-9] if len(df) > 8 else None
        val_24hr_ago = df["close"].iloc[-25] if len(df) > 24 else None
        val_7d_ago = df["close"].iloc[-169] if len(df) > 168 else None

        data = {
            "symbol": symbol,
            "val1hrAgo": val_1hr_ago,
            "val2hrAgo": val_2hr_ago,
            "val4hrAgo": val_4hr_ago,
            "val8hrAgo": val_8hr_ago,
            "val24hrAgo": val_24hr_ago,
            "val7dAgo": val_7d_ago,
            "market": market,
        }

        return pd.DataFrame(data, index=[0])

    except Exception as e:
        print("Error get_symbol_tracker: ", e)
        return pd.DataFrame()
