import asyncio
from datetime import datetime, timedelta
from app.models.signal_model import SignalModel
from app.a_database_client.db_connect_client import database_mongodb_client
from utils.chuck_dates_by_month import chuck_dates_by_month
from dateutil.relativedelta import relativedelta


async def get_closed_signals_results_summary(
    signalsCollection: str = None, name: str = None, nameVersion: str = None, startDate: datetime = None, endDate: datetime = None
):
    chuck_dates = chuck_dates_by_month(startDate, endDate)

    data = []
    task = []
    for chuck_date in chuck_dates:
        task.append(get_closed_signals_results_summary_by_month(signalsCollection, name, nameVersion, chuck_date["startDate"], chuck_date["endDate"]))
    results = await asyncio.gather(*task)

    full_date = await get_closed_signals_results_summary_by_month(signalsCollection, name, nameVersion, startDate, endDate)

    for result in results:
        data.append(result)

    # append to start of list
    data = [full_date] + data

    # delete where totalCount = 0
    data = [x for x in data if x["profitByLevel1"]["count"] > 0]

    return data


async def get_closed_signals_results_summary_by_month(
    signalsCollection: str = None, name: str = None, nameVersion: str = None, startDate: datetime = None, endDate: datetime = None
):
    try:
        collection = database_mongodb_client[signalsCollection]

        data_total_query = collection.aggregate(
            [
                {"$match": {"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": startDate, "$lte": endDate}}},
                {"$match": {"entryProfitPct": {"$ne": 0}}},
                {"$group": {"_id": "$symbol", "count": {"$sum": 1}, "entryProfitPct": {"$sum": "$entryProfitPct"}}},
                {"$group": {"_id": None, "totalCount": {"$sum": "$count"}, "totalEntryProfitPct": {"$sum": "$entryProfitPct"}}},
            ]
        ).to_list(length=None)

        data_winners_query_level1 = collection.aggregate(
            [
                {"$match": {"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": startDate, "$lte": endDate}}},
                {"$match": {"entryProfitLevel": {"$gte": 1}}},
                {"$group": {"_id": None, "totalCount": {"$sum": 1}, "totalEntryProfitPct": {"$sum": "$entryProfitLevel"}}},
            ]
        ).to_list(length=None)

        data_winners_query_level2 = collection.aggregate(
            [
                {"$match": {"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": startDate, "$lte": endDate}}},
                {"$match": {"entryProfitLevel": {"$gte": 2}}},
                {"$group": {"_id": None, "totalCount": {"$sum": 1}, "totalEntryProfitPct": {"$sum": "$entryProfitLevel"}}},
            ]
        ).to_list(length=None)

        data_winners_query_level3 = collection.aggregate(
            [
                {"$match": {"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": startDate, "$lte": endDate}}},
                {"$match": {"entryProfitLevel": {"$gte": 3}}},
                {"$group": {"_id": None, "totalCount": {"$sum": 1}, "totalEntryProfitPct": {"$sum": "$entryProfitLevel"}}},
            ]
        ).to_list(length=None)

        data_winners_query_level4 = collection.aggregate(
            [
                {"$match": {"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": startDate, "$lte": endDate}}},
                {"$match": {"entryProfitLevel": {"$gte": 4}}},
                {"$group": {"_id": None, "totalCount": {"$sum": 1}, "totalEntryProfitPct": {"$sum": "$entryProfitLevel"}}},
            ]
        ).to_list(length=None)

        tasks = [data_total_query, data_winners_query_level1, data_winners_query_level2, data_winners_query_level3, data_winners_query_level4]
        data_total, data_winners1, data_winners2, data_winners3, data_winners4 = await asyncio.gather(*tasks)

        total_count = 0
        total_entry_profit_pct = 0

        total_winners_count1 = 0
        total_winrate1 = 0
        ave_per_trade1 = 0

        total_winners_count2 = 0
        total_winrate2 = 0
        ave_per_trade2 = 0

        total_winners_count3 = 0
        total_winrate3 = 0
        ave_per_trade3 = 0

        total_winners_count4 = 0
        total_winrate4 = 0
        ave_per_trade4 = 0

        if len(data_total) > 0:
            total_count = data_total[0].get("totalCount", 0)
            total_entry_profit_pct = data_total[0].get("totalEntryProfitPct", 0)

        if len(data_winners1) > 0:
            total_winners_count1 = data_winners1[0].get("totalCount", 0)
        if total_count > 0:
            ave_per_trade1 = total_entry_profit_pct / total_count if total_count > 0 else 0
        if total_winners_count1 > 0:
            total_winrate1 = total_winners_count1 / total_count if total_count > 0 else 0

        if len(data_winners2) > 0:
            total_winners_count2 = data_winners2[0].get("totalCount", 0)
        if total_count > 0:
            ave_per_trade2 = total_entry_profit_pct / total_count if total_count > 0 else 0
        if total_winners_count2 > 0:
            total_winrate2 = total_winners_count2 / total_count if total_count > 0 else 0

        if len(data_winners3) > 0:
            total_winners_count3 = data_winners3[0].get("totalCount", 0)
        if total_count > 0:
            ave_per_trade3 = total_entry_profit_pct / total_count if total_count > 0 else 0
        if total_winners_count3 > 0:
            total_winrate3 = total_winners_count3 / total_count if total_count > 0 else 0

        if len(data_winners4) > 0:
            total_winners_count4 = data_winners4[0].get("totalCount", 0)
        if total_count > 0:
            ave_per_trade4 = total_entry_profit_pct / total_count if total_count > 0 else 0
        if total_winners_count4 > 0:
            total_winrate4 = total_winners_count4 / total_count if total_count > 0 else 0

        data = {
            "startDate": startDate,
            "endDate": endDate,
            "profitByLevel1": {
                "count": total_count,
                "winnersCount": total_winners_count1,
                "winrate": total_winrate1,
                "avePerTrade": ave_per_trade1,
            },
            "profitByLevel2": {
                "count": total_count,
                "winnersCount": total_winners_count2,
                "winrate": total_winrate2,
                "avePerTrade": ave_per_trade2,
            },
            "profitByLevel3": {
                "count": total_count,
                "winnersCount": total_winners_count3,
                "winrate": total_winrate3,
                "avePerTrade": ave_per_trade3,
            },
            "profitByLevel4": {
                "count": total_count,
                "winnersCount": total_winners_count4,
                "winrate": total_winrate4,
                "avePerTrade": ave_per_trade4,
            },
        }

        return data

    except Exception as e:
        raise e
