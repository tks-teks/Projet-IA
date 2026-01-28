import asyncio
from typing import Any, Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        async with self._lock:
            connections = list(self.active_connections)
        for connection in connections:
            await connection.send_json(message)


manager = ConnectionManager()
