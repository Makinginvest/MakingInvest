import asyncio
import os
import re
import pandas as pd
from app._database_data.db_connect_data import database_mongodb_data
from pymongo import InsertOne, ReplaceOne, UpdateOne
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


async def get_mongodb_historical(symbol, histCollection=None, timeframe="15m", limit=20000, datetime_start: datetime = None) -> pd.DataFrame:
    if histCollection is None:
        raise Exception("baseCollection is None")

    try:
        historical_crypto = database_mongodb_data[f"{histCollection}{timeframe}"]
        data = []

        if datetime_start == None:
            data = await historical_crypto.find({"symbol": symbol, "timeframe": timeframe}).sort("dateTimeUtc", -1).limit(limit).to_list(length=limit)

        if datetime_start != None:
            data = (
                await historical_crypto.find({"symbol": symbol, "timeframe": timeframe, "dateTimeUtc": {"$gte": datetime_start}}).sort("dateTimeUtc", -1).to_list(length=None)
            )

        data = [{k: v for k, v in item.items() if k != "_id"} for item in data]
        df = pd.DataFrame(data)

        if df.empty:
            return None

        df["time"] = pd.to_datetime(df["dateTimeUtc"])
        df = df.sort_values(by="time")
        df = df.set_index("time")

        return df

    except Exception as e:
        print(e)
        return None


async def update_mongodb_data_by_symbol(data, baseCollection=None, timeframe="15m", batch_size=100000, use_replace_one=True):
    if baseCollection is None:
        raise Exception("baseCollection is None")

    try:
        collection_historical_crypto_by_timeframe = database_mongodb_data[f"{baseCollection}{timeframe}"]
        total_items = len(data)
        print(f"Updating {total_items} items to {baseCollection}{timeframe}...")

        for i in range(0, total_items, batch_size):
            batch = data[i : i + batch_size]

            if use_replace_one:
                operations = [
                    ReplaceOne(
                        filter={
                            "symbol": item["symbol"],
                            "dateTimeUtc": item["dateTimeUtc"],
                            "timeframe": timeframe,
                        },
                        replacement={
                            "open": item["open"],
                            "high": item["high"],
                            "low": item["low"],
                            "close": item["close"],
                            "volume": item["volume"],
                            "dateTimeUtc": item["dateTimeUtc"],
                            "dateTimeEst": item["dateTimeEst"],
                            "symbol": item["symbol"],
                            "timeframe": timeframe,
                        },
                        upsert=True,
                    )
                    for item in batch
                ]
            else:
                operations = [
                    InsertOne(
                        {
                            "open": item["open"],
                            "high": item["high"],
                            "low": item["low"],
                            "close": item["close"],
                            "volume": item["volume"],
                            "dateTimeUtc": item["dateTimeUtc"],
                            "dateTimeEst": item["dateTimeEst"],
                            "symbol": item["symbol"],
                            "timeframe": timeframe,
                        }
                    )
                    for item in batch
                ]

            result = None
            try:
                result = await collection_historical_crypto_by_timeframe.bulk_write(operations, ordered=False)
            except Exception as e:
                # if error is broken pipe, then try again
                if ("broken pipe" in str(e)) or ("connection reset by peer" in str(e)) or ("Broken pipe" in str(e)):
                    print("Trying broken pipe", e) if is_production != "True" else None
                    await asyncio.sleep(15)
                    result = await collection_historical_crypto_by_timeframe.bulk_write(operations, ordered=False)
                    print("Broken pipe fixed") if is_production != "True" else None
                if "duplicate key error" not in str(e):
                    pass
            if result and is_production != "True":
                inserted_count = result.inserted_count
                modified_count = result.modified_count
                upserted_count = result.upserted_count
                print(f"inserted_count: {inserted_count}")
                print(f"modified_count: {modified_count}")
                print(f"upserted_count: {upserted_count}")

        return {"status": "done"}

    except Exception as e:
        # if the error is a duplicate key error, then just ignore it
        if "duplicate key error" not in str(e):
            print("update_mongodb_data_by_symbol2", e)


async def update_signals_by_symbol(
    baseCollection=None,
    data=None,
    name=None,
    nameVersion="1.0.0",
):
    if baseCollection is None:
        raise Exception("baseCollection is None")

    # if is_production != "True":
    #     collection = database_mongodb[f"{baseCollection}"]
    #     await collection.create_index([("entryDateTimeUtc", -1)], unique=False)
    #     await collection.create_index([("entryDateTimeUtc", 1)], unique=False)
    #     await collection.create_index([("isAlgo", 1)], unique=False)
    #     await collection.create_index([("name", 1)], unique=False)
    #     await collection.create_index([("nameVersion", 1)], unique=False)
    #     await collection.create_index([("symbol", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("entryDateTimeUtc", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("entryDateTimeUtc", -1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", -1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", 1), ("entryType", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isAlgo", 1), ("symbol", 1), ("isClosed", -1), ("entryType", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isClosed", 1)], unique=False)
    #     await collection.create_index([("name", 1), ("nameVersion", 1), ("isClosed", -1)], unique=False)
    #     return False

    try:
        collection = database_mongodb_data[f"{baseCollection}"]

        updates = []

        data_list_8 = []
        for i in range(0, len(data), 8):
            data_list_8.append(data[i : i + 8])

        for i in range(0, len(data_list_8), 8):
            batch = data_list_8[i : i + 8]
            tasks = [get_signal_update_one(d, name, nameVersion, collection) for d in batch]
            res = await asyncio.gather(*tasks)
            updates += res

        updates = [item for sublist in updates for item in sublist]
        print("updates", len(updates))

        for i in range(0, len(updates), 1000):
            await collection.bulk_write(updates[i : i + 1000])

        return True

    except Exception as e:
        print("ERROR update_signals_by_symbol", e)
        raise e


async def get_signal_update_one(data, name, nameVersion, collection):
    updates = []
    try:
        for item in data:
            symbol = item["symbol"]
            current_signal = await collection.find_one(
                {
                    "name": name,
                    "nameVersion": nameVersion,
                    "isAlgo": True,
                    "symbol": symbol,
                    "isClosed": True,
                    "entryType": item["entryType"],
                    "entryDateTimeUtc": item["entryDateTimeUtc"],
                }
            )
            if current_signal is None:
                updates.append(
                    UpdateOne(
                        {
                            "entryDateTimeUtc": item["entryDateTimeUtc"],
                            "isAlgo": item["isAlgo"],
                            "name": name,
                            "nameVersion": nameVersion,
                            "symbol": symbol,
                            "entryType": item["entryType"],
                        },
                        {
                            "$set": {
                                "entryDateTimeUtc": item["entryDateTimeUtc"],
                                "isAlgo": item["isAlgo"],
                                "name": name,
                                "nameVersion": nameVersion,
                                "symbol": symbol,
                                **item,
                            }
                        },
                        upsert=True,
                    )
                )

        return updates

    except Exception as e:
        print("get_signal_update_one", e)
        return updates
