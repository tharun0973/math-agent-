# Math Routing Agent

A sophisticated AI-powered mathematics assistant with Agentic-RAG system that mimics a professor. The system intelligently routes questions through multiple sources to provide accurate, step-by-step math solutions.

## 🎯 Features

### 🧠 Intelligent Routing
- **Knowledge Base Search**: Vector-based semantic search using Qdrant
- **Web Search Fallback**: Tavily API integration for external resources
- **MCP Fallback**: Direct Ollama queries for contextual answers
- **SymPy Solver**: Symbolic math solving as final fallback
- **Robust Error Handling**: No hallucination, graceful degradation

### 🔐 Input & Output Guardrails
- **Input Validation**: Filters unsafe, irrelevant, or non-math queries
- **Output Sanitization**: Removes hallucinations and profanity
- **Math Content Extraction**: Focuses on mathematical content only
- **Safety First**: Comprehensive banned topic filtering

### 📚 Knowledge Base
- **Qdrant Vector Database**: Efficient semantic search
- **Sentence Transformer Embeddings**: all-MiniLM-L6-v2 model
- **Rich Metadata**: Topic, difficulty, and tag support
- **Sample Dataset Included**: 15+ pre-populated math problems

### 🌐 Web Search & MCP Integration
- **Tavily Search**: Real-time web math content retrieval
- **Ollama MCP**: Local LLM fallback (Gemma 2B)
- **Context Packaging**: Structured context extraction
- **Markdown Formatting**: Clean, readable step-by-step solutions

### 👤 Human-in-the-Loop Feedback
- **Rating System**: Thumbs up/down feedback (1-5 scale)
- **Feedback Storage**: JSON-based persistence
- **Statistics Dashboard**: Track user satisfaction
- **Optional DSPy Integration**: Ready for reranking and refinement

### 🎨 Modern Frontend
- **React + Tailwind**: Beautiful dark-themed UI
- **Markdown Rendering**: LaTeX support with KaTeX
- **Real-time Streaming**: Live response display
- **Chat History**: Persistent localStorage tracking
- **File Upload Simulation**: Extend with OCR for images

## 🏗️ Tech Stack

### Frontend
- **React** ^19.1.1 - UI framework
- **Tailwind CSS** ^3.4.18 - Utility-first styling
- **React Markdown** ^10.1.0 - Markdown rendering
- **KaTeX** ^0.16.25 - Math equation rendering
- **React Icons** ^4.12.0 - Icon library
- **Axios** ^1.13.1 - HTTP client
- **Vite** ^7.1.7 - Build tool

### Backend
- **FastAPI** ^0.109.0 - Modern Python web framework
- **Qdrant** ^1.7.0 - Vector database
- **Sentence Transformers** ^2.2.2 - Embeddings
- **SymPy** ^1.12 - Symbolic mathematics
- **Tavily** ^0.3.0 - Web search API
- **Ollama** ^0.1.7 - Local LLM (optional)
- **DSPy** ^2.3.5 - AI framework (optional)

## 🚀 Getting Started

### Prerequisites

**Backend:**
- Python 3.9+
- Qdrant running on `http://localhost:6333`
- (Optional) Ollama on `http://localhost:11434` with Gemma 2B
- (Optional) Tavily API key for web search

**Frontend:**
- Node.js 16+
- npm or yarn

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/tharun0973/-math-routing-agent.git
cd -math-routing-agent
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Start Qdrant (using Docker)
docker run -d -p 6333:6333 qdrant/qdrant

# Populate knowledge base
python populate_kb.py

# Start backend server
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

#### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📁 Project Structure

```
math-routing-agent/
├── backend/
│   ├── agent/
│   │   ├── routing.py          # Intelligent routing logic
│   │   ├── knowledge_base.py   # Qdrant KB search
│   │   ├── web_search.py       # Web search + MCP
│   │   ├── guardrails.py       # Input/output filtering
│   │   ├── math_solver.py      # SymPy solver
│   │   ├── feedback.py         # Feedback management
│   │   └── verifier.py         # Answer verification
│   ├── main.py                 # FastAPI app
│   ├── populate_kb.py          # KB population script
│   ├── math_dataset.json       # Sample dataset
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MainContent.jsx # Main chat UI
│   │   │   └── Sidebar.jsx     # Chat history
│   │   └── App.jsx             # Root component
│   └── package.json
└── README.md
```

## 🔌 API Endpoints

### POST `/solve`
Solve a math problem
```json
{
  "question": "Solve x^2 + 5x + 6 = 0",
  "stream": false
}
```

### POST `/feedback`
Submit user feedback
```json
{
  "question": "...",
  "answer": "...",
  "rating": 5,
  "comment": "Great explanation!"
}
```

### GET `/feedback/stats`
Get feedback statistics

### POST `/solve/stream`
Stream solution in real-time

### GET `/health`
Health check endpoint

## 🧪 Usage Examples

### Basic Equation
```
Question: "Solve 2x + 5 = 13"
Route: SymPy → Answer: x = 4
```

### Quadratic Equation
```
Question: "Solve x^2 + 5x + 6 = 0"
Route: KB → Answer: x = -2 or x = -3
```

### Calculus
```
Question: "Differentiate f(x) = x^2 + 3x"
Route: KB → Answer: f'(x) = 2x + 3
```

## 🎯 Routing Flow

1. **Input Validation**: Check if question is math-related and safe
2. **Knowledge Base**: Search Qdrant vector database
3. **Web Search**: Fallback to Tavily if KB misses
4. **MCP Fallback**: Query Ollama directly
5. **SymPy Solver**: Final symbolic math fallback
6. **Output Sanitization**: Remove hallucinations before responding

## 📊 Feedback System

Users can rate responses with thumbs up/down:
- **👍 Like**: Rating 5/5
- **👎 Dislike**: Rating 1/5

Feedback is stored in `backend/feedback.json` and can be used for:
- Quality monitoring
- Model refinement
- DSPy reranking (optional)

## 🛠️ Development

### Adding More Math Problems

Edit `backend/math_dataset.json` and run:
```bash
python backend/populate_kb.py
```

### Testing Different Models

Update Ollama model in `backend/agent/web_search.py`:
```python
json={"model": "llama2", "prompt": prompt, ...}
```

### Custom Guardrails

Edit `backend/agent/guardrails.py` to add/modify:
- Banned topics
- Math keywords
- Hallucination markers

## 🐛 Troubleshooting

**Qdrant not found**: Make sure Qdrant is running
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

**Ollama errors**: Install Ollama and Gemma 2B
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull gemma:2b
```

**Import errors**: Install missing dependencies
```bash
pip install -r requirements.txt
```

## 🎓 Next Steps

### Optional Enhancements
- [ ] JEE Bench benchmarking
- [ ] OCR for image uploads
- [ ] DSPy reranking with feedback
- [ ] Multi-language support
- [ ] Graph visualizations

### Dataset Expansion
Add more problems to `math_dataset.json`:
- JEE questions
- AoPS problems
- SymPy documentation
- Custom math content

## 📝 License

MIT

## 👤 Author

**Tharun Kumar**

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🌟 Acknowledgments

- Qdrant for vector search
- Sentence Transformers for embeddings
- SymPy for symbolic math
- Tavily for web search
- Ollama for local LLM
