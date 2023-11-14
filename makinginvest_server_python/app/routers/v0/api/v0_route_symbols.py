from pandas import Timestamp
from _log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app.a_firebase.a_validate_api_key import validate_apikey


from app.helpers.data.symbols_crypto import (
    generate_binance_future_usdt_busd_csv,
    generate_binance_usdt_busd_csv,
    get_binance_data_daily_futures_symbol_value,
    get_binance_data_daily_spot_symbol_value,
    update_all_symbols_from_data_db_mongodb_aggr,
    update_all_symbols_mongodb_aggr,
    update_symbols_crypto_mongodb_aggr,
    update_symbols_forex_mongodb_aggr,
    update_symbols_stocks_mongodb_aggr,
)
from app.helpers.data.update_futures_symbols import update_future_prices_firestore

router_symbols_v0 = APIRouter()


@router_symbols_v0.patch("/symbols-all-from-data-db")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_all_symbols_from_data_db_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-all")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_all_symbols_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-crypto-futures")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_future_prices_firestore()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-crypto")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_symbols_crypto_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-forex")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_symbols_forex_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-stocks")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_symbols_stocks_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-generate-binance-usdt-busd")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await generate_binance_usdt_busd_csv()
        symbols = await get_binance_data_daily_spot_symbol_value()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router_symbols_v0.patch("/symbols-generate-binance-futures-usdt-busd")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await generate_binance_future_usdt_busd_csv()
        symbols = await get_binance_data_daily_futures_symbol_value()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
