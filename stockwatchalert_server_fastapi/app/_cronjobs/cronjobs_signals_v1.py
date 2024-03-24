import asyncio
import os
import time

import aiocron
import aiohttp
from fastapi import HTTPException
from _project.log_config.app_logger import app_logger
from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")
apikey = os.getenv("APIKEY")

BASE_URL = "http://makinginvest-python-engines-worker:8074"


# ---------------------------------- CRYPTO ---------------------------------- #
# @aiocron.crontab("*/15 * * * *")
# async def cron_signals_crypto_macd_momemtum_long_v1():
#     if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
#         app_logger().info("started crypto-1")
#         await asyncio.sleep(60 * 1)
#         start = time.time()
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.patch(f"{BASE_URL}/v1/signals/crypto-1?apikey={apikey}", timeout=1200) as response:
#                     await response.json()
#                     stat = f"crypto-1: {(time.time() - start) / 60:.2f} minutes"
#                     app_logger().info(stat)

#         except HTTPException as e:
#             app_logger().error("crypto-1: ", e)
#             raise e

#         except Exception as e:
#             app_logger().error("crypto-1", e)


@aiocron.crontab("*/15 * * * *")
async def cron_signals_crypto_macd_momemtum_long_v1():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
        app_logger().info("started crypto-2")
        await asyncio.sleep(60 * 1)
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"{BASE_URL}/v1/signals/crypto-2?apikey={apikey}", timeout=1200) as response:
                    await response.json()
                    stat = f"crypto-2: {(time.time() - start) / 60:.2f} minutes"
                    app_logger().info(stat)

        except HTTPException as e:
            app_logger().error("crypto-2: ", e)
            raise e

        except Exception as e:
            app_logger().error("crypto-2", e)


# ----------------------------------- FOREX ---------------------------------- #
@aiocron.crontab("*/15 * * * *")
async def cron_signals_forex_macd_momemtum_long_v1():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
        app_logger().info("started forex-1")
        await asyncio.sleep(60 * 1)
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"{BASE_URL}/v1/signals/forex-1?apikey={apikey}", timeout=1200) as response:
                    await response.json()
                    stat = f"forex-1: {(time.time() - start) / 60:.2f} minutes"
                    app_logger().info(stat)

        except HTTPException as e:
            app_logger().error("forex-1: ", e)
            raise e

        except Exception as e:
            app_logger().error("forex-2", e)


# ----------------------------------- STOCKS ---------------------------------- #
@aiocron.crontab("*/15 * * * *")
async def cron_signals_stocks_macd_momemtum_long_v1():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
        app_logger().info("started stocks-1")
        await asyncio.sleep(60 * 1)
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"{BASE_URL}/v1/signals/stocks-1?apikey={apikey}", timeout=1200) as response:
                    await response.json()
                    stat = f"stocks-1: {(time.time() - start) / 60:.2f} minutes"
                    app_logger().info(stat)

        except HTTPException as e:
            app_logger().error("stocks-1: ", e)
            raise e

        except Exception as e:
            app_logger().error("stocks-1", e)


@aiocron.crontab("*/15 * * * *")
async def cron_signals_stocks_macd_momemtum_long_v1():
    if is_production == "True" and is_allow_cron == "True" and is_data_mode != "True":
        app_logger().info("started stocks-2")
        await asyncio.sleep(60 * 1)
        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(f"{BASE_URL}/v1/signals/stocks-2?apikey={apikey}", timeout=1200) as response:
                    await response.json()
                    stat = f"stocks-1: {(time.time() - start) / 60:.2f} minutes"
                    app_logger().info(stat)

        except HTTPException as e:
            app_logger().error("stocks-2: ", e)
            raise e

        except Exception as e:
            app_logger().error("stocks-2", e)
