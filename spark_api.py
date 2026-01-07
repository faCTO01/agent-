# spark_api.py
# Публічний API для керування агентами Spark‑1

import os
from agent_registry import AgentRegistry


class SparkAPI:
    """
    Зовнішній інтерфейс для Telegram Command Center та інших модулів.
    Інкапсулює роботу з AgentRegistry та конкретними агентами.
    """

    def __init__(self):
        self.registry = AgentRegistry()
        self.registry.load_all_agents()

    # -----------------------------------------------------
    #  Базові операції з агентами
    # -----------------------------------------------------

    def list_agents(self):
        """
        Повертає список імен зареєстрованих агентів.
        """
        # AgentRegistry.list_agents уже повертає list, тому просто віддаємо його
        return self.registry.list_agents()

    def get_agent(self, name: str):
        """
        Повертає екземпляр агента за ім'ям або None.
        """
        return self.registry.get_agent(name)

    def run_agent(self, name: str, task: str) -> str:
        """
        Запускає вказаного агента з переданою задачею.
        """
        agent = self.get_agent(name)
        if agent is None:
            return f"❌ Агент '{name}' не знайдений."

        try:
            return agent.run(task)
        except Exception as e:
            return f"❌ Помилка при виконанні агента '{name}': {e}"

    def create_agent(self, name: str, description: str, capabilities: list) -> str:
        """
        Тимчасовий простий API для створення агента-заглушки (якщо потрібно).
        Зараз може просто реєструвати нового агента в пам'яті або відповідати текстом.
        """
        # Тут ти зможеш додати реальне збереження/генерацію коду агента.
        return f"Створення кастомних агентів ще не реалізоване. Запитаний агент: {name}"

    # -----------------------------------------------------
    #  Цикли Spark‑1 (short / medium / long / auto)
    #  Поки що — заглушки, які звертаються до ISCRY1,
    #  якщо він існує.
    # -----------------------------------------------------

    def _run_iscry_cycle(self, mode: str, task: str | None = None) -> str:
        """
        Внутрішній хелпер: запускає ISCRY1 в різних режимах.
        mode: 'short' | 'medium' | 'long' | 'auto'
        """
        iscry = self.get_agent("ISCRY1")
        if iscry is None:
            return "❌ Агент ISCRY1 не завантажений."

        # Якщо твій ISCRY1 має спеціальні методи типу run_short/..., можна викликати їх тут.
        # Поки що — один універсальний run з контекстом режиму.
        if task is None:
            task = f"Запусти {mode}_cycle в твоєму внутрішньому режимі."

        full_task = f"[MODE={mode}] {task}"
        try:
            return iscry.run(full_task)
        except Exception as e:
            return f"❌ Помилка при виконанні циклу {mode}: {e}"

    def run_short_cycle(self) -> str:
        """
        Короткий цикл Spark‑1.
        """
        return self._run_iscry_cycle("short")

    def run_medium_cycle(self) -> str:
        """
        Середній цикл Spark‑1.
        """
        return self._run_iscry_cycle("medium")

    def run_long_cycle(self) -> str:
        """
        Довгий цикл Spark‑1.
        """
        return self._run_iscry_cycle("long")

    def auto(self, task: str) -> str:
        """
        Автономний режим: делегує завдання ISCRY1 з позначкою auto.
        """
        return self._run_iscry_cycle("auto", task)
