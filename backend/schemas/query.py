from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)


class ProcessSummary(BaseModel):
    id: int
    name: str
    business_function: str
    ai_score: Optional[float] = None
    priority: Optional[str] = None
    automation_potential: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    processes: List[ProcessSummary] = []
    evidence: List[str] = []
