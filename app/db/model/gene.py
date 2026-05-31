from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Gene(Base):
    __tablename__ = "gene"

    id = Column(Integer, primary_key=True, autoincrement=True)
    panel_id = Column(Integer, ForeignKey("panel.id"), nullable=False)
    name = Column(String, nullable=False)
    transcript = Column(String)

    panel = relationship("Panel", back_populates="genes")
    variants = relationship("Variant", back_populates="gene")
