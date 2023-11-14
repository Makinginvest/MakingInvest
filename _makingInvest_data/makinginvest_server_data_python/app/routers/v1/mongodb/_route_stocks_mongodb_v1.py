import os
import time
from fastapi.exceptions import HTTPException

from fastapi import APIRouter
from app.a_firebase.a_validate_api_key import validate_apikey

from app.helpers.a_functions_mongodb.stocks__mongodb_update import stocks_update_all_mongodb_historical_all, stocks_update_all_mongodb_historical_recent

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
        result = await stocks_update_all_mongodb_historical_all(interval="15min", lookback_days=365 * 1)
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.patch("/stocks-update-mongodb-recent")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        result = await stocks_update_all_mongodb_historical_recent(interval="15min")
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))
