from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json, asyncio, traceback, os
from datetime import datetime
from agent.routing import route_question

app = FastAPI(title="Math Routing Agent API", version="1.0.0")

# Feedback storage file
FEEDBACK_FILE = "feedback.json"

# ✅ CORS setup
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

# ✅ Request schema
class MathRequest(BaseModel):
    question: str
    stream: bool = False

# ✅ Response schema
class MathResponse(BaseModel):
    question: str
    answer: str
    steps: List[str]
    solution: str
    confidence: float

# ✅ Feedback schemas
class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int  # 1-5
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

# ✅ Main solve endpoint
@app.post("/solve", response_model=MathResponse)
async def solve_math(request: MathRequest):
    try:
        result = route_question(request.question)
        print("🔍 Routing result:", result)

        required_keys = ["answer", "steps", "solution", "confidence"]
        if not result or not all(k in result for k in required_keys):
            raise ValueError("Routing failed or incomplete result.")

        return MathResponse(
            question=request.question,
            answer=result["answer"],
            steps=result["steps"],
            solution=result["solution"],
            confidence=result["confidence"]
        )
    except Exception as e:
        print("❌ Error solving question:", request.question)
        print("🔧 Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error fetching answer.")

# ✅ Streaming endpoint (unchanged)
@app.post("/solve/stream")
async def solve_math_stream(request: MathRequest):
    async def generate():
        try:
            result = route_question(request.question)
            if result is None:
                yield json.dumps({"type": "error", "data": "Routing failed or no result returned."}) + "\n"
                return
            chunks = [
                json.dumps({"type": "question", "data": request.question}) + "\n",
                json.dumps({"type": "status", "data": "Solving..."}) + "\n"
            ]
            for i, step in enumerate(result["steps"], 1):
                chunks.append(json.dumps({"type": "step", "data": step, "number": i}) + "\n")
            chunks.append(json.dumps({"type": "solution", "data": result["solution"]}) + "\n")
            chunks.append(json.dumps({"type": "answer", "data": result["answer"]}) + "\n")
            chunks.append(json.dumps({"type": "done", "data": "Complete"}) + "\n")
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.05)
        except Exception as e:
            print("Stream Error Traceback:", traceback.format_exc())
            yield json.dumps({"type": "error", "data": str(e)}) + "\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

# ✅ Feedback endpoint
@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback for a question-answer pair"""
    try:
        # Validate rating
        if request.rating < 1 or request.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Create feedback entry
        feedback_entry = {
            "id": f"fb_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "question": request.question,
            "answer": request.answer,
            "rating": request.rating,
            "comment": request.comment
        }
        
        # Load existing feedback
        feedbacks = []
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, 'r') as f:
                    feedbacks = json.load(f)
            except json.JSONDecodeError:
                feedbacks = []
        
        # Add new feedback
        feedbacks.append(feedback_entry)
        
        # Save to file
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(feedbacks, f, indent=2)
        
        print(f"✅ Feedback received: {request.rating}/5 for question: {request.question[:50]}...")
        
        return FeedbackResponse(
            status="success",
            message="Feedback submitted successfully",
            feedback_id=feedback_entry["id"]
        )
        
    except Exception as e:
        print(f"❌ Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

# ✅ Get feedback statistics
@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    try:
        if not os.path.exists(FEEDBACK_FILE):
            return {
                "total_feedback": 0,
                "average_rating": 0.0,
                "ratings_distribution": {}
            }
        
        with open(FEEDBACK_FILE, 'r') as f:
            feedbacks = json.load(f)
        
        if not feedbacks:
            return {
                "total_feedback": 0,
                "average_rating": 0.0,
                "ratings_distribution": {}
            }
        
        # Calculate stats
        total = len(feedbacks)
        avg_rating = sum(f.get("rating", 0) for f in feedbacks) / total
        ratings_dist = {}
        for i in range(1, 6):
            ratings_dist[i] = sum(1 for f in feedbacks if f.get("rating") == i)
        
        return {
            "total_feedback": total,
            "average_rating": round(avg_rating, 2),
            "ratings_distribution": ratings_dist
        }
        
    except Exception as e:
        print(f"❌ Error getting feedback stats: {e}")
        return {
            "total_feedback": 0,
            "average_rating": 0.0,
            "ratings_distribution": {},
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
