import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

import numpy as np
import pandas as pd
from pymongo import UpdateOne

from app._database.db_connect_client import database_mongodb_client
from app.models.signal_model import SignalModel

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")


async def update_signals_by_symbol_v1(
    coll_name=None, signals=None, nameId=None, nameVersion="1.0.0", use_old_signal=True, current_time_floor=None, backtest_mode=False, force_db_update=False
):
    if coll_name is None:
        raise Exception("baseCollection is None")

    try:
        if use_old_signal == False:
            await delete_old_signals_v1(nameId=nameId, nameVersion=nameVersion, collection=coll_name)

        collection = database_mongodb_client[f"{coll_name}"]

        updates = []

        data_list_8 = []
        for i in range(0, len(signals), 8):
            data_list_8.append(signals[i : i + 8])

        for i in range(0, len(data_list_8), 8):
            batch = data_list_8[i : i + 8]
            tasks = [
                get_signal_update_one_v1(
                    d,
                    nameId,
                    nameVersion,
                    coll_name,
                    use_old_signal=use_old_signal,
                    current_time_floor=current_time_floor,
                    backtest_mode=backtest_mode,
                    force_db_update=force_db_update,
                )
                for d in batch
            ]
            res = await asyncio.gather(*tasks)
            updates += res

        updates = [item for sublist in updates for item in sublist]
        print("updates", len(updates))

        for i in range(0, len(updates), 1000):
            r = await collection.bulk_write(updates[i : i + 1000])

        return True

    except Exception as e:
        print("ERROR update_signals_by_symbol", e)
        raise e


