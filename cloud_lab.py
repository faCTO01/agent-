class CloudLab:
    def __init__(self):
        # Список завдань, відправлених у "хмару"
        self.jobs = []

    def submit(self, job: dict):
        """
        Додає завдання у список для виконання (симуляція).
        job: {"name": "exp1", "params": {...}}
        """
        job["status"] = "submitted"
        self.jobs.append(job)
        return job

    def list_jobs(self):
        """Повертає список усіх завдань"""
        return self.jobs

    def get_status(self, name: str):
        """Повертає статус завдання за назвою"""
        for job in self.jobs:
            if job.get("name") == name:
                return job.get("status")
        return None
