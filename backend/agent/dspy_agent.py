import dspy
from agent.knowledge_base import search_knowledge_base

class MathFeedbackAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prompt_template = dspy.Predict("question -> answer, steps, solution")

    def format_markdown(self, answer, steps, solution):
        return f"""## ✅ Final Answer
\

\[
{solution}
\\]



## 🧠 Step-by-Step Breakdown
""" + "\n".join([f"### Step {i+1}\n{step}" for i, step in enumerate(steps)])

    def forward(self, question):
        # First try KB
        kb_result = search_knowledge_base(question)
        if kb_result:
            markdown = self.format_markdown(kb_result["answer"], kb_result["steps"], kb_result["solution"])
            print("✅ KB hit:", kb_result["answer"])
            return dspy.Prediction(
                answer=kb_result["answer"],
                steps=kb_result["steps"],
                solution=kb_result["solution"],
                markdown=markdown
            )

        # Fallback to DSPy
        print("🤖 Fallback to DSPy")
        pred = self.prompt_template(question=question)
        markdown = self.format_markdown(pred.answer, pred.steps, pred.solution)
        return dspy.Prediction(
            answer=pred.answer,
            steps=pred.steps,
            solution=pred.solution,
            markdown=markdown
        )
