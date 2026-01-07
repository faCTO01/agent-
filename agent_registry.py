import os
import importlib.util
import inspect

class AgentRegistry:
    """
    Завантажує всі агенти з папки agents/
    """

    def __init__(self):
        self.agents = {}
        self.agents_dir = os.path.join(os.getcwd(), "agents")

    def load_agents(self):
        print(f"[AgentRegistry] AGENTS_DIR = {self.agents_dir}")

        files = os.listdir(self.agents_dir)
        print(f"[AgentRegistry] Знайдені файли в agents/: {files}")

        for filename in files:
            if not filename.endswith(".py"):
                continue

            full_path = os.path.join(self.agents_dir, filename)
            print(f"[AgentRegistry] Завантажую файл: {full_path}")

            try:
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                print(f"[AgentRegistry] Імпорт модуля {module_name} з {full_path}")

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if hasattr(obj, "run") and obj.__module__ == module_name:
                        self.agents[name] = obj
                        print(f"[AgentRegistry] → Завантажено агента: {name}")

            except Exception as e:
                print(f"[AgentRegistry] ❌ Помилка імпорту {full_path}: {e}")

        print(f"[AgentRegistry] Підсумок: завантажено агентів: {list(self.agents.keys())}")

    def get_agent(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())
