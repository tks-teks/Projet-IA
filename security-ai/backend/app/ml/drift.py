from sqlalchemy.orm import Session

from app.config import settings
from app.models import Detection, Setting


def update_threshold(session: Session) -> float:
    recent = session.query(Detection).order_by(Detection.created_at.desc()).limit(100).all()
    if not recent:
        return settings.default_threshold
    avg_score = sum(det.score for det in recent) / len(recent)
    new_threshold = min(settings.default_threshold, avg_score - 0.05)
    setting = session.query(Setting).filter_by(key=settings.threshold_setting_key).first()
    if setting:
        setting.value = str(new_threshold)
    else:
        setting = Setting(key=settings.threshold_setting_key, value=str(new_threshold))
        session.add(setting)
    session.commit()
    return new_threshold
