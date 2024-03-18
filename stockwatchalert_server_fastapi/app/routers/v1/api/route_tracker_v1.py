from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.api.symbols_tracker import get_symbol_tracker_all


router_tracker_v1 = APIRouter(prefix="/v1")


@router_tracker_v1.get("/symbols-trackers")
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
