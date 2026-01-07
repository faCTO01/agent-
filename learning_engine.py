from statistics import mean


class LearningEngine:
    def __init__(self):
        pass

    # -----------------------------
    # 1. Оцінка ефективності
    # -----------------------------
    def evaluate_performance(self, cycles):
        profits = [c["results"]["profit"] for c in cycles if "profit" in c["results"]]
        if not profits:
            return {"avg_profit": 0, "trend": "unknown"}

        avg_profit = mean(profits)
        trend = "up" if avg_profit > 0 else "down"

        return {
            "avg_profit": avg_profit,
            "trend": trend
        }

    # -----------------------------
    # 2. Виявлення патернів
    # -----------------------------
    def detect_patterns(self, cycles):
        patterns = []

        for c in cycles:
            if c["results"]["profit"] > 0:
                patterns.append("positive")
            else:
                patterns.append("negative")

        return patterns

    # -----------------------------
    # 3. Пропозиції покращень
    # -----------------------------
    def suggest_improvements(self, performance):
        if performance["avg_profit"] > 0:
            return "Поточна стратегія працює. Підсилити параметри."
        else:
            return "Стратегія слабка. Спробувати інший підхід."

    # -----------------------------
    # 4. Оновлення внутрішньої моделі
    # -----------------------------
    def update_model(self, performance, patterns):
        return {
            "status": "updated",
            "performance": performance,
            "patterns": patterns
        }
