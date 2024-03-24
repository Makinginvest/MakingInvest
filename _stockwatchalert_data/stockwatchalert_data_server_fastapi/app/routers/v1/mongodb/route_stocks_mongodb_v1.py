import asyncio
import os
import timeit
from fastapi.exceptions import HTTPException

from fastapi import APIRouter
from app._security.a_validate_api_key import validate_apikey

from app.helpers._functions_mongodb.stocks_mongodb_update import stocks_update_all_mongodb_historical_all, stocks_update_all_mongodb_historical_recent
from app.utils.measure_duration import measure_duration

router = APIRouter(prefix="/v1")

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


# ----------------------------------  5m --------------------------------- #
@router.patch("/stocks-update-mongodb-all")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        await stocks_update_all_mongodb_historical_all(timeframe="1d", lookback_days=500)
        await stocks_update_all_mongodb_historical_all(timeframe="15m", lookback_days=380)
        await stocks_update_all_mongodb_historical_all(timeframe="1h", lookback_days=380)
        return "done"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.patch("/stocks-update-mongodb-recent")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)

        _, d = await measure_duration(60)(stocks_update_all_mongodb_historical_recent)(timeframe="15m")
        _, d = await measure_duration(60)(stocks_update_all_mongodb_historical_recent)(timeframe="1d")
        _, d = await measure_duration(1)(stocks_update_all_mongodb_historical_recent)(timeframe="1h")

        return "done"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))
