import asyncio
import re

import pandas as pd
from pymongo import UpdateOne
from app.helpers._mongodb.a_mongodb_data import get_mongodb_data_historical
from app.helpers.signals.a_get_dataframes_indicators import get_symbols_local_by_market_v1
from app._database.db_connect_client import database_mongodb_client
from more_itertools import chunked

from app.utils.convert_bson_json import convert_bson_json


async def run_ratings_stock():
    try:
        df = pd.DataFrame()
        symbols = await get_symbols_local_by_market_v1(market="stocks")
        # symbols = symbols[:10]
        tasks = [get_mongodb_data_historical(symbol, hist_coll_name="historicalStocks", timeframe="1d", limit=1) for symbol in symbols]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result is not None:
                df = pd.concat([df, result])

        # get rating df
        df_ratings = pd.read_csv("_project/data/fmp/ratings.csv")

        collection = database_mongodb_client["ratingsStocks"]
        # await collection.create_index([("symbol", 1)], unique=True)
        # await collection.create_index([("close", 1)], unique=False)
        # await collection.create_index([("volume", 1)], unique=False)
        # await collection.create_index([("close", 1), ("volume", 1)], unique=False)

        batch = []
        for index, row in df.iterrows():
            r = UpdateOne(
                {"symbol": row["symbol"]},
                {
                    "$set": {
                        "dateTimeUtc": row["dateTimeUtc"],
                        "dateTimeEst": row["dateTimeEst"],
                        "close": row["close"],
                        "high": row["high"],
                        "low": row["low"],
                        "open": row["open"],
                        "volume": row["volume"],
                    }
                },
                upsert=True,
            )
            batch.append(r)

        for x in chunked(batch, 1000):
            await collection.bulk_write(x)

        return "done"

    except Exception as e:
        print(e)
        return {}


async def get_screener_stocks(minClose: float = 0, maxClose: float = 1000000000, volume: float = 0):
    try:
        collection = database_mongodb_client["screenerStocks"]

        res = (
            await collection.find(
                {"close": {"$gte": minClose, "$lte": maxClose}, "volume": {"$gte": volume}},
                {"dateTimeEst": 0, "dateTimeUtc": 0, "high": 0, "low": 0, "open": 0, "_id": 0},
            )
            .limit(1000)
            .to_list(length=1000)
        )

        res = [convert_bson_json(r) for r in res]
        return {
            "count": len(res),
            "data": res,
        }

    except Exception as e:
        print(e)
        return {}
