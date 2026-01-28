from typing import Dict

from app.config import settings
from app.models import Event


def build_alert(event: Event, score: float) -> Dict[str, str]:
    if score < settings.critical_threshold:
        severity = "CRITICAL"
    elif score < settings.default_threshold:
        severity = "HIGH"
    else:
        severity = "MEDIUM"
    title = f"Anomalie {event.parsed_type or 'log'} détectée"
    description = f"Score {score:.2f} sur {event.source}: {event.message}"
    return {
        "event_id": event.id,
        "severity": severity,
        "title": title,
        "description": description,
    }
