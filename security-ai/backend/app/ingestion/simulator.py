import json
import random
import time
from pathlib import Path
from typing import Iterable
from urllib import request

SAMPLE_PATH = Path(__file__).resolve().parents[3] / "sample_logs"
API_URL = "http://localhost:8000/logs/parse"


def iter_log_lines() -> Iterable[tuple[str, str]]:
    sources = {
        "auth": SAMPLE_PATH / "auth.log",
        "web": SAMPLE_PATH / "web.log",
        "system": SAMPLE_PATH / "system.log",
    }
    for source, path in sources.items():
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                yield source, line.strip()


def post_log(source: str, line: str) -> None:
    payload = json.dumps({"source": source, "line": line}).encode("utf-8")
    req = request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
    request.urlopen(req, timeout=5)


def run_simulation(loop_once: bool = False, delay: float = 1.5) -> None:
    lines = list(iter_log_lines())
    while True:
        random.shuffle(lines)
        for source, line in lines:
            try:
                post_log(source, line)
            except Exception:
                pass
            time.sleep(delay)
        if loop_once:
            break


if __name__ == "__main__":
    run_simulation()
