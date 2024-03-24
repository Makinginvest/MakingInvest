import os
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from _project.log_config.app_logger import app_logger
from app._firebase.a_validate_api_key import validate_apikey
from app.helpers.api.backtest_data import get_backtesting_data_crypto, get_backtesting_data_forex, get_backtesting_data_stocks

router_backtest_data_v1 = APIRouter(prefix="/v1/backtest-data")

from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")

use_old_signal = False
if is_production == "True":
    use_old_signal = True


# ----------------------------  CRYPTO ---------------------------- #
@router_backtest_data_v1.get("/crypto")
async def func(apikey: str = None, start_date: str = "2023-01-01", end_date: str = "2024-03-08", timeframe: str = "2h"):
    try:
        validate_apikey(apikey)
        r = await get_backtesting_data_crypto(timeframe=timeframe, start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_crypto(timeframe="1h", start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_crypto(timeframe="30m", start_datetime=start_date, end_datetime=end_date)
        return r

    except HTTPException as e:
        app_logger().info("get_backtesting_data_crypto: ", str(e))
        raise HTTPException(500, detail=str(e))

    except Exception as e:
        app_logger().info("get_backtesting_data_crypto: ", str(e))
        raise HTTPException(500, detail=str(e))


# ---------------------------------- STOCKS ---------------------------------- #
@router_backtest_data_v1.get("/stocks")
async def func(apikey: str = None, start_date: str = "2023-01-01", end_date: str = "2024-03-22", timeframe: str = "1h"):
    try:
        validate_apikey(apikey)
        r = await get_backtesting_data_stocks(timeframe=timeframe, start_datetime=start_date, end_datetime=end_date)
        # r = await get_backtesting_data_stocks(timeframe="15m", start_datetime=start_date, end_datetime=end_date)
        return r

    except HTTPException as e:
        app_logger().info("get_backtesting_data_stocks: ", str(e))
        raise HTTPException(500, detail=str(e))

    except Exception as e:
        app_logger().info("get_backtesting_data_stocks: ", str(e))
        raise HTTPException(500, detail=str(e))


# ---------------------------------- STOCKS ---------------------------------- #
@router_backtest_data_v1.get("/forex")
async def func(apikey: str = None, start_date: str = "2023-01-01", end_date: str = "2024-02-29", timeframe: str = "4h"):
    try:
        validate_apikey(apikey)
        r = await get_backtesting_data_forex(timeframe=timeframe, start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_forex(timeframe="2h", start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_forex(timeframe="1h", start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_forex(timeframe="30m", start_datetime=start_date, end_datetime=end_date)
        r = await get_backtesting_data_forex(timeframe="15m", start_datetime=start_date, end_datetime=end_date)
        return r

    except HTTPException as e:
        app_logger().info("get_backtesting_data_forex: ", str(e))
        raise HTTPException(500, detail=str(e))

    except Exception as e:
        app_logger().info("get_backtesting_data_forex: ", str(e))
        raise HTTPException(500, detail=str(e))
