from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Panel(Base):
    __tablename__ = "panel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    disease = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    genes = relationship("Gene", back_populates="panel")
