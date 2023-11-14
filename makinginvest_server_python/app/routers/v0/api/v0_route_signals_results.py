from datetime import datetime, timedelta
from _log_config.app_logger import app_logger
from app.a_database_client.db_connect_client import database_mongodb_client


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken
from app.helpers.a_functions.get_signals_results_v1 import get_closed_signals_results_v1
from app.helpers.a_functions.get_signals_results_v2 import get_closed_signals_results_v2
from app.helpers.a_functions.get_signals_summary import get_closed_signals_results_summary
from app.helpers.a_functions.get_symbol_results_v1 import get_closed_symbol_results_v1


v0_router_signals_results = APIRouter()


@v0_router_signals_results.get("/signals-results")
async def get_signals(apikey: str = None, jsonWebToken=None, signalsCollection: str = None, name: str = None, nameVersion: str = None):
    try:
        if not signalsCollection or not name or not nameVersion:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_closed_signals_results_v1(signalsCollection, name, nameVersion)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_signals_results.get("/api/v2/signals-results")
async def get_signals(apikey: str = None, jsonWebToken=None, signalsCollection: str = None, name: str = None, nameVersion: str = None):
    try:
        if not signalsCollection or not name or not nameVersion:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_closed_signals_results_v2(signalsCollection, name, nameVersion)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_signals_results.get("/signals-results/summary")
async def get_signals(apikey: str = None, jsonWebToken=None, signalsCollection: str = None, name: str = None, nameVersion: str = None):
    try:
        if not signalsCollection or not name or not nameVersion:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        start_date = datetime.now() - timedelta(days=30 * 13)
        end_date = datetime.now()
        data = await get_closed_signals_results_summary(signalsCollection, name, nameVersion, start_date, end_date)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_signals_results.get("/signals-results/{symbol}")
async def get_signals(apikey: str = None, jsonWebToken=None, signalsCollection: str = None, name: str = None, nameVersion: str = None, symbol: str = None):
    try:
        if not signalsCollection or not name or not nameVersion or not symbol:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion, symbol")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_closed_symbol_results_v1(signalsCollection, name, nameVersion, symbol)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_signals_results.get("/api/v2/signals-results/{symbol}")
async def get_signals(apikey: str = None, jsonWebToken=None, signalsCollection: str = None, name: str = None, nameVersion: str = None, symbol: str = None):
    try:
        if not signalsCollection or not name or not nameVersion or not symbol:
            raise HTTPException(400, detail="Missing required fields: apikey, signalsCollection, name, nameVersion, symbol")

        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        data = await get_closed_symbol_results_v1(signalsCollection, name, nameVersion, symbol)
        return data

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@v0_router_signals_results.get("/signals-aggr-open")
async def get_signals(apikey: str = None, jsonWebToken=None):
    try:
        validate_apikey_json_webtoken(apikey=apikey, token=jsonWebToken)
        collection = database_mongodb_client["signalsAggrOpen"]
        data = await collection.find().to_list(length=100)

        if len(data) > 0:
            for d in data:
                d["_id"] = str(d["_id"])

            return data

        return []

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
