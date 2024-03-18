from _project.log_config.app_logger import app_logger
from app._database.db_connect_client import database_mongodb_client


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers._functions.get_symbol_results_v1 import get_closed_signals_v1


router_signals_results_v1 = APIRouter(prefix="/v1")


@router_signals_results_v1.get("/signals-results")
async def get_signals(apikey: str = None, jsonWebToken=None, nameCollection: str = None, nameId: str = None, nameVersion: str = None):
    try:
        if not nameCollection or not nameId or not nameVersion:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_closed_signals_v1(nameCollection, nameId, nameVersion)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
