from typing import List

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.is_background_task_running = False

    def set_is_background_task_running(self, value: bool):
        self.is_background_task_running = value

    def get_active_connections(self):
        return self.active_connections

    async def connect(self, websocket: WebSocket):
        try:
            await websocket.accept()
            if websocket not in self.active_connections:
                self.active_connections.append(websocket)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError as e:
            # print(e)
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            # print(e)
            pass

    async def broadcast_str(self, message: str):
        try:
            for connection in self.active_connections:
                await connection.send_text(message)
        except Exception as e:
            # print(e)
            pass

    async def broadcast_json(self, message: dict):
        try:
            for connection in self.active_connections:
                await connection.send_json(message)
        except Exception as e:
            self.disconnect(connection)
            # print(e)
