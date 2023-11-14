from _log_config.app_logger import app_logger

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_api_key import validate_apikey

from app.a_database_client.db_indexes_client import update_mongodb_indexes

v0_router_indexes = APIRouter()


@v0_router_indexes.patch("/updates-mongodb-indexes")
async def patch_signals(apikey: str = None):
    try:
        if not apikey:
            raise HTTPException(400, detail="Missing required fields: apikey")
        validate_apikey(apikey)

        await update_mongodb_indexes()

        return {"message": "Indexes updated"}

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
