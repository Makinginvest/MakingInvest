import asyncio
from asyncio import tasks
import os
import aiocron
from dotenv import load_dotenv
from app.helpers._functions_mongodb.crypto__mongodb_update import crypto_update_all_mongodb_historical_recent
from app.helpers._functions_mongodb.forex__mongodb_update import forex_update_all_mongodb_historical_recent
from app.helpers._functions_mongodb.stocks__mongodb_update import stocks_update_all_mongodb_historical_recent
from app.helpers.data.symbols_crypto import update_all_symbols_mongodb_aggr

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")


# # ---------------------------  CRYPTO --------------------------- #
@aiocron.crontab("*/5 * * * *")
async def cron_crypto_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        tasks = [crypto_update_all_mongodb_historical_recent(timeframe="5m", limit=30)]

        await asyncio.gather(*tasks)


@aiocron.crontab("*/15 * * * *")
async def cron_crypto_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        tasks = [
            crypto_update_all_mongodb_historical_recent(timeframe="15m", limit=20),
            crypto_update_all_mongodb_historical_recent(timeframe="1h", limit=50),
        ]
        await asyncio.gather(*tasks)


# ---------------------------  FOREX --------------------------- #
@aiocron.crontab("*/5 * * * *")
async def cron_forex_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        tasks = [
            forex_update_all_mongodb_historical_recent(granularity="M5", timeframe="5m"),
        ]
        await asyncio.gather(*tasks)


@aiocron.crontab("*/15 * * * *")
async def cron_forex_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        tasks = [
            forex_update_all_mongodb_historical_recent(granularity="M15", timeframe="15m"),
            forex_update_all_mongodb_historical_recent(granularity="D", timeframe="1d"),
        ]
        await asyncio.gather(*tasks)


# # ---------------------------  STOCKS --------------------------- #
# @aiocron.crontab("*/15 12-21 * * 1-5")
@aiocron.crontab("*/15 * * * *")
async def cron_stocks_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        tasks = [
            # stocks_update_all_mongodb_historical_recent(interval="5min", timeframe="5m"),
            stocks_update_all_mongodb_historical_recent(interval="15min", timeframe="15m"),
            stocks_update_all_mongodb_historical_recent(interval="1d", timeframe="1d"),
        ]
        await asyncio.gather(*tasks)


# ---------------------------- CRYPTO FOREX STOCKS --------------------------- #
# update database symbols everydat 12:07 am
@aiocron.crontab("7 0 * * *")
async def cron_crypto_update_symbols_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(5)
        await update_all_symbols_mongodb_aggr()
