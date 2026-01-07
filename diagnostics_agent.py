# E:\Spark-1\agents\diagnostics_agent.py
from agents.agent_base import AgentBase
from core.llm_core import LLMCore
import psutil
import os
import time

class DiagnosticsAgent(AgentBase):
    name = "DiagnosticsAgent"
    description = "Агент для внутрішньої діагностики системи Spark-1"

    def __init__(self):
        super().__init__()
        self.llm = LLMCore(model="phi3")  # або твоя дефолтна модель

    def run(self, task: str) -> str:
        """
        task: короткий тригер, типу 'full', 'quick', 'memory', 'agents'
        """
        raw_snapshot = self._collect_snapshot()
        summary = self._summarize_snapshot(raw_snapshot, task)
        return summary

    def _collect_snapshot(self) -> dict:
        """Збираємо сирі метрики системи + стан агентів."""
        snapshot = {}

        # Системні ресурси
        snapshot["system"] = {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage(os.getcwd())._asdict(),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cwd": os.getcwd(),
        }

        # Тут можна підключити реальний список агентів з AgentRegistry
        from agents.agent_registry import AgentRegistry
        registry = AgentRegistry()
        agents = registry.list_agents()

        snapshot["agents"] = {
            "count": len(agents),
            "names": agents,
        }

        # Стан LLMCore / Ollama умовно
        snapshot["llmcore"] = {
            "primary_endpoint": "http://localhost:11434/api/chat",
            "fallback_endpoint": "http://localhost:11434/api/generate",
            "recent_errors": self._get_recent_llm_errors(limit=10),
        }

        return snapshot

    def _get_recent_llm_errors(self, limit: int = 10):
        # Якщо в тебе є лог-файл LLMCore — тут можна його реально парсити.
        # Поки що повернемо заглушку.
        return []

    def _summarize_snapshot(self, snapshot: dict, task: str) -> str:
        """Даємо LLM-у сировину, щоб зробити структурований звіт."""
        prompt = f"""
Ти — внутрішній діагностичний модуль системи Spark‑1.

Отримуєш JSON-структуру зі станом системи, агентів і LLMCore.
Твоє завдання — побудувати ЗРОЗУМІЛИЙ, СТРУКТУРОВАНИЙ людський звіт українською.

Формат відповіді:
- Загальний стан
- Ресурси системи (CPU, пам’ять, диск)
- Агенти (кількість, імена, можливі проблеми)
- LLMCore/Ollama (ризики, нестабільність)
- Рекомендації (конкретні наступні кроки)

Не пропонуй файлові операції. Не використовуй виконувані блоки [CD]/[MKDIR]/[AF].
Просто текстовий структурований звіт.

Ось дані:
{snapshot}

Режим задачі: {task}
"""
        result = self.llm.simple_chat(prompt)
        return result
