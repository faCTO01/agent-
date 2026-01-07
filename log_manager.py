import json
from datetime import datetime
from pathlib import Path

class LogManager:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, category: str, payload: dict):
        record = {
            "ts": datetime.utcnow().isoformat(),
            "cat": category,
            "payload": payload
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
