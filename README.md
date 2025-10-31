──────────────────────────────────────────────────────────────
🏗️  AI MATH SOLVER SYSTEM ARCHITECTURE
──────────────────────────────────────────────────────────────

📦 TECH STACK
──────────────────────────────────────────────────────────────
Frontend: React.js + Tailwind CSS + Framer Motion
Math Rendering: KaTeX + React Markdown + Remark-Math + Rehype-KaTeX
Backend: Node.js / Express (API layer)
LLM Interface: OpenAI / Ollama / Local Model (e.g. Mistral, LLaMA)
Routing & Guardrails: LangChain / Custom Logic
Computation Engine: SymPy / Wolfram / Math.js
Database (optional): ChromaDB / MongoDB
Deployment: Docker + Streamlit / Vercel
Version Control: GitHub

──────────────────────────────────────────────────────────────
🔁 DATA FLOW OVERVIEW
──────────────────────────────────────────────────────────────
┌────────────────────┐
│     User Query     │
└────────────────────┘
          ↓
┌────────────────────────────┐
│     Input Guardrails       │
│ (e.g., prompt filtering,   │
│  equation format check)    │
└────────────────────────────┘
          ↓
┌────────────────────────────┐
│        Routing Layer        │
│ (decides which module to    │
│  handle the request)        │
└────────────────────────────┘
     ↓         ↓         ↓
┌────────┐ ┌────────────┐ ┌───────────────┐
│ KB Match │ │ Symbolic Solve │ │ Web Search (MCP) │
│ (VectorDB)│ │ (SymPy/Math.js)│ │ (API Call)       │
└────────┘ └────────────┘ └───────────────┘
     ↓         ↓         ↓
        ┌────────────────────────────┐
        │     Output Guardrails      │
        │ (sanity checks, formatting)│
        └────────────────────────────┘
                      ↓
        ┌────────────────────────────┐
        │ Frontend Rendering (KaTeX) │
        │ (displays equations &      │
        │  step-by-step solution)    │
        └────────────────────────────┘
                      ↓
        ┌────────────────────────────┐
        │ Human-in-the-Loop (optional)│
        │ (manual validation, QA)    │
        └────────────────────────────┘

──────────────────────────────────────────────────────────────
⚙️  MODULE INTERACTIONS
──────────────────────────────────────────────────────────────
1️⃣ User enters a math query in UI (React component).
2️⃣ Input Guardrails sanitize and classify the type (symbolic/numeric/query).
3️⃣ Routing Layer forwards:
    • KB Match → retrieves from ChromaDB if similar solved examples exist.
    • Symbolic Solve → uses SymPy or Math.js to solve equation.
    • Web Search → fetches contextual or formula info if needed.
4️⃣ Results go through Output Guardrails → ensures LaTeX formatting + correct math syntax.
5️⃣ KaTeX renderer shows final output neatly in green/white boxes.
6️⃣ Optionally, Human-in-the-Loop validates and provides feedback to fine-tune the reasoning.

──────────────────────────────────────────────────────────────
📘 NOTES
──────────────────────────────────────────────────────────────
- All math outputs formatted via KaTeX / ReactMarkdown.
- Optional feedback buttons (👍 👎 Copy).
- Containerized using Docker for reproducible environments.
- Logs stored in JSON / MongoDB for performance and debugging.
- Supports offline solving (Math.js) + LLM reasoning (OpenAI API).

──────────────────────────────────────────────────────────────
✅ END OF FLOW
──────────────────────────────────────────────────────────────
EOF
