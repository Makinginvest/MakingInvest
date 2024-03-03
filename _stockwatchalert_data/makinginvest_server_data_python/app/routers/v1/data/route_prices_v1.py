import asyncio
from _log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_api_key import validate_apikey

from app.helpers.data.get_news_data import update_all_news_mongodb_aggr
from app.helpers.prices.prices_all import update_all_prices
from app.helpers.prices.prices_crypto import getPricesCrypto
from app.helpers.prices.prices_forex import getPricesForex
from app.helpers.prices.prices_stocks import getPricesStocks
from app.a_database_data.db_connect_data import database_mongodb_data

router = APIRouter(prefix="/v1")


@router.patch("/prices-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        res = await update_all_prices()

        return res

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
