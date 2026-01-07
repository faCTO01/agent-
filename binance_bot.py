class BinanceBot:
    def __init__(self):
        # За замовчуванням реальна торгівля вимкнена
        self.enabled = False

    def paper_trade(self, signal: dict):
        """
        Виконує симуляцію угоди (paper trading).
        signal: {"symbol": "BTCUSDT", "action": "buy", "amount": 0.01}
        """
        return {
            "result": "paper_trade_executed",
            "signal": signal
        }

    def live_trade(self, signal: dict):
        """
        Реальна торгівля заблокована у цьому режимі.
        """
        return {
            "result": "denied",
            "reason": "Simulation mode only"
        }
