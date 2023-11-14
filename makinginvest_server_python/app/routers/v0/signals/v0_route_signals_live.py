import os
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from _log_config.app_logger import app_logger
from app.a_firebase.a_validate_api_key import validate_apikey
from app.helpers.engines.signals_crypto_live1.crypto_strat_macd_all_live1 import get_signals_crypto_all_live1
from app.helpers.engines.signals_crypto_live1.crypto_strat_macd_all_live1 import get_signals_crypto_all_live1
from app.helpers.engines.signals_forex_live1.forex_strat_macd_all_live1 import get_signals_forex_all_live1
from app.helpers.engines.signals_stocks_live1.stocks_strat_macd_all_live1 import get_signals_stocks_all_live1

router_signals_live_v0 = APIRouter()

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION")

useOldSignal = False
if is_production == "True":
    useOldSignal = True


# ----------------------------  CRYPTO ---------------------------- #
@router_signals_live_v0.patch("/signals-crypto-all-live1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_signals_crypto_all_live1(useOldSignal=useOldSignal)
        return r

    except HTTPException as e:
        app_logger().info("pure-signals: ", e)
        raise e

    except Exception as e:
        app_logger().info("pure-signals: ", e)
        raise HTTPException(500, detail=e)


# ----------------------------  FOREX ---------------------------- #
@router_signals_live_v0.patch("/signals-forex-all-live1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_signals_forex_all_live1(useOldSignal=useOldSignal)
        return r

    except HTTPException as e:
        app_logger().info("pure-signals: ", e)
        raise e

    except Exception as e:
        app_logger().info("pure-signals: ", e)
        raise HTTPException(500, detail=e)


# ----------------------------  STOCKS ---------------------------- #
@router_signals_live_v0.patch("/signals-stocks-all-live1")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        r = await get_signals_stocks_all_live1(useOldSignal=useOldSignal)
        return r

    except HTTPException as e:
        app_logger().info("pure-signals: ", e)
        raise e

    except Exception as e:
        app_logger().info("pure-signals: ", e)
        raise HTTPException(500, detail=e)
