import asyncio
import os

import motor.motor_asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from _log_config.app_logger import app_logger

load_dotenv()


is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")


conection_string_mongodb = os.getenv("MONGO_URI_DROPLET_EXTERNAL_CLIENT")

if is_production == "True":
    conection_string_mongodb = os.getenv("MONGO_URI_DROPLET_EXTERNAL_CLIENT")


client: AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(conection_string_mongodb)
client.get_io_loop = asyncio.get_event_loop
database_mongodb_client = client.makinginvestClientSignals


async def connect_to_mongodb():
    global client
    global database_mongodb_client

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(conection_string_mongodb)
        database_mongodb_client = client.makinginvestClientSignals
        return database_mongodb_client

    except Exception as e:
        print("Connection to MongoDB failed")
        app_logger.error("Connection to MongoDB failed")
        raise Exception("Connection to MongoDB failed", e)


async def close_mongodb_connection():
    global client
    client.close()
