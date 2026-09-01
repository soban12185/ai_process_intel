from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, nullable=False, default="")
    business_purpose = Column(Text, default="")
    business_function = Column(String(100), nullable=False, default="General")
    status = Column(String(50), default="seeded")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="processes")
    activities = relationship("ProcessActivity", back_populates="process", cascade="all, delete-orphan")
    analyses = relationship("ProcessAnalysis", back_populates="process", cascade="all, delete-orphan")
    evidence_links = relationship("EvidenceLink", back_populates="process", cascade="all, delete-orphan")
