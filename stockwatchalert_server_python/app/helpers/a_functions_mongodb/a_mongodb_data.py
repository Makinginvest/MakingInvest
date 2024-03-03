import os
import pandas as pd
from app.a_database_data.db_connect_data import database_mongodb_data
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


async def get_mongodb_data_historical(
    symbol, histCollection=None, timeframe="15m", limit=20000, datetime_start: datetime = None, datetime_end: datetime = None
) -> pd.DataFrame:
    if histCollection is None:
        raise Exception("baseCollection is None")

    try:
        historical_crypto = database_mongodb_data[f"{histCollection}{timeframe}"]
        data = []

        if datetime_start == None:
            data = await historical_crypto.find({"symbol": symbol, "timeframe": timeframe}).sort("dateTimeUtc", -1).limit(limit).to_list(length=limit)

        if datetime_start != None:
            data = (
                await historical_crypto.find({"symbol": symbol, "timeframe": timeframe, "dateTimeUtc": {"$gte": datetime_start}})
                .sort("dateTimeUtc", -1)
                .to_list(length=None)
            )

        if datetime_end != None and datetime_start != None:
            data = (
                await historical_crypto.find({"symbol": symbol, "timeframe": timeframe, "dateTimeUtc": {"$gte": datetime_start, "$lte": datetime_end}})
                .sort("dateTimeUtc", -1)
                .to_list(length=None)
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
