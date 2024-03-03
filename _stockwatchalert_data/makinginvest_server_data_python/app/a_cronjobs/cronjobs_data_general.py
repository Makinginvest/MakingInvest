import asyncio
import os

import aiocron
from dotenv import load_dotenv

from app.helpers.data.get_news_data import update_all_news_mongodb_aggr
from app.helpers.market_analysis.market_analysis import update_market_analysis
from app.helpers.prices.prices_crypto import getPricesCrypto
from app.helpers.prices.prices_forex import getPricesForex
from app.helpers.prices.prices_stocks import getPricesStocks
from app.helpers.tracker.symbols_tracker import update_symbol_tracker_all

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")


# ------------------------------  NEWS CRON ----------------------------- #
@aiocron.crontab("*/10 * * * *")
async def cron_news():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await update_all_news_mongodb_aggr()


# ------------------------------  PRICES CRON ----------------------------- #
# every 10 sec
@aiocron.crontab("* * * * * */10")
async def cron_prices():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await getPricesCrypto()


@aiocron.crontab("* * * * * */30")
async def cron_prices():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await getPricesStocks()


# every 1 min
@aiocron.crontab("* * * * *")
async def cron_prices():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await getPricesForex()


# ------------------------------ MARKET ANALYSIS ----------------------------- #
@aiocron.crontab("*/15 * * * *")
async def cron_tracker():
    await asyncio.sleep(120)
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await update_market_analysis()


# ------------------------------ TRACKER ----------------------------- #
# job will execute 24 times in a day, specifically at the 3rd minute of each hour
@aiocron.crontab("3 * * * *")
async def cron_tracker():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode == "True":
        await update_symbol_tracker_all()
