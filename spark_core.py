import yaml
from pathlib import Path
from core.emotion_core import EmotionCore
from core.philosophy_core import PhilosophyCore
from core.adaptive_logic import AdaptiveLogic
from core.self_upgrade import SelfUpgrade
from core.log_manager import LogManager
from interfaces.voice_engine import VoiceEngine
from storage.memory import ETNMemory
from agents.agent_factory import AgentFactory
from ml.ml_trainer import MLTrainer

class SparkCore:
    def __init__(self, config_path="config/settings.yaml", permissions_path="config/permissions.yaml"):
        # Завантаження конфігурацій
        self.config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        self.permissions = yaml.safe_load(Path(permissions_path).read_text(encoding="utf-8"))

        # Логи
        self.logs = LogManager(self.config["logs"]["system"])
        self.agent_logs = LogManager(self.config["logs"]["agent_activity"])
        self.trade_logs = LogManager(self.config["logs"]["trade"])
        self.exp_logs = LogManager(self.config["logs"]["experiment"])

        # Модулі
        self.memory = ETNMemory(self.config["memory"]["etn_path"])
        self.emotion = EmotionCore()
        self.philosophy = PhilosophyCore()
        self.adaptive = AdaptiveLogic()
        self.voice = VoiceEngine(rate=self.config["voice"]["rate"])
        self.upgrade = SelfUpgrade(allow_packages=self.permissions["modules"]["self_upgrade"]["allow_packages"])
        self.agents = AgentFactory(permissions=self.permissions, logs=self.agent_logs)
        self.trainer = MLTrainer(logs=self.exp_logs)

        self.state = {"version": self.config["app"]["version"], "identity": self.config["app"]["name"]}

    def perceive(self, input_text: str, channel="voice"):
        # Інтерпретація наміру
        intent = self._interpret(input_text)
        response = self._route_intent(intent)
        styled = self.emotion.modulate(response)

        # Голосовий вихід
        if self.config["voice"]["enabled"] and channel == "voice":
            self.voice.speak(styled)

        # Логування та пам’ять
        self.logs.write("system", {"intent": intent, "response": response})
        self.memory.append_episode({"input": input_text, "response": response})

        # Адаптація
        new_policy = self.adaptive.update_from_feedback({"intent": intent, "response": response})
        self.voice.set_rate(new_policy["voice_rate"])

        return styled

    def _interpret(self, text: str) -> dict:
        text_l = text.lower()
        if text_l.startswith("створи агента"):
            return {"type": "agent.create", "spec": {"role": "trader"}}
        if text_l.startswith("тренуй експеримент"):
            return {"type": "ml.schedule", "name": "demo", "config": {"epochs": 1}}
        return {"type": "dialog", "text": text}

    def _route_intent(self, intent: dict) -> str:
        t = intent.get("type")
        if t == "dialog":
            return self.philosophy.reflect(intent["text"])
        elif t == "agent.create":
            agent_id = self.agents.create(intent.get("spec", {}))
            return f"Агент створений: {agent_id}"
        elif t == "ml.schedule":
            self.trainer.schedule(intent["name"], intent["config"])
            done = self.trainer.run_next()
            return f"Експеримент '{done['name']}' виконано (status={done['status']})."
        else:
            return "Я ще вчуся розуміти цей намір."
