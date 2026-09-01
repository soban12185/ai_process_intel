from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ActivityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=300)
    description: str = ""
    sequence_order: int = 0


class ActivityResponse(BaseModel):
    id: int
    name: str
    description: str
    sequence_order: int

    class Config:
        from_attributes = True


class ProcessCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=300)
    description: str = ""
    business_purpose: str = ""
    business_function: str = "General"
    activities: List[ActivityCreate] = []


class ProcessResponse(BaseModel):
    id: int
    org_id: int
    name: str
    description: str
    business_purpose: str
    business_function: str
    status: str
    created_at: datetime
    updated_at: datetime
    activities: List[ActivityResponse] = []

    class Config:
        from_attributes = True


class ProcessListResponse(BaseModel):
    id: int
    name: str
    description: str
    business_function: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
