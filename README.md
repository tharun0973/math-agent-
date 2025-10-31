# 📘 Math Routing Agent
# =====================

A sophisticated AI-powered mathematics assistant built with an Agentic-RAG system that mimics a professor.  
It intelligently routes math queries through multiple reasoning layers (KB, Symbolic Solver, Web Search)  
to deliver accurate, step-by-step, and human-readable solutions.

──────────────────────────────────────────────────────────────
🎯 FEATURES
──────────────────────────────────────────────────────────────
🧠 INTELLIGENT ROUTING
- Knowledge Base Search → Vector-based semantic search (Qdrant)
- Web Search Fallback → Tavily API integration for real-time math data
- MCP Fallback → Ollama local model (Gemma 2B)
- SymPy Solver → Symbolic and algebraic computations
- Robust Error Handling → No hallucinations, graceful degradation

🔐 INPUT & OUTPUT GUARDRAILS
- Input Validation → Detects unsafe / irrelevant / non-math inputs
- Output Sanitization → Filters hallucinations, profanity, off-topic responses
- Math Content Extraction → Focused mathematical text parsing
- Safety First → Banned topic and prompt filter

📚 KNOWLEDGE BASE
- Qdrant Vector DB → Semantic retrieval
- Sentence Transformer Embeddings → all-MiniLM-L6-v2 model
- Metadata Enrichment → Tags, topics, difficulty
- Sample Dataset → 15+ curated math problems

🌐 WEB SEARCH & MCP
- Tavily Search API → External fallback
- Ollama MCP (Gemma 2B) → Context-aware local inference
- Context Packaging → Structured prompt formatting
- Markdown / KaTeX → Stepwise, readable math display

👤 HUMAN-IN-THE-LOOP
- Rating System → Thumbs up/down (1–5)
- Feedback JSON Storage → Persistent ratings
- Stats Dashboard → Track quality metrics
- DSPy Integration (Optional) → Fine-tuning reranking

🎨 MODERN FRONTEND
- React + Tailwind → Beautiful dark-themed UI
- Markdown Rendering → With KaTeX & Math support
- Real-time Streaming → Live step display
- Chat History → Persistent localStorage
- File Upload (Future) → Extend with OCR for handwritten math

──────────────────────────────────────────────────────────────
🏗️ TECH STACK
──────────────────────────────────────────────────────────────
Frontend:
  - React ^19.1.1
  - Tailwind CSS ^3.4.18
  - React Markdown ^10.1.0
  - KaTeX ^0.16.25
  - React Icons ^4.12.0
  - Axios ^1.13.1
  - Vite ^7.1.7

Backend:
  - FastAPI ^0.109.0
  - Qdrant ^1.7.0
  - Sentence Transformers ^2.2.2
  - SymPy ^1.12
  - Tavily ^0.3.0
  - Ollama ^0.1.7
  - DSPy ^2.3.5

──────────────────────────────────────────────────────────────
🚀 GETTING STARTED
──────────────────────────────────────────────────────────────
# 1️⃣ Clone the Repository
git clone https://github.com/tharun0973/math-agent-.git
cd math-agent-

# 2️⃣ Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate      # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env          # Add your API keys
docker run -d -p 6333:6333 qdrant/qdrant   # Start Qdrant
python populate_kb.py         # Populate KB
uvicorn main:app --reload     # Start backend

# 3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

# Backend → http://localhost:8000
# Frontend → http://localhost:5173

