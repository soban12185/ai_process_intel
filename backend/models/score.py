from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class ProcessScore(Base):
    __tablename__ = "process_scores"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("process_analyses.id"), nullable=False, unique=True)
    automation_potential = Column(Float, default=5.0)
    business_benefit = Column(Float, default=5.0)
    data_availability = Column(Float, default=5.0)
    ai_feasibility = Column(Float, default=5.0)
    process_repetition = Column(Float, default=5.0)
    risk_factor = Column(Float, default=3.0)
    regulatory_sensitivity = Column(Float, default=3.0)
    total_score = Column(Float, default=0.0)
    priority = Column(String(50), default="Medium")
    scoring_formula = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())

    analysis = relationship("ProcessAnalysis", back_populates="score")
