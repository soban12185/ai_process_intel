from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class ProcessAnalysis(Base):
    __tablename__ = "process_analyses"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    analysis_run_id = Column(Integer, ForeignKey("analysis_runs.id"), nullable=True)
    business_purpose = Column(Text, default="")
    key_activities = Column(Text, default="[]")
    current_challenges = Column(Text, default="[]")
    ai_opportunities = Column(Text, default="[]")
    automation_potential = Column(String(50), default="Medium")
    human_involvement = Column(Text, default="[]")
    technologies = Column(Text, default="[]")
    business_benefits = Column(Text, default="[]")
    risks = Column(Text, default="[]")
    reasoning = Column(Text, default="")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    process = relationship("Process", back_populates="analyses")
    run = relationship("AnalysisRun", back_populates="analyses")
    score = relationship("ProcessScore", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    evidence_links = relationship("EvidenceLink", back_populates="analysis", cascade="all, delete-orphan")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    run_type = Column(String(50), default="seeded")
    model_used = Column(String(200), default="")
    status = Column(String(50), default="pending")
    error_message = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    analyses = relationship("ProcessAnalysis", back_populates="run")
