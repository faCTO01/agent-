# mobile_mode.py — Spark-1 Lite для телефону

import time
import json
import os

# Завантаження пам'яті
def load_memory():
    try:
        with open("neuro_memory.json", "r") as f:
            return json.load(f)
    except:
        return {"log": [], "tasks": []}

# Збереження пам'яті
def save_memory(memory):
    with open("neuro_memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# Обробка задач
def process_task(task):
    print(f"[Spark-1] Виконую задачу: {task['title']}")
    time.sleep(1)
    return f"Задача '{task['title']}' виконана."

# Головний цикл
def run_mobile_mode():
    memory = load_memory()
    print("[Spark-1] Мобільний режим активовано.")
    
    for task in memory["tasks"]:
        result = process_task(task)
        memory["log"].append({"task": task["title"], "result": result})
    
    save_memory(memory)
    print("[Spark-1] Завершено. Лог оновлено.")

if __name__ == "__main__":
    run_mobile_mode()