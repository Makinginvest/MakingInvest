import asyncio
import datetime
import os
from typing import List
import socketio
from dotenv import load_dotenv
from fastapi import APIRouter
from _log_config.app_logger import app_logger
from app.a_firebase.a_validate_key_jsonwebtoken import validate_apikey_json_webtoken_bool

from app.classes.connection_socketio import ConnectionManagerSockerIo
from app.a_database_data.db_connect_data import database_mongodb_data
from app.a_database_client.db_connect_client import database_mongodb_client


from utils.convert_bson_json import convert_bson_json

router_websocket_v0 = APIRouter()
manager = ConnectionManagerSockerIo()

load_dotenv()
is_websocket_mode = os.getenv("WEBSOCKET_MODE")

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio)


@sio.event
async def connect(sid, data):
    jsonWebToken = data.get("HTTP_JSONWEBTOKEN", "")
    apikey = data.get("HTTP_APIKEY", "")
    appBuildNumber = data.get("HTTP_APPBUILDNUMBER", 0)
    is_token_valid = validate_apikey_json_webtoken_bool(apikey=apikey, token=jsonWebToken)
    if not is_token_valid and int(appBuildNumber) >= 55:
        app_logger().error(f"token not valid {jsonWebToken} {apikey} {appBuildNumber}")
        return False

    asyncio.create_task(start_background_tasks_crypto_prices(manager=manager, sid=sid))
    asyncio.create_task(start_background_tasks_forex_prices(manager=manager, sid=sid))
    asyncio.create_task(start_background_tasks_stocks_prices(manager=manager, sid=sid))

    asyncio.create_task(start_background_tasks_market_analysis(manager=manager, sid=sid))
    asyncio.create_task(start_background_tasks_symbols_tracker(manager=manager, sid=sid))

    asyncio.create_task(start_background_tasks_news_aggr(manager=manager, sid=sid))
    asyncio.create_task(start_background_signal_aggr_open_mongodb(manager=manager, sid=sid))

    await sio.emit("connect", f"connected {sid} ", room=sid)


@sio.event
def connect_error(data):
    print("connect_error", data)


@sio.event
def disconnect(sid):
    print("disconnect", sid)


async def start_background_tasks_crypto_prices(manager: ConnectionManagerSockerIo, sid=None):
    if len(manager.prices_crypto) > 0:
        await sio.emit("prices_crypto", {"data": manager.prices_crypto}, room=sid)

    if not manager.is_background_task_running_crypto and is_websocket_mode == "True":
        while True:
            data = []

            manager.set_is_background_task_running_crypto(True)
            try:
                data = await getPricesMongodbData("crypto")
                if len(data) > 0:
                    await sio.emit("prices_crypto", {"data": data})
                    manager.set_is_background_task_running_crypto(True)
                    manager.set_prices_crypto(data)

                await asyncio.sleep(15)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_crypto(False)
                manager.set_prices_crypto([])


async def start_background_tasks_forex_prices(manager: ConnectionManagerSockerIo, sid=None):
    if len(manager.prices_forex) > 0:
        await sio.emit("prices_forex", {"data": manager.prices_forex}, room=sid)

    if not manager.is_background_task_running_forex and is_websocket_mode == "True":
        while True:
            data = []

            manager.set_is_background_task_running_forex(True)
            try:
                data = await getPricesMongodbData("forex")
                if len(data) > 0:
                    await sio.emit("prices_forex", {"data": data})
                    manager.set_is_background_task_running_forex(True)
                    manager.set_prices_forex(data)

                await asyncio.sleep(30)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_forex(False)
                manager.set_prices_forex([])


async def start_background_tasks_stocks_prices(manager: ConnectionManagerSockerIo, sid=None):
    if len(manager.prices_stocks) > 0:
        await sio.emit("prices_stocks", {"data": manager.prices_stocks}, room=sid)

    if not manager.is_background_task_running_stocks and is_websocket_mode == "True":
        while True:
            data = []

            manager.set_is_background_task_running_stocks(True)
            try:
                data = await getPricesMongodbData("stocks")
                if len(data) > 0:
                    await sio.emit("prices_stocks", {"data": data})
                    manager.set_is_background_task_running_stocks(True)
                    manager.set_prices_stocks(data)

                await asyncio.sleep(30)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_stocks(False)
                manager.set_prices_stocks([])


async def start_background_tasks_market_analysis(manager: ConnectionManagerSockerIo, sid=None):
    if manager.market_analysis is not None and manager.market_analysis.get("cryptoSymbolsAnalysis") is not None:
        data = convert_bson_json(manager.market_analysis)
        await sio.emit("market_analysis", {"data": data}, room=sid)

    if not manager.is_background_task_running_market_analysis and is_websocket_mode == "True":
        while True:
            manager.set_is_background_task_running_market_analysis(True)
            try:
                collection = database_mongodb_data["marketAnalysis"]
                data = await collection.find_one({"name": "marketAnalysis"})
                #

                if data is not None and data["dtUpdated"] != manager.dt_market_analysis_updated:
                    manager.set_dt_market_analysis_updated(data["dtUpdated"])
                    manager.set_market_analysis(data)

                    data = convert_bson_json(data)
                    await sio.emit("market_analysis", {"data": data})

                await asyncio.sleep(30)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_market_analysis(False)
                manager.set_market_analysis(None)
                await asyncio.sleep(30)


