import asyncio
import os
import aiocron
from dotenv import load_dotenv
from app.helpers.api.symbols_crypto import update_all_symbols_from_data_db_mongodb_aggr
from app.helpers.api.screener_stock import run_screener_stock

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")
is_allow_cron = os.getenv("ALLOW_CRON")


# update database symbols every hour at 7 minutes past the hour
@aiocron.crontab("7 * * * *")
async def cron_crypto_update_symbols_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True":
        await asyncio.sleep(60)
        await update_all_symbols_from_data_db_mongodb_aggr()


@aiocron.crontab("8 0 * * *")
async def cron_daily_task():
    if is_production == "True" and is_allow_cron == "True":
        await asyncio.sleep(1)
        await run_screener_stock()
