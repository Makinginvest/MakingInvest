from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.api.market_analysis import get_market_analysis


router_analysis_v1 = APIRouter(prefix="/v1")


@router_analysis_v1.get("/signals-analysis")
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
