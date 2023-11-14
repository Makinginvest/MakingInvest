from fastapi.exceptions import HTTPException

from fastapi import APIRouter
from app.a_firebase.a_validate_api_key import validate_apikey

from app.helpers.a_functions_mongodb.forex__mongodb_update import forex_update_all_mongodb_historical_all, forex_update_all_mongodb_historical_recent


router = APIRouter(prefix="/v1")


# ----------------------------------  5m --------------------------------- #
@router.patch("/forex-update-mongodb-all")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        result = await forex_update_all_mongodb_historical_all(resolution="M15")
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.patch("/forex-update-mongodb-recent")
async def route(apikey: str = None):
    try:
        validate_apikey(apikey)
        result = await forex_update_all_mongodb_historical_recent(resolution="M5")
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(500, detail=str(e))
