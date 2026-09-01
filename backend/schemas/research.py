from pydantic import BaseModel
from typing import List
from datetime import datetime


class ResearchSourceResponse(BaseModel):
    id: int
    title: str
    url: str
    publisher: str
    publication_date: str
    source_type: str
    excerpt: str

    class Config:
        from_attributes = True


class EvidenceResponse(BaseModel):
    id: int
    source: ResearchSourceResponse
    finding_summary: str
    relevance_score: float
    process_id: int

    class Config:
        from_attributes = True
