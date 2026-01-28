from typing import Dict, Optional

import joblib
from sqlalchemy.orm import Session

from app.config import settings
from app.features.feature_builder import build_features
from app.models import Alert, Detection, Event, Setting
from app.response.policy import build_alert


def load_model():
    if settings.model_path.exists():
        return joblib.load(settings.model_path)
    return None


def get_threshold(session: Session) -> float:
    setting = session.query(Setting).filter_by(key=settings.threshold_setting_key).first()
    if setting:
        return float(setting.value)
    return settings.default_threshold


def store_event(session: Session, payload: Dict[str, str]) -> Event:
    event = Event(**payload)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def detect_event(session: Session, payload: Dict[str, str]) -> Optional[Dict[str, str]]:
    event = store_event(session, payload)
    model = load_model()
    if not model:
        return None
    features = build_features(payload).reshape(1, -1)
    score = float(model.decision_function(features)[0])
    threshold = get_threshold(session)
    is_anomaly = score < threshold
    detection = Detection(event_id=event.id, score=score, is_anomaly=is_anomaly, reason="IsolationForest")
    session.add(detection)
    session.commit()
    if is_anomaly:
        alert_payload = build_alert(event, score)
        alert = Alert(**alert_payload)
        session.add(alert)
        session.commit()
        return {
            "id": alert.id,
            "event_id": event.id,
            "severity": alert.severity,
            "title": alert.title,
            "description": alert.description,
        }
    return None
