class SelfUpgrade:
    def __init__(self, allow_packages=None):
        # Список дозволених пакетів для оновлення
        self.allow = allow_packages or []

    def plan(self, proposal: dict) -> dict:
        """
        Створює план оновлення (симуляція).
        proposal: {"package": "назва", "version": "x.y.z"}
        """
        return {"proposal": proposal, "status": "queued"}

    def execute_safe(self, plan: dict) -> dict:
        """
        Виконує оновлення лише у безпечному режимі (симуляція).
        """
        return {
            "executed": False,
            "reason": "Simulation mode only — реальні оновлення заблоковані"
        }
