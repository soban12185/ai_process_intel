from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class ProcessActivity(Base):
    __tablename__ = "process_activities"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text, default="")
    sequence_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    process = relationship("Process", back_populates="activities")
