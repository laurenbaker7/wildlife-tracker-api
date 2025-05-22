from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Herd(Base):
    __tablename__ = "herds"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, nullable=False)

    families = relationship("Family", back_populates="herd", cascade="all, delete-orphan")