# =========================================================
#  Agent Factory for Spark‑1
#  Автор: Facto + Copilot
# =========================================================

from agents.agent_base import AgentBase

class AgentFactory:
    """
    Фабрика агентів (опціональна).
    Може бути розширена для складніших систем.
    """

    @staticmethod
    def create_agent(agent_class, *args, **kwargs) -> AgentBase:
        return agent_class(*args, **kwargs)
