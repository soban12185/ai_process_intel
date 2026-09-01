# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER / EXECUTIVE                         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                        │
│  Dashboard | Processes | Top 10 | Human-Led | Query | Add New  │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI APPLICATION                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  API Routes    /api/processes, /api/query, /api/stats  │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐    │
│  │  Service Layer: ProcessService, AnalysisService,        │    │
│  │  ScoringService, ResearchService, QueryService          │    │
│  └───┬──────────┬────────────┬──────────────┬─────────────┘    │
│      │          │            │              │                   │
│  ┌───▼───┐ ┌───▼────┐ ┌────▼─────┐ ┌─────▼──────┐           │
│  │  AI   │ │Research│ │ Scoring  │ │  Database   │           │
│  │ Layer │ │ Layer  │ │  Engine  │ │   Layer     │           │
│  └───┬───┘ └───┬────┘ └────┬─────┘ └─────┬──────┘           │
│      │         │           │              │                    │
│      ▼         ▼           ▼              ▼                    │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              SQLite Database                          │     │
│  │  organizations | processes | activities | analyses   │     │
│  │  scores | research_sources | evidence_links         │     │
│  └──────────────────────────────────────────────────────┘     │
│      │                                                         │
│      ▼                                                         │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              Groq Cloud API (Free)                    │     │
│  │         llama-3.1-8b-instant (configurable)          │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Frontend (React + Vite)
- Dashboard: KPIs, charts, process table
- Process List: Search, filter, sort, paginate
- Process Detail: Full analysis view, score breakdown, evidence
- Top 10: Ranked AI opportunities
- Human-Led: Processes requiring human oversight
- Query: Natural language interface
- Add Process: Dynamic Process 101 creation

### API Layer (FastAPI)
- Request validation via Pydantic
- RESTful endpoint design
- CORS configuration
- Error handling with proper HTTP codes

### Service Layer
- **ProcessService**: CRUD operations, statistics, rankings
- **AnalysisService**: Orchestrates AI analysis pipeline
- **ScoringService**: Deterministic score calculation
- **ResearchService**: Research source management and evidence linking
- **QueryService**: Natural language query processing

### AI Layer
- **LLM Client**: Groq API integration (OpenAI-compatible)
- **Prompts**: System and user prompt templates
- **Response Parser**: JSON validation and fallback handling

### Scoring Engine
- Deterministic formula-based scoring
- Configurable weights per dimension
- Priority classification (Very High/High/Medium/Low)
- Transparent scoring formula stored per analysis

### Database Layer
- SQLAlchemy ORM for SQL injection prevention
- Normalized schema with proper foreign keys
- Timestamps for audit trail
- JSON fields for flexible list storage

## Data Flow: Process Analysis

```
1. Process data -> Prompt construction
2. Prompt -> Groq API (structured JSON response)
3. Response -> Parser (validate + fallback)
4. Parsed data -> Scoring engine (deterministic)
5. Score + Analysis -> Database storage
6. Research matching -> Evidence linking
7. Results -> API response -> Frontend display
```

## Data Flow: Natural Language Query

```
1. User question -> Query intent classification
2. Relevant processes -> Database retrieval
3. Process data + evidence -> Context assembly
4. Context -> Groq API (synthesis)
5. Answer -> Process references -> Frontend display
```
