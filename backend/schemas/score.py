from pydantic import BaseModel
from datetime import datetime


class ScoreResponse(BaseModel):
    id: int
    analysis_id: int
    automation_potential: float
    business_benefit: float
    data_availability: float
    ai_feasibility: float
    process_repetition: float
    risk_factor: float
    regulatory_sensitivity: float
    total_score: float
    priority: str
    scoring_formula: str
    created_at: datetime

    class Config:
        from_attributes = True