async def get_signal_update_one_v1(data, nameId, nameVersion, coll_name, use_old_signal=True, current_time_floor=None, backtest_mode=False, force_db_update=False):
    updates = []
    try:
        collection = database_mongodb_client[f"{coll_name}"]
        for item in data:
            symbol = item["symbol"]
            has_old_closed_signal = await collection.find_one(
                {
                    "nameId": nameId,
                    "nameVersion": nameVersion,
                    "symbol": symbol,
                    "isClosed": True,
                    "entryType": item["entryType"],
                    "entryDateTimeUtc": item["entryDateTimeUtc"],
                }
            )

            allow_db_update = False
            if item["entryDateTimeUtc"] >= current_time_floor and item["isNew"] == True:
                allow_db_update = True

            if item["isNew"] == False:
                allow_db_update = True

            if use_old_signal == False or backtest_mode == True:
                allow_db_update = True

            if (is_production != "True") and force_db_update == True:
                allow_db_update = True

            if has_old_closed_signal is None and allow_db_update == True:
                updates.append(
                    UpdateOne(
                        {
                            "entryDateTimeUtc": item["entryDateTimeUtc"],
                            "entryType": item["entryType"],
                            "nameId": nameId,
                            "nameVersion": nameVersion,
                            "symbol": symbol,
                        },
                        {
                            "$set": {
                                "entryDateTimeUtc": item["entryDateTimeUtc"],
                                "nameId": nameId,
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


async def get_active_signals_from_mongodb_v1(nameId: str, nameVersion: str, use_old_signal: bool = True, coll_name: str = "signalsCrypto"):
    try:
        collection = database_mongodb_client[coll_name]

        if use_old_signal == False:
            await delete_old_signals_v1(nameId=nameId, nameVersion=nameVersion, collection=coll_name)
            return []

        data = await collection.find({"isClosed": False, "nameId": nameId, "nameVersion": nameVersion}).to_list(length=None)
        if len(data) == 0:
            return []

        # delete _id if exists in one line
        data = [{k: v for k, v in d.items() if k != "_id"} for d in data]
        df = pd.DataFrame(data)
        df = df.sort_values(by=["entryDateTimeUtc"], ascending=False)
        df = df.reset_index(drop=True)
        df.replace([np.inf, -np.inf, np.nan], None, inplace=True)
        df["isNew"] = False

        datetime_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
        for col in datetime_columns:
            df[col] = df[col].where(df[col].notnull(), None)

        # column = ["symbol", "entryDateTimeUtc", "entryType", "tp1DateTimeUtc", "tp2DateTimeUtc", "tp3DateTimeUtc", "slDateTimeUtc"]
        # print(df[column])
        return df

    except Exception as e:
        print(f"Error get_current_active_signals_from_mongodb_v1: {e}")
        return []


async def delete_old_signals_v1(nameId: str, nameVersion: str, collection: str = "signalsCrypto"):
    try:
        print("delete_old_signals_v1", nameId, nameVersion, collection)
        collection = database_mongodb_client[collection]
        await collection.delete_many({"nameId": nameId, "nameVersion": nameVersion})
        return True

    except Exception as e:
        print(f"Error delete_old_signals_v1: {e}")
        return Exception(f"Error in pulling live signals: {e}")


async def update_signals_aggr_open_v1(
    nameId: str,
    nameLeverage: str,
    nameIsActive: bool,
    nameIsAdminOnly: bool,
    nameSort: int,
    nameVersion: str,
    nameType: str,
    nameTypeSubtitle: str,
    nameNotificationTitle: str,
    nameMarket: str,
    nameCollection: str,
    signals: list,
    results: list,
):
    try:
        collection_signal_aggr_open_v1 = database_mongodb_client["signalsAggrOpenV1"]
        await collection_signal_aggr_open_v1.update_one(
            {"nameId": nameId},
            {
                "$set": {
                    "nameId": nameId,
                    "nameLeverage": nameLeverage,
                    "nameIsActive": nameIsActive,
                    "nameIsAdminOnly": nameIsAdminOnly,
                    "nameMarket": nameMarket,
                    "nameSort": nameSort,
                    "nameVersion": nameVersion,
                    "nameType": nameType,
                    "nameCollection": nameCollection,
                    "nameTypeSubtitle": nameTypeSubtitle,
                    "nameNotificationTitle": nameNotificationTitle,
                    "nameLastUpdatedDateTime": datetime.utcnow(),
                    "signals": signals,
                    "results": results,
                }
            },
            upsert=True,
        )

        collection_app_controls_private = database_mongodb_client["appControlsPrivateV1"]
        await collection_app_controls_private.update_one(
            {"nameId": "appControlsPrivateV1"},
            {
                "$set": {
                    "nameId": "appControlsPrivateV1",
                    "signalsAggrOpenUpdatedDateTime": datetime.utcnow(),
                }
            },
            upsert=True,
        )

        return True

    except Exception as e:
        print("ERROR update_signals_aggr_open_v1", e)
        raise e


async def get_closed_signals_results_v1(coll_name: str = None, nameId: str = None, nameVersion: str = None):
    try:
        collection_signal_aggrs = database_mongodb_client[coll_name]

        date_ago_365 = datetime.utcnow() - timedelta(days=365)
        date_ago_180 = datetime.utcnow() - timedelta(days=180)
        date_ago_90 = datetime.utcnow() - timedelta(days=90)
        date_ago_30 = datetime.utcnow() - timedelta(days=30)
        date_ago_14 = datetime.utcnow() - timedelta(days=14)
        date_ago_7 = datetime.utcnow() - timedelta(days=7)

        date_ago_365_data = await collection_signal_aggrs.find(
            {
                "nameId": nameId,
                "nameVersion": nameVersion,
                "entryDateTimeUtc": {"$gte": date_ago_365},
                "$or": [
                    {"tp1DateTimeUtc": {"$ne": None}},
                    {"slDateTimeUtc": {"$ne": None}},
                ],
            }
        ).to_list(length=None)

        if len(date_ago_365_data) == 0:
            return []

        date_ago_180_data = [entry for entry in date_ago_365_data if entry["entryDateTimeUtc"] >= date_ago_180]
        date_ago_90_data = [entry for entry in date_ago_365_data if entry["entryDateTimeUtc"] >= date_ago_90]
        date_ago_30_data = [entry for entry in date_ago_365_data if entry["entryDateTimeUtc"] >= date_ago_30]
        date_ago_14_data = [entry for entry in date_ago_365_data if entry["entryDateTimeUtc"] >= date_ago_14]
        date_ago_7_data = [entry for entry in date_ago_365_data if entry["entryDateTimeUtc"] >= date_ago_7]

        results = [
            # {
            #     "days": 365,
            #     "sort": 1,
            #     "total": len(date_ago_365_data),
            #     "win": len([entry for entry in date_ago_365_data if entry["statusTrade"] == "win"]),
            #     "loss": len([entry for entry in date_ago_365_data if entry["statusTrade"] == "loss"]),
            #     "winRate": calculate_win_rate_v1(date_ago_365_data),
            # },
            # {
            #     "days": 180,
            #     "sort": 2,
            #     "total": len(date_ago_180_data),
            #     "win": len([entry for entry in date_ago_180_data if entry["statusTrade"] == "win"]),
            #     "loss": len([entry for entry in date_ago_180_data if entry["statusTrade"] == "loss"]),
            #     "winRate": calculate_win_rate_v1(date_ago_180_data),
            # },
            # {
            #     "days": 90,
            #     "sort": 3,
            #     "total": len(date_ago_90_data),
            #     "win": len([entry for entry in date_ago_90_data if entry["statusTrade"] == "win"]),
            #     "loss": len([entry for entry in date_ago_90_data if entry["statusTrade"] == "loss"]),
            #     "winRate": calculate_win_rate_v1(date_ago_90_data),
            # },
            {
                "days": 30,
                "sort": 2,
                "total": len(date_ago_30_data),
                "win": len([entry for entry in date_ago_30_data if entry["statusTrade"] == "win"]),
                "loss": len([entry for entry in date_ago_30_data if entry["statusTrade"] == "loss"]),
                "winRate": calculate_win_rate_v1(date_ago_30_data),
            },
            {
                "days": 14,
                "sort": 1,
                "total": len(date_ago_14_data),
                "win": len([entry for entry in date_ago_14_data if entry["statusTrade"] == "win"]),
                "loss": len([entry for entry in date_ago_14_data if entry["statusTrade"] == "loss"]),
                "winRate": calculate_win_rate_v1(date_ago_14_data),
            },
            # {
            #     "days": 7,
            #     "sort": 6,
            #     "total": len(date_ago_7_data),
            #     "win": len([entry for entry in date_ago_7_data if entry["statusTrade"] == "win"]),
            #     "loss": len([entry for entry in date_ago_7_data if entry["statusTrade"] == "loss"]),
            #     "winRate": calculate_win_rate_v1(date_ago_7_data),
            # },
        ]

        # sort by sort
        results = sorted(results, key=lambda x: x["sort"])

        return results

    except Exception as e:
        print(f"Error get_closed_signals_results_v1: {e}")
        return Exception(f"Error in pulling closed signals results: {e}")


def calculate_win_rate_v1(data) -> float:
    try:
        total = len(data)
        win = len([entry for entry in data if entry["statusTrade"] == "win"])
        # ensure total is not zero
        if total == 0:
            return 0
        else:
            return round(win / total, 4)

    except Exception as e:
        print(f"Error calculate_win_rate_v1: {e}")
        return Exception(f"Error in calculating win rate: {e}")
