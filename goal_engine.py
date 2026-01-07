import os
import json
from datetime import datetime
from core.ai_delegate import delegate_dialog, delegate_code
def execute_steps(self, steps: list, goal: dict):
    from core.neuro_core import NeuroCore
    neuro = NeuroCore()
    ...


class GoalEngine:
    def __init__(self):
        self.goals = []

    def extract_goal(self, message: str):
        message = message.lower()
        if "створи" in message or "побудуй" in message:
            return {"type": "build", "description": message}
        elif "навчи" in message or "вивчи" in message:
            return {"type": "learn", "description": message}
        elif "аналізуй" in message or "розбери" in message:
            return {"type": "analyze", "description": message}
        return None

    def plan_steps(self, goal: dict):
        if goal["type"] == "build":
            return ["визначити структуру", "згенерувати код", "зберегти файл"]
        elif goal["type"] == "learn":
            return ["визначити тему", "знайти джерела", "створити тест"]
        elif goal["type"] == "analyze":
            return ["розбити на частини", "виявити зв’язки", "сформулювати висновки"]
        return []

    def execute_steps(self, steps: list, goal: dict):
        neuro = NeuroCore()

        for step in steps:
            print(f"[GoalEngine] Виконую крок: {step}")

            if "згенерувати код" in step:
                prompt = f"Створи код для: {goal['description']}"
                result = delegate_code(prompt)
                print(f"[AI Delegate] Код:\n{result}")
                neuro.store_code(goal["description"], result)

            elif "аналізуй" in step or "розбери" in step or "структура" in step:
                prompt = f"Проаналізуй задачу: {goal['description']}"
                result = delegate_dialog(prompt)
                print(f"[AI Delegate] Аналіз:\n{result}")
                neuro.log_thought(result)

        self.complete_goal(goal)

    def complete_goal(self, goal: dict):
        path = "core/completed_goals.json"
        completed = []

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                completed = json.load(f)

        completed.append({
            "description": goal["description"],
            "type": goal["type"],
            "timestamp": datetime.now().isoformat()
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(completed[-50:], f, indent=2, ensure_ascii=False)

        print(f"[GoalEngine] Ціль завершено: {goal['description']}")

    def recall_completed_goals(self):
        path = "core/completed_goals.json"
        if not os.path.exists(path):
            print("[GoalEngine] Немає завершених цілей.")
            return []

        with open(path, "r", encoding="utf-8") as f:
            completed = json.load(f)

        print(f"[GoalEngine] Завершено {len(completed)} цілей:")
        for goal in completed[-5:]:
            print(f"✅ {goal['description']} ({goal['type']}) — {goal['timestamp']}")
        return completed
