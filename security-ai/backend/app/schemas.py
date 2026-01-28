from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class EventOut(BaseModel):
    id: int
    timestamp: datetime
    source: str
    raw: str
    parsed_type: Optional[str]
    user: Optional[str]
    ip: Optional[str]
    status: Optional[str]
    message: Optional[str]


class AlertOut(BaseModel):
    id: int
    event_id: int
    severity: str
    title: str
    description: str
    acknowledged: bool
    created_at: datetime


class AssistantQuery(BaseModel):
    text: str
    context: Dict[str, Any] = {}


class AssistantResponse(BaseModel):
    intent: str
    confidence: float
    reply: str
    ui: Dict[str, Any]
    tts: bool
