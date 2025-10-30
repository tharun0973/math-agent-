"""
Feedback management module for storing and analyzing user feedback.
"""
import json
import os
from typing import List, Dict

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "..", "feedback.json")

def store_feedback(question: str, answer: str, rating: int, comment: str = "") -> str:
    """
    Store user feedback in a JSON file.
    Returns feedback ID.
    """
    from datetime import datetime
    
    feedback_entry = {
        "id": f"fb_{datetime.now().timestamp()}",
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "rating": rating,
        "comment": comment
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
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=2)
    
    return feedback_entry["id"]

def get_feedback_stats() -> Dict:
    """
    Get statistics about collected feedback.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return {
            "total_feedback": 0,
            "average_rating": 0.0,
            "ratings_distribution": {}
        }
    
    try:
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
        print(f"Error loading feedback: {e}")
        return {
            "total_feedback": 0,
            "average_rating": 0.0,
            "ratings_distribution": {}
        }

def get_low_rated_feedback(min_rating: int = 2) -> List[Dict]:
    """
    Get feedback entries with low ratings for improvement.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return []
    
    try:
        with open(FEEDBACK_FILE, 'r') as f:
            feedbacks = json.load(f)
        
        return [f for f in feedbacks if f.get("rating", 5) <= min_rating]
    except Exception as e:
        print(f"Error loading feedback: {e}")
        return []
