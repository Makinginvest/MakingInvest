import os
import numpy as np
import pandas as pd
from app.a_database_client.db_connect_client import database_mongodb_client
from app.a_firebase.firebase import firestore_db
from datetime import datetime, timedelta
from firebase_admin import firestore

from dotenv import load_dotenv
from app.helpers.a_functions.dev_print import dev_print

from app.models.signal_model import SignalModel

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


async def update_signals_aggr(
    firestore_col_name="signalsAggrOpen",
    firestore_doc_name=None,
    name=None,
    nameType=None,
    nameTypeSubtitle=None,
    nameVersion="1.0.0",
    nameSort=1,
    signalsCollection="sSignalsCryptoTest",
    did_gen_signals=False,
    is_risky=False,
    nameIsActive=True,
    nameMarket="crypto",
):
    try:
        collection_signalAggr = database_mongodb_client[signalsCollection]
        data_open_signals = await collection_signalAggr.find({"name": name, "nameVersion": nameVersion, "isClosed": False}).to_list(length=None)

        for item in data_open_signals:
            item["id"] = str(item["_id"])

        # convert to SignalModel
        data_open_signals = [SignalModel(**item) for item in data_open_signals]
        data_open_signals = [item.dict() for item in data_open_signals]

        # sort by entryDateTimeUtc new to old
        data_open_signals = sorted(data_open_signals, key=lambda k: k["entryDateTimeUtc"], reverse=True)

        # remove the fields from data if present
        delete_fields = [
            "isClosedAuto",
            "isClosedManual",
            "isNew",
            "lastCheckDateTimeEst",
            "lastCheckDateTimeUtc",
            "signalName",
            "timeframe",
            "highestPct",
            "highestPips",
        ]

        for item in data_open_signals:
            item["signalName"] = name

            for field in delete_fields:
                if field in item:
                    del item[field]

                # 365 days ago
        three_sixty_five_days_ago = datetime.utcnow() - timedelta(days=365)
        data365days = await collection_signalAggr.find({"name": name, "nameVersion": nameVersion, "entryDateTimeUtc": {"$gte": three_sixty_five_days_ago}}).to_list(
            length=None
        )

        noResults365DaysWinners = 0
        noResults365DaysLosers = 0
        noResults365DaysTotal = 0
        noResults365DaysWinnersPct = 0
        noResults365DaysLosersPct = 0
        noResults365DaysWinnersPips = 0
        noResults365DaysLosersPips = 0

        for item in data365days:
            if item["entryResult"] == "profit":
                noResults365DaysWinners += 1
                noResults365DaysWinnersPct += item["entryProfitPct"]
                noResults365DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults365DaysLosers += 1
                noResults365DaysLosersPct += item["entryProfitPct"]
                noResults365DaysLosersPips += item["entryProfitPips"]

        noResults365DaysTotal = noResults365DaysWinners + noResults365DaysLosers
        noResults365DaysPctTotal = noResults365DaysWinnersPct + noResults365DaysLosersPct
        noResults365DaysPipsTotal = noResults365DaysWinnersPips + noResults365DaysLosersPips
        noResults365DaysPctTotalAvg = noResults365DaysPctTotal / noResults365DaysTotal if noResults365DaysTotal > 0 else 0
        noResults365DaysPipsTotalAvg = noResults365DaysPipsTotal / noResults365DaysTotal if noResults365DaysTotal > 0 else 0

        # 180 days ago
        one_eighty_days_ago = datetime.utcnow() - timedelta(days=180)
        data180days = [entry for entry in data365days if entry["entryDateTimeUtc"] >= one_eighty_days_ago]
        #
        noResults180DaysWinners = 0
        noResults180DaysLosers = 0
        noResults180DaysTotal = 0
        noResults180DaysWinnersPct = 0
        noResults180DaysLosersPct = 0
        noResults180DaysWinnersPips = 0
        noResults180DaysLosersPips = 0

        for item in data180days:
            if item["entryResult"] == "profit":
                noResults180DaysWinners += 1
                noResults180DaysWinnersPct += item["entryProfitPct"]
                noResults180DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults180DaysLosers += 1
                noResults180DaysLosersPct += item["entryProfitPct"]
                noResults180DaysLosersPips += item["entryProfitPips"]

        noResults180DaysTotal = noResults180DaysWinners + noResults180DaysLosers
        noResults180DaysPctTotal = noResults180DaysWinnersPct + noResults180DaysLosersPct
        noResults180DaysPipsTotal = noResults180DaysWinnersPips + noResults180DaysLosersPips
        noResults180DaysPctTotalAvg = noResults180DaysPctTotal / noResults180DaysTotal if noResults180DaysTotal > 0 else 0
        noResults180DaysPipsTotalAvg = noResults180DaysPipsTotal / noResults180DaysTotal if noResults180DaysTotal > 0 else 0

        # 90 days ago
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        data90days = [entry for entry in data365days if entry["entryDateTimeUtc"] >= ninety_days_ago]
        #
        noResults90DaysWinners = 0
        noResults90DaysLosers = 0
        noResults90DaysTotal = 0
        noResults90DaysWinnersPct = 0
        noResults90DaysLosersPct = 0
        noResults90DaysWinnersPips = 0
        noResults90DaysLosersPips = 0

        for item in data90days:
            if item["entryResult"] == "profit":
                noResults90DaysWinners += 1
                noResults90DaysWinnersPct += item["entryProfitPct"]
                noResults90DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults90DaysLosers += 1
                noResults90DaysLosersPct += item["entryProfitPct"]
                noResults90DaysLosersPips += item["entryProfitPips"]

        noResults90DaysTotal = noResults90DaysWinners + noResults90DaysLosers
        noResults90DaysPctTotal = noResults90DaysWinnersPct + noResults90DaysLosersPct
        noResults90DaysPipsTotal = noResults90DaysWinnersPips + noResults90DaysLosersPips
        noResults90DaysPctTotalAvg = noResults90DaysPctTotal / noResults90DaysTotal if noResults90DaysTotal > 0 else 0
        noResults90DaysPipsTotalAvg = noResults90DaysPipsTotal / noResults90DaysTotal if noResults90DaysTotal > 0 else 0

        # 30 days ago
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        data30days = [entry for entry in data365days if entry["entryDateTimeUtc"] >= thirty_days_ago]
        #
        noResults30DaysWinners = 0
        noResults30DaysLosers = 0
        noResults30DaysTotal = 0
        noResults30DaysWinnersPct = 0
        noResults30DaysLosersPct = 0
        noResults30DaysWinnersPips = 0
        noResults30DaysLosersPips = 0

        for item in data30days:
            if item["entryResult"] == "profit":
                noResults30DaysWinners += 1
                noResults30DaysWinnersPct += item["entryProfitPct"]
                noResults30DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults30DaysLosers += 1
                noResults30DaysLosersPct += item["entryProfitPct"]
                noResults30DaysLosersPips += item["entryProfitPips"]

        noResults30DaysTotal = noResults30DaysWinners + noResults30DaysLosers
        noResults30DaysPctTotal = noResults30DaysWinnersPct + noResults30DaysLosersPct
        noResults30DaysPipsTotal = noResults30DaysWinnersPips + noResults30DaysLosersPips
        noResults30DaysPctTotalAvg = noResults30DaysPctTotal / noResults30DaysTotal if noResults30DaysTotal > 0 else 0
        noResults30DaysPipsTotalAvg = noResults30DaysPipsTotal / noResults30DaysTotal if noResults30DaysTotal > 0 else 0

        # 14 days ago
        fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
        data14days = [entry for entry in data365days if entry["entryDateTimeUtc"] >= fourteen_days_ago]
        #
        noResults14DaysWinners = 0
        noResults14DaysLosers = 0
        noResults14DaysTotal = 0
        noResults14DaysWinnersPct = 0
        noResults14DaysLosersPct = 0
        noResults14DaysWinnersPips = 0
        noResults14DaysLosersPips = 0

        for item in data14days:
            if item["entryResult"] == "profit":
                noResults14DaysWinners += 1
                noResults14DaysWinnersPct += item["entryProfitPct"]
                noResults14DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults14DaysLosers += 1
                noResults14DaysLosersPct += item["entryProfitPct"]
                noResults14DaysLosersPips += item["entryProfitPips"]

        noResults14DaysTotal = noResults14DaysWinners + noResults14DaysLosers
        noResults14DaysPctTotal = noResults14DaysWinnersPct + noResults14DaysLosersPct
        noResults14DaysPipsTotal = noResults14DaysWinnersPips + noResults14DaysLosersPips
        noResults14DaysPctTotalAvg = noResults14DaysPctTotal / noResults14DaysTotal if noResults14DaysTotal > 0 else 0
        noResults14DaysPipsTotalAvg = noResults14DaysPipsTotal / noResults14DaysTotal if noResults14DaysTotal > 0 else 0

        # filter get last 7 days field entryDateTimeUtc
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        data7days = [entry for entry in data365days if entry["entryDateTimeUtc"] >= seven_days_ago]
        noResults7DaysWinners = 0
        noResults7DaysLosers = 0
        noResults7DaysTotal = 0
        noResults7DaysWinnersPct = 0
        noResults7DaysLosersPct = 0
        noResults7DaysWinnersPips = 0
        noResults7DaysLosersPips = 0

        for item in data7days:
            if item["entryResult"] == "profit":
                noResults7DaysWinners += 1
                noResults7DaysWinnersPct += item["entryProfitPct"]
                noResults7DaysWinnersPips += item["entryProfitPips"]

            elif item["entryResult"] == "loss":
                noResults7DaysLosers += 1
                noResults7DaysLosersPct += item["entryProfitPct"]
                noResults7DaysLosersPips += item["entryProfitPips"]

        noResults7DaysTotal = noResults7DaysWinners + noResults7DaysLosers
        noResults7DaysPctTotal = noResults7DaysWinnersPct + noResults7DaysLosersPct
        noResults7DaysPipsTotal = noResults7DaysWinnersPips + noResults7DaysLosersPips
        noResults7DaysPctTotalAvg = noResults7DaysPctTotal / noResults7DaysTotal if noResults7DaysTotal > 0 else 0
        noResults7DaysPipsTotalAvg = noResults7DaysPipsTotal / noResults7DaysTotal if noResults7DaysTotal > 0 else 0

        # win rate, pips, pips avg, pct, pct avg use 365 days
        results = []
        d = data365days
        symbols = set([item["symbol"] for item in d])
        for symbol in symbols:
            symbolData = [item for item in d if item["symbol"] == symbol]
            noWinners = len([item for item in symbolData if item["entryResult"] == "profit"])
            noLosers = len([item for item in symbolData if item["entryResult"] == "loss"])
            noTotal = noWinners + noLosers
            noWinnersPct = sum([item["entryProfitPct"] for item in symbolData if item["entryResult"] == "profit"])
            noLosersPct = sum([item["entryProfitPct"] for item in symbolData if item["entryResult"] == "loss"])
            noWinnersPips = sum([item["entryProfitPips"] for item in symbolData if item["entryResult"] == "profit"])
            noLosersPips = sum([item["entryProfitPips"] for item in symbolData if item["entryResult"] == "loss"])
            noPctTotal = noWinnersPct + noLosersPct
            noPipsTotal = noWinnersPips + noLosersPips
            noPctTotalAvg = noPctTotal / noTotal if noTotal > 0 else 0
            noPipsTotalAvg = noPipsTotal / noTotal if noTotal > 0 else 0
            winRate = noWinners / noTotal if noTotal > 0 else 0
            results.append(
                {
                    "symbol": symbol,
                    "winners": noWinners,
                    "losers": noLosers,
                    "total": noTotal,
                    "winnersPct": noWinnersPct,
                    "losersPct": noLosersPct,
                    "winnersPips": noWinnersPips,
                    "losersPips": noLosersPips,
                    "pctTotal": noPctTotal,
                    "pipsTotal": noPipsTotal,
                    "pctTotalAvg": noPctTotalAvg,
                    "pipsTotalAvg": noPipsTotalAvg,
                    "winRate": winRate,
                }
            )

        # data
        data_open_signals = {
            "nameIsRisky": is_risky,
            "data": data_open_signals,
            "totalSignals": len(data_open_signals),
            "name": name,
            "nameType": nameType,
            "nameTypeSubtitle": nameTypeSubtitle,
            "nameVersion": nameVersion,
            "nameSort": nameSort,
            "nameIsActive": nameIsActive,
            "nameMarket": nameMarket,
            "nameSignalsCollection": signalsCollection,
            "lastUpdatedDateTime": firestore.SERVER_TIMESTAMP,
            "lastGenSignalsDateTime": firestore.SERVER_TIMESTAMP,
            #
            "result": results,
            #
            "results7Days": {
                "winners": noResults7DaysWinners,
                "losers": noResults7DaysLosers,
                "total": noResults7DaysTotal,
                "winnersPct": noResults7DaysWinnersPct,
                "losersPct": noResults7DaysLosersPct,
                "winnersPips": noResults7DaysWinnersPips,
                "losersPips": noResults7DaysLosersPips,
                "avePct": noResults7DaysPctTotalAvg,
                "avePips": noResults7DaysPipsTotalAvg,
            },
            #
            "results14Days": {
                "winners": noResults14DaysWinners,
                "losers": noResults14DaysLosers,
                "total": noResults14DaysTotal,
                "winnersPct": noResults14DaysWinnersPct,
                "losersPct": noResults14DaysLosersPct,
                "winnersPips": noResults14DaysWinnersPips,
                "losersPips": noResults14DaysLosersPips,
                "avePct": noResults14DaysPctTotalAvg,
                "avePips": noResults14DaysPipsTotalAvg,
            },
            "results30Days": {
                "winners": noResults30DaysWinners,
                "losers": noResults30DaysLosers,
                "total": noResults30DaysTotal,
                "winnersPct": noResults30DaysWinnersPct,
                "losersPct": noResults30DaysLosersPct,
                "winnersPips": noResults30DaysWinnersPips,
                "losersPips": noResults30DaysLosersPips,
                "avePct": noResults30DaysPctTotalAvg,
                "avePips": noResults30DaysPipsTotalAvg,
            },
            "results90Days": {
                "winners": noResults90DaysWinners,
                "losers": noResults90DaysLosers,
                "total": noResults90DaysTotal,
                "winnersPct": noResults90DaysWinnersPct,
                "losersPct": noResults90DaysLosersPct,
                "winnersPips": noResults90DaysWinnersPips,
                "losersPips": noResults90DaysLosersPips,
                "avgPct": noResults90DaysPctTotalAvg,
                "avgPips": noResults90DaysPipsTotalAvg,
            },
            "results180Days": {
                "winners": noResults180DaysWinners,
                "losers": noResults180DaysLosers,
                "total": noResults180DaysTotal,
                "winnersPct": noResults180DaysWinnersPct,
                "losersPct": noResults180DaysLosersPct,
                "winnersPips": noResults180DaysWinnersPips,
                "losersPips": noResults180DaysLosersPips,
                "avgPct": noResults180DaysPctTotalAvg,
                "avgPips": noResults180DaysPipsTotalAvg,
            },
            "results365Days": {
                "winners": noResults365DaysWinners,
                "losers": noResults365DaysLosers,
                "total": noResults365DaysTotal,
                "winnersPct": noResults365DaysWinnersPct,
                "losersPct": noResults365DaysLosersPct,
                "winnersPips": noResults365DaysWinnersPips,
                "losersPips": noResults365DaysLosersPips,
                "avgPct": noResults365DaysPctTotalAvg,
                "avgPips": noResults365DaysPipsTotalAvg,
            },
        }

        if did_gen_signals == False:
            del data_open_signals["lastGenSignalsDateTime"]

        # firestore_db.collection(firestore_col_name).document(firestore_doc_name).delete()
        firestore_db.collection(firestore_col_name).document(firestore_doc_name).set(data_open_signals, merge=True)
        # write to mongodb

        collection_signalAggr = database_mongodb_client["signalsAggrOpen"]
        await collection_signalAggr.update_one(
            {"name": name},
            {"$set": {**data_open_signals, "name": name, "lastUpdatedDateTime": datetime.utcnow(), "lastGenSignalsDateTime": datetime.utcnow()}},
            upsert=True,
        )

        collection_app_controls_private = database_mongodb_client["appControlsPrivate"]
        await collection_app_controls_private.update_one(
            {"name": "appControlsPrivate"},
            {"$set": {"name": "appControlsPrivate", "dtSignalsAggrOpenUpdated": datetime.utcnow()}},
            upsert=True,
        )

        dev_print("7 days Winners %", noResults7DaysWinners / noResults7DaysTotal if noResults7DaysTotal > 0 else 0)
        dev_print("7 days % per trade", noResults7DaysPctTotalAvg)
        dev_print("7 days total trades", noResults7DaysTotal)

        dev_print("14 days Winners %", noResults14DaysWinners / noResults14DaysTotal if noResults14DaysTotal > 0 else 0)
        dev_print("14 days % per trade", noResults14DaysPctTotalAvg)
        dev_print("14 days total trades", noResults14DaysTotal)
        #
        dev_print("30 days Winners %", noResults30DaysWinners / noResults30DaysTotal if noResults30DaysTotal > 0 else 0)
        dev_print("30 days % per trade", noResults30DaysPctTotalAvg)
        dev_print("30 days total trades", noResults30DaysTotal)
        #
        dev_print("90 days Winners %", noResults90DaysWinners / noResults90DaysTotal if noResults90DaysTotal > 0 else 0)
        dev_print("90 days % per trade", noResults90DaysPctTotalAvg)
        dev_print("90 days total trades", noResults90DaysTotal)
        #
        dev_print("180 days Winners %", noResults180DaysWinners / noResults180DaysTotal if noResults180DaysTotal > 0 else 0)
        dev_print("180 days % per trade", noResults180DaysPctTotalAvg)
        dev_print("180 days total trades", noResults180DaysTotal)

        dev_print("365 days Winners %", noResults365DaysWinners / noResults365DaysTotal if noResults365DaysTotal > 0 else 0)
        dev_print("365 days % per trade", noResults365DaysPctTotalAvg)
        dev_print("365 days total trades", noResults365DaysTotal)

    except Exception as e:
        print("Error update_firestore_crypto_signals", e)

    return True


