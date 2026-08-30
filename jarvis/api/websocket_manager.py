# ==================================================
# JARVIS AI — Real-time WebSocket Connection Manager
# ==================================================

import json
import logging
from typing import List
from fastapi import WebSocket

logger = logging.getLogger("jarvis.api.ws")


class WebSocketManager:
    """
    Manages connected Web/Desktop HUD clients and broadcasts telemetry,
    voice waveforms, task progress, and permission popups.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"HUD Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"HUD Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Send JSON payload to all active clients."""
        dead_connections = []
        payload = json.dumps(message)

        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)


ws_manager = WebSocketManager()
