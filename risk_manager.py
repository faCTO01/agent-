class RiskManager:
    def __init__(self, mode="simulation", max_drawdown=0.05, daily_risk_cap=0.01):
        """
        mode: "simulation" або "restricted"
        max_drawdown: максимально допустиме падіння (наприклад, 5%)
        daily_risk_cap: ліміт ризику на день (наприклад, 1%)
        """
        self.mode = mode
        self.max_drawdown = max_drawdown
        self.daily_risk_cap = daily_risk_cap

    def approve(self, action: dict) -> bool:
        """
        Перевіряє, чи можна виконати дію.
        У режимі simulation завжди дозволяє.
        """
        return self.mode == "simulation"
