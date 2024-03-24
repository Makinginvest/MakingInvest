import os
from logging.config import dictConfig
import warnings

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import app._firebase.firebase
from app._firebase.firebase import ensure_firebase_app
from _project.log_config.dict_config import log_config
from app._database.db_connect_data import close_mongodb_connection, connect_to_mongodb
from app.helpers.api.symbols_crypto import update_all_symbols_from_data_db_mongodb_aggr

warnings.simplefilter(action="ignore", category=FutureWarning)

# ---------------------------------- V1 CRON --------------------------------- #
import app._cronjobs.cronjobs_signals_v1

# --------------------------------- V1 ROUTES -------------------------------- #
from app.routers.v1.api.route_analysis_v1 import router_analysis_v1
from app.routers.v1.api.route_indexes_v1 import router_indexes_v1
from app.routers.v1.api.route_news_v1 import router_news_v1
from app.routers.v1.api.route_symbols_v1 import router_symbols_v1
from app.routers.v1.api.route_tracker_v1 import router_tracker_v1
from app.routers.v1.api.route_users_v1 import router_users_v1
from app.routers.v1.websockets.route_socketio_v1 import sio_app_v1
from app.routers.v1.signals.route_backtest_data_v1 import router_backtest_data_v1
from app.routers.v1.signals.route_signals_v1 import router_signals_v1
from app.routers.v1.api.route_signals_results_v1 import router_signals_results_v1
from app.routers.v1.api.route_screener_v1 import router_screener_v1

dictConfig(log_config)

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")
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
    app.mount("/socketio_v1", sio_app_v1)

if is_production != "True":
    app.mount("/socketio_v1", sio_app_v1)


@app.on_event("startup")
async def startup():
    await connect_to_mongodb()
    # await update_all_symbols_from_data_db_mongodb_aggr()
    ensure_firebase_app()


@app.on_event("shutdown")
async def shutdown():
    await close_mongodb_connection()


@app.get("/")
def read_root():
    return {" Hello": "World"}


# ------------------------------------ V1 ------------------------------------ #
app.include_router(router_analysis_v1)
app.include_router(router_indexes_v1)
app.include_router(router_news_v1)
app.include_router(router_symbols_v1)
app.include_router(router_tracker_v1)
app.include_router(router_users_v1)

app.include_router(router_backtest_data_v1)
app.include_router(router_signals_v1)
app.include_router(router_signals_results_v1)
app.include_router(router_screener_v1)
