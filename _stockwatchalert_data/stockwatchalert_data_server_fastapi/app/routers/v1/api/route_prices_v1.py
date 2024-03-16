from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._security.a_validate_api_key import validate_apikey

from app.helpers.prices.prices_all import update_all_prices

router = APIRouter(prefix="/v1")


@router.patch("/prices-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        res = await update_all_prices()

        return res

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
