import socketio
import asyncio


sio = socketio.AsyncClient()


async def connect_sockerio():
    await sio.connect("ws://0.0.0.0:8999", socketio_path="socketio-crypto/socket.io", transports="websocket")
    await sio.wait()


@sio.on("prices")
def on_message(data):
    print("I received a message!", data)


@sio.event
async def message(data):
    print("I received a message!")


asyncio.run(connect_sockerio())
