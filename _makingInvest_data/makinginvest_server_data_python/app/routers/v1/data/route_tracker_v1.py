from _log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.tracker.symbols_tracker import get_symbol_tracker_all, update_symbol_tracker_all


router = APIRouter(prefix="/v1")


@router.patch("/symbols-trackers")
async def patch_signals(jsonWebToken: str = None, data: dict = None, apikey: str = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await update_symbol_tracker_all()
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(400, detail=e)


@router.get("/symbols-trackers")
async def get_signals(jsonWebToken: str = None, apikey: str = None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_symbol_tracker_all()
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
