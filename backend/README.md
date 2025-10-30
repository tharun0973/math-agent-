# Math Routing Agent Backend

FastAPI backend for the Math Routing Agent with SymPy integration and optional RAG support.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
python main.py
```

## API Endpoints

### Health Check
```
GET /health
```

### Solve Math Problem (Standard)
```
POST /solve
Content-Type: application/json

{
  "question": "Solve 3x² - 7x + 2 = 0",
  "stream": false
}
```

### Solve Math Problem (Streaming)
```
POST /solve/stream
Content-Type: application/json

{
  "question": "Solve 3x² - 7x + 2 = 0"
}
```

## Features

- ✅ Core SymPy integration for math solving
- ✅ Step-by-step solutions
- ✅ Streaming responses
- ✅ CORS enabled for frontend
- 🔄 RAG integration (optional)
- 🔄 LLM fallback (optional)

## Testing

Test the API using curl:

```bash
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Solve 3x² - 7x + 2 = 0"}'
```

## Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

