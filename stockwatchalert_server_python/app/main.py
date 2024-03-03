import asyncio
import os
from logging.config import dictConfig

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import app.a_cronjobs.cronjobs_data_general
import app.a_cronjobs.cronjobs_signals_crypto
import app.a_cronjobs.cronjobs_signals_forex
import app.a_cronjobs.cronjobs_signals_stocks
import app.a_firebase.firebase
from app.a_firebase.firebase import ensure_firebase_app
from _log_config.dict_config import log_config


from app.a_database_data.db_connect_data import close_mongodb_connection, connect_to_mongodb
from app.helpers.data.symbols_crypto import update_all_symbols_from_data_db_mongodb_aggr
from app.routers.v0.api.v0_route_analysis import v0_router_analysis
from app.routers.v0.api.v0_route_indexes import v0_router_indexes
from app.routers.v0.api.v0_route_news import v0_router_news
from app.routers.v0.api.v0_route_signals_results import v0_router_signals_results
from app.routers.v0.api.v0_route_symbols_rank import router_symbols_rank_v0
from app.routers.v0.api.v0_route_symbols import router_symbols_v0
from app.routers.v0.api.v0_route_tracker import router_tracker_v0
from app.routers.v0.api.v0_route_users import router_users_v0
from app.routers.v0.signals.v0_route_signals_live import router_signals_live_v0
from app.routers.v0.websockets.v0_route_socketio import sio_app

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


if is_websocket_mode == "True":
    app.mount("/socketio", sio_app)

app.mount("/socketio", sio_app)


@app.on_event("startup")
async def startup():
    await connect_to_mongodb()
    await update_all_symbols_from_data_db_mongodb_aggr()
    ensure_firebase_app()


@app.on_event("shutdown")
async def shutdown():
    await close_mongodb_connection()


@app.get("/")
def read_root():
    return {" Hello": "World"}


app.include_router(v0_router_analysis)
app.include_router(v0_router_indexes)
app.include_router(v0_router_news)
app.include_router(router_signals_live_v0)
app.include_router(v0_router_signals_results)
app.include_router(router_symbols_rank_v0)
app.include_router(router_symbols_v0)
app.include_router(router_tracker_v0)
app.include_router(router_users_v0)

#
