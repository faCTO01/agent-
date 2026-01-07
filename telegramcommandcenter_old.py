import json
from telegram_bridge import send_message
from datetime import datetime

def handle_command(cmd):
    if cmd == "/start":
        return "Spark-1 запущено."
    elif cmd == "/stop":
        return "Spark-1 зупинено."
    elif cmd == "/balance":
        return "Поточний баланс: $1,024.50"
    elif cmd == "/timer":
        return f"Час роботи: {get_uptime()}"
    elif cmd == "/cloudbets":
        return "Хмарні ставки: 3 активні, 2 в очікуванні"
    elif cmd == "/log":
        return get_log()
    elif cmd == "/strategy":
        return "Стратегія: адаптивна, ризик — середній"
    elif cmd == "/scalp":
        return "Скальпінг активний. Шанс успіху: 72%"
    elif cmd == "/profit":
        return "Орієнтовний прибуток сьогодні: $84.20"
    elif cmd == "/base":
        return "База: 12 валют, 3 індикатори, 2 моделі"
    elif cmd == "/news":
        return get_news()
    elif cmd == "/volatility":
        return "Волатильність: BTC — висока, ETH — середня"
    elif cmd.startswith("/stage"):
        return handle_stage(cmd)
    else:
        return "Невідома команда."

def get_uptime():
    # Заглушка
    return "3 год 42 хв"

def get_log():
    try:
        with open("genesis_log.json", "r") as f:
            log = json.load(f)
        return f"Останні дії: {log['last_action']}"
    except:
        return "Лог недоступний."

def get_news():
    return "Новини: BTC зростає, FED готує заяву."

def handle_stage(cmd):
    if "початковий" in cmd:
        return "Етап: Початковий — запуск, тестування, логування"
    elif "середній" in cmd:
        return "Етап: Середній — стратегія, новини, адаптація"
    elif "завершений" in cmd:
        return "Етап: Завершений — вибір валюти, плеча, ставки"
    else:
        return "Вкажи етап: /stage початковий | середній | завершений"