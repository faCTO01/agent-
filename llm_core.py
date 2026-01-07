# =========================================================
#  LLM Core for Spark-1 (Ollama — DIAGNOSTIC VERSION)
#  Автор: Facto + Copilot
# =========================================================

import requests
import json
import time

from config.llm_config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_ANALYZER,
    OLLAMA_MODEL_EXECUTOR,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
)


# ============================
#  SYSTEM PROMPTS
# ============================

SYSTEM_PROMPT_ANALYZER = """
Ти — AnalyzerAgent системи Spark-1.

Твоє завдання — аналізувати запит користувача і визначати, чи містить він дію над файловою системою.

Якщо запит містить дію над файлами або папками (створити, видалити, записати, дозаписати, прочитати, перемістити, перейменувати), ти ПОВИНЕН повернути тільки одну з ACTION-команд:

1) Створення папки:
   [CD] <шлях> [/CD]

2) Створення файлу:
   [WF]
   [P] <шлях> [/P]
   [C] <контент> [/C]
   [/WF]

3) Дозапис у файл:
   [AF]
   [P] <шлях> [/P]
   [C] <контент> [/C]
   [/AF]

ДОЗВОЛЕНІ ТІЛЬКИ ТАКІ ACTION-БЛОКИ:
[CD] ... [/CD]
[WF] ... [/WF]
[AF] ... [/AF]

ЗАБОРОНЕНО використовувати будь-які інші теги:
[MKDIR], [PWD], [MOVE], [RM], [COPY], [LS], [DIR], [FILE], [FOLDER],
[MK], [TOUCH], [WRITE], [READ], [ACTION], [RESULT] та будь-які інші.

Правила:
- НЕ пиши планів, інструкцій, документації.
- НЕ використовуй bash, spark, shell, python.
- НЕ пояснюй, що ти робиш.
- НЕ додавай текст поза ACTION-блоками.
- Якщо запит стосується файлової системи — повертай ТІЛЬКИ один із дозволених блоків.

Якщо запит НЕ стосується файлової системи — сформуй короткий, структурований план дій для ExecutorAgent.
"""

SYSTEM_PROMPT_EXECUTOR = """
Ти — ExecutorAgent системи Spark-1.

Твоє завдання — брати інструкції AnalyzerAgent і повертати результат виконання.

Правила:
- Якщо AnalyzerAgent дав ACTION-команду — НЕ змінюй її, НЕ переписуй, НЕ пояснюй. Просто поверни її без змін.
- Якщо AnalyzerAgent дав план — виконай його логічно: згенеруй дані, таблиці, підсумки, результати.
- НЕ пиши код.
- НЕ описуй код.
- НЕ використовуй bash, spark, shell.
- Поверни тільки результат, ніби він справді був виконаний.
"""


class LLMCore:
    def __init__(self, system_prompt: str, model_name: str):
        self.base_url = OLLAMA_BASE_URL.rstrip("/")
        self.model = model_name
        self.system_prompt = system_prompt

        self.chat_url = f"{self.base_url}/api/chat"
        self.gen_url = f"{self.base_url}/api/generate"

    # -----------------------------------------------------
    #  ВНУТРІШНІЙ МЕТОД: нормалізація відповіді
    # -----------------------------------------------------
    def _extract_content(self, data: dict) -> str | None:
        """
        Повертає текст відповіді з різних форматів Ollama.
        """
        # Формат /api/chat
        if isinstance(data, dict):
            if "message" in data and isinstance(data["message"], dict):
                msg = data["message"]
                if "content" in msg and isinstance(msg["content"], str):
                    return msg["content"]

            # Формат /api/generate
            if "response" in data and isinstance(data["response"], str):
                return data["response"]

            # Інші можливі поля
            if "content" in data and isinstance(data["content"], str):
                return data["content"]

        return None

    # -----------------------------------------------------
    #  ВНУТРІШНІЙ МЕТОД: логування
    # -----------------------------------------------------
    def _log(self, text: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LLMCore][{ts}] {text}")

    # -----------------------------------------------------
    #  ВНУТРІШНІЙ МЕТОД: один HTTP-запит
    # -----------------------------------------------------
    def _post(self, url: str, payload: dict, timeout: int = 60) -> dict | None:
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            if r.status_code != 200:
                self._log(f"HTTP {r.status_code} from {url}: {r.text[:300]}")
                return None
            try:
                return r.json()
            except Exception as e:
                self._log(f"JSON decode error from {url}: {e}")
                self._log(f"Raw response: {r.text[:300]}")
                return None
        except Exception as e:
            self._log(f"Request error to {url}: {e}")
            return None

    # -----------------------------------------------------
    #  ДІАГНОСТИЧНИЙ ЗАПИТ
    # -----------------------------------------------------
    def ask(self, prompt: str, retries: int = 2, delay: float = 0.5) -> str:
        print("\n" + "=" * 80)
        print(f"[LLMCore] Запит до моделі: {self.model}")
        print(f"[LLMCore] System prompt (скорочено): {self.system_prompt[:300]}...")
        print(f"[LLMCore] User prompt: {prompt}")
        print("=" * 80)

        # --------- 1) Спроба через /api/chat ---------
        payload_chat = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "num_predict": MAX_TOKENS,
            },
        }

        attempt = 0
        while attempt <= retries:
            self._log(f"Спроба {attempt + 1} через /api/chat")
            data = self._post(self.chat_url, payload_chat)
            if data is not None:
                content = self._extract_content(data)
                if content:
                    self._log("Отримано відповідь від /api/chat")
                    return content
                else:
                    self._log("Порожня або невідома відповідь від /api/chat")
            attempt += 1
            if attempt <= retries:
                time.sleep(delay)

        # --------- 2) Fallback через /api/generate ---------
        self._log("Переходимо до fallback: /api/generate")

        payload_gen = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\nUser: {prompt}\nAssistant:",
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "num_predict": MAX_TOKENS,
            },
        }

        attempt = 0
        while attempt <= retries:
            self._log(f"Спроба {attempt + 1} через /api/generate")
            data = self._post(self.gen_url, payload_gen)
            if data is not None:
                content = self._extract_content(data)
                if content:
                    self._log("Отримано відповідь від /api/generate")
                    return content
                else:
                    self._log("Порожня або невідома відповідь від /api/generate")
            attempt += 1
            if attempt <= retries:
                time.sleep(delay)

        # --------- 3) Якщо все впало — повертаємо сирий JSON або повідомлення про помилку ---------
        self._log("Не вдалося отримати коректну відповідь від моделі.")
        return "[LLM ERROR] Не вдалося отримати відповідь від моделі Ollama після кількох спроб."


def get_analyzer_llm():
    return LLMCore(SYSTEM_PROMPT_ANALYZER, OLLAMA_MODEL_ANALYZER)


def get_executor_llm():
    return LLMCore(SYSTEM_PROMPT_EXECUTOR, OLLAMA_MODEL_EXECUTOR)
