from _project.log_config.app_logger import app_logger


from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app._security.a_validate_api_key import validate_apikey


from app.helpers.data.symbols_crypto import (
    generate_binance_usdt_busd_csv,
    update_all_symbols_mongodb_aggr,
    update_symbols_crypto_futures_mongodb_aggr,
    update_symbols_crypto_mongodb_aggr,
    update_symbols_forex_mongodb_aggr,
    update_symbols_stocks_mongodb_aggr,
)

router = APIRouter(prefix="/v1")


@router.patch("/symbols-all")
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


@router.patch("/symbols-crypto")
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


@router.patch("/symbols-crypto-futures")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await update_symbols_crypto_futures_mongodb_aggr()
        return symbols

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)


@router.patch("/symbols-forex")
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


@router.patch("/symbols-stocks")
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


@router.patch("/symbols-generate-binance-usdt-busd")
async def patch_signals(apikey: str = None):
    try:
        validate_apikey(apikey)
        symbols = await generate_binance_usdt_busd_csv()
        return symbols.to_dict("records")

    except HTTPException as e:
        raise e

    except Exception as e:
        app_logger().info("Error generating news: ", e)
        raise HTTPException(500, detail=e)
