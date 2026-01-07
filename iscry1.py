from agents.agent_base import AgentBase
from core.llm_core import LLMCore
from core.file_manager import FileManager
import re


class ISCRY1(AgentBase):
    """
    ISCRY1 — саморефлексивний агент Spark‑1.
    Підтримує режими:
    - default: звичайний reasoning
    - diagnostics: внутрішня діагностика
    - evolve: генерація нейронів
    """

    def __init__(self):
        super().__init__("ISCRY1")
        self.llm = LLMCore(
            system_prompt="Ти — внутрішній агент ISCRY1 Spark‑1.",
            model_name="phi3"
        )
        self.fm = FileManager()

    # ---------------------------------------------------------
    # ГОЛОВНИЙ ВХІД
    # ---------------------------------------------------------
    def run(self, task: str):
        task_low = task.lower().strip()

        if "evolve" in task_low or "neuron" in task_low:
            return self._run_evolution(task)

        if "diagnos" in task_low or "scan" in task_low:
            return self._run_diagnostics(task)

        return self._run_default(task)

    # ---------------------------------------------------------
    # DEFAULT — просто відповідь моделі
    # ---------------------------------------------------------
    def _run_default(self, task: str) -> str:
        prompt = f"""
Ти — ISCRY1, внутрішній агент Spark‑1.

Користувацький запит:
{task}

Відповідай логічно, структуровано, без файлових операцій.
"""
        return self.llm.ask(prompt)

    # ---------------------------------------------------------
    # DIAGNOSTICS — внутрішня діагностика
    # ---------------------------------------------------------
    def _run_diagnostics(self, task: str) -> str:
        prompt = f"""
Ти — внутрішній діагностичний модуль ISCRY1.

Проведи самодіагностику Spark‑1.

Формат відповіді:
- Загальний стан
- Стан пам'яті ISCRY1
- Стан LLMCore
- Стан агентів
- Стан інтеграцій
- Рекомендації

Не використовуй файлові блоки.
Не генеруй код.
"""
        return self.llm.ask(prompt)

    # ---------------------------------------------------------
    # EVOLUTION — нейронні блоки
    # ---------------------------------------------------------
    def _run_evolution(self, task: str) -> str:
        prompt = f"""
Ти — внутрішній нейронний архітектор ISCRY1.

Мета: створювати нові "нейрони" — фрагменти логіки, функції, модулі.

Користувацький запит:
{task}

Формат відповіді:

[NEURON_PLAN]
goal: ...
context: ...
steps:
  - ...
risks:
  - ...
next_action: code | reflect | log_only
[/NEURON_PLAN]

Якщо next_action = code — додай:

[NEURON_CODE]
filename: core/iscry1_neurons.py
mode: append
language: python
code:
\"\"\"Тут Python-код нейронів\"\"\"
[/NEURON_CODE]

Не використовуй файлові блоки.
"""
        raw = self.llm.ask(prompt)

        plan = self._extract_block(raw, "NEURON_PLAN")
        code = self._extract_block(raw, "NEURON_CODE")

        output = ""

        if plan:
            output += "🧠 NEURON PLAN:\n" + plan + "\n\n"

        if code:
            output += "💾 NEURON CODE DETECTED — записую...\n"
            self._apply_neuron_code(code)
            output += "✅ Код додано до core/iscry1_neurons.py\n"

        if not plan and not code:
            output += "⚠️ Модель не повернула нейронних блоків."

        return output

    # ---------------------------------------------------------
    # ДОПОМІЖНІ МЕТОДИ
    # ---------------------------------------------------------
    def _extract_block(self, text: str, block_name: str):
        pattern = rf"

\[{block_name}\]

(.*?)

\[/{block_name}\]

"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None
    def _apply_neuron_code(self, block: str):
        filename_match = re.search(r"filename:\s*(.*)", block)
        mode_match = re.search(r"mode:\s*(.*)", block)
        code_match = re.search(r'code:\s*"""(.*?)"""', block, re.DOTALL)

        if not filename_match or not code_match:
            return

        filename = filename_match.group(1).strip()
        mode = mode_match.group(1).strip() if mode_match else "append"
        code = code_match.group(1)

        if mode == "append":
            self.fm.append_to_file(filename, code)
        elif mode == "replace":
            self.fm.write_file(filename, code)

    