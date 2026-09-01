from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class ResearchSource(Base):
    __tablename__ = "research_sources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(Text, default="")
    publisher = Column(String(200), default="")
    publication_date = Column(String(50), default="")
    source_type = Column(String(100), default="industry_report")
    retrieved_date = Column(String(50), default="")
    excerpt = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())

    evidence_links = relationship("EvidenceLink", back_populates="source", cascade="all, delete-orphan")


class EvidenceLink(Base):
    __tablename__ = "evidence_links"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("research_sources.id"), nullable=False)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("process_analyses.id"), nullable=True)
    finding_summary = Column(Text, default="")
    relevance_score = Column(Float, default=0.5)
    created_at = Column(DateTime, server_default=func.now())

    source = relationship("ResearchSource", back_populates="evidence_links")
    process = relationship("Process", back_populates="evidence_links")
    analysis = relationship("ProcessAnalysis", back_populates="evidence_links")
