import sys
from core.spark_core import SparkCore
# Отримуємо повідомлення з командного рядка
if len(sys.argv) < 2:
    print("❗️ Введи повідомлення як аргумент")
    sys.exit()

msg = sys.argv[1]

# Ініціалізація модулів
neuro = NeuroCore()
spark = SparkCore()
goal_engine = GoalEngine()

# Озвучення повідомлення
speak_text(msg)
print(f"[Spark-1] Озвучено повідомлення: {msg}")

# Аналіз стилю
style = neuro.analyze_message(msg)
print(f"[NeuroCore] Стиль відповіді: {style}")

# Визначення творчого режиму
if neuro.is_creative_mode(msg):
    print("[NeuroCore] Активовано режим: creative")
    response = "Ось ідея: гра, де час зупиняється, коли ти не рухаєшся. Назва: 'Тиша Хвилин'."
else:
    response = "Я готова! Давай вчитися разом. Що саме хочеш опанувати сьогодні?"

# Самопокращення
neuro.self_improve(msg, response)

# Оновлення діалогу
neuro.update_dialogue_history(msg, response)

# Рефлексія
neuro.reflect_on_thoughts()

# Згадування останнього повідомлення
last = neuro.get_last_user_message()
print(f"[NeuroCore] Останнє повідомлення користувача: {last}")

# Повторний аналіз стилю (опційно)
last_style = neuro.analyze_message(last)
print(f"[NeuroCore] Стиль: {last_style}")

# Постановка цілі
goal = goal_engine.extract_goal(msg)
if goal:
    steps = goal_engine.plan_steps(goal)
    neuro.log_thought(f"Визначено ціль: {goal['description']}")
    print(f"[GoalEngine] Ціль: {goal['description']}")
    print(f"[GoalEngine] Кроки: {steps}")
    goal_engine.execute_steps(steps)
else:
    print("[GoalEngine] Ціль не виявлено.")

# Вивід відповіді
print(f"[Spark‑1] {response}")
msg = "Створи гру про час"
completed = goal_engine.recall_completed_goals()
def suggest_next_goal(self):
    suggestions = [
        "Створи візуалізацію для гри",
        "Додай таймер у гру",
        "Навчися працювати з подіями в Python",
        "Зроби гру багатомовною"
    ]
    print("[GoalEngine] Можливі наступні кроки:")
    for s in suggestions:
        print(f"➡️ {s}")
from core.goal_engine import GoalEngine

if __name__ == "__main__":
    msg = "Створи гру про час і поясни її логіку"
    goal_engine = GoalEngine()
    goal = goal_engine.extract_goal(msg)
    if goal:
        steps = goal_engine.plan_steps(goal)
        goal_engine.execute_steps(steps, goal)
    else:
        print("[Spark-1] Не вдалося визначити ціль.")
