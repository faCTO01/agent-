import requests
import os

# 🔍 Діалогова та аналітична частина — OpenRouter
def delegate_dialog(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # або Claude, GPT-4
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# 💻 Генерація коду — DeepInfra
def delegate_code(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPINFRA_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "codellama/CodeLlama-7b-Instruct",  # або StarCoder
        "prompt": prompt,
        "max_tokens": 500
    }
    response = requests.post("https://api.deepinfra.com/v1/openai/completions", headers=headers, json=data)
    return response.json()["choices"][0]["text"]
