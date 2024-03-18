from datetime import datetime, timezone
import aiohttp
import pandas as pd
from pandas import Timestamp
from app.a_database_data.db_connect_data import database_mongodb_data


import os
from dotenv import load_dotenv

load_dotenv()


async def update_all_market_activities_mongodb_aggr():
    try:
        collection = database_mongodb_data["marketActivities"]

        gainers = await get_market_activity(type="gainers")
        await collection.update_one({"type": "gainers"}, {"$set": {"data": gainers}}, upsert=True)

        losers = await get_market_activity(type="losers")
        await collection.update_one({"type": "losers"}, {"$set": {"data": losers}}, upsert=True)

        actives = await get_market_activity(type="actives")
        await collection.update_one({"type": "actives"}, {"$set": {"data": actives}}, upsert=True)

        data = {"type": "all", "gainers": gainers, "losers": losers, "actives": actives, "lastUpdatedDateTimeUtc": datetime.now(timezone.utc).isoformat()}
        await collection.update_one({"type": "all"}, {"$set": data}, upsert=True)

        return data

    except Exception as e:
        print(e)
        return {}

        return []


async def get_market_activity(type: str):
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")

    try:
        async with aiohttp.ClientSession() as session:
            df = pd.DataFrame()
            url = f"https://financialmodelingprep.com/api/v3/stock_market/{type}?apikey={api_key}"

            # response shape   {
            # "symbol": "MTC",
            # "name": "MMTec, Inc.",
            # "change": 1.26,
            # "price": 2.56,
            # "changesPercentage": 96.9231

            async with session.get(url) as response:
                data = await response.json()
                res = []
                for d in data:
                    r = {
                        "symbol": d["symbol"],
                        "name": d["name"],
                        "change": d["change"],
                        "price": d["price"],
                        "changesPercentage": d["changesPercentage"],
                    }
                    res.append(r)

                _df = pd.DataFrame(res)
                df = df.append(_df)

            return df.to_dict("records")

    except Exception as e:
        print(f"error:", e)
        return None
