import os
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from _project.log_config.app_logger import app_logger
from app._firebase.a_validate_api_key import validate_apikey
from app.helpers.signals.signals_crypto_v1.crypto_signals_ichimoku_v1 import get_crypto_signals_ichimoku_v1
from app.helpers.signals.signals_crypto_v1.crypto_signals_ichimoku_v2 import get_crypto_signals_ichimoku_v2
from app.helpers.signals.signals_forex_v1.forex_signals_ichimoku_v1 import get_forex_signals_ichimoku_v1
from app.helpers.signals.signals_stocks_v1.stocks_signals_ichimoku_v1 import get_stocks_signals_ichimoku_v1
from app.helpers.signals.signals_stocks_v1.stocks_signals_ichimoku_v2 import get_stocks_signals_ichimoku_v2

router_signals_v1 = APIRouter(prefix="/v1/signals")

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")

use_old_signal = False
if is_production == "True":
    use_old_signal = True


# ----------------------------  CRYPTO ---------------------------- #
@router_signals_v1.patch("/crypto-1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_crypto_signals_ichimoku_v1()
        return r

    except HTTPException as e:
        app_logger().info("get_crypto_signals_ichimoku_v1 ", str(e))
        raise e

    except Exception as e:
        app_logger().info("get_crypto_signals_ichimoku_v1 ", e)
        raise HTTPException(500, detail=str(e))


@router_signals_v1.patch("/crypto-2")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_crypto_signals_ichimoku_v2()
        return r

    except HTTPException as e:
        app_logger().info("get_crypto_signals_ichimoku_v2: ", str(e))
        raise e

    except Exception as e:
        app_logger().info("get_crypto_signals_ichimoku_v2: ", e)
        raise HTTPException(500, detail=str(e))


# ----------------------------  STOCKS ---------------------------- #
@router_signals_v1.patch("/stocks-1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_stocks_signals_ichimoku_v1()
        return r

    except HTTPException as e:
        app_logger().info("get_stocks_signals_ichimoku_v1: ", str(e))
        raise e

    except Exception as e:
        app_logger().info("get_stocks_signals_ichimoku_v1: ", e)
        raise HTTPException(500, detail=str(e))


@router_signals_v1.patch("/stocks-2")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_stocks_signals_ichimoku_v2()
        return r

    except HTTPException as e:
        app_logger().info("get_stocks_signals_ichimoku_v2: ", str(e))
        raise e

    except Exception as e:
        app_logger().info("get_stocks_signals_ichimoku_v2: ", e)
        raise HTTPException(500, detail=str(e))


# ----------------------------  FOREX ---------------------------- #
@router_signals_v1.patch("/forex-1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_forex_signals_ichimoku_v1()
        return r

    except HTTPException as e:
        app_logger().info("get_forex_signals_ichimoku_v1: ", str(e))
        raise e

    except Exception as e:
        app_logger().info("get_forex_signals_ichimoku_v1: ", e)
        raise HTTPException(500, detail=str(e))
