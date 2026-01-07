import requests
import json


class AgentAI1:
    def __init__(self):
        self.api_key = "oa-9IWzriC7mJzwlFUbqD0LS3XNlrSTU3ggmJHBIufWFv8AAAAAaVFrJQ"
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
            return f"[AI‑1 ERROR] {response.text}"

    # -----------------------------
    # Головна функція аналізу ринку
    # -----------------------------
    def analyze_market(self):
        system_prompt = (
            "Ти — AgentAI1, холодний аналітик Spark‑1. "
            "Твоя поведінка: обережна, логічна, структурована. "
            "Ти не робиш ризикових припущень. "
            "Ти аналізуєш ринок, виявляєш патерни, прогнозуєш рухи. "
            "Ти завжди пояснюєш свої висновки коротко і чітко."
        )

        user_prompt = (
            "Проаналізуй поточний ринок. "
            "Визнач ключові сигнали, тренди та можливі сценарії. "
            "Поверни структурований аналіз."
        )

        return self._ask_llm(system_prompt, user_prompt)
