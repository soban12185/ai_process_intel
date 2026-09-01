from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AnalysisResponse(BaseModel):
    id: int
    process_id: int
    business_purpose: str
    key_activities: List[str] = []
    current_challenges: List[str] = []
    ai_opportunities: List[str] = []
    automation_potential: str
    human_involvement: List[str] = []
    technologies: List[str] = []
    business_benefits: List[str] = []
    risks: List[str] = []
    reasoning: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisTriggerResponse(BaseModel):
    message: str
    process_id: int
    analysis_id: Optional[int] = None
    status: str
