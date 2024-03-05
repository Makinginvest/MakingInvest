from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from _log_config.app_logger import app_logger
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.market_analysis.market_analysis import get_market_analysis, update_market_analysis


router = APIRouter(prefix="/v1")


@router.get("/signals-analysis")
async def get_signals(apikey: str = None, jsonWebToken=None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_market_analysis()

        if data is None:
            data = await update_market_analysis()

        if data is None:
            raise HTTPException(500, detail="Error generating signals analysis")

        if data:
            data["_id"] = str(data["_id"])

        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router.patch("/signals-analysis")
async def get_signals(apikey: str = None, jsonWebToken=None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await update_market_analysis()
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
