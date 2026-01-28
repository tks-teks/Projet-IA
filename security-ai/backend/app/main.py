from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.assistant.assistant_service import available_commands, process_query
from app.config import settings
from app.db import SessionLocal, init_db
from app.ingestion.parsers import parse_line
from app.ml.detector import detect_event
from app.ml.drift import update_threshold
from app.realtime.ws import manager
from app.response.voice import speak
from app.schemas import AssistantQuery

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    init_db()


@app.post("/events/ingest")
async def ingest_event(payload: dict):
    with SessionLocal() as session:
        detection = detect_event(session, payload)
        if detection:
            await manager.broadcast({"type": "new_alert", "data": detection})
            if detection.get("severity") == "CRITICAL":
                await manager.broadcast(
                    {
                        "type": "assistant_say",
                        "data": {
                            "text": f"Alerte critique : {detection.get('title')}",
                            "severity": "CRITICAL",
                        },
                    }
                )
    return {"status": "ok"}


@app.post("/logs/parse")
async def parse_log(payload: dict):
    source = payload.get("source", "system")
    line = payload.get("line", "")
    parsed = parse_line(source, line)
    parsed["source"] = source
    parsed["raw"] = line
    with SessionLocal() as session:
        detection = detect_event(session, parsed)
        if detection:
            await manager.broadcast({"type": "new_alert", "data": detection})
            if detection.get("severity") == "CRITICAL":
                await manager.broadcast(
                    {
                        "type": "assistant_say",
                        "data": {
                            "text": f"Alerte critique : {detection.get('title')}",
                            "severity": "CRITICAL",
                        },
                    }
                )
    return {"status": "parsed"}


@app.post("/assistant/query")
async def assistant_query(payload: AssistantQuery):
    response = process_query(payload.text)
    return response


@app.get("/assistant/commands")
async def assistant_commands():
    return {"commands": available_commands()}


@app.post("/assistant/speak")
async def assistant_speak(payload: dict):
    text = payload.get("text", "")
    if text:
        speak(text)
    return {"status": "spoken"}


@app.post("/settings/threshold/auto")
async def auto_threshold():
    with SessionLocal() as session:
        value = update_threshold(session)
    return {"threshold": value}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
