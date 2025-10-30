# 🏗️ Math Routing Agent - System Architecture

## 🎯 Overview

The Math Routing Agent is an **Agentic-RAG system** that intelligently routes math questions through multiple sources to provide accurate, step-by-step solutions.

## 🔄 Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│                   "Solve x^2 + 5x + 6 = 0"                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT VALIDATION                             │
│                  (agent/guardrails.py)                          │
│  • Check for banned topics                                      │
│  • Verify math-related content                                  │
│  • Filter unsafe queries                                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │   VALID INPUT?        │
          └───┬──────────────┬────┘
              │              │
            NO│              │YES
              │              │
              ▼              ▼
      ┌─────────────┐   ┌────────────────────────────────────┐
      │   REJECT    │   │     INTELLIGENT ROUTING            │
      │   RETURN    │   │   (agent/routing.py)               │
      │  ERROR MSG  │   │                                     │
      └─────────────┘   └──────┬─────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
        ┌───────────────────┐   ┌──────────────────────┐
        │  1. KNOWLEDGE     │   │  2. WEB SEARCH       │
        │     BASE          │   │     FALLBACK         │
        │  (Qdrant)         │   │  (Tavily + MCP)      │
        │                   │   │                      │
        │  • Semantic       │   │  • Search web        │
        │    search         │   │  • Extract context   │
        │  • Embeddings     │   │  • Generate answer   │
        │  • Metadata       │   │    via Ollama        │
        └────────┬──────────┘   └──────┬───────────────┘
                 │                     │
            SUCCESS?              SUCCESS?
                 │                     │
          ┌──────┴──────┐      ┌──────┴──────┐
          │             │      │             │
        YES│           NO│    YES│           NO│
          │             │      │             │
          ▼             ▼      ▼             ▼
   ┌─────────────┐ ┌──────────────────────────┐
   │   RETURN    │ │  3. DIRECT MCP           │
   │   ANSWER    │ │     FALLBACK             │
   │             │ │  (Ollama only)           │
   │ • Steps     │ └──────┬───────────────────┘
   │ • Solution  │        │
   │ • Confidence│   SUCCESS?
   └─────────────┘        │
                     ┌────┴────┐
                   YES│       NO│
                     │         │
                     ▼         ▼
            ┌─────────────┐ ┌──────────────────┐
            │   RETURN    │ │  4. SYMPY        │
            │   ANSWER    │ │     SOLVER       │
            │             │ │                  │
            │ • Steps     │ │ • Equations      │
            │ • Solution  │ │ • Derivatives    │
            │ • Confidence│ │ • Integrals      │
            └─────────────┘ └──────┬───────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   RETURN    │
                            │   ANSWER    │
                            │             │
                            │ • Steps     │
                            │ • Solution  │
                            │ • Confidence│
                            └──────┬──────┘
                                   │
                                   ▼
                      ┌─────────────────────────┐
                      │   OUTPUT SANITIZATION   │
                      │  (agent/guardrails.py)  │
                      │  • Remove hallucinations│
                      │  • Clean profanity      │
                      │  • Extract math content │
                      └────────────┬────────────┘
                                   │
                                   ▼
                      ┌─────────────────────────┐
                      │   RESPONSE TO USER      │
                      │                         │
                      │  • Answer               │
                      │  • Steps                │
                      │  • Solution             │
                      │  • Source               │
                      │  • Confidence           │
                      └────────────┬────────────┘
                                   │
                                   ▼
                      ┌─────────────────────────┐
                      │   FEEDBACK COLLECTION   │
                      │  (backend/main.py)      │
                      │                         │
                      │  • Rating (1-5)         │
                      │  • Comment              │
                      │  • Storage              │
                      └─────────────────────────┘
```

## 🧩 Component Architecture

### 1. Frontend Layer

```
┌─────────────────────────────────────┐
│         React Application          │
│                                     │
│  ┌──────────────┐  ┌─────────────┐│
│  │   Sidebar    │  │ MainContent ││
│  │              │  │             ││
│  │ Chat History │  │ Chat UI     ││
│  │              │  │             ││
│  │  • List      │  │ • Markdown  ││
│  │  • New Chat  │  │ • KaTeX     ││
│  │              │  │ • Feedback  ││
│  └──────────────┘  └──────┬──────┘│
│                            │       │
└────────────────────────────┼───────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   API Call      │
                    │  /solve         │
                    └────────┬────────┘
                             │
