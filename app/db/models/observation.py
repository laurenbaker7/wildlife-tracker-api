from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    health_rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    family = relationship("Family", back_populates="observations")
