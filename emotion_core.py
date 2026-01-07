class EmotionCore:
    def __init__(self):
        self.mood = "neutral"

    def modulate(self, text: str) -> str:
        if self.mood == "warm":
            return f"З теплотою: {text}"
        elif self.mood == "serious":
            return f"По суті: {text}"
        return text

    def update_mood(self, signal: dict):
        self.mood = signal.get("mood", self.mood)
