# Database Model Documentation

## Entity Relationship Diagram

```
organizations 1───N processes
processes 1───N process_activities
processes 1───N process_analyses
processes 1───N evidence_links
process_analyses 1───1 process_scores
process_analyses 1───N evidence_links
analysis_runs 1───N process_analyses
research_sources 1───N evidence_links
```

## Table Descriptions

### organizations
Top-level entity. Stores company information. Exists to support multi-organization architecture in future scaling.

### processes
Core entity. Each row represents a banking business process with name, description, purpose, and function classification. Status field tracks whether process was seeded or user-added.

### process_activities
Individual steps within a process. Normalized (not JSON) for queryability. Each activity has a sequence order.

### process_analyses
AI-generated analysis results. Stores structured intelligence output from the LLM. A process can have multiple analyses (re-analysis history). Contains JSON fields for lists (activities, challenges, opportunities, etc.).

### process_scores
Deterministic scoring results linked 1:1 to an analysis. Stores individual dimension scores (1-10), total score (0-100), priority classification, and the scoring formula used. Separated from analysis for transparency.

### analysis_runs
Audit trail for analysis executions. Tracks which model was used, run status, timing, and errors. Enables reproducibility tracking.

### research_sources
External evidence repository. Pre-loaded with ~12 banking/AI research publications from McKinsey, BIS, Federal Reserve, Deloitte, PwC, IMF, OCC, Gartner, Bain, Accenture, FDIC.

### evidence_links
Many-to-many junction between research sources and processes/analyses. Stores the finding summary and relevance score for each evidence connection.

## Why Each Entity Exists

| Entity | Reason |
|--------|--------|
| organizations | Multi-org support, data isolation |
| processes | Core business entity, ~120+ banking processes |
| process_activities | Queryable activity steps, not JSON blobs |
| process_analyses | AI output storage, re-analysis history |
| process_scores | Transparent scoring, dimension breakdown |
| analysis_runs | Audit trail, model tracking, reproducibility |
| research_sources | Reusable evidence across processes |
| evidence_links | Traceable evidence-to-conclusion mapping |
