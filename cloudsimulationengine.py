import json
import random
from datetime import datetime

def simulate_cloud_bet(pair, entry_price, leverage):
    # Імітація зміни ціни
    change = random.uniform(-0.05, 0.08)  # -5% до +8%
    exit_price = entry_price * (1 + change)
    pnl = (exit_price - entry_price) * leverage

    result = {
        "pair": pair,
        "entry": entry_price,
        "exit": round(exit_price, 4),
        "leverage": leverage,
        "pnl": round(pnl, 2),
        "timestamp": datetime.now().isoformat()
    }

    log_cloud_bet(result)
    return result

def log_cloud_bet(result):
    try:
        with open("cloud_bets_log.json", "r") as f:
            log = json.load(f)
    except:
        log = []

    log.append(result)
    with open("cloud_bets_log.json", "w") as f:
        json.dump(log, f, indent=2)