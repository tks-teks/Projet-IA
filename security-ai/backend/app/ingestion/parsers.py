from datetime import datetime
from typing import Dict


def parse_auth_log(line: str) -> Dict[str, str]:
    parts = line.split(" ")
    user = None
    ip = None
    status = None
    if "Failed" in line or "failure" in line:
        status = "FAIL"
    if "Accepted" in line or "success" in line:
        status = "SUCCESS"
    for part in parts:
        if part.startswith("user="):
            user = part.split("=", 1)[1]
        if part.startswith("ip="):
            ip = part.split("=", 1)[1]
    return {
        "timestamp": datetime.utcnow(),
        "parsed_type": "auth",
        "user": user,
        "ip": ip,
        "status": status,
        "message": line.strip(),
    }


def parse_web_log(line: str) -> Dict[str, str]:
    parts = line.split(" ")
    ip = parts[0] if parts else None
    status = None
    if len(parts) > 1:
        status = parts[1]
    return {
        "timestamp": datetime.utcnow(),
        "parsed_type": "web",
        "user": None,
        "ip": ip,
        "status": status,
        "message": line.strip(),
    }


def parse_system_log(line: str) -> Dict[str, str]:
    level = "INFO"
    if "WARN" in line:
        level = "WARN"
    if "ERROR" in line:
        level = "ERROR"
    return {
        "timestamp": datetime.utcnow(),
        "parsed_type": "system",
        "user": None,
        "ip": None,
        "status": level,
        "message": line.strip(),
    }


def parse_line(source: str, line: str) -> Dict[str, str]:
    if source == "auth":
        return parse_auth_log(line)
    if source == "web":
        return parse_web_log(line)
    return parse_system_log(line)