──────────────────────────────────────────────────────────────
📁 PROJECT STRUCTURE
──────────────────────────────────────────────────────────────
math-routing-agent/
├── backend/
│   ├── agent/
│   │   ├── routing.py          → Intelligent routing logic
│   │   ├── knowledge_base.py   → Qdrant KB search
│   │   ├── web_search.py       → Tavily + MCP fallback
│   │   ├── guardrails.py       → Input/output safety
│   │   ├── math_solver.py      → SymPy symbolic math
│   │   ├── feedback.py         → Feedback collection
│   │   └── verifier.py         → Output verification
│   ├── main.py                 → FastAPI entrypoint
│   ├── populate_kb.py          → Knowledge base builder
│   ├── math_dataset.json       → Sample dataset
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MainContent.jsx → Chat interface
│   │   │   └── Sidebar.jsx     → Chat history
│   │   └── App.jsx             → Root component
│   └── package.json
└── README.md

──────────────────────────────────────────────────────────────
🔌 API ENDPOINTS
──────────────────────────────────────────────────────────────
POST /solve
  { "question": "Solve x^2 + 5x + 6 = 0", "stream": false }

POST /feedback
  { "question": "...", "answer": "...", "rating": 5, "comment": "Nice!" }

GET /feedback/stats   → Feedback metrics
POST /solve/stream    → Stream response
GET /health           → Server health check

──────────────────────────────────────────────────────────────
🧪 SAMPLE USAGE
──────────────────────────────────────────────────────────────
Q: Solve 2x + 5 = 13
Route: SymPy → x = 4

Q: Solve x^2 + 5x + 6 = 0
Route: KB → x = -2 or -3

Q: Differentiate f(x) = x^2 + 3x
Route: KB → f'(x) = 2x + 3

──────────────────────────────────────────────────────────────
🔁 ROUTING FLOW
──────────────────────────────────────────────────────────────
┌────────────────────┐
│     User Query     │
└────────────────────┘
          ↓
┌────────────────────────────┐
│     Input Guardrails       │
└────────────────────────────┘
          ↓
┌────────────────────────────┐
│        Routing Layer        │
└────────────────────────────┘
     ↓         ↓         ↓
┌────────┐ ┌────────────┐ ┌───────────────┐
│ KB Match │ │ Symbolic Solve │ │ Web Search (MCP) │
└────────┘ └────────────┘ └───────────────┘
     ↓         ↓         ↓
        ┌────────────────────────────┐
        │     Output Guardrails      │
        └────────────────────────────┘
                      ↓
        ┌────────────────────────────┐
        │   Frontend Rendering (KaTeX) │
        └────────────────────────────┘
                      ↓
        ┌────────────────────────────┐
        │ Human-in-the-Loop (if needed) │
        └────────────────────────────┘

──────────────────────────────────────────────────────────────
📊 FEEDBACK SYSTEM
──────────────────────────────────────────────────────────────
👍 Like → Rating 5/5  
👎 Dislike → Rating 1/5  
Stored in `backend/feedback.json`  
Used for reranking, DSPy fine-tuning, and quality stats.

──────────────────────────────────────────────────────────────
🐛 TROUBLESHOOTING
──────────────────────────────────────────────────────────────
Qdrant not found → Run: docker run -d -p 6333:6333 qdrant/qdrant  
Ollama missing → curl -fsSL https://ollama.ai/install.sh | sh  
Import errors → pip install -r requirements.txt  

──────────────────────────────────────────────────────────────
🎯 FUTURE ENHANCEMENTS
──────────────────────────────────────────────────────────────
- [ ] JEE Benchmark dataset  
- [ ] OCR for equation image uploads  
- [ ] DSPy reranking pipeline  
- [ ] Multi-language support  
- [ ] Graph visualizations  

──────────────────────────────────────────────────────────────
👤 AUTHOR
──────────────────────────────────────────────────────────────
Tharun Kumar  
GitHub: https://github.com/tharun0973/math-agent-  
MIT License © 2025  

──────────────────────────────────────────────────────────────
🌟 ACKNOWLEDGMENTS
──────────────────────────────────────────────────────────────
- Qdrant → Vector search
- Sentence Transformers → Embeddings
- SymPy → Symbolic math solving
- Tavily → Web search
- Ollama → Local LLM inference
- DSPy → Intelligent reranking
