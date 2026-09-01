# AI Methodology Documentation

## Overview

The AI intelligence layer uses a large language model (Groq-hosted) to analyze banking business processes and generate structured intelligence about AI opportunities.

## Model Configuration

- **Provider**: Groq Cloud API (free tier)
- **Default Model**: llama-3.1-8b-instant
- **Configurable via**: `GROQ_MODEL` environment variable
- **Temperature**: 0.3 (deterministic output)
- **Response Format**: JSON (structured output mode)

## Analysis Pipeline

### Step 1: Context Assembly
- Retrieve process name, description, purpose, function
- Retrieve existing activities from database
- Format as structured user prompt

### Step 2: LLM Analysis
- System prompt establishes banking domain expert persona
- User prompt provides process details
- LLM returns structured JSON with 10+ fields

### Step 3: Response Validation
- Check all required fields present
- Validate data types (lists vs strings)
- Enforce value constraints (automation_potential in valid set)
- Apply fallback values for missing fields

### Step 4: Score Calculation (Deterministic)
The LLM provides numerical assessments (1-10) for scoring dimensions. The scoring engine applies a weighted formula:

```
raw = (automation_potential × 0.20) + (business_benefit × 0.18) +
      (data_availability × 0.15) + (ai_feasibility × 0.15) +
      (process_repetition × 0.12) - (risk_factor × 0.10) -
      (regulatory_sensitivity × 0.10)

total_score = (raw / 10) × 100   [clamped to 0-100]
```

### Step 5: Priority Classification
| Score | Priority |
|-------|----------|
| 75-100 | Very High |
| 50-74 | High |
| 25-49 | Medium |
| 0-24 | Low |

## Structured Output Schema

```json
{
  "business_purpose": "string",
  "key_activities": ["string"],
  "current_challenges": ["string"],
  "ai_opportunities": ["string"],
  "automation_potential": "Very High|High|Medium|Low",
  "human_involvement": ["string"],
  "technologies": ["string"],
  "business_benefits": ["string"],
  "risks": ["string"],
  "reasoning": "string",
  "confidence": 0.0-1.0,
  "scoring_dimensions": {
    "automation_potential": 1-10,
    "business_benefit": 1-10,
    "data_availability": 1-10,
    "ai_feasibility": 1-10,
    "process_repetition": 1-10,
    "risk_factor": 1-10,
    "regulatory_sensitivity": 1-10
  }
}
```

## Error Handling

- **LLM unavailable**: Returns fallback analysis with zero confidence
- **Malformed response**: Parser applies defaults for missing fields
- **Rate limits**: Application continues; user can retry
- **Never fabricates**: Clear indication when AI service is unavailable

## Why Deterministic Scoring

The LLM generates analysis text, but scores are calculated by formula. This ensures:
- Reproducibility (same inputs = same score)
- Transparency (formula is visible and auditable)
- No LLM hallucination in numerical assessments
- Configurable weights without retraining
