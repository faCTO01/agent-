# telegram_bridge.py — модуль зв'язку Spark-1 з Telegram

import requests
import json

def send_message(text):
    try:
        with open("telegram_config.json", "r") as f:
            config = json.load(f)
        url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
        payload = {
            "chat_id": config["chat_id"],
            "text": text
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[Spark-1] Повідомлення надіслано в Telegram.")
        else:
            print(f"[Spark-1] Помилка надсилання: {response.text}")
    except Exception as e:
        print(f"[Spark-1] Telegram помилка: {e}")