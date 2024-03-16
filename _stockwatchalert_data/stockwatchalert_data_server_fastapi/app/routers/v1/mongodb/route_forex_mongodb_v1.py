import asyncio
import time
from fastapi.exceptions import HTTPException

from fastapi import APIRouter
from app._security.a_validate_api_key import validate_apikey

from app.helpers._functions_mongodb.forex__mongodb_update import forex_update_all_mongodb_historical_all, forex_update_all_mongodb_historical_recent


router = APIRouter(prefix="/v1")


# ----------------------------------  5m --------------------------------- #
@router.patch("/forex-update-mongodb-all")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        tasks = [
            forex_update_all_mongodb_historical_all(granularity="M5", timeframe="5m"),
            forex_update_all_mongodb_historical_all(granularity="M15", timeframe="15m"),
            forex_update_all_mongodb_historical_all(granularity="D", timeframe="1d"),
        ]
        await asyncio.gather(*tasks)
        return "done"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.patch("/forex-update-mongodb-recent")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        tasks = [
            forex_update_all_mongodb_historical_recent(granularity="M5", timeframe="5m"),
            forex_update_all_mongodb_historical_recent(granularity="M15", timeframe="15m"),
            forex_update_all_mongodb_historical_recent(granularity="D", timeframe="1d"),
        ]
        await asyncio.gather(*tasks)
        return "done"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))
