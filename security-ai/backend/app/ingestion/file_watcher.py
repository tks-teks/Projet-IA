from pathlib import Path
from typing import Iterable


def tail_lines(path: Path) -> Iterable[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return handle.readlines()
