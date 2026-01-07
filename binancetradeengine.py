import json
from datetime import datetime, timedelta

def load_mission():
    with open("trade_mission.json", "r") as f:
        return json.load(f)

def evaluate_progress(current_balance):
    mission = load_mission()
    target = mission["target_profit"]
    if current_balance >= target:
        return "Мета досягнута. Готово до реальних угод."
    else:
        return f"Поточний баланс: ${current_balance}. Мета: ${target}"

def analyze_failure(log):
    # Заглушка: аналіз логу
    return "Провал: неправильний вибір часу. Ринок був нестабільний."

def retry_mission():
    # Заглушка: повторна спроба
    return "Повторна спроба активована. Стратегія оновлена."