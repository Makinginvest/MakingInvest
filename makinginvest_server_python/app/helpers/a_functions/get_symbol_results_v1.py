from datetime import datetime, timedelta
from app.models.signal_model import SignalModel
from app.a_database_client.db_connect_client import database_mongodb_client


async def get_closed_symbol_results_v1(signalsCollection: str = None, name: str = None, nameVersion: str = None, symbol: str = None):
    try:
        collection = database_mongodb_client[signalsCollection]
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        one_year_ago = datetime.utcnow() - timedelta(days=365)
        data365days = await collection.find({"name": name, "nameVersion": nameVersion, "symbol": symbol, "entryDateTimeUtc": {"$gte": one_year_ago}}).to_list(
            length=None
        )

        if len(data365days) == 0:
            return None

        for item in data365days:
            item["id"] = str(item["_id"])

        # convert to SignalModel
        data = [SignalModel(**item) for item in data365days]
        for item in data:
            if item.closedDateTimeUtc == None:
                if item.takeProfit1DateTimeUtc != None:
                    item.closedDateTimeUtc = item.takeProfit1DateTimeUtc
                if item.takeProfit2DateTimeUtc != None:
                    item.closedDateTimeUtc = item.takeProfit2DateTimeUtc
                if item.takeProfit3DateTimeUtc != None:
                    item.closedDateTimeUtc = item.takeProfit3DateTimeUtc

        # if closedDateTimeUtc is None delete it
        data = [item for item in data if item.closedDateTimeUtc != None]

        # sort byt closedDateTimeUtc decs
        data = sorted(data, key=lambda k: k.closedDateTimeUtc, reverse=True)
        data = [item.dict() for item in data]

        delete_fields = [
            "isClosedAuto",
            "isClosedManual",
            "isNew",
            "lastCheckDateTimeEst",
            "lastCheckDateTimeUtc",
            "signalName",
        ]

        for item in data:
            item["signalName"] = name

            for field in delete_fields:
                if field in item:
                    del item[field]

        data_with_results = []

        for item in data:
            if item["entryResult"] == "profit" or item["entryResult"] == "loss":
                data_with_results.append(item)

        noResults7DaysWinners = 0
        noResults7DaysLosers = 0
        noResults7DaysTotal = 0
        noResults7DaysWinnersPct = 0
        noResults7DaysLosersPct = 0
        noResults7DaysWinnersPips = 0
        noResults7DaysLosersPips = 0

        noResults30DaysWinners = 0
        noResults30DaysLosers = 0
        noResults30DaysTotal = 0
        noResults30DaysWinnersPct = 0
        noResults30DaysLosersPct = 0
        noResults30DaysWinnersPips = 0
        noResults30DaysLosersPips = 0

        noResults365DaysWinners = 0
        noResults365DaysLosers = 0
        noResults365DaysTotal = 0
        noResults365DaysWinnersPct = 0
        noResults365DaysLosersPct = 0
        noResults365DaysWinnersPips = 0
        noResults365DaysLosersPips = 0

        # seven days
        for item in data_with_results:
            if item["entryResult"] == "profit":
                if item["entryDateTimeUtc"] > seven_days_ago:
                    noResults7DaysWinners += 1
                    noResults7DaysWinnersPct += item["entryProfitPct"]
                    noResults7DaysWinnersPips += item["entryProfitPips"]
                if item["entryDateTimeUtc"] > thirty_days_ago:
                    noResults30DaysWinners += 1
                    noResults30DaysWinnersPct += item["entryProfitPct"]
                    noResults30DaysWinnersPips += item["entryProfitPips"]

                noResults365DaysWinners += 1
                noResults365DaysWinnersPct += item["entryProfitPct"]
                noResults365DaysWinnersPips += item["entryProfitPips"]
            else:
                if item["entryDateTimeUtc"] > seven_days_ago:
                    noResults7DaysLosers += 1
                    noResults7DaysLosersPct += item["entryProfitPct"]
                    noResults7DaysLosersPips += item["entryProfitPips"]
                if item["entryDateTimeUtc"] > thirty_days_ago:
                    noResults30DaysLosers += 1
                    noResults30DaysLosersPct += item["entryProfitPct"]
                    noResults30DaysLosersPips += item["entryProfitPips"]
                noResults365DaysLosers += 1
                noResults365DaysLosersPct += item["entryProfitPct"]
                noResults365DaysLosersPips += item["entryProfitPips"]

        noResults7DaysTotal = noResults7DaysWinners + noResults7DaysLosers
        noResults7DaysPctTotal = noResults7DaysWinnersPct + noResults7DaysLosersPct
        noResults7DaysPipsTotal = noResults7DaysWinnersPips + noResults7DaysLosersPips
        noResults7DaysPctTotalAvg = noResults7DaysPctTotal / noResults7DaysTotal if noResults7DaysTotal > 0 else 0
        noResults7DaysPipsTotalAvg = noResults7DaysPipsTotal / noResults7DaysTotal if noResults7DaysTotal > 0 else 0

        noResults30DaysTotal = noResults30DaysWinners + noResults30DaysLosers
        noResults30DaysPctTotal = noResults30DaysWinnersPct + noResults30DaysLosersPct
        noResults30DaysPipsTotal = noResults30DaysWinnersPips + noResults30DaysLosersPips
        noResults30DaysPctTotalAvg = noResults30DaysPctTotal / noResults30DaysTotal if noResults30DaysTotal > 0 else 0
        noResults30DaysPipsTotalAvg = noResults30DaysPipsTotal / noResults30DaysTotal if noResults30DaysTotal > 0 else 0

        noResults365DaysTotal = noResults365DaysWinners + noResults365DaysLosers
        noResults365DaysPctTotal = noResults365DaysWinnersPct + noResults365DaysLosersPct
        noResults365DaysPipsTotal = noResults365DaysWinnersPips + noResults365DaysLosersPips
        noResults365DaysPctTotalAvg = noResults365DaysPctTotal / noResults365DaysTotal if noResults365DaysTotal > 0 else 0
        noResults365DaysPipsTotalAvg = noResults365DaysPipsTotal / noResults365DaysTotal if noResults365DaysTotal > 0 else 0

        # sort byt closedDateTimeUtc decs and then by entryDateTimeUtc
        data_with_results = sorted(data_with_results, key=lambda k: (k["entryDateTimeUtc"]), reverse=True)
        data_with_results = sorted(data_with_results, key=lambda k: (k["closedDateTimeUtc"]), reverse=True)

        return {
            "data": data_with_results,
            "totalSignals": len(data_with_results),
            "name": name,
            "nameVersion": nameVersion,
            "noResults7DaysWinners": noResults7DaysWinners,
            "noResults7DaysLosers": noResults7DaysLosers,
            "noResults7DaysTotal": noResults7DaysTotal,
            "noResults7DaysPctTotal": noResults7DaysPctTotal,
            "noResults7DaysPipsTotal": noResults7DaysPipsTotal,
            "noResults7DaysPctTotalAvg": noResults7DaysPctTotalAvg,
            "noResults7DaysPipsTotalAvg": noResults7DaysPipsTotalAvg,
            #
            "noResults30DaysWinners": noResults30DaysWinners,
            "noResults30DaysLosers": noResults30DaysLosers,
            "noResults30DaysTotal": noResults30DaysTotal,
            "noResults30DaysPctTotal": noResults30DaysPctTotal,
            "noResults30DaysPipsTotal": noResults30DaysPipsTotal,
            "noResults30DaysPctTotalAvg": noResults30DaysPctTotalAvg,
            "noResults30DaysPipsTotalAvg": noResults30DaysPipsTotalAvg,
            #
            "noResults365DaysWinners": noResults365DaysWinners,
            "noResults365DaysLosers": noResults365DaysLosers,
            "noResults365DaysTotal": noResults365DaysTotal,
            "noResults365DaysPctTotal": noResults365DaysPctTotal,
            "noResults365DaysPipsTotal": noResults365DaysPipsTotal,
            "noResults365DaysPctTotalAvg": noResults365DaysPctTotalAvg,
            "noResults365DaysPipsTotalAvg": noResults365DaysPipsTotalAvg,
        }

    except Exception as e:
        raise e
