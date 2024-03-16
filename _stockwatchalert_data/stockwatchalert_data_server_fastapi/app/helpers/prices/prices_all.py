import asyncio
from datetime import datetime, timezone
from _project.log_config.app_logger import app_logger


from fastapi import APIRouter

from app.helpers.prices.prices_crypto import getPricesCrypto
from app.helpers.prices.prices_forex import getPricesForex
from app.helpers.prices.prices_stocks import getPricesStocks
from app._database_data.db_connect_data import database_mongodb_data

router = APIRouter()


async def update_all_prices():
    try:
        tasks = [getPricesCrypto(), getPricesForex(), getPricesStocks()]
        dateCrypto, dataForex, dataStocks = await asyncio.gather(*tasks)

        collection = database_mongodb_data["prices"]
        await collection.update_one({"type": "all"}, {"$set": {"dataCrypto": dateCrypto, "dataForex": dataForex, "dataStocks": dataStocks}}, upsert=True)

        collection_app_controls_private = database_mongodb_data["appControlsPrivate"]
        await collection_app_controls_private.update_one(
            {"name": "appControlsPrivate"},
            {"$set": {"pricesAllLastUpdatedDateTime": datetime.now(timezone.utc)}},
            upsert=True,
        )

        return {"status": "ok"}

    except Exception as e:
        app_logger().info("Error updafing prices: ", e)
        return {"status": "error"}
