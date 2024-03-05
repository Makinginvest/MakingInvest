import asyncio
import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import UpdateOne

from app.a_database_client.db_connect_client import database_mongodb_client
from app.models.signal_model import SignalModel, get_columns_signals

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


async def update_signals_by_symbol(baseCollection=None, data=None, name=None, nameVersion="1.0.0", useOldSignal=True, current_time_floor=None):
    if baseCollection is None:
        raise Exception("baseCollection is None")

    try:
        collection = database_mongodb_client[f"{baseCollection}"]

        updates = []

        data_list_8 = []
        for i in range(0, len(data), 8):
            data_list_8.append(data[i : i + 8])

        for i in range(0, len(data_list_8), 8):
            batch = data_list_8[i : i + 8]
            tasks = [get_signal_update_one(d, name, nameVersion, collection, useOldSignal=useOldSignal, current_time_floor=current_time_floor) for d in batch]
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


async def get_signal_update_one(data, name, nameVersion, collection, useOldSignal=True, current_time_floor=None):
    updates = []
    try:
        for item in data:
            symbol = item["symbol"]
            current_signal1Query = collection.find_one(
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

            current_signal = await current_signal1Query

            # -------------- NOTE FIX FOR ONLY ALLOW NEW SIGNALS TO BE ADDED ------------- #
            allow_db_update = False
            if (item["entryDateTimeUtc"] >= current_time_floor) and item["isNew"] == True:
                allow_db_update = True

            if (useOldSignal == False) or item["isNew"] == False:
                allow_db_update = True

            # print("current_signal", symbol, current_signal, item["isNew"], allow_db_update)

            if current_signal is None and allow_db_update == True:
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


async def get_current_live_signals_from_mongodb(name: str, nameVersion: str, useOldSignal: bool = True, signalsCollection: str = "signalsCrypto"):
    try:
        collection = database_mongodb_client[signalsCollection]

        if useOldSignal == False:
            res = await collection.delete_many({"name": name, "nameVersion": nameVersion, "isAlgo": True})

        data = await collection.find({"isClosed": False, "name": name, "nameVersion": nameVersion}).to_list(length=None)
        df = pd.DataFrame(data)
        # convert to SignalModel
        data = [SignalModel(**d) for d in data]
        data = [d.dict() for d in data]

        df = pd.DataFrame(data, columns=get_columns_signals)
        df = df.sort_values(by=["entryDateTimeUtc"], ascending=False)
        df = df.reset_index(drop=True)

        df["isNew"] = False

        return df

    except Exception as e:
        print(f"Error in pulling live signals: {e}")
        return []
