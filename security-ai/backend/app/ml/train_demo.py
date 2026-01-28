from pathlib import Path

from app.ingestion.parsers import parse_line
from app.ml.trainer import train_model

SAMPLE_PATH = Path(__file__).resolve().parents[3] / "sample_logs"


def load_events():
    events = []
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
                payload = parse_line(source, line.strip())
                payload["source"] = source
                payload["raw"] = line.strip()
                events.append(payload)
    return events


def main() -> None:
    events = load_events()
    train_model(events)
    print("Model trained with sample logs.")


if __name__ == "__main__":
    main()
