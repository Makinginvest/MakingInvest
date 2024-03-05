import asyncio
import os
from fastapi.exceptions import HTTPException


from fastapi import APIRouter
from app.a_firebase.a_validate_api_key import validate_apikey

from app.helpers.a_functions_mongodb.crypto__mongodb_update import crypto_update_all_mongodb_historical_all, crypto_update_all_mongodb_historical_recent

router = APIRouter(prefix="/v1")

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


@router.patch("/crypto-update-mongodb-all")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        result = await crypto_update_all_mongodb_historical_all(timeframe="15m", lookback_days=30, lookback_months=12, pull_monthly=True)
        # result = await crypto_update_all_mongodb_historical_all(timeframe="1h", lookback_days=35, lookback_months=13, pull_monthly=True)
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.patch("/crypto-update-mongodb-recent")
async def route(limit: int = 105, apikey: str = None):
    try:
        validate_apikey(apikey)
        tasks = [
            crypto_update_all_mongodb_historical_recent(timeframe="5m", limit=limit),
            crypto_update_all_mongodb_historical_recent(timeframe="15m", limit=limit),
            # crypto_update_all_mongodb_historical_recent(timeframe="1h", limit=limit),
        ]

        await asyncio.gather(*tasks)

        return "ok"

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))
