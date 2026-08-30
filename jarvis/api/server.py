# ==================================================
# JARVIS AI — FastAPI REST & Real-time WebSocket Server
# ==================================================

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

try:
    import psutil
except ImportError:
    psutil = None

from jarvis.api.schemas import (
    ChatRequest,
    ChatResponse,
    PermissionDecisionRequest,
    SystemStatusResponse,
    WorkflowCreateRequest,
)
from jarvis.api.websocket_manager import ws_manager
from jarvis.config.constants import PermissionLevel, PermissionScope
from jarvis.config.settings import settings
from jarvis.core.agent import agent
from jarvis.core.permission_manager import permission_manager
from jarvis.memory.conversation_history import conversation_history
from jarvis.memory.long_term_memory import long_term_memory
from jarvis.memory.user_preferences import user_preferences
from jarvis.tools.registry import tool_registry

logger = logging.getLogger("jarvis.api.server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing JARVIS API & Agent subsystems...")
    # Link agent events to WebSocket broadcaster
    agent.set_hud_broadcaster(ws_manager.broadcast)
    
    # Set up interactive permission handler via WebSocket broadcast
    async def prompt_ui_for_permission(scope: str, action: str, target: str = None) -> str:
        req_id = f"perm_{asyncio.get_event_loop().time()}"
        fut = asyncio.get_event_loop().create_future()
        permission_manager._pending_requests[req_id] = fut

        await ws_manager.broadcast({
            "type": "permission_request",
            "request_id": req_id,
            "scope": scope,
            "action": action,
            "target": target,
        })
        try:
            # Wait up to 30 seconds for user response
            decision = await asyncio.wait_for(fut, timeout=30.0)
            return decision
        except asyncio.TimeoutError:
            permission_manager._pending_requests.pop(req_id, None)
            return PermissionLevel.DENY.value

    permission_manager.set_prompt_handler(prompt_ui_for_permission)
    yield
    logger.info("JARVIS API Server shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Enable CORS for Next.js / React / Mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from jarvis.voice.speaker import speaker

# --------------------------------------------------
# REST Endpoints
# --------------------------------------------------
@app.get("/api/status", response_model=SystemStatusResponse)
async def get_status():
    battery_obj = psutil.sensors_battery() if psutil else None
    battery = f"{battery_obj.percent}%" if battery_obj else "AC Power"
    return SystemStatusResponse(
        cpu_percent=psutil.cpu_percent() if psutil else 15.0,
        ram_percent=psutil.virtual_memory().percent if psutil else 40.0,
        disk_percent=(psutil.disk_usage("C:").percent if psutil.WINDOWS else psutil.disk_usage("/").percent) if psutil else 50.0,
        battery=battery,
        ai_provider=settings.AI_PROVIDER,
        active_tools_count=len(tool_registry.list_tools()),
        online=True,
    )


@app.post("/api/chat", response_model=ChatResponse)
async def post_chat(req: ChatRequest):
    response_text = await agent.process_input(req.message)
    if response_text:
        await speaker.speak_async(response_text)
    return ChatResponse(response=response_text, success=True)


@app.get("/api/tools")
async def get_tools():
    return {"tools": tool_registry.get_schemas()}


@app.get("/api/memory")
async def get_memory():
    return {"memories": long_term_memory.all()}


@app.post("/api/memory")
async def add_memory(payload: Dict[str, str]):
    text = payload.get("text", "")
    item = long_term_memory.add(text)
    return {"success": True, "memory": item}


@app.delete("/api/memory/{memory_id}")
async def delete_memory(memory_id: str):
    success = long_term_memory.remove(memory_id)
    return {"success": success}


@app.get("/api/permissions")
async def get_permissions():
    return {"permissions": permission_manager.get_status()}


@app.post("/api/permissions/decision")
async def post_permission_decision(payload: Dict[str, str]):
    req_id = payload.get("request_id")
    decision = payload.get("decision", "deny")
    if req_id:
        permission_manager.resolve_external_decision(req_id, decision)
    return {"success": True}


@app.get("/api/preferences")
async def get_preferences():
    return user_preferences.get_all()


@app.post("/api/preferences")
async def update_preferences(data: Dict[str, Any]):
    for k, v in data.items():
        user_preferences.set(k, v)
    return {"success": True, "preferences": user_preferences.get_all()}


@app.get("/api/history")
async def get_history():
    return {"history": conversation_history.get_recent(50)}


# --------------------------------------------------
# WebSocket Endpoint for HUD Realtime Streaming
# --------------------------------------------------
@app.websocket("/ws/hud")
async def websocket_hud_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send initial full state upon connection
        await websocket.send_json({
            "type": "init_state",
            "preferences": user_preferences.get_all(),
            "permissions": permission_manager.get_status(),
            "tools": tool_registry.get_schemas(),
            "memories": long_term_memory.all(),
            "history": conversation_history.get_recent(30),
        })

        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            if event_type == "user_message":
                msg = data.get("message", "")
                resp = await agent.process_input(msg)
                await websocket.send_json({"type": "assistant_response", "text": resp})

            elif event_type == "permission_response":
                req_id = data.get("request_id")
                decision = data.get("decision", "deny")
                if req_id:
                    permission_manager.resolve_external_decision(req_id, decision)

            elif event_type == "gesture_event":
                from jarvis.vision.gesture_detection import gesture_bridge
                mode = data.get("mode", "idle")
                hands = data.get("hands", 0)
                gesture_bridge.handle_gesture_event(mode, hands)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket exception: {e}")
        ws_manager.disconnect(websocket)
