import json, os
from pathlib import Path

class ETNMemory:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write({"episodes": [], "traits": {}})

    def append_episode(self, data: dict):
        obj = self.read()
        obj["episodes"].append(data)
        self.write(obj)

    def read(self) -> dict:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, obj: dict):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
