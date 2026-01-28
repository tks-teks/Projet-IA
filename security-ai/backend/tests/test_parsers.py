from app.ingestion.parsers import parse_auth_log, parse_system_log, parse_web_log


def test_parse_auth_log():
    line = "Failed password for user=alice ip=10.0.0.5"
    parsed = parse_auth_log(line)
    assert parsed["parsed_type"] == "auth"
    assert parsed["user"] == "alice"
    assert parsed["ip"] == "10.0.0.5"
    assert parsed["status"] == "FAIL"


def test_parse_web_log():
    line = "192.168.1.10 500 /login"
    parsed = parse_web_log(line)
    assert parsed["parsed_type"] == "web"
    assert parsed["ip"] == "192.168.1.10"
    assert parsed["status"] == "500"


def test_parse_system_log():
    line = "ERROR disk full"
    parsed = parse_system_log(line)
    assert parsed["parsed_type"] == "system"
    assert parsed["status"] == "ERROR"
