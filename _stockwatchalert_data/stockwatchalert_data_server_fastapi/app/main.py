import asyncio
from logging.config import dictConfig
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.helpers.data.symbols_crypto import update_all_symbols_mongodb_aggr

from app.routers.v1.mongodb import route_crypto_mongodb_v1
from app.routers.v1.mongodb import route_forex_mongodb_v1
from app.routers.v1.mongodb import route_stocks_mongodb_v1

from app.routers.v1.api import route_symbols_v1
from app.routers.v1.api import route_indexes_v1
from app.routers.v1.api import route_news_v1
from app.routers.v1.api import route_prices_v1
from app.routers.v1.api import route_analysis_v1
from app.routers.v1.api import route_tracker_v1


import app._cronjobs.cronjobs_data_database
import app._cronjobs.cronjobs_data_general


from _project.log_config.dict_config import log_config
from app._database_data.db_connect_data import close_mongodb_connection, connect_to_mongodb

dictConfig(log_config)

load_dotenv()
is_production = os.getenv("PRODUCTION")
is_allow_cron = os.getenv("ALLOW_CRON")
is_data_mode = os.getenv("DATA_MODE")
is_websocket_mode = os.getenv("WEBSOCKET_MODE")

show_docs = True
if is_production == "True" or is_data_mode == "True" or is_websocket_mode == "True" or is_allow_cron == "False":
    show_docs = False


app = FastAPI() if show_docs else FastAPI(docs_url=None, redoc_url=None)


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup():
    await connect_to_mongodb()
    if is_production == "True":
        asyncio.create_task(update_all_symbols_mongodb_aggr())


@app.on_event("shutdown")
async def shutdown():
    await close_mongodb_connection()


@app.get("/")
def read_root():
    return {" Hello": "World"}


app.include_router(route_crypto_mongodb_v1.router)
app.include_router(route_forex_mongodb_v1.router)
app.include_router(route_stocks_mongodb_v1.router)

app.include_router(route_symbols_v1.router)
app.include_router(route_news_v1.router)
app.include_router(route_prices_v1.router)
app.include_router(route_analysis_v1.router)
app.include_router(route_tracker_v1.router)

app.include_router(route_indexes_v1.router)
