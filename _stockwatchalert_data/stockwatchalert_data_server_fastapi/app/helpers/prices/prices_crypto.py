from datetime import datetime, timezone
import aiohttp
from app._database_data.db_connect_data import database_mongodb_data


async def getPricesCrypto():
    url = "https://api.binance.com/api/v3/ticker/price"
    data = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                for symbol_info in await response.json():
                    data.append({"s": symbol_info["symbol"], "p": convert_string_to_float(symbol_info["price"])})

                # keep symbols ending in USDT or BUSD
                data = [symbol for symbol in data if symbol["s"].endswith("USDT") or symbol["s"].endswith("BUSD")]

                # write to mongodb
                collection = database_mongodb_data["prices"]
                await collection.update_one({"type": "crypto"}, {"$set": {"data": data}}, upsert=True)

                collection_app_controls_private = database_mongodb_data["appControlsPrivate"]
                await collection_app_controls_private.update_one(
                    {"name": "appControlsPrivate"},
                    {"$set": {"pricesCryptoLastUpdatedDateTime": datetime.now(timezone.utc)}},
                    upsert=True,
                )

                return data
    except Exception as e:
        print(e)
        return []


def convert_string_to_float(string):
    if type(string) is str:
        return float(string)
    elif type(string) is float:
        return string
    else:
        return 0.0
