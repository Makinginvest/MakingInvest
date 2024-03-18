import asyncio
import os
import aiocron
from dotenv import load_dotenv
from app.helpers.data.symbols_crypto import update_all_symbols_from_data_db_mongodb_aggr

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")
is_allow_cron = os.getenv("ALLOW_CRON")


# update database symbols every hour at 7 minutes past the hour
@aiocron.crontab("7 * * * *")
async def cron_crypto_update_symbols_all_mongodb_historical_recent():
    if is_production == "True" and is_allow_cron == "True":
        await asyncio.sleep(60)
        await update_all_symbols_from_data_db_mongodb_aggr()
