import asyncio
import os
import time

import aiocron
import aiohttp
from fastapi import HTTPException
from _log_config.app_logger import app_logger
from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")
apikey = os.getenv("APIKEY")

BASE_URL = "https://makinginvest-server-python-api-engines-all-v1.makinginvest.com"
BASE_URL = "http://makinginvest-python-engines-all:8074"


# Sunday: 17:00 to 23:45, every 15 minutes (0)
@aiocron.crontab("*/15 17-23 * * 0")
async def call_cron():
    await cron_signals_forex_macd_momemtum_long_v1()


# Monday to Thursday: every 15 minutes
@aiocron.crontab("*/15 0-23 * * 1-4")
async def call_cron():
    await cron_signals_forex_macd_momemtum_long_v1()


# Friday: 00:00 to 17:00, every 15 minutes (0)
@aiocron.crontab("*/15 0-17 * * 5")
async def call_cron():
    await cron_signals_forex_macd_momemtum_long_v1()


# cron
async def cron_signals_forex_macd_momemtum_long_v1():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
        app_logger().error("started signals-forex-all-live1")
        await asyncio.sleep(60)
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"{BASE_URL}/signals-forex-all-live1?apikey={apikey}", timeout=1200) as response:
                    await response.json()
                    stat = f"signals-forex-all-live1: {(time.time() - start) / 60:.2f} minutes"
                    app_logger().info(stat)
        except HTTPException as e:
            app_logger().info("signals-forex-all-live1: ", e)
            raise e
        except Exception as e:
            app_logger().error("signals-forex-all-live1", e)
