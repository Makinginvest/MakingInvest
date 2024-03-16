from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from _project.log_config.app_logger import app_logger

from app._security.a_validate_api_key import validate_apikey
from app.helpers.market_analysis.market_analysis import get_market_analysis, update_market_analysis


router = APIRouter(prefix="/v1")


@router.get("/signals-analysis")
async def get_signals(apikey: str = None, jsonWebToken=None):
    try:
        validate_apikey(apikey=apikey)
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
        validate_apikey(apikey=apikey)
        data = await update_market_analysis()
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
