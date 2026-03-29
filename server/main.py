"""World Server - relay + state storage.
- App connects via WebSocket (/ws/app)
- OpenClaw connects via WebSocket (/ws/openclaw) for real-time chat
- OpenClaw uses HTTP (/api/action, /api/state) for heartbeat/cron
"""
import asyncio
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from models import StateUpdate, AIPush
import state

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("world-server")

app_clients: list[WebSocket] = []
openclaw_ws: WebSocket | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("World Server starting on :8080")
    yield
    log.info("World Server shutting down.")


app = FastAPI(title="World Server", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HTTP API - OpenClaw heartbeat/cron (outbound from internal)
# ============================================================

@app.get("/api/state")
def api_get_state():
    """OpenClaw reads current world state."""
    return state.get_state().to_dict()


@app.post("/api/action")
async def api_action(push: AIPush):
    """OpenClaw heartbeat/cron updates state via HTTP.
    Also used by world_action tool during heartbeat.
    """
    if push.state_update:
        state.update_state(push.state_update)

    event = {
        "type": "ai_push",
        "state": state.get_state().to_dict(),
    }
    if push.message:
        event["message"] = push.message

    await broadcast_to_apps(event)
    log.info(f"HTTP action: scene={state.get_state().scene} action={state.get_state().action}")
    return {"ok": True, "state": state.get_state().to_dict()}


# ============================================================
# WebSocket - App clients
# ============================================================

@app.websocket("/ws/app")
async def ws_app(ws: WebSocket):
    await ws.accept()
    app_clients.append(ws)
    log.info(f"App connected. Total: {len(app_clients)}")

    # Send current state
    await ws.send_json({
        "type": "state_update",
        "state": state.get_state().to_dict(),
    })

    try:
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "user_message":
                await handle_user_message(data.get("message", ""))
            elif msg_type == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    finally:
        if ws in app_clients:
            app_clients.remove(ws)
        log.info(f"App disconnected. Total: {len(app_clients)}")


# ============================================================
# WebSocket - OpenClaw (like Discord Bot pattern)
# OpenClaw initiates connection from internal network.
# ============================================================

@app.websocket("/ws/openclaw")
async def ws_openclaw(ws: WebSocket):
    global openclaw_ws
    await ws.accept()
    openclaw_ws = ws
    log.info("OpenClaw connected via WebSocket.")

    # Send current state on connect
    await ws.send_json({
        "type": "state_sync",
        "state": state.get_state().to_dict(),
    })

    try:
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "ai_response":
                # AI replied to user chat message
                await handle_ai_response(data)
            elif msg_type == "ai_push":
                # AI-initiated state change (can also come via WS)
                await handle_ai_push(data)
            elif msg_type == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    finally:
        openclaw_ws = None
        log.info("OpenClaw disconnected.")


# ============================================================
# Handlers
# ============================================================

async def handle_user_message(message: str):
    """User sent chat message → forward to OpenClaw via WS."""
    state.set_engaged(True)

    # Push engaged state to apps
    await broadcast_to_apps({
        "type": "state_update",
        "state": state.get_state().to_dict(),
    })

    if openclaw_ws is None:
        await broadcast_to_apps({
            "type": "ai_response",
            "reply": "[小爱还没上线哦，稍等一下～]",
            "state": state.get_state().to_dict(),
        })
        return

    # Forward to OpenClaw
    await openclaw_ws.send_json({
        "type": "user_message",
        "message": message,
        "state": state.get_state().to_dict(),
        "timestamp": time.time(),
    })
    log.info(f"Forwarded to OpenClaw: {message[:50]}")


async def handle_ai_response(data: dict):
    """AI replied to user → push to App."""
    reply = data.get("reply", "")
    update = data.get("state_update")

    if update:
        state.update_state(StateUpdate(**update))

    await broadcast_to_apps({
        "type": "ai_response",
        "reply": reply,
        "state": state.get_state().to_dict(),
    })
    log.info(f"AI reply: {reply[:50]}")


async def handle_ai_push(data: dict):
    """AI-initiated state change via WS."""
    message = data.get("message")
    update = data.get("state_update")

    if update:
        state.update_state(StateUpdate(**update))

    event = {
        "type": "ai_push",
        "state": state.get_state().to_dict(),
    }
    if message:
        event["message"] = message

    await broadcast_to_apps(event)
    log.info(f"AI push: scene={state.get_state().scene}")


# ============================================================
# Broadcast
# ============================================================

async def broadcast_to_apps(event: dict):
    dead = []
    for ws in app_clients:
        try:
            await ws.send_json(event)
        except Exception:
            dead.append(ws)
    for ws in dead:
        app_clients.remove(ws)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
