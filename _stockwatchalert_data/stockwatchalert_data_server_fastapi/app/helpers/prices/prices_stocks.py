from datetime import datetime, timezone
import aiohttp
import pandas as pd
from app._database_data.db_connect_data import database_mongodb_data
import os
from dotenv import load_dotenv

load_dotenv()


async def getPricesStocks():
    api_key = os.getenv("FINANCIALMODELINGPREP_APIKEY")
    url = f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}"

    try:
        symbols = await get_USDT_symbols_by_value("_project/datasets/data/_data_symbols_stock_us_market.csv")

        data = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                for symbol_info in await response.json():
                    data.append({"s": symbol_info["symbol"], "p": convert_string_to_float(symbol_info["price"])})
                data = [x for x in data if x["s"] in symbols]

        # write to mongodb
        collection = database_mongodb_data["prices"]
        await collection.update_one({"type": "stocks"}, {"$set": {"data": data}}, upsert=True)

        collection_app_controls_private = database_mongodb_data["appControlsPrivate"]
        await collection_app_controls_private.update_one(
            {"name": "appControlsPrivate"},
            {"$set": {"pricesStocksLastUpdatedDateTime": datetime.now(timezone.utc)}},
            upsert=True,
        )

        return data

    except Exception as e:
        print(e)
        return []


async def get_USDT_symbols_by_value(path="_project/datasets/data/_data_symbols_stock_us_market.csv"):
    symbols = pd.read_csv(path)
    symbols = symbols["symbol"].tolist()
    return symbols


def convert_string_to_float(string):
    if type(string) is str:
        return float(string)
    elif type(string) is float:
        return string
    else:
        return 0.0
