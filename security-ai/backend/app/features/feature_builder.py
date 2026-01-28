from typing import Dict, List

import numpy as np

FEATURE_COLUMNS = [
    "is_auth_fail",
    "is_web_5xx",
    "is_system_error",
    "hour",
    "message_length",
]


def build_features(event: Dict[str, str]) -> np.ndarray:
    is_auth_fail = 1 if event.get("parsed_type") == "auth" and event.get("status") == "FAIL" else 0
    is_web_5xx = 1 if event.get("parsed_type") == "web" and str(event.get("status", "")).startswith("5") else 0
    is_system_error = 1 if event.get("parsed_type") == "system" and event.get("status") == "ERROR" else 0
    hour = event.get("timestamp").hour if event.get("timestamp") else 0
    message_length = len(event.get("message", ""))
    return np.array([is_auth_fail, is_web_5xx, is_system_error, hour, message_length], dtype=float)


def batch_features(events: List[Dict[str, str]]) -> np.ndarray:
    return np.vstack([build_features(event) for event in events])
