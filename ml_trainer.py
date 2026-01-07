class MLTrainer:
    def __init__(self, logs):
        self.experiments = []
        self.logs = logs

    def schedule(self, name: str, config: dict):
        """
        Додає експеримент у чергу.
        name: назва експерименту
        config: словник з параметрами (наприклад, {"epochs": 1})
        """
        exp = {"name": name, "config": config, "status": "queued"}
        self.experiments.append(exp)
        self.logs.write("experiment_schedule", exp)

    def run_next(self):
        """
        Виконує наступний експеримент у черзі (симуляція).
        """
        if not self.experiments:
            return None
        exp = self.experiments.pop(0)
        # Тут у майбутньому буде реальне тренування
        exp["status"] = "done"
        self.logs.write("experiment_done", exp)
        return exp
