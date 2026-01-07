import json
import random
import time
from datetime import datetime

# Завантаження топ валют для симуляції
def load_market_snapshot():
    try:
        with open("market_snapshot.json", "r") as f:
            return json.load(f)["top_pairs"]
    except:
        return ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

# Симуляція однієї хмарної ставки
def simulate_trade(pair, leverage=25):
    entry_price = get_mock_price(pair)
    change = random.uniform(-0.04, 0.07)  # -4% до +7%
    exit_price = round(entry_price * (1 + change), 4)
    pnl = round((exit_price - entry_price) * leverage, 2)

    result = {
        "pair": pair,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "leverage": leverage,
        "pnl": pnl,
        "strategy": choose_strategy(change),
        "timestamp": datetime.now().isoformat()
    }

    log_result(result)
    return result

# Вибір стратегії на основі зміни ціни
def choose_strategy(change):
    if change > 0.03:
        return "sprint"
    elif change > 0.005:
        return "scalping"
    else:
        return "hold"

# Генерація фіктивної ціни (можна замінити на API Binance)
def get_mock_price(pair):
    base_prices = {
        "BTCUSDT": 35000,
        "ETHUSDT": 1900,
        "SOLUSDT": 42,
        "XRPUSDT": 0.65,
        "DOGEUSDT": 0.075
    }
    return round(base_prices.get(pair, 100) * random.uniform(0.98, 1.02), 4)

# Логування результату
def log_result(result):
    try:
        with open("cloud_bets_log.json", "r") as f:
            log = json.load(f)
    except:
        log = []

    log.append(result)
    with open("cloud_bets_log.json", "w") as f:
        json.dump(log, f, indent=2)

# Запуск симуляції по всіх парах
def run_simulation():
    pairs = load_market_snapshot()
    results = []
    for pair in pairs:
        result = simulate_trade(pair, leverage=random.choice([25, 30, 50]))
        print(f"[{pair}] {result['strategy']} | PnL: {result['pnl']}$")
        results.append(result)
        time.sleep(1)
    return results

if __name__ == "__main__":
    run_simulation()