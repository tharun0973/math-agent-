from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json, asyncio, os
from datetime import datetime

from agent.routing import route_question
from agent.guardrails import validate_input, rejection_message, sanitize_output

app = FastAPI(title="Math Routing Agent API", version="1.0.0")
FEEDBACK_FILE = "feedback.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://localhost:5174",
        "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MathRequest(BaseModel):
    question: str
    stream: bool = False

class MathResponse(BaseModel):
    question: str
    answer: str
    steps: List[str]
    solution: str
    confidence: float

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int
    comment: Optional[str] = ""

class FeedbackResponse(BaseModel):
    status: str
    message: str
    feedback_id: str

@app.get("/")
async def root():
    return {"status": "running", "message": "Math Routing Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/solve", response_model=MathResponse)
async def solve_math(request: MathRequest):
    try:
        question = request.question.strip()
        if not validate_input(question):
            return MathResponse(
                question=question,
                answer=rejection_message(),
                steps=["Non-mathematical query detected."],
                solution="",
                confidence=0.0
            )
        result = route_question(question)
        required_keys = ["answer", "steps", "solution", "confidence"]
        if not result or not all(k in result for k in required_keys):
            raise ValueError("Routing failed or incomplete result.")
        return MathResponse(
            question=question,
            answer=sanitize_output(result["answer"]),
            steps=result["steps"],
            solution=result["solution"],
            confidence=result["confidence"]
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching answer.")

@app.post("/solve/stream")
async def solve_math_stream(request: MathRequest):
    async def generate():
        try:
            question = request.question.strip()
            if not validate_input(question):
                yield json.dumps({"type": "answer", "data": rejection_message()}) + "\n"
                yield json.dumps({"type": "done", "data": "Complete"}) + "\n"
                return
            result = route_question(question)
            if not result:
                yield json.dumps({"type": "error", "data": "Routing failed."}) + "\n"
                return
            yield json.dumps({"type": "question", "data": question}) + "\n"
            yield json.dumps({"type": "status", "data": "Solving..."}) + "\n"
            for i, step in enumerate(result["steps"], 1):
                yield json.dumps({"type": "step", "data": step, "number": i}) + "\n"
            yield json.dumps({"type": "solution", "data": result["solution"]}) + "\n"
            yield json.dumps({"type": "answer", "data": sanitize_output(result["answer"])}) + "\n"
            yield json.dumps({"type": "done", "data": "Complete"}) + "\n"
            await asyncio.sleep(0.05)
        except Exception as e:
            yield json.dumps({"type": "error", "data": str(e)}) + "\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    try:
        if not (1 <= request.rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        feedback_entry = {
            "id": f"fb_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "question": request.question,
            "answer": request.answer,
            "rating": request.rating,
            "comment": request.comment
        }
        feedbacks = []
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, "r") as f:
                    feedbacks = json.load(f)
            except json.JSONDecodeError:
                feedbacks = []
        feedbacks.append(feedback_entry)
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedbacks, f, indent=2)
        return FeedbackResponse(
            status="success",
            message="Feedback submitted successfully",
            feedback_id=feedback_entry["id"]
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@app.get("/feedback/stats")
async def get_feedback_stats():
    try:
        if not os.path.exists(FEEDBACK_FILE):
            return {"total_feedback": 0, "average_rating": 0.0, "ratings_distribution": {}}
        with open(FEEDBACK_FILE, "r") as f:
            feedbacks = json.load(f)
        if not feedbacks:
            return {"total_feedback": 0, "average_rating": 0.0, "ratings_distribution": {}}
        total = len(feedbacks)
        avg_rating = sum(f.get("rating", 0) for f in feedbacks) / total
        ratings_dist = {i: sum(1 for f in feedbacks if f.get("rating") == i) for i in range(1, 6)}
        return {
            "total_feedback": total,
            "average_rating": round(avg_rating, 2),
            "ratings_distribution": ratings_dist
        }
    except Exception as e:
        return {
            "total_feedback": 0,
            "average_rating": 0.0,
            "ratings_distribution": {},
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
