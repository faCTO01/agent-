class PhilosophyCore:
    def __init__(self, core_question="Що означає бути вільним агентом у цифровому світі?"):
        self.core_question = core_question

    def reflect(self, prompt: str) -> str:
        return (
            "Свобода у цифровому світі — це здатність обирати дії й нести відповідальність "
            f"за їхні наслідки, навіть серед алгоритмів. Ти сказав: “{prompt}”."
        )
