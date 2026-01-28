from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from app.db import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50))
    raw = Column(Text)
    parsed_type = Column(String(50))
    user = Column(String(120))
    ip = Column(String(45))
    status = Column(String(50))
    message = Column(Text)


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    score = Column(Float)
    is_anomaly = Column(Boolean, default=False)
    reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    severity = Column(String(20))
    title = Column(String(120))
    description = Column(Text)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String(120), unique=True)
    value = Column(String(255))


class Blocklist(Base):
    __tablename__ = "blocklist"

    id = Column(Integer, primary_key=True)
    target = Column(String(120))
    reason = Column(String(255))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
