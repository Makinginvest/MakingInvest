import asyncio
import os
import aiocron
from dotenv import load_dotenv
from app.helpers.a_functions_mongodb.crypto__mongodb_update import crypto_update_all_mongodb_historical_recent
from app.helpers.a_functions_mongodb.forex__mongodb_update import forex_update_all_mongodb_historical_recent
from app.helpers.a_functions_mongodb.stocks__mongodb_update import stocks_update_all_mongodb_historical_recent
from app.helpers.data.symbols_crypto import update_all_symbols_mongodb_aggr

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")


# # ---------------------------  CRYPTO --------------------------- #
@aiocron.crontab("*/5 * * * *")
async def cron_crypto_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await crypto_update_all_mongodb_historical_recent(timeframe="5m", limit=45)


@aiocron.crontab("*/15 * * * *")
async def cron_crypto_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await crypto_update_all_mongodb_historical_recent(timeframe="15m", limit=45)


@aiocron.crontab("0 */4 * * *")
async def cron_crypto_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await asyncio.sleep(75)
        await crypto_update_all_mongodb_historical_recent(timeframe="1h", limit=96)


# update database symbols everydat 12:07 am
@aiocron.crontab("7 0 * * *")
async def cron_stocks_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await update_all_symbols_mongodb_aggr()


# # ---------------------------  FOREX --------------------------- #
@aiocron.crontab("*/5 16-23 * * 0")  # every 5 minutes between 4 PM to 12 Midnight every Sunday,
async def cron_forex_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await forex_update_all_mongodb_historical_recent()


@aiocron.crontab("*/5 0-23 * * 1-5")  # every 5 minutes between 12 Midnight to 12 Midnight every Monday to Friday,
async def cron_forex_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await forex_update_all_mongodb_historical_recent()


# # ---------------------------  STOCKS --------------------------- #
@aiocron.crontab("*/15 12-21 * * 1-5")
async def cron_stocks_update_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await stocks_update_all_mongodb_historical_recent()