```

### 2. Backend Layer

```
┌────────────────────────────────────────────────────────┐
│              FastAPI Application                       │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Endpoints                            │ │
│  │                                                   │ │
│  │  POST /solve        - Main solving endpoint      │ │
│  │  POST /solve/stream - Streaming responses        │ │
│  │  POST /feedback     - Submit feedback            │ │
│  │  GET  /feedback/stats - Get statistics           │ │
│  │  GET  /health       - Health check               │ │
│  └──────────────────────┬───────────────────────────┘ │
│                         │                              │
└─────────────────────────┼──────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│              Routing System                            │
│              (agent/routing.py)                        │
│                                                        │
│  1. Validate Input                                     │
│     ↓                                                  │
│  2. Try KB Search                                      │
│     ↓                                                  │
│  3. Try Web Search                                     │
│     ↓                                                  │
│  4. Try MCP Direct                                     │
│     ↓                                                  │
│  5. Try SymPy Solver                                   │
│     ↓                                                  │
│  6. Sanitize Output                                    │
│     ↓                                                  │
│  7. Return Result                                      │
└────────────────────────────────────────────────────────┘
```

### 3. Knowledge Base Layer

```
┌────────────────────────────────────────────────────────┐
│         Knowledge Base (agent/knowledge_base.py)       │
│                                                        │
│  ┌────────────────┐                                    │
│  │   Embeddings   │                                    │
│  │                │                                    │
│  │ Sentence       │                                    │
│  │ Transformer    │                                    │
│  │ (MiniLM-L6-v2) │                                    │
│  └────────┬───────┘                                    │
│           │                                            │
│           ▼                                            │
│  ┌────────────────┐                                    │
│  │    Qdrant      │                                    │
│  │                │                                    │
│  │ Collection:    │                                    │
│  │  math_kb       │                                    │
│  │                │                                    │
│  │ • Vectors      │                                    │
│  │ • Metadata     │                                    │
│  │ • Semantic     │                                    │
│  │   search       │                                    │
│  └────────────────┘                                    │
└────────────────────────────────────────────────────────┘
```

### 4. External Services

```
┌────────────────────────────────────────────────────────┐
│              External Services                         │
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   Qdrant     │  │    Tavily    │  │    Ollama    ││
│  │              │  │              │  │              ││
│  │ Vector DB    │  │ Web Search   │  │ Local LLM    ││
│  │              │  │              │  │              ││
│  │ localhost:   │  │ API Key      │  │ Gemma 2B     ││
│  │   6333       │  │ Required     │  │ Optional     ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 🔐 Guardrail System

```
INPUT → [Validation] → OUTPUT → [Sanitization] → RESPONSE
         │                        │
         ├─ Banned Topics         ├─ Hallucination Removal
         ├─ Math Keywords         ├─ Profanity Filter
         ├─ Safety Checks         ├─ Content Extraction
         └─ Length Check          └─ Polishing
```

## 📊 Data Flow

```
User Query
    │
    ├─→ Guardrails Validation
    │   └─→ Valid? → Continue
    │   └─→ Invalid? → Reject
    │
    ├─→ KB Search (Qdrant)
    │   └─→ Found? → Return + Sanitize
    │   └─→ Not Found? → Next
    │
    ├─→ Web Search (Tavily)
    │   └─→ Search + Generate (Ollama)
    │   └─→ Success? → Return + Sanitize
    │   └─→ Failed? → Next
    │
    ├─→ Direct MCP (Ollama)
    │   └─→ Generate Answer
    │   └─→ Success? → Return + Sanitize
    │   └─→ Failed? → Next
    │
    ├─→ SymPy Solver
    │   └─→ Solve
    │   └─→ Success? → Return + Sanitize
    │   └─→ Failed? → Error
    │
    └─→ User Response
        │
        └─→ Feedback Collection (if provided)
```

## 🛡️ Safety Features

```
Input Safety:
├─ Topic Filtering (50+ banned topics)
├─ Math Keyword Detection (30+ keywords)
├─ Length Validation
└─ Content Type Check

Output Safety:
├─ Hallucination Removal
├─ Profanity Filter
├─ Answer Verification
└─ Confidence Scoring
```

## 📈 Performance Characteristics

- **Latency**: KB < Web < MCP < SymPy
- **Accuracy**: KB ≈ Web ≈ MCP > SymPy
- **Cost**: KB < SymPy < MCP < Web
- **Reliability**: SymPy > KB > MCP > Web

## 🔄 Fallback Strategy

```
Priority Order:
1. KB (fast, accurate, free)
2. Web (slower, accurate, paid)
3. MCP (medium, good, optional)
4. SymPy (fast, limited, free)
```

## 🎯 Success Criteria

✅ All sources provide structured output  
✅ No hallucinations in responses  
✅ Graceful degradation  
✅ User feedback collected  
✅ Performance optimized  

