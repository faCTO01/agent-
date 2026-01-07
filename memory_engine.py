import json
import os
from datetime import datetime


class MemoryEngine:
    def __init__(self, path="data/memory.json"):
        self.path = path
        self._ensure_file()

    # -----------------------------
    # 1. Створення файлу пам’яті
    # -----------------------------
    def _ensure_file(self):
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"cycles": []}, f, ensure_ascii=False, indent=4)

    # -----------------------------
    # 2. Завантаження пам’яті
    # -----------------------------
    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------
    # 3. Збереження пам’яті
    # -----------------------------
    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # -----------------------------
    # 4. Збереження циклу
    # -----------------------------
    def save_cycle(self, signals, strategy, results):
        memory = self.load()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "signals": signals,
            "strategy": strategy,
            "results": results
        }

        memory["cycles"].append(entry)
        self.save(memory)

    # -----------------------------
    # 5. Отримати останні N циклів
    # -----------------------------
    def get_last_cycles(self, n=10):
        memory = self.load()
        return memory["cycles"][-n:]
