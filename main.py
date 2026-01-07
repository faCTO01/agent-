import sys
import os
import yaml
from datetime import datetime

# -----------------------------
# 0. Імпорти внутрішніх модулів
# -----------------------------

from core.memory_engine import MemoryEngine
from core.learning_engine import LearningEngine


# -----------------------------
# 1. Завантаження конфігурації
# -----------------------------

def load_yaml(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        print(f"⚠ Конфіг файл не знайдено: {path}. Використовую default.")
        return default
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or default


def load_config():
    return load_yaml("config/settings.yaml", default={})


def load_paths():
    return load_yaml("config/paths.yaml", default={})


# -----------------------------
# 2. Підключення зовнішніх репозиторіїв
# -----------------------------

def attach_external_repos(paths):
    print("🔗 Підключення зовнішніх модулів...")
    for key, path in paths.items():
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            print(f"   ✔ {key} → {path}")
        else:
            print(f"   ✖ НЕ ЗНАЙДЕНО: {key} → {path}")


# -----------------------------
# 3. Імпорт агентів
# -----------------------------

def import_agents():
    try:
        from agent_ai1 import AgentAI1
        from agent_ai2 import AgentAI2
        return AgentAI1, AgentAI2
    except Exception as e:
        print("❗ Помилка імпорту агентів:", e)
        sys.exit(1)


# -----------------------------
# 4. Активація агентів
# -----------------------------

def activate_agents(AgentAI1, AgentAI2):
    print("🧠 Активація агентів...")

    agent1 = AgentAI1()
    agent2 = AgentAI2()

    print("   ⚡ AgentAI1 активовано")
    print("   ⚡ AgentAI2 активовано")

    return agent1, agent2


# -----------------------------
# 5. Логування результатів стратегії
# -----------------------------

def log_results(strategy, results):
    log_path = "data/strategy_log.yaml"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "strategy": strategy,
        "results": results
    }

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f) or []
    else:
        existing = []

    existing.append(entry)

    with open(log_path, "w", encoding="utf-8") as f:
        yaml.dump(existing, f, allow_unicode=True)

    print("   📝 Логи оновлено.")


# -----------------------------
# 6. Хмарний цикл
# -----------------------------

def run_cloud_cycle(agent1, agent2):
    print("\n🌩 Запуск хмарного циклу...")

    # 1. Аналіз ринку
    print("   🔍 AgentAI1 аналізує ринок...")
    signals = agent1.analyze_market()

    # 2. Генерація стратегії
    print("   📊 AgentAI2 формує стратегію...")
    strategy = agent2.generate_strategy(signals)

    # 3. Симуляція
    print("   🧪 Запуск симуляції...")
    results = agent2.simulate_strategy(strategy)

    # 4. Адаптація
    print("   🔧 Адаптація стратегії...")
    agent2.adapt_strategy(results)

    # 5. Логування
    log_results(strategy, results)

    print("   ✅ Хмарний цикл завершено.")
    return signals, strategy, results


# -----------------------------
# 7. Головна функція
# -----------------------------

def start_system():
    print("🚀 Spark‑1 system starting...\n")

    # 1. Конфігурація
    config = load_config()
    paths = load_paths()

    # 2. Підключення зовнішніх репозиторіїв
    attach_external_repos(paths)

    # 3. Імпорт агентів
    AgentAI1, AgentAI2 = import_agents()

    # 4. Активація агентів
    agent1, agent2 = activate_agents(AgentAI1, AgentAI2)

    # 5. Ініціалізація пам’яті та навчання
    memory = MemoryEngine(path="data/memory.json")
    learning = LearningEngine()

    # 6. Хмарний цикл
    signals, strategy, results = run_cloud_cycle(agent1, agent2)

    # 7. Збереження в пам’ять
    memory.save_cycle(signals, strategy, results)

    # 8. Аналіз історії та навчання
    cycles = memory.get_last_cycles(20)
    performance = learning.evaluate_performance(cycles)
    patterns = learning.detect_patterns(cycles)
    improvements = learning.suggest_improvements(performance)
    model_update = learning.update_model(performance, patterns)

    print("\n🧠 АНАЛІЗ І НАВЧАННЯ:")
    print("   Середній профіт:", performance.get("avg_profit"))
    print("   Тренд:", performance.get("trend"))
    print("   Патерни:", patterns)
    print("   Рекомендації:", improvements)
    print("   Модель оновлено:", model_update.get("status"))

    print("\n🔥 Spark‑1 готовий до наступних циклів.")


def run():
    start_system()


if __name__ == "__main__":
    run()
