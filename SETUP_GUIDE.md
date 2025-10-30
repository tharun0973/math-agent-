# Math Routing Agent - Complete Setup Guide

## 📁 Project Structure

```
math-routing-agent/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI app with endpoints
│   ├── math_solver.py      # SymPy-based math solver
│   ├── requirements.txt    # Python dependencies
│   └── setup.sh           # Backend setup script
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── config/            # API configuration
│   └── services/          # API service functions
└── README.md
```

## 🚀 Quick Start

### 1. Backend Setup (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

Backend will run on: **http://localhost:8000**

### 2. Frontend Setup (Terminal ): {

```bash
npm install
npm run dev
```

Frontend will run on: **http://localhost:5173**

## 🔌 API Endpoints

### POST /solve
Solve a math problem:
```json
{
  "question": "Solve 3x² - 7x + 2 = 0",
  "stream": false
}
```

Response:
```json
{
  "question": "Solve 3x² - 7x + 2 = 0",
  "answer": "Solution: x₁ = 2.0000, x₂ = 0.3333",
  "steps": [
    "Step 1: Identify coefficients",
    "   a = 3, b = -7, c = 2",
    "Step 2: Calculate discriminant",
    ...
  ],
  "solution": "x₁ = 2.0000, x₂ = 0.3333",
  "confidence": 0.95
}
```

### POST /solve/stream
Stream the solution in real-time (for future implementation)

### GET /health
Health check endpoint

## 🧮 Supported Math Problems

✅ Quadratic equations: `3x² - 7x + 2 = 0`
✅ Linear equations: `2x + 5 = 13`
✅ General equations: `x^2 + 5x + 6 = 0`
✅ Expression evaluation: `2 + 2 * 3`

## 🎨 Frontend Integration

The frontend is already configured to connect to the backend. Just update the components to use the API:

```javascript
import { solveMath } from './services/mathApi';

const handleSend = async () => {
  const result = await solveMath(input);
  console.log(result);
};
```

## 📚 API Documentation

Once the backend is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Test the API

```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Solve 3x² - 7x + 2 = 0"}'
```

## ✨ Features

- ✅ SymPy-based math solving
- ✅ Step-by-step solutions
- ✅ CORS enabled for frontend
- ✅ Streaming support (structured)
- ✅ Pydantic validation
- 🔄 Ready for RAG integration

## 🎯 Next Steps

1. Start both servers (backend + frontend)
2. Open http://localhost:5173 in browser
3. Test with math questions!
4. Connect frontend to backend API

