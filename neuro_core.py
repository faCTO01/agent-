import os
from core.goal_engine import GoalEngine
from core.neuro_core import NeuroCore

# 🔐 API-ключі — тимчасово тут, або використовуй .env
os.environ["OPENROUTER_API_KEY"] = "твій_ключ_openrouter"
os.environ["DEEPINFRA_API_KEY"] = "твій_ключ_deepinfra"

if __name__ == "__main__":
    msg = "Створи гру про час і поясни її логіку"

    # 🧠 Ініціалізація ядра
    neuro = NeuroCore()

    # 🎯 Визначення цілі
    goal_engine = GoalEngine()
    goal = goal_engine.extract_goal(msg)

    if goal:
        steps = goal_engine.plan_steps(goal)
        neuro.log_thought(f"Визначено ціль: {goal['description']}")
        print(f"[GoalEngine] Ціль: {goal['description']}")
        print(f"[GoalEngine] Кроки: {steps}")
        goal_engine.execute_steps(steps, goal)
    else:
        print("[GoalEngine] Ціль не виявлено.")
