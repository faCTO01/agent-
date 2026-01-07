import requests
import json
from datetime import datetime


class AgentAI2:
    def __init__(self):
        self.api_key = "oa-6QZQ3O3lXC8LWS5phAiLEjvDrxOI2aSWehrwiydbmUAAAAAAaVFrjw"
        self.api_url = "https://openagents.org/api/v1/chat/completions"
        self.model = "gpt-4.1"

    def _ask_llm(self, system_prompt, user_prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"[AI‑2 ERROR] {response.text}"

    # -----------------------------
    # 1. Генерація стратегії
    # -----------------------------
    def generate_strategy(self, signals):
        system_prompt = (
            "Ти — AgentAI2, стратег і творча півкуля Spark‑1. "
            "Твоя поведінка: обережна, структурована, без ризикових рішень. "
            "Ти будуєш стратегії на основі сигналів AgentAI1. "
            "Ти пропонуєш чіткі, безпечні, логічні кроки."
        )

        user_prompt = (
            f"Сигнали від AgentAI1:\n{signals}\n\n"
            "Побудуй обережну, низькоризикову торгову стратегію."
        )

        return self._ask_llm(system_prompt, user_prompt)

    # -----------------------------
    # 2. Симуляція стратегії
    # -----------------------------
    def simulate_strategy(self, strategy):
        # Поки що симуляція базова — пізніше замінимо на реальну
        return {
            "timestamp": datetime.now().isoformat(),
            "profit": 0.0,
            "status": "simulated",
            "strategy_used": strategy
        }

    # -----------------------------
    # 3. Адаптація стратегії
    # -----------------------------
    def adapt_strategy(self, results):
        system_prompt = (
            "Ти — AgentAI2, стратег Spark‑1. "
            "Твоя поведінка: обережна, логічна. "
            "Ти аналізуєш результати симуляції і пропонуєш покращення."
        )

        user_prompt = (
            f"Результати симуляції:\n{results}\n\n"
            "Запропонуй безпечні покращення стратегії."
        )

        return self._ask_llm(system_prompt, user_prompt)
