from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.api.screener_stock import get_screener_stocks, run_screener_stock


router_screener_v1 = APIRouter(prefix="/v1")


@router_screener_v1.patch("/screener-stocks")
async def get_signals(jsonWebToken: str = None, apikey: str = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await run_screener_stock()
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error running stock screener: ", e)
        raise HTTPException(500, detail=e)


@router_screener_v1.get("/screener-stocks")
async def get_signals(jsonWebToken: str = None, apikey: str = None, minClose: float = 0, maxClose: float = 1000000000, minVolume: float = 0):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_screener_stocks(minClose, maxClose, minVolume)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error running stock screener: ", e)
        raise HTTPException(500, detail=e)
