# =========================================================
#  Agent Manager for Spark‑1
#  Автор: Facto + Copilot
#  Призначення: керування агентами системи
# =========================================================

import os
import importlib

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.load_agents()

    # -----------------------------------------------------
    #  Завантаження всіх агентів із директорії /agents
    # -----------------------------------------------------
    def load_agents(self):
        agents_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents")

        for filename in os.listdir(agents_path):
            if filename.endswith(".py") and filename not in ["__init__.py"]:
                module_name = filename[:-3]  # без .py
                module_path = f"agents.{module_name}"

                try:
                    module = importlib.import_module(module_path)

                    # шукаємо клас з такою ж назвою, як файл
                    class_name = module_name.upper()
                    if hasattr(module, class_name):
                        agent_class = getattr(module, class_name)
                        self.agents[class_name] = agent_class()
                        print(f"[AgentManager] Завантажено агента: {class_name}")

                except Exception as e:
                    print(f"[AgentManager] Помилка завантаження {module_name}: {e}")

    # -----------------------------------------------------
    #  Отримати список агентів
    # -----------------------------------------------------
    def list_agents(self):
        return list(self.agents.keys())

    # -----------------------------------------------------
    #  Отримати агента за ім'ям
    # -----------------------------------------------------
    def get_agent(self, name: str):
        name = name.upper()
        return self.agents.get(name, None)
