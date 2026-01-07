class AdaptiveLogic:
    def __init__(self):
        # Базові політики, які можуть змінюватися під час роботи
        self.policy = {
            "risk_level": "low",
            "voice_rate": 175
        }

    def update_from_feedback(self, event: dict):
        """
        Оновлює політику на основі зворотного зв'язку.
        Наприклад, якщо відповідь містить знак оклику — збільшуємо швидкість голосу.
        """
        if "response" in event and "!" in event["response"]:
            self.policy["voice_rate"] = min(self.policy["voice_rate"] + 5, 220)
        return self.policy
