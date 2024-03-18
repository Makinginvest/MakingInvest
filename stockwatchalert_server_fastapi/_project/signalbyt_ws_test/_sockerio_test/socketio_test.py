import json
import socketio
import asyncio


sio = socketio.AsyncClient()


async def connect_socketio():
    try:
        await sio.connect(
            "ws://0.0.0.0:9999",
            socketio_path="socketio_v1/socket.io",
            transports="websocket",
            headers={"apikey": "Qqf3afqfqe82B6s3G1", "appBuildNumber": "1000"},
        )
        await sio.wait()
        print("connected")
    except Exception as e:
        print("error", e)


# @sio.on("prices_crypto")
# def on_message(message):
#     print("crypto data", len(message["data"]))


# @sio.on("prices_forex")
# def on_message(message):
#     print("forex data", len(message["data"]))


# @sio.on("prices_stocks")
# def on_message(message):
#     print("stock data", len(message["data"]))


@sio.on("signal_aggr_open_v1")
def on_message(message):
    data = message.get("data")
    print("signal_aggr_open data", len(data))


# @sio.on("market_analysis")
# def on_message(message):
#     data = message.get("data")
#     print("market_analysis data", len(data))


# @sio.on("symbols_tracker")
# def on_message(message):
#     data = message.get("data")
#     print("symbols_tracker data", len(data))


@sio.event
async def message(data):
    print("I received a message!")


asyncio.run(connect_socketio())
