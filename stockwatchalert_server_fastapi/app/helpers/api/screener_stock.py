import asyncio
import re
import numpy as np

import pandas as pd
from pymongo import ReplaceOne, UpdateOne
from app.helpers._mongodb.a_mongodb_data import get_mongodb_data_historical
from app.helpers.signals.a_get_dataframes_indicators import get_symbols_local_by_market_v1
from app._database.db_connect_client import database_mongodb_client
from more_itertools import chunked

from app.utils.convert_bson_json import convert_bson_json


async def run_screener_stock():
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
        df_ratings = df_ratings[["symbol", "rating", "ratingRecommendation"]]
        df = df.merge(df_ratings, on="symbol", how="left")

        # get bulk profile
        df_profile = pd.read_csv("_project/data/fmp/profile_bulk.csv")
        # rename Symbol to symbol
        df_profile = df_profile.rename(columns={"Symbol": "symbol"})
        df_profile = df_profile[["symbol", "image", "exchangeShortName"]]
        df = df.merge(df_profile, on="symbol", how="left")

        # replace all NaN infinity values with None
        df = df.replace([np.inf, -np.inf, np.nan], None)

        collection = database_mongodb_client["screenerStocks"]
        # await collection.create_index([("symbol", 1)], unique=True)
        # await collection.create_index([("close", 1)], unique=False)
        # await collection.create_index([("volume", 1)], unique=False)
        # await collection.create_index([("close", 1), ("volume", 1)], unique=False)
        # await collection.create_index([("close", 1), ("volume", 1), ("ratingRecommendation", 1)], unique=False)

        batch = []
        for index, row in df.iterrows():
            r = ReplaceOne(
                {"symbol": row["symbol"]},
                {
                    "symbol": row["symbol"],
                    "dateTimeUtc": row["dateTimeUtc"],
                    "dateTimeEst": row["dateTimeEst"],
                    "close": row["close"],
                    "high": row["high"],
                    "low": row["low"],
                    "open": row["open"],
                    "volume": row["volume"],
                    "rating": row["rating"],
                    "ratingRecommendation": row["ratingRecommendation"],
                    "image": row["image"],
                    "exchangeShortName": row["exchangeShortName"],
                },
                upsert=True,
            )
            batch.append(r)

        for x in chunked(batch, 1000):
            await collection.bulk_write(x)

        return "done"

    except Exception as e:
        print(e)
        raise str(e)


async def get_screener_stocks(minClose: float = 0, maxClose: float = 1000000000, minVolume: float = 0):
    try:
        collection = database_mongodb_client["screenerStocks"]

        res = (
            await collection.find(
                {"close": {"$gte": minClose, "$lte": maxClose}, "volume": {"$gte": minVolume}},
                {"dateTimeEst": 0, "dateTimeUtc": 0, "high": 0, "low": 0, "open": 0, "_id": 0},
            )
            .limit(1000)
            .to_list(length=1000)
        )

        res = [convert_bson_json(r) for r in res]
        # if ratingRecommendation is '' replace with None
        for r in res:
            if r["ratingRecommendation"] == "":
                r["ratingRecommendation"] = None
        return {
            "count": len(res),
            "data": res,
        }

    except Exception as e:
        print(e)
        return {}