async def start_background_tasks_symbols_tracker(manager: ConnectionManagerSockerIo, sid=None):
    if manager.symbols_tracker is not None:
        data = convert_bson_json(manager.symbols_tracker)
        await sio.emit("symbols_tracker", {"data": data}, room=sid)

    if not manager.is_background_task_running_symbols_tracker and is_websocket_mode == "True":
        while True:
            manager.set_is_background_task_running_symbols_tracker(True)
            try:
                collection = database_mongodb_data["symbolsTracker"]
                data = await collection.find_one({"name": "symbolsTracker"})
                #

                if data is not None and data["dtUpdated"] != manager.dt_symbols_tracker_updated:
                    manager.set_dt_symbols_tracker_updated(data["dtUpdated"])
                    manager.set_symbols_tracker(data)

                    data = convert_bson_json(data)
                    await sio.emit("symbols_tracker", {"data": data})

                await asyncio.sleep(30)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_symbols_tracker(False)
                manager.set_symbols_tracker(None)
                await asyncio.sleep(30)


async def start_background_tasks_news_aggr(manager: ConnectionManagerSockerIo, sid=None):
    if manager.news_aggr is not None:
        data = convert_bson_json(manager.news_aggr)
        await sio.emit("news_aggr", {"data": data}, room=sid)

    if not manager.is_background_task_running_news_aggr and is_websocket_mode == "True":
        while True:
            manager.set_is_background_task_running_news_aggr(True)
            try:
                collection = database_mongodb_data["news"]
                data = await collection.find_one({"type": "all"})
                #

                if data is not None and data["dtNewsAggrUpdated"] != manager.dt_news_aggr_updated:
                    manager.set_dt_news_aggr_updated(data["dtNewsAggrUpdated"])
                    manager.set_news_aggr(data)

                    data = convert_bson_json(data)
                    await sio.emit("news_aggr", {"data": data})

                await asyncio.sleep(30)

            except Exception as e:
                print(e)
                manager.set_is_background_task_running_news_aggr(False)
                manager.set_news_aggr(None)
                app_logger.error(e)
                await asyncio.sleep(30)


async def start_background_signal_aggr_open_mongodb(manager: ConnectionManagerSockerIo, sid=None):
    if len(manager.signal_aggr_open) > 0:
        await sio.emit("signal_aggr_open", {"data": manager.signal_aggr_open}, room=sid)

    if not manager.is_background_task_running_signal_aggr_open and is_websocket_mode == "True":
        while True:
            try:
                run_update, lastUpdateDatetime = await get_signals_aggr_open_mongodb_lastest_change(manager.dt_signal_aggr_open_updated, manager.signal_aggr_open)
                manager.set_dt_signal_aggr_open_updated(lastUpdateDatetime)

                if run_update:
                    data = await get_signals_aggr_open_mongodb()
                    data = convert_bson_json(data)
                    manager.set_signal_aggr_open(data)
                    await sio.emit("signal_aggr_open", {"data": data})

                await asyncio.sleep(10)

            except Exception as e:
                manager.set_is_background_task_running_signal_aggr_open(False)
                manager.set_signal_aggr_open([])
                app_logger().error("start_background_signal_aggr_open_mongodb %s", e)
                await asyncio.sleep(10)


# ------------------- GET AGGR SIGNALS OPEN MONGODB CLIENT ------------------- #
async def get_signals_aggr_open_mongodb():
    try:
        collection = database_mongodb_client["signalsAggrOpen"]
        data = await collection.find({"nameIsActive": True}).to_list(length=100)

        if len(data) > 0:
            for d in data:
                d["_id"] = str(d["_id"])
            return data
        return []

    except Exception as e:
        return []


# ------------- VALIDATE IF THERE IS A NEW UPDATE IN THE MONGODB ------------- #
async def get_signals_aggr_open_mongodb_lastest_change(lastUpdatedDateTime: datetime, signalsAggr: List):
    try:
        collection = database_mongodb_client["appControlsPrivate"]

        if lastUpdatedDateTime is None:
            query = await collection.find({"name": "appControlsPrivate"}).limit(1).to_list(length=1)
            if query:
                return True, query[0].get("dtSignalsAggrOpenUpdated")

            return False, lastUpdatedDateTime
        query = await collection.find({"name": "appControlsPrivate", "dtSignalsAggrOpenUpdated": {"$gt": lastUpdatedDateTime}}).limit(1).to_list(length=1)

        if query:
            return True, query[0].get("dtSignalsAggrOpenUpdated")

        return False, lastUpdatedDateTime

    except Exception as e:
        print(e)
        return True, None


# ----------------------- GET PRICES FROM MONGODB DATA ----------------------- #
async def getPricesMongodbData(type):
    try:
        collection = database_mongodb_data["prices"]
        data = await collection.find_one({"type": type})

        if data:
            return data.get("data", [])
        return []

    except Exception as e:
        return []
