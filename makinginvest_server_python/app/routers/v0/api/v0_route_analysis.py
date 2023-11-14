from _log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.market_analysis.market_analysis import get_market_analysis


v0_router_analysis = APIRouter()


@v0_router_analysis.get("/signals-analysis")
async def get_signals(apikey: str = None, jsonWebToken=None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_market_analysis()

        if data:
            data["_id"] = str(data["_id"])

        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
