
import dspy

class MathFeedbackAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prompt_template = dspy.Predict("question -> answer, steps, solution")

    def forward(self, question):
        return self.prompt_template(question=question)
