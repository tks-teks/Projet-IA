from typing import Dict, List

from app.assistant.intents import INTENTS, detect_intent
from app.assistant.responder import build_reply


def process_query(text: str) -> Dict[str, object]:
    intent, confidence = detect_intent(text)
    reply_payload = build_reply(intent)
    return {
        "intent": intent,
        "confidence": confidence,
        "reply": reply_payload["reply"],
        "ui": reply_payload["ui"],
        "tts": True,
    }


def available_commands() -> List[str]:
    commands = []
    for intent, keywords in INTENTS.items():
        commands.append(f"{intent}: {', '.join(keywords)}")
    return commands