def validate_firestore_update(df_res, useOldSignal=False, did_gen_signals=False, current_time_floor=None):
    if useOldSignal == False:
        return True

    if did_gen_signals == True and is_production == "True":
        return True

    entryDateTimeUtc_all = df_res["entryDateTimeUtc"].unique()
    stopLossDateTimeUtc_all = df_res["stopLossDateTimeUtc"].unique()
    takeProfit1DateTimeUtc_all = df_res["takeProfit1DateTimeUtc"].unique()
    takeProfit2DateTimeUtc_all = df_res["takeProfit2DateTimeUtc"].unique()
    takeProfit3DateTimeUtc_all = df_res["takeProfit3DateTimeUtc"].unique()
    takeProfit4DateTimeUtc_all = df_res["takeProfit4DateTimeUtc"].unique()
    stopLossRevisedDateTimeUtc_all = df_res["stopLossRevisedDateTimeUtc"].unique()

    # merge all the dates
    all_dates = np.concatenate(
        (
            entryDateTimeUtc_all,
            stopLossDateTimeUtc_all,
            takeProfit1DateTimeUtc_all,
            takeProfit2DateTimeUtc_all,
            takeProfit3DateTimeUtc_all,
            stopLossRevisedDateTimeUtc_all,
            takeProfit4DateTimeUtc_all,
        )
    )
    #  remove all the null values
    all_dates = all_dates[~pd.isnull(all_dates)]
    # remove all the duplicates
    all_dates = np.unique(all_dates)
    all_dates = sorted(all_dates, reverse=True)

    # removes extra 00+00 from the date
    now = current_time_floor
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    has_update = False
    for date in all_dates:
        if date == now:
            has_update = True
            break

    return has_update
