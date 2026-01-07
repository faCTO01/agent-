import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "agent_memory")
LOGS_DIR = os.path.join(BASE_DIR, "agent_logs")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


class BaseAgent:
    """
    Базовий клас для всіх агентів Spark‑1.

    Можливості:
    - Детальне логування в окремий файл для кожного агента
    - Максимальна JSON‑пам'ять (knowledge, context, history, custom_data)
    - Метод brain() як точка входу до LLM (GPT‑4.1) — реалізація підключається ззовні
    """

    def __init__(self, name: str, description: str = "", capabilities: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.capabilities = capabilities or []

        self.memory_path = os.path.join(MEMORY_DIR, f"{self.name}.json")
        self.log_path = os.path.join(LOGS_DIR, f"{self.name}.log")

        self.memory: Dict[str, Any] = self._load_or_init_memory()

    # -------------------------
    #  ПАМ'ЯТЬ
    # -------------------------

    def _init_memory(self) -> Dict[str, Any]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "agent_name": self.name,
            "created": now,
            "tasks_completed": 0,
            "knowledge": {
                "patterns": [],
                "custom": {}
            },
            "context": {
                "last_input": "",
                "last_output": "",
                "session_data": {}
            },
            "history": [],
            "last_task": "",
            "custom_data": {}
        }

    def _load_or_init_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                # Якщо файл битий — переініціалізуємо
                return self._init_memory()
        else:
            mem = self._init_memory()
            self._save_memory(mem)
            return mem

    def _save_memory(self, mem: Optional[Dict[str, Any]] = None) -> None:
        data = mem if mem is not None else self.memory
        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self._raw_log(f"[MEMORY ERROR] Не вдалося зберегти пам'ять: {e}")

    def update_memory(self, **kwargs) -> None:
        """
        Оновити ключі в пам'яті агента.
        """
        self.memory.update(kwargs)
        self._save_memory()

    def add_history_entry(self, task: str, result: Any) -> None:
        """
        Додає запис в історію задач агента.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "result": result
        }
        self.memory.setdefault("history", []).append(entry)
        self.memory["last_task"] = task
        self.memory["tasks_completed"] = self.memory.get("tasks_completed", 0) + 1
        self._save_memory()

    # -------------------------
    #  ЛОГИ
    # -------------------------

    def _raw_log(self, text: str) -> None:
        """
        Запис без форматування (використовується всередині).
        """
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except Exception:
            pass

    def log(self, message: str) -> None:
        """
        Детальне логування у форматі:

        [AgentName | 19:42:10] Повідомлення
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{self.name} | {timestamp}] {message}"
        self._raw_log(line)

    # -------------------------
    #  LLM / МОЗОК
    # -------------------------

    def brain(self, prompt: str, **kwargs) -> Any:
        """
        Точка входу до LLM (GPT‑4.1).

        Тут потрібно підключити реальний виклик до моделі.
        Зараз — заглушка, щоб не ламати структуру.

        Рекомендація:
        - передати в агента об'єкт/функцію LLM при створенні
        - або перевизначити цей метод в дочірньому класі
        """
        self.log("🧠 brain() викликано, але LLM ще не підключений.")
        raise NotImplementedError("Метод brain() має бути перевизначений або підключений до LLM.")

    # -------------------------
    #  ГОЛОВНЕ API АГЕНТА
    # -------------------------

    def run(self, task: Any) -> Any:
        """
        Головний метод, який має реалізувати кожен конкретний агент.
        """
        raise NotImplementedError("Метод run() має бути реалізований у дочірньому класі.")
